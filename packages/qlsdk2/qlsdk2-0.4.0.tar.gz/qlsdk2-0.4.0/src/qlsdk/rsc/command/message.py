import abc
from typing import Dict, Type
from enum import Enum
from loguru import logger
from rsc.core.crctools import crc16

class DeviceCommand(abc.ABC):
    # 消息头
    HEADER_PREFIX = b'\x5A\xA5'
    # 消息头总长度 2(prefix) +1(pkgType) +1(deviceType) +4(deviceId) +4(len) +2(cmd)
    HEADER_LEN = 14  
    # 消息指令码位置
    CMD_POS = 12
    
    def __init__(self, device):
        self.device = device
        
    @classmethod
    def build(cls, device) :
        return cls(device)
    
    @property
    @abc.abstractmethod
    def cmd_code(self) -> int:
        pass
    
    @staticmethod
    def checksum(data: bytes) -> bytes:
        return crc16(data).to_bytes(2, 'little')

    def pack(self, body=b'') -> bytes:
        # header+body+checksum
        header = self.header_pack(len(body))
        payload = header + body
        return payload + DeviceCommand.checksum(payload)
    
    def header_pack(self, body_len: int) -> bytes:
        """构建消息头"""
        return (
            DeviceCommand.HEADER_PREFIX
            + self.device.pkg_type.to_bytes(1, 'little')            
            + self.device.device_type.to_bytes(1, 'little')
            + self.device.device_id.to_bytes(4, 'little')
            + (DeviceCommand.HEADER_LEN + body_len + 2).to_bytes(4, 'little')  # +1 for checksum
            + self.cmd_code.to_bytes(2, 'little')
        )
    
    def unpack(self, payload: bytes) -> bytes:
        """解析消息体"""
        # 解析消息体
        body = payload[self.HEADER_LEN:-2]
    
    
class DeviceInfoCommand(DeviceCommand):
    """设备信息指令"""
    cmd_code = 0x01
    
    def parse_body(self, body: bytes):
        # 解析设备信息
        pass

class SignalDataCommand(DeviceCommand):
    """设备信息指令"""
    cmd_code = 0x02
    
    def parse_body(self, body: bytes):
        # 解析设备信息
        pass
    
if __name__ == "__main__":
    # 测试代码
    device = None  # 这里应该是设备实例
    command1 = DeviceInfoCommand.build(device)
    logger.debug(command1.cmd_code)
    command2 = SignalDataCommand.build(device)
    logger.debug(command2.cmd_code)
    
    

class CommandFactory:
    """Registry for command implementations"""
    _commands: Dict[int, Type[DeviceCommand]] = {}
    
    @classmethod
    def register_command(cls, code: int, command: Type[DeviceCommand]):
        cls._commands[code] = command
    
    @classmethod
    def create_command(cls, code: int) -> Type[DeviceCommand]:
        logger.debug(f"Creating command for code: {hex(code)}")
        if code not in cls._commands:
            logger.warning(f"Unsupported command code: {hex(code)}")
            return cls._commands[DefaultCommand.cmd_code]
        return cls._commands[code]

# =============================================================================
class DefaultCommand(DeviceCommand):    
    cmd_code = 0x00   
        
    def parse_body(self, body: bytes):
        # Response parsing example: 2 bytes version + 4 bytes serial
        logger.info(f"Received body len: {len(body)}")
    
class GetDeviceInfoCommand(DeviceCommand):
    cmd_code = 0x17
    
    def parse_body(self, body: bytes):
        logger.info(f"Received GetDeviceInfoCommand body len: {len(body)}")
        # time - 8b
        self.device.connect_time = int.from_bytes(body[0:8], 'little')
        self.device.current_time = self.device.connect_time
        # result - 1b
        result = body[8]
        # deviceId - 4b
        self.device.device_id = body[9:13].hex()
        # deviceType - 4b
        self.device.device_type = body[13:17].hex()
        # softVersion - 4b
        self.device.software_version = body[17:21].hex()
        # hardVersion - 4b
        self.device.hardware_version = body[21:25].hex()
        # deviceName - 16b
        self.device.device_name = body[25:41].decode('utf-8').rstrip('\x00')
        # flag - 4b
        flag = int.from_bytes(body[41:45], 'little')
        logger.debug(f"Received device info: {result}, {flag}, {self.device}")
        

# 握手
class HandshakeCommand(DeviceCommand):
    cmd_code = 0x01
    
    def parse_body(self, body: bytes):
        logger.info(f"Received handshake response: {body.hex()}")

# 查询电量
class QueryBatteryCommand(DeviceCommand):
    cmd_code = 0x16
    def parse_body(self, body: bytes):
        logger.info(f"Received QueryBatteryCommand body len: {len(body)}")
        # time - 8b
        self.device.current_time = int.from_bytes(body[0:8], 'little')
        # result - 1b
        result = body[8]
        # 更新设备信息
        if result == 0:
            # voltage - 2b mV
            self.device.voltage = int.from_bytes(body[9:11], 'little')
            # soc - 1b
            self.device.battery_remain = body[11]
            # soh - 1b
            self.device.battery_total = body[12]
            # state - 1b
            # state = body[13]
        else:
            logger.warning(f"QueryBatteryCommand message received but result is failed.")

# 设置采集参数
class SetAcquisitionParamCommand(DeviceCommand):
    cmd_code = 0x451
    def parse_body(self, body: bytes):
        logger.info(f"Received SetAcquisitionParam response: {body.hex()}")
        
# 启动采集
class StartAcquisitionCommand(DeviceCommand):
    cmd_code = 0x452
    def parse_body(self, body: bytes):
        logger.info(f"Received acquisition start response: {body.hex()}")

# 停止采集
class StopAcquisitionCommand(DeviceCommand):
    cmd_code = 0x453
    
    def parse_body(self, body: bytes):
        logger.info(f"Received acquisition stop response: {body.hex()}")
# 设置阻抗采集参数
class SetImpedanceParamCommand(DeviceCommand):
    cmd_code = 0x411
    def parse_body(self, body: bytes):
        logger.info(f"Received SetImpedanceParamCommand response: {body.hex()}")
# 启动采集
class StartImpedanceCommand(DeviceCommand):
    cmd_code = 0x412
    def parse_body(self, body: bytes):
        logger.info(f"Received StartImpedanceCommand response: {body.hex()}")

# 停止采集
class StopImpedanceCommand(DeviceCommand):
    cmd_code = 0x413
    
    def parse_body(self, body: bytes):
        logger.info(f"Received StopImpedanceCommand response: {body.hex()}")
        
# 启动采集
class StartStimulationCommand(DeviceCommand):
    cmd_code = 0x48C
    def parse_body(self, body: bytes):
        logger.info(f"Received acquisition start response: {body.hex()}")

# 停止采集
class StopStimulationCommand(DeviceCommand):
    cmd_code = 0x488
    
    def parse_body(self, body: bytes):
        logger.info(f"Received acquisition stop response: {body.hex()}")

# 阻抗数据
class ImpedanceDataCommand(DeviceCommand):
    cmd_code = 0x415
    
    def parse_body(self, body: bytes):
        logger.info(f"Received impedance data: {body.hex()}")

# 信号数据
class SignalDataCommand(DeviceCommand):
    cmd_code = 0x455
    
    def parse_body(self, body: bytes):        
        logger.info(f"Received signal data: {len(body)}字节, the subscribe is {self.device.signal_consumers}")
        for q in list(self.device.signal_consumers.values()):
            q.put(body)

# =============================================================================
# Command Registration
# =============================================================================

CommandFactory.register_command(DefaultCommand.cmd_code, DefaultCommand)
CommandFactory.register_command(GetDeviceInfoCommand.cmd_code, GetDeviceInfoCommand)
CommandFactory.register_command(HandshakeCommand.cmd_code, HandshakeCommand)
CommandFactory.register_command(QueryBatteryCommand.cmd_code, QueryBatteryCommand)
CommandFactory.register_command(SetAcquisitionParamCommand.cmd_code, SetAcquisitionParamCommand)
CommandFactory.register_command(StartAcquisitionCommand.cmd_code, StartAcquisitionCommand)
CommandFactory.register_command(StopAcquisitionCommand.cmd_code, StopAcquisitionCommand)
CommandFactory.register_command(SetImpedanceParamCommand.cmd_code, SetImpedanceParamCommand)
CommandFactory.register_command(StartImpedanceCommand.cmd_code, StartImpedanceCommand)
CommandFactory.register_command(StopImpedanceCommand.cmd_code, StopImpedanceCommand)
CommandFactory.register_command(StartStimulationCommand.cmd_code, StartStimulationCommand)
CommandFactory.register_command(ImpedanceDataCommand.cmd_code, ImpedanceDataCommand)
CommandFactory.register_command(SignalDataCommand.cmd_code, SignalDataCommand)