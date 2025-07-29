from datetime import datetime
from multiprocessing import Lock, Queue
from time import time_ns
from pyedflib import FILETYPE_BDFPLUS, FILETYPE_EDFPLUS, EdfWriter
from threading import Thread
from loguru import logger
import numpy as np
import os
from qlsdk.core import RscPacket

EDF_FILE_TYPE = {
    "bdf": FILETYPE_BDFPLUS,
    "edf": FILETYPE_EDFPLUS
}

class EDFStreamWriter(Thread):
    def __init__(self, channels, sample_frequency, physical_max, digital_min, file_type, file_path):
        super().__init__()
        self._writer : EdfWriter = None
        self.data_queue : Queue = Queue()
        self._recording = False
        self._points = 0
        self._duration = 0
        self._buffer = None
        
        # signal info
        self._channels = channels
        self._n_channels = len(channels)
        self.sample_frequency = sample_frequency
        self.physical_max = physical_max
        self.physical_min = digital_min
        # 和位数相关，edf 16 bits/bdf  24 bits
        self.digital_max = 8388607 if file_type == EDF_FILE_TYPE['bdf'] else 32767
        self.digital_min = -8388608 if file_type == EDF_FILE_TYPE['bdf'] else -32768
        self.file_type = file_type
        self.file_path = file_path
        
        # 记录开始时间
        self.start_time = None
        
        # header info
        self.equipment = "equipment"
        self.patient_code = "patient_code"
        self.patient_name = "patient_name"
        
    def set_channels(self, channels):
        self._channels = channels
        self._n_channels = len(channels)
        
    def set_sample_rate(self, sample_rate):
        self._sample_rate = sample_rate
        
    def set_start_time(self, time):
        self.start_time = time

    def stop_recording(self):
        self._recording = False
        
    def append(self, data):
        if data:
            # 数据
            self.data_queue.put(data)
            
    def trigger(self, onset, desc):
        if self._writer:            
            self._writer.writeAnnotation(onset, 1, desc)
        else:
            logger.warning("未创建文件，无法写入Trigger标记")
        
        
    def run(self):
        logger.debug(f"启动bdf文件写入线程，写入数据到文件 {self.file_path}")
        # 记录状态
        self._recording = True
        
        #  初始化
        if self._writer is None:
            self._init_writer()
            
        while True:
            if self._recording or (not self.data_queue.empty()):
                try:
                    data = self.data_queue.get(timeout=30)
                    if data is None:
                        logger.debug("收到结束信号，停止写入数据")
                        break
                    # 处理数据
                    self._points += len(data[1])
                    logger.trace(f"已处理数据点数：{self._points}")
                    self._write_file(data)
                except Exception as e:
                    logger.error(f"异常或超时(30s)结束: {str(e)}")
                    break
            else:
                logger.debug("数据记录完成")
                break
            
        self.close()
        
    def _init_writer(self):
        
        # 创建EDF+写入器
        self._writer = EdfWriter(
            self.file_path,
            self._n_channels,
            file_type=self.file_type
        )
        
        # 设置头信息
        self._writer.setPatientCode(self.patient_code)
        self._writer.setPatientName(self.patient_name)
        self._writer.setEquipment(self.equipment)
        self._writer.setStartdatetime(self.start_time if self.start_time else datetime.now())
        
        # 配置通道参数
        signal_headers = []
        for ch in range(self._n_channels):
            signal_headers.append({
                "label": f'channels {self._channels[ch]}',
                "dimension": 'uV',
                "sample_frequency": self.sample_frequency,
                "physical_min": self.physical_min,
                "physical_max": self.physical_max,
                "digital_min": self.digital_min,
                "digital_max": self.digital_max
            })
        
        self._writer.setSignalHeaders(signal_headers)
        
    def _write_file(self, eeg_data):
        try:            
            if self._buffer is None or self._buffer.size == 0:
                self._buffer = np.asarray(eeg_data)
            else:                
                self._buffer = np.hstack((self._buffer, eeg_data))
            
            if self._buffer.shape[1] >= self.sample_frequency:      
                block = self._buffer[:, :self.sample_frequency]          
                self._write_block(block)
                self._buffer = self._buffer[:, self.sample_frequency:]      
            
        except Exception as e:
            logger.error(f"写入数据异常: {str(e)}")
        
    def close(self):
        self._recording = False
        if self._writer:            
            self._writer.writeAnnotation(0, 1, "recording start")
            self._writer.writeAnnotation(self._duration, 1, "recording end")
            self._writer.close()
        
        logger.info(f"文件: {self.file_path}完成记录, 总点数: {self._points}, 总时长: {self._duration}秒")
    
    # 写入1秒的数据
    def _write_block(self, block):
        logger.trace(f"写入数据: {block}")
        # 转换数据类型为float64
        data_float64 = block.astype(np.float64)
        # 写入时转置为(样本数, 通道数)格式
        self._writer.writeSamples(data_float64)
        self._duration += 1

# 用作数据结构一致化处理，通过调用公共类写入edf文件
# 入参包含写入edf的全部前置参数
# 实时数据包为个性化数据包，含有eeg数据部分
class RscEDFHandler(object):
    '''
        Rsc EDF Handler
        处理EDF文件的读写
        RSC设备通道数根据选择变化，不同通道采样频率相同
        eeg_sample_rate: 采样频率
        physical_max: 物理最大值    
        physical_min: 物理最小值
        resolution: 分辨率
        storage_path: 存储路径        
        
        @author: qlsdk
        @since: 0.4.0
    '''
    def __init__(self, eeg_sample_rate, physical_max, physical_min, resolution=24, storage_path = None):
        # edf文件参数
        self.physical_max = physical_max
        self.physical_min = physical_min
        self.digital_max = 8388607
        self.digital_min = -8388607
        self.file_type = EDF_FILE_TYPE["bdf"] if resolution == 24 else EDF_FILE_TYPE["edf"]
        # 点分辨率
        self.resolution = resolution
        # eeg通道数
        self.channels = None
        # eeg采样率
        self.sample_rate = eeg_sample_rate
        # bytes per second
        self.bytes_per_second = 0
        self._edf_writer = None
        self._cache2 = tuple()
        self._recording = False
        self._edf_writer = None
        self.annotations = None
        # 每个数据块大小
        self._chunk = np.array([])
        self._Lock = Lock()
        self._duration = 0
        self._points = 0
        self._first_pkg_id = None
        self._last_pkg_id = None
        self._first_timestamp = None
        self._start_time = None
        self._end_time = None
        self._patient_code = "patient_code"
        self._patient_name = "patient_name"
        self._device_type = "24130032"
        self._device_no = "24130032"
        self._total_packets = 0
        self._lost_packets = 0
        self._storage_path = storage_path
        self._edf_writer_thread = None
        self._file_prefix = None
        
    @property
    def file_name(self): 
        suffix = "bdf" if self.resolution == 24 else "edf"
        
        # 文件名称
        file_name = f"{self._file_prefix}_{self._device_no}_{self._start_time.strftime('%y%m%d%H%I%M')}.{suffix}" if self._file_prefix else f"{self._device_no}_{self._start_time.strftime('%y%m%d%H%I%M')}.{suffix}"
        
        if self._storage_path:
            try:
                os.makedirs(self._storage_path, exist_ok=True)  # 自动创建目录，存在则忽略
                return f"{self._storage_path}/{file_name}"
            except Exception as e:
                logger.error(f"创建目录[{self._storage_path}]失败: {e}")
            
        
        return file_name
    
    def set_device_type(self, device_type):
        if device_type == 0x39:
            self._device_type = "C64RS"
        elif device_type == 0x40:
            self._device_type = "LJ64S1"
        else:
            self._device_type = hex(device_type)
        
    def set_device_no(self, device_no):
        self._device_no = device_no
        
    def set_storage_path(self, storage_path):
        self._storage_path = storage_path
        
    def set_file_prefix(self, file_prefix):
        self._file_prefix = file_prefix
        
    def set_patient_code(self, patient_code):
        self._patient_code = patient_code
        
    def set_patient_name(self, patient_name):
        self._patient_name = patient_name
    
    def write(self, packet: RscPacket):
        logger.debug(f"packet: {packet}")    
        if packet is None:
            self._edf_writer_thread.stop_recording()
            return
    
        if self.channels is None:
            logger.info(f"开始记录数据到文件...")
            self.channels = packet.channels
            self._first_pkg_id = packet.pkg_id if self._first_pkg_id is None else self._first_pkg_id
            self._first_timestamp = packet.time_stamp if self._first_timestamp is None else self._first_timestamp
            self._start_time = datetime.now()
            logger.info(f"第一个包id: {self._first_pkg_id }, 时间戳:{self._first_timestamp}， 当前时间:{datetime.now().timestamp()}  offset: {datetime.now().timestamp() - self._first_timestamp}")
            
        if self._last_pkg_id and self._last_pkg_id != packet.pkg_id - 1:  
            self._lost_packets += packet.pkg_id - self._last_pkg_id - 1
            logger.warning(f"数据包丢失: {self._last_pkg_id} -> {packet.pkg_id}, 丢包数: {packet.pkg_id - self._last_pkg_id - 1}")
            
        self._last_pkg_id = packet.pkg_id
        self._total_packets += 1
        
        if self._edf_writer_thread is None:
            self._edf_writer_thread = EDFStreamWriter(self.channels, self.sample_rate, self.physical_max, self.physical_min, self.file_type, self.file_name)
            self._edf_writer_thread.set_start_time(self._start_time)
            self._edf_writer_thread.start()
            logger.info(f"开始写入数据: {self.file_name}")
            
        self._edf_writer_thread.append(packet.eeg)
            
    
    # trigger标记
    # desc: 标记内容
    # cur_time: 设备时间时间戳，非设备发出的trigger不要设置
    def trigger(self, desc, cur_time=None):
        if cur_time is None:
            onset = datetime.now().timestamp() - self._start_time.timestamp()
        else:
            onset = cur_time - self._first_timestamp
        self._edf_writer_thread.trigger(onset, desc)     
    