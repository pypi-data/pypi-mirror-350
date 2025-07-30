"""

    ArducamEvkSDK
"""
from __future__ import annotations
import numpy
import typing
__all__ = ['Camera', 'CameraConfig', 'CaptureMethodConflict', 'CaptureTimeout', 'ConfigFileEmpty', 'ConfigFormatError', 'Control', 'ControlFormatError', 'Critical', 'DMA', 'Debug', 'Device', 'DeviceConnect', 'DeviceDisconnect', 'DeviceList', 'DeviceToHost', 'Empty', 'Err', 'ErrorCode', 'EventCode', 'Exit', 'Firmware', 'Format', 'FormatMode', 'Frame', 'FrameEnd', 'FrameStart', 'FreeEmptyBuffer', 'FreeUnknowBuffer', 'Full', 'High', 'HostToDevice', 'I2CMode', 'I2C_MODE_16_16', 'I2C_MODE_16_32', 'I2C_MODE_16_8', 'I2C_MODE_8_16', 'I2C_MODE_8_8', 'Info', 'InitCameraFailed', 'JPG', 'LoggerLevel', 'Low', 'MON', 'MON_D', 'MemType', 'MemoryAllocateFailed', 'NotSupported', 'Off', 'OpenCameraFailed', 'Param', 'RAM', 'RAW', 'RAW_D', 'RGB', 'RGB_IR', 'ReadConfigFileFailed', 'RegisterMultipleCallback', 'STATS', 'StateError', 'Success', 'Super', 'SuperPlus', 'SyncTime', 'System', 'TOF', 'TimeSource', 'Trace', 'TransferError', 'TransferLengthError', 'TransferTimeout', 'USBSpeed', 'USBTypeMismatch', 'Unknown', 'UnknownDeviceType', 'UnknownError', 'UnknownUSBType', 'UserdataAddrError', 'UserdataLenError', 'VRCommandDirection', 'VRCommandError', 'Warn', 'YUV', 'get_error_name']
class Camera:
    def __init__(self) -> None:
        ...
    def add_log_file(self, filename: str) -> bool:
        """
        add a log file
        """
    def capture(self, timeout: int = 2000) -> typing.Any:
        """
        capture a image, return a object of Frame, or None if failed
        """
    def check_usb_type(self) -> bool:
        """
        check the connection usb type is expected or not
        """
    def clear_buffer(self) -> bool:
        """
        clear the buffer
        """
    def close(self) -> bool:
        """
        close the camera
        """
    def enable_console_log(self, enable: bool = True) -> None:
        """
        enable/disable console log
        """
    def get_auto_transfer(self) -> typing.Any:
        """
        get the recommended transfer configuration
        """
    def get_avail_count(self) -> int:
        """
        get the available frame count
        """
    def has_capture_callback(self) -> bool:
        """
        check if the callback function for reading a frame is set
        """
    def has_event_callback(self) -> bool:
        """
        check if the callback function for event is set
        """
    def has_message_callback(self) -> bool:
        """
        check if the callback function for message is set
        """
    def init(self) -> bool:
        """
        init the camera
        """
    def is_opened(self) -> bool:
        """
        check if the camera is opened
        """
    def open(self, param: Param) -> bool:
        """
        open the camera
        """
    def read_board_config(self, command: int, value: int, index: int, buf_size: int) -> typing.Any:
        """
        read sensor register
        """
    def read_reg(self, mode: I2CMode, i2c_addr: int, regAddr: int) -> typing.Any:
        """
        read sensor register
        """
    def read_reg_16_16(self, ship_addr: int, reg_addr: int) -> typing.Any:
        """
        Reads a register value with 16 bit address and 16-bit value.
        """
    def read_reg_16_8(self, ship_addr: int, reg_addr: int) -> typing.Any:
        """
        Reads a register value with 16 bit address and 8-bit value.
        """
    def read_reg_8_16(self, ship_addr: int, reg_addr: int) -> typing.Any:
        """
        Reads a register value with 8 bit address and 16-bit value.
        """
    def read_reg_8_8(self, ship_addr: int, reg_addr: int) -> typing.Any:
        """
        Reads a register value with 8 bit address and 8-bit value.
        """
    def read_sensor_reg(self, reg_addr: int) -> typing.Any:
        """
        read sensor register
        """
    def read_user_data(self, addr: int, len: int) -> typing.Any:
        """
        read sensor register
        """
    def register_control(self, controls: list[Control]) -> bool:
        """
        register controls
        """
    def send_vr(self, command: int, direction: int, value: int, index: int, buffer: list[int]) -> typing.Any:
        """
        send vendor request
        """
    def set_auto_transfer(self, auto_transfer: bool) -> bool:
        """
        enable or disable the automatic transfer configuration before starting the camera
        """
    def set_capture_callback(self, callback: typing.Callable[[Frame], None]) -> None:
        """
        set the callback function for reading a frame, or None to disable it
        """
    def set_control(self, controlId: str, value: int) -> bool:
        """
        set control value
        """
    def set_event_callback(self, callback: typing.Callable[[EventCode], None]) -> None:
        """
        set the callback function for event, or None to disable it
        """
    def set_message_callback(self, callback: typing.Callable[[LoggerLevel, str], None]) -> None:
        """
        set the callback function for messages, or None to disable it
        """
    def set_time_source(self, val: TimeSource) -> bool:
        """
        set time source
        """
    def set_transfer(self, transfer_size: int, transfer_buffer_size: int) -> bool:
        """
        set transfer size and buffer size
        """
    def start(self) -> bool:
        """
        start the camera
        """
    def stop(self) -> bool:
        """
        stop the camera
        """
    def switch_mode(self, mode_id: int) -> bool:
        """
        switch the camera mode
        """
    def wait_capture(self, timeout: int = 2000) -> bool:
        """
        wait for a frame to be captured, return True if success, False if timeout
        """
    def write_board_config(self, command: int, value: int, index: int, buffer: list[int]) -> bool:
        """
        write sensor register
        """
    def write_reg(self, mode: I2CMode, i2c_addr: int, regAddr: int, value: int) -> bool:
        """
        write sensor register
        """
    def write_reg_16_16(self, ship_addr: int, reg_addr: int, value: int) -> bool:
        """
        Writes a register value with 16 bit address and 16-bit value.
        """
    def write_reg_16_8(self, ship_addr: int, reg_addr: int, value: int) -> bool:
        """
        Writes a register value with 16 bit address and 8-bit value.
        """
    def write_reg_8_16(self, ship_addr: int, reg_addr: int, value: int) -> bool:
        """
        Writes a register value with 8 bit address and 16-bit value.
        """
    def write_reg_8_8(self, ship_addr: int, reg_addr: int, value: int) -> bool:
        """
        Writes a register value with 8 bit address and 8-bit value.
        """
    def write_sensor_reg(self, reg_addr: int, value: int) -> bool:
        """
        write sensor register
        """
    def write_user_data(self, addr: int, data: list[int]) -> bool:
        """
        write sensor register
        """
    @property
    def bandwidth(self) -> int:
        """
        A property of bandwidth (read-only).
        """
    @bandwidth.setter
    def bandwidth() -> None:
        ...
    @property
    def bin_config(self) -> dict:
        """
        A property of bin_config (read-only).
        """
    @bin_config.setter
    def bin_config() -> None:
        ...
    @property
    def capture_fps(self) -> int:
        """
        A property of capture_fps (read-only).
        """
    @capture_fps.setter
    def capture_fps() -> None:
        ...
    @property
    def config(self) -> CameraConfig:
        """
        A property of config.
        """
    @config.setter
    def config(self, arg1: CameraConfig) -> bool:
        ...
    @property
    def config_type(self) -> str:
        """
        A property of config_type (read-only). ('NONE' | 'TEXT' | 'BINARY')
        """
    @config_type.setter
    def config_type() -> None:
        ...
    @property
    def controls(self) -> list[Control]:
        """
        A property of controls (read-only).
        """
    @controls.setter
    def controls() -> None:
        ...
    @property
    def device(self) -> Device:
        """
        A property of device (read-only).
        """
    @device.setter
    def device() -> None:
        ...
    @property
    def force_capture(self) -> bool:
        """
        A property of force_capture.
        """
    @force_capture.setter
    def force_capture(self, arg1: bool) -> None:
        ...
    @property
    def last_error(self) -> int:
        """
        A property of last_error (read-only).
        """
    @last_error.setter
    def last_error() -> None:
        ...
    @property
    def last_error_message(self) -> str:
        """
        A property of last_error_message (read-only).
        """
    @last_error_message.setter
    def last_error_message() -> None:
        ...
    @property
    def log_level(self) -> LoggerLevel:
        """
        A property of log_level.
        """
    @log_level.setter
    def log_level(self, arg1: LoggerLevel) -> None:
        ...
    @property
    def mem_type(self) -> MemType:
        """
        A property of mem_type.
        """
    @mem_type.setter
    def mem_type(self, arg1: MemType) -> bool:
        ...
    @property
    def usb_type(self) -> str:
        """
        A property of usb_type (read-only).
        """
    @usb_type.setter
    def usb_type() -> None:
        ...
    @property
    def usb_type_num(self) -> int:
        """
        A property of usb_type_num (read-only).
        """
    @usb_type_num.setter
    def usb_type_num() -> None:
        ...
class CameraConfig:
    def __init__(self) -> None:
        ...
    @property
    def bit_width(self) -> int:
        """
        A property of bit_width.
        """
    @bit_width.setter
    def bit_width(self, arg0: int) -> None:
        ...
    @property
    def camera_name(self) -> str:
        """
        A property of camera_name.
        """
    @camera_name.setter
    def camera_name(self, arg1: str) -> None:
        ...
    @property
    def format(self) -> int:
        """
        A property of format.
        """
    @format.setter
    def format(self, arg0: int) -> None:
        ...
    @property
    def height(self) -> int:
        """
        A property of height.
        """
    @height.setter
    def height(self, arg0: int) -> None:
        ...
    @property
    def i2c_addr(self) -> int:
        """
        A property of i2c_addr.
        """
    @i2c_addr.setter
    def i2c_addr(self, arg0: int) -> None:
        ...
    @property
    def i2c_mode(self) -> int:
        """
        A property of i2c_mode.
        """
    @i2c_mode.setter
    def i2c_mode(self, arg0: int) -> None:
        ...
    @property
    def width(self) -> int:
        """
        A property of width.
        """
    @width.setter
    def width(self, arg0: int) -> None:
        ...
class Control:
    def __init__(self) -> None:
        """
        Creates a new control.
        """
    def __repr__(self) -> str:
        """
        Returns a string representation of the control.
        """
    def __str__(self) -> str:
        """
        Returns a string representation of the control.
        """
    @property
    def code(self) -> str:
        """
        A property of code.
        """
    @code.setter
    def code(self, arg0: str) -> None:
        ...
    @property
    def default(self) -> int:
        """
        A property of default.
        """
    @default.setter
    def default(self, arg0: int) -> None:
        ...
    @property
    def flags(self) -> int:
        """
        A property of flags.
        """
    @flags.setter
    def flags(self, arg0: int) -> None:
        ...
    @property
    def func(self) -> str:
        """
        A property of func (read-only).
        """
    @func.setter
    def func() -> None:
        ...
    @property
    def max(self) -> int:
        """
        A property of max.
        """
    @max.setter
    def max(self, arg0: int) -> None:
        ...
    @property
    def min(self) -> int:
        """
        A property of min.
        """
    @min.setter
    def min(self, arg0: int) -> None:
        ...
    @property
    def name(self) -> str:
        """
        A property of name (read-only).
        """
    @name.setter
    def name() -> None:
        ...
    @property
    def step(self) -> int:
        """
        A property of step.
        """
    @step.setter
    def step(self, arg0: int) -> None:
        ...
class Device:
    def __eq__(self, arg0: Device) -> bool:
        """
        Check the Devices are same.
        """
    def __hash__(self) -> int:
        """
        Returns the hash value of the device.
        """
    def __repr__(self) -> str:
        """
        Returns a string representation of the device.
        """
    @property
    def dev_path(self) -> str:
        """
        A property of dev_path (const).
        """
    @property
    def id_product(self) -> int:
        """
        A property of id_product (const).
        """
    @property
    def id_vendor(self) -> int:
        """
        A property of id_vendor (const).
        """
    @property
    def in_used(self) -> bool:
        """
        A property of in_used (const).
        """
    @property
    def serial_number(self) -> list[int]:
        """
        A property of serial_number (const).This is a list with 12 elements.
        """
    @property
    def speed(self) -> USBSpeed:
        """
        A property of speed (const).
        """
    @property
    def usb_type(self) -> int:
        """
        A property of usb_type (const).
        """
class DeviceList:
    def __init__(self) -> None:
        ...
    def devices(self) -> list[Device]:
        """
        All supported devices
        """
    def has_event_callback(self) -> bool:
        """
        Check if the callback function for event is set
        """
    def refresh(self) -> bool:
        """
        Refreshes the device list
        """
    def set_event_callback(self, callback: typing.Callable[[EventCode, Device | None], None]) -> bool:
        """
        Set the callback function for event, or None to disable it
        """
class ErrorCode:
    """
    Members:
    
      Success : Success.
    
      Empty : Empty.
    
      ReadConfigFileFailed : Failed to read configuration file.
    
      ConfigFileEmpty : Configuration file is empty.
    
      ConfigFormatError : Camera configuration format error.
    
      ControlFormatError : Camera control format error.
    
      OpenCameraFailed : Failed to open camera.
    
      UnknownUSBType : Unknown USB type.
    
      UnknownDeviceType : Unknown Device type.
    
      InitCameraFailed : Failed to initialize camera.
    
      MemoryAllocateFailed : Failed to allocate memory.
    
      USBTypeMismatch : USB type mismatch.
    
      CaptureTimeout : Capture timeout.
    
      CaptureMethodConflict : Capture method conflict.
    
      FreeEmptyBuffer : Free empty buffer.
    
      FreeUnknowBuffer : Free unknown buffer.
    
      RegisterMultipleCallback : Register multiple callback.
    
      StateError : Camera state error.
    
      NotSupported : Not supported.
    
      VRCommandError : Vendor command error.
    
      UserdataAddrError : Userdata address error.
    
      UserdataLenError : Userdata length error.
    
      UnknownError : Unknown error.
    """
    CaptureMethodConflict: typing.ClassVar[ErrorCode]  # value = <ErrorCode.CaptureMethodConflict: 1538>
    CaptureTimeout: typing.ClassVar[ErrorCode]  # value = <ErrorCode.CaptureTimeout: 1537>
    ConfigFileEmpty: typing.ClassVar[ErrorCode]  # value = <ErrorCode.ConfigFileEmpty: 258>
    ConfigFormatError: typing.ClassVar[ErrorCode]  # value = <ErrorCode.ConfigFormatError: 259>
    ControlFormatError: typing.ClassVar[ErrorCode]  # value = <ErrorCode.ControlFormatError: 260>
    Empty: typing.ClassVar[ErrorCode]  # value = <ErrorCode.Empty: 16>
    FreeEmptyBuffer: typing.ClassVar[ErrorCode]  # value = <ErrorCode.FreeEmptyBuffer: 1793>
    FreeUnknowBuffer: typing.ClassVar[ErrorCode]  # value = <ErrorCode.FreeUnknowBuffer: 1794>
    InitCameraFailed: typing.ClassVar[ErrorCode]  # value = <ErrorCode.InitCameraFailed: 769>
    MemoryAllocateFailed: typing.ClassVar[ErrorCode]  # value = <ErrorCode.MemoryAllocateFailed: 770>
    NotSupported: typing.ClassVar[ErrorCode]  # value = <ErrorCode.NotSupported: 61441>
    OpenCameraFailed: typing.ClassVar[ErrorCode]  # value = <ErrorCode.OpenCameraFailed: 513>
    ReadConfigFileFailed: typing.ClassVar[ErrorCode]  # value = <ErrorCode.ReadConfigFileFailed: 257>
    RegisterMultipleCallback: typing.ClassVar[ErrorCode]  # value = <ErrorCode.RegisterMultipleCallback: 2049>
    StateError: typing.ClassVar[ErrorCode]  # value = <ErrorCode.StateError: 32769>
    Success: typing.ClassVar[ErrorCode]  # value = <ErrorCode.Success: 0>
    USBTypeMismatch: typing.ClassVar[ErrorCode]  # value = <ErrorCode.USBTypeMismatch: 1025>
    UnknownDeviceType: typing.ClassVar[ErrorCode]  # value = <ErrorCode.UnknownDeviceType: 515>
    UnknownError: typing.ClassVar[ErrorCode]  # value = <ErrorCode.UnknownError: 65535>
    UnknownUSBType: typing.ClassVar[ErrorCode]  # value = <ErrorCode.UnknownUSBType: 514>
    UserdataAddrError: typing.ClassVar[ErrorCode]  # value = <ErrorCode.UserdataAddrError: 65377>
    UserdataLenError: typing.ClassVar[ErrorCode]  # value = <ErrorCode.UserdataLenError: 65378>
    VRCommandError: typing.ClassVar[ErrorCode]  # value = <ErrorCode.VRCommandError: 65283>
    __members__: typing.ClassVar[dict[str, ErrorCode]]  # value = {'Success': <ErrorCode.Success: 0>, 'Empty': <ErrorCode.Empty: 16>, 'ReadConfigFileFailed': <ErrorCode.ReadConfigFileFailed: 257>, 'ConfigFileEmpty': <ErrorCode.ConfigFileEmpty: 258>, 'ConfigFormatError': <ErrorCode.ConfigFormatError: 259>, 'ControlFormatError': <ErrorCode.ControlFormatError: 260>, 'OpenCameraFailed': <ErrorCode.OpenCameraFailed: 513>, 'UnknownUSBType': <ErrorCode.UnknownUSBType: 514>, 'UnknownDeviceType': <ErrorCode.UnknownDeviceType: 515>, 'InitCameraFailed': <ErrorCode.InitCameraFailed: 769>, 'MemoryAllocateFailed': <ErrorCode.MemoryAllocateFailed: 770>, 'USBTypeMismatch': <ErrorCode.USBTypeMismatch: 1025>, 'CaptureTimeout': <ErrorCode.CaptureTimeout: 1537>, 'CaptureMethodConflict': <ErrorCode.CaptureMethodConflict: 1538>, 'FreeEmptyBuffer': <ErrorCode.FreeEmptyBuffer: 1793>, 'FreeUnknowBuffer': <ErrorCode.FreeUnknowBuffer: 1794>, 'RegisterMultipleCallback': <ErrorCode.RegisterMultipleCallback: 2049>, 'StateError': <ErrorCode.StateError: 32769>, 'NotSupported': <ErrorCode.NotSupported: 61441>, 'VRCommandError': <ErrorCode.VRCommandError: 65283>, 'UserdataAddrError': <ErrorCode.UserdataAddrError: 65377>, 'UserdataLenError': <ErrorCode.UserdataLenError: 65378>, 'UnknownError': <ErrorCode.UnknownError: 65535>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class EventCode:
    """
    Members:
    
      FrameStart : Frame start
    
      FrameEnd : Frame end
    
      Exit : Exit
    
      SyncTime : SyncTime
    
      TransferError : Transfer error
    
      TransferTimeout : Transfer timeout
    
      TransferLengthError : Transfer length error
    
      DeviceConnect : Device connect
    
      DeviceDisconnect : Device disconnect
    """
    DeviceConnect: typing.ClassVar[EventCode]  # value = <EventCode.DeviceConnect: 512>
    DeviceDisconnect: typing.ClassVar[EventCode]  # value = <EventCode.DeviceDisconnect: 514>
    Exit: typing.ClassVar[EventCode]  # value = <EventCode.Exit: 3>
    FrameEnd: typing.ClassVar[EventCode]  # value = <EventCode.FrameEnd: 2>
    FrameStart: typing.ClassVar[EventCode]  # value = <EventCode.FrameStart: 1>
    SyncTime: typing.ClassVar[EventCode]  # value = <EventCode.SyncTime: 4>
    TransferError: typing.ClassVar[EventCode]  # value = <EventCode.TransferError: 256>
    TransferLengthError: typing.ClassVar[EventCode]  # value = <EventCode.TransferLengthError: 258>
    TransferTimeout: typing.ClassVar[EventCode]  # value = <EventCode.TransferTimeout: 257>
    __members__: typing.ClassVar[dict[str, EventCode]]  # value = {'FrameStart': <EventCode.FrameStart: 1>, 'FrameEnd': <EventCode.FrameEnd: 2>, 'Exit': <EventCode.Exit: 3>, 'SyncTime': <EventCode.SyncTime: 4>, 'TransferError': <EventCode.TransferError: 256>, 'TransferTimeout': <EventCode.TransferTimeout: 257>, 'TransferLengthError': <EventCode.TransferLengthError: 258>, 'DeviceConnect': <EventCode.DeviceConnect: 512>, 'DeviceDisconnect': <EventCode.DeviceDisconnect: 514>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Format:
    def __init__(self) -> None:
        ...
    @property
    def bit_depth(self) -> int:
        """
        A property of bit_depth.
        """
    @bit_depth.setter
    def bit_depth(self, arg0: int) -> None:
        ...
    @property
    def format_code(self) -> int:
        """
        A property of format_code.
        """
    @format_code.setter
    def format_code(self, arg0: int) -> None:
        ...
    @property
    def height(self) -> int:
        """
        A property of height.
        """
    @height.setter
    def height(self, arg0: int) -> None:
        ...
    @property
    def width(self) -> int:
        """
        A property of width.
        """
    @width.setter
    def width(self, arg0: int) -> None:
        ...
class FormatMode:
    """
    Members:
    
      RAW : RAW
    
      RGB : RGB
    
      YUV : YUV
    
      JPG : JPG
    
      MON : MON
    
      RAW_D : RAW_D
    
      MON_D : MON_D
    
      TOF : TOF, deprecated
    
      STATS : STATS
    
      RGB_IR : RGB_IR
    """
    JPG: typing.ClassVar[FormatMode]  # value = <FormatMode.JPG: 3>
    MON: typing.ClassVar[FormatMode]  # value = <FormatMode.MON: 4>
    MON_D: typing.ClassVar[FormatMode]  # value = <FormatMode.MON_D: 6>
    RAW: typing.ClassVar[FormatMode]  # value = <FormatMode.RAW: 0>
    RAW_D: typing.ClassVar[FormatMode]  # value = <FormatMode.RAW_D: 5>
    RGB: typing.ClassVar[FormatMode]  # value = <FormatMode.RGB: 1>
    RGB_IR: typing.ClassVar[FormatMode]  # value = <FormatMode.RGB_IR: 9>
    STATS: typing.ClassVar[FormatMode]  # value = <FormatMode.STATS: 8>
    TOF: typing.ClassVar[FormatMode]  # value = <FormatMode.TOF: 7>
    YUV: typing.ClassVar[FormatMode]  # value = <FormatMode.YUV: 2>
    __members__: typing.ClassVar[dict[str, FormatMode]]  # value = {'RAW': <FormatMode.RAW: 0>, 'RGB': <FormatMode.RGB: 1>, 'YUV': <FormatMode.YUV: 2>, 'JPG': <FormatMode.JPG: 3>, 'MON': <FormatMode.MON: 4>, 'RAW_D': <FormatMode.RAW_D: 5>, 'MON_D': <FormatMode.MON_D: 6>, 'TOF': <FormatMode.TOF: 7>, 'STATS': <FormatMode.STATS: 8>, 'RGB_IR': <FormatMode.RGB_IR: 9>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Frame:
    def __init__(self) -> None:
        ...
    @property
    def bad(self) -> bool:
        """
        A property of bad.
        """
    @bad.setter
    def bad(self, arg0: bool) -> None:
        ...
    @property
    def data(self) -> numpy.ndarray[typing.Any, numpy.dtype[typing.Any]]:
        """
        A property of data.
        """
    @data.setter
    def data(self, arg0: numpy.ndarray[typing.Any, numpy.dtype[typing.Any]]) -> None:
        ...
    @property
    def format(self) -> Format:
        """
        A property of format.
        """
    @format.setter
    def format(self, arg0: Format) -> None:
        ...
    @property
    def seq(self) -> int:
        """
        A property of seq.
        """
    @seq.setter
    def seq(self, arg0: int) -> None:
        ...
    @property
    def size(self) -> int:
        """
        A property of size.
        """
    @size.setter
    def size(self, arg0: int) -> None:
        ...
    @property
    def timestamp(self) -> int:
        """
        A property of timestamp.
        """
    @timestamp.setter
    def timestamp(self, arg0: int) -> None:
        ...
class I2CMode:
    """
    Members:
    
      I2C_MODE_8_8 : 8-bit register address and 8-bit data
    
      I2C_MODE_8_16 : 8-bit register address and 16-bit data
    
      I2C_MODE_16_8 : 16-bit register address and 8-bit data
    
      I2C_MODE_16_16 : 16-bit register address and 16-bit data
    
      I2C_MODE_16_32 : 16-bit register address and 32-bit data
    """
    I2C_MODE_16_16: typing.ClassVar[I2CMode]  # value = <I2CMode.I2C_MODE_16_16: 3>
    I2C_MODE_16_32: typing.ClassVar[I2CMode]  # value = <I2CMode.I2C_MODE_16_32: 4>
    I2C_MODE_16_8: typing.ClassVar[I2CMode]  # value = <I2CMode.I2C_MODE_16_8: 2>
    I2C_MODE_8_16: typing.ClassVar[I2CMode]  # value = <I2CMode.I2C_MODE_8_16: 1>
    I2C_MODE_8_8: typing.ClassVar[I2CMode]  # value = <I2CMode.I2C_MODE_8_8: 0>
    __members__: typing.ClassVar[dict[str, I2CMode]]  # value = {'I2C_MODE_8_8': <I2CMode.I2C_MODE_8_8: 0>, 'I2C_MODE_8_16': <I2CMode.I2C_MODE_8_16: 1>, 'I2C_MODE_16_8': <I2CMode.I2C_MODE_16_8: 2>, 'I2C_MODE_16_16': <I2CMode.I2C_MODE_16_16: 3>, 'I2C_MODE_16_32': <I2CMode.I2C_MODE_16_32: 4>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class LoggerLevel:
    """
    Members:
    
      Trace : trace log level
    
      Debug : debug log level
    
      Info : info log level
    
      Warn : warn log level
    
      Err : err log level
    
      Critical : critical log level
    
      Off : off log level
    """
    Critical: typing.ClassVar[LoggerLevel]  # value = <LoggerLevel.Critical: 5>
    Debug: typing.ClassVar[LoggerLevel]  # value = <LoggerLevel.Debug: 1>
    Err: typing.ClassVar[LoggerLevel]  # value = <LoggerLevel.Err: 4>
    Info: typing.ClassVar[LoggerLevel]  # value = <LoggerLevel.Info: 2>
    Off: typing.ClassVar[LoggerLevel]  # value = <LoggerLevel.Off: 6>
    Trace: typing.ClassVar[LoggerLevel]  # value = <LoggerLevel.Trace: 0>
    Warn: typing.ClassVar[LoggerLevel]  # value = <LoggerLevel.Warn: 3>
    __members__: typing.ClassVar[dict[str, LoggerLevel]]  # value = {'Trace': <LoggerLevel.Trace: 0>, 'Debug': <LoggerLevel.Debug: 1>, 'Info': <LoggerLevel.Info: 2>, 'Warn': <LoggerLevel.Warn: 3>, 'Err': <LoggerLevel.Err: 4>, 'Critical': <LoggerLevel.Critical: 5>, 'Off': <LoggerLevel.Off: 6>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class MemType:
    """
    Members:
    
      DMA : DMA
    
      RAM : RAM
    """
    DMA: typing.ClassVar[MemType]  # value = <MemType.DMA: 1>
    RAM: typing.ClassVar[MemType]  # value = <MemType.RAM: 2>
    __members__: typing.ClassVar[dict[str, MemType]]  # value = {'DMA': <MemType.DMA: 1>, 'RAM': <MemType.RAM: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Param:
    def __init__(self) -> None:
        """
        construct a default param
        """
    @property
    def bin_config(self) -> bool:
        """
        A property of bin_config.
        """
    @bin_config.setter
    def bin_config(self, arg0: bool) -> None:
        ...
    @property
    def config_file_name(self) -> str:
        """
        A property of config_file_name.
        """
    @config_file_name.setter
    def config_file_name(self, arg0: str) -> None:
        ...
    @property
    def device(self) -> Device:
        """
        A property of device.
        """
    @device.setter
    def device(self, arg0: Device) -> None:
        ...
    @property
    def ext_config_file_name(self) -> str:
        """
        A property of ext_config_file_name.
        """
    @ext_config_file_name.setter
    def ext_config_file_name(self, arg0: str) -> None:
        ...
    @property
    def mem_type(self) -> MemType:
        """
        A property of mem_type.
        """
    @mem_type.setter
    def mem_type(self, arg0: MemType) -> None:
        ...
class TimeSource:
    """
    Members:
    
      System : System
    
      Firmware : Firmware
    """
    Firmware: typing.ClassVar[TimeSource]  # value = <TimeSource.Firmware: 1>
    System: typing.ClassVar[TimeSource]  # value = <TimeSource.System: 0>
    __members__: typing.ClassVar[dict[str, TimeSource]]  # value = {'System': <TimeSource.System: 0>, 'Firmware': <TimeSource.Firmware: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class USBSpeed:
    """
    Members:
    
      Unknown : The OS doesn't report or know the device speed.
    
      Low : The device is operating at low speed (1.5MBit/s).
    
      Full : The device is operating at full speed (12MBit/s).
    
      High : The device is operating at high speed (480MBit/s).
    
      Super : The device is operating at super speed (5000MBit/s).
    
      SuperPlus : The device is operating at super speed plus (10000MBit/s).
    """
    Full: typing.ClassVar[USBSpeed]  # value = <USBSpeed.Full: 2>
    High: typing.ClassVar[USBSpeed]  # value = <USBSpeed.High: 3>
    Low: typing.ClassVar[USBSpeed]  # value = <USBSpeed.Low: 1>
    Super: typing.ClassVar[USBSpeed]  # value = <USBSpeed.Super: 4>
    SuperPlus: typing.ClassVar[USBSpeed]  # value = <USBSpeed.SuperPlus: 5>
    Unknown: typing.ClassVar[USBSpeed]  # value = <USBSpeed.Unknown: 0>
    __members__: typing.ClassVar[dict[str, USBSpeed]]  # value = {'Unknown': <USBSpeed.Unknown: 0>, 'Low': <USBSpeed.Low: 1>, 'Full': <USBSpeed.Full: 2>, 'High': <USBSpeed.High: 3>, 'Super': <USBSpeed.Super: 4>, 'SuperPlus': <USBSpeed.SuperPlus: 5>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class VRCommandDirection:
    """
    Members:
    
      HostToDevice : Host to device
    
      DeviceToHost : Device to host
    """
    DeviceToHost: typing.ClassVar[VRCommandDirection]  # value = <VRCommandDirection.DeviceToHost: 128>
    HostToDevice: typing.ClassVar[VRCommandDirection]  # value = <VRCommandDirection.HostToDevice: 0>
    __members__: typing.ClassVar[dict[str, VRCommandDirection]]  # value = {'HostToDevice': <VRCommandDirection.HostToDevice: 0>, 'DeviceToHost': <VRCommandDirection.DeviceToHost: 128>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
def get_error_name(ec: int) -> str:
    """
    get the error name
    """
CaptureMethodConflict: ErrorCode  # value = <ErrorCode.CaptureMethodConflict: 1538>
CaptureTimeout: ErrorCode  # value = <ErrorCode.CaptureTimeout: 1537>
ConfigFileEmpty: ErrorCode  # value = <ErrorCode.ConfigFileEmpty: 258>
ConfigFormatError: ErrorCode  # value = <ErrorCode.ConfigFormatError: 259>
ControlFormatError: ErrorCode  # value = <ErrorCode.ControlFormatError: 260>
Critical: LoggerLevel  # value = <LoggerLevel.Critical: 5>
DMA: MemType  # value = <MemType.DMA: 1>
Debug: LoggerLevel  # value = <LoggerLevel.Debug: 1>
DeviceConnect: EventCode  # value = <EventCode.DeviceConnect: 512>
DeviceDisconnect: EventCode  # value = <EventCode.DeviceDisconnect: 514>
DeviceToHost: VRCommandDirection  # value = <VRCommandDirection.DeviceToHost: 128>
Empty: ErrorCode  # value = <ErrorCode.Empty: 16>
Err: LoggerLevel  # value = <LoggerLevel.Err: 4>
Exit: EventCode  # value = <EventCode.Exit: 3>
Firmware: TimeSource  # value = <TimeSource.Firmware: 1>
FrameEnd: EventCode  # value = <EventCode.FrameEnd: 2>
FrameStart: EventCode  # value = <EventCode.FrameStart: 1>
FreeEmptyBuffer: ErrorCode  # value = <ErrorCode.FreeEmptyBuffer: 1793>
FreeUnknowBuffer: ErrorCode  # value = <ErrorCode.FreeUnknowBuffer: 1794>
Full: USBSpeed  # value = <USBSpeed.Full: 2>
High: USBSpeed  # value = <USBSpeed.High: 3>
HostToDevice: VRCommandDirection  # value = <VRCommandDirection.HostToDevice: 0>
I2C_MODE_16_16: I2CMode  # value = <I2CMode.I2C_MODE_16_16: 3>
I2C_MODE_16_32: I2CMode  # value = <I2CMode.I2C_MODE_16_32: 4>
I2C_MODE_16_8: I2CMode  # value = <I2CMode.I2C_MODE_16_8: 2>
I2C_MODE_8_16: I2CMode  # value = <I2CMode.I2C_MODE_8_16: 1>
I2C_MODE_8_8: I2CMode  # value = <I2CMode.I2C_MODE_8_8: 0>
Info: LoggerLevel  # value = <LoggerLevel.Info: 2>
InitCameraFailed: ErrorCode  # value = <ErrorCode.InitCameraFailed: 769>
JPG: FormatMode  # value = <FormatMode.JPG: 3>
Low: USBSpeed  # value = <USBSpeed.Low: 1>
MON: FormatMode  # value = <FormatMode.MON: 4>
MON_D: FormatMode  # value = <FormatMode.MON_D: 6>
MemoryAllocateFailed: ErrorCode  # value = <ErrorCode.MemoryAllocateFailed: 770>
NotSupported: ErrorCode  # value = <ErrorCode.NotSupported: 61441>
Off: LoggerLevel  # value = <LoggerLevel.Off: 6>
OpenCameraFailed: ErrorCode  # value = <ErrorCode.OpenCameraFailed: 513>
RAM: MemType  # value = <MemType.RAM: 2>
RAW: FormatMode  # value = <FormatMode.RAW: 0>
RAW_D: FormatMode  # value = <FormatMode.RAW_D: 5>
RGB: FormatMode  # value = <FormatMode.RGB: 1>
RGB_IR: FormatMode  # value = <FormatMode.RGB_IR: 9>
ReadConfigFileFailed: ErrorCode  # value = <ErrorCode.ReadConfigFileFailed: 257>
RegisterMultipleCallback: ErrorCode  # value = <ErrorCode.RegisterMultipleCallback: 2049>
STATS: FormatMode  # value = <FormatMode.STATS: 8>
StateError: ErrorCode  # value = <ErrorCode.StateError: 32769>
Success: ErrorCode  # value = <ErrorCode.Success: 0>
Super: USBSpeed  # value = <USBSpeed.Super: 4>
SuperPlus: USBSpeed  # value = <USBSpeed.SuperPlus: 5>
SyncTime: EventCode  # value = <EventCode.SyncTime: 4>
System: TimeSource  # value = <TimeSource.System: 0>
TOF: FormatMode  # value = <FormatMode.TOF: 7>
Trace: LoggerLevel  # value = <LoggerLevel.Trace: 0>
TransferError: EventCode  # value = <EventCode.TransferError: 256>
TransferLengthError: EventCode  # value = <EventCode.TransferLengthError: 258>
TransferTimeout: EventCode  # value = <EventCode.TransferTimeout: 257>
USBTypeMismatch: ErrorCode  # value = <ErrorCode.USBTypeMismatch: 1025>
Unknown: USBSpeed  # value = <USBSpeed.Unknown: 0>
UnknownDeviceType: ErrorCode  # value = <ErrorCode.UnknownDeviceType: 515>
UnknownError: ErrorCode  # value = <ErrorCode.UnknownError: 65535>
UnknownUSBType: ErrorCode  # value = <ErrorCode.UnknownUSBType: 514>
UserdataAddrError: ErrorCode  # value = <ErrorCode.UserdataAddrError: 65377>
UserdataLenError: ErrorCode  # value = <ErrorCode.UserdataLenError: 65378>
VRCommandError: ErrorCode  # value = <ErrorCode.VRCommandError: 65283>
Warn: LoggerLevel  # value = <LoggerLevel.Warn: 3>
YUV: FormatMode  # value = <FormatMode.YUV: 2>
__version__: str = 'v1.0.7-9-g4658b2c'
