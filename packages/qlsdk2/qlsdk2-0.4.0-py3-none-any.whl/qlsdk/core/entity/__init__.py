from qlsdk.core.utils import to_channels
from loguru import logger

class DataPacket(object):
    def __init__(self, device_type, device_id, channels, data):
        self.data = data
        self.channels = None
        
            
class RscPacket(object):
    def __init__(self):
        self.time_stamp = None
        self.pkg_id = None
        self.result = None
        self.channels = None
        self.origin_sample_rate = None
        self.sample_rate = None
        self.sample_num = None
        self.resolution = None
        self.filter = None
        self.data_len = None
        self.trigger = None
        self.eeg = None
    
    def transfer(self, body: bytes) -> 'RscPacket':
        self.time_stamp = int.from_bytes(body[0:8], 'little')
        self.result = body[8]
        self.pkg_id = int.from_bytes(body[9: 13], 'little')
        self.channels = to_channels(body[13: 45])
        self.origin_sample_rate = int.from_bytes(body[45: 49], 'little')
        self.sample_rate = int.from_bytes(body[49: 53], 'little')
        self.sample_num = int.from_bytes(body[53: 57], 'little')
        self.resolution = int(int(body[57]) / 8)
        self.filter = body[58]
        self.data_len = int.from_bytes(body[59: 63], 'little')
        # 步径 相同通道的点间隔
        step = int(len(self.channels) * self.resolution + 4)
        self.trigger = [int.from_bytes(body[i:i+4], 'little') for i in range(63, len(body) - 3, step)]
        b_eeg = body[63:]
        ch_num = len(self.channels) 
        self.eeg = [
            [
                int.from_bytes(b_eeg[i * self.resolution + 4 + j * step:i * self.resolution + 4 + j * step + 3], 'big', signed=True)
                for j in range(self.sample_num)
            ]
            for i in range(ch_num)
        ]
                
        # logger.trace(self)
        return self
        
    def __str__(self):
        return f"""
            time_stamp: {self.time_stamp}
            pkg_id: {self.pkg_id}
            origin_sample_rate: {self.origin_sample_rate}
            sample_rate: {self.sample_rate}
            sample_num: {self.sample_num}
            resolution: {self.resolution}
            filter: {self.filter}
            channels: {self.channels}
            data len: {self.data_len}
            trigger: {self.trigger}
            eeg: {self.eeg}
        """
        
class ImpedancePacket(object):
    def __init__(self):
        self.time_stamp = None
        self.pkg_id = None
        self.result = None
        self.channels = None
        self.data_len = None
        self.impedance = None
        
    def transfer(self, body:bytes) -> 'ImpedancePacket':
        self.time_stamp = int.from_bytes(body[0:8], 'little')
        self.result = body[8]
        self.pkg_id = int.from_bytes(body[9: 13], 'little')
        self.channels = to_channels(body[13: 45])
        
        logger.debug(f"impedance: {self}")
        
    def __str__(self):
        return f"""
            time_stamp: {self.time_stamp}
            pkg_id: {self.pkg_id}
            result: {self.result}
            channels: {self.channels}
            data len: {self.data_len}
            impedance: {self.impedance}
        """