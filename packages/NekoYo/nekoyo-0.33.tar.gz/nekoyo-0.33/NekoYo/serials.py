import serial

ser_port = "COM5"
ser_baudrate = 4800

import serial

# 初始化参数移至模块顶部
ser_port = "COM5"
ser_baudrate = 4800
cat_ser = None  # 新增全局变量声明

def init_connection():
    """显式初始化串口连接"""
    global cat_ser
    try:
        cat_ser = serial.Serial(port=ser_port, baudrate=ser_baudrate)
        cat_ser.setRTS(False)
        cat_ser.setDTR(False)
        cat_ser.timeout = 1
        return True
    except Exception as e:
        print(f"串口初始化失败: {str(e)}")
        return False


def set_port(port):
    global ser_port
    ser_port = port
    return ser_port
    # set port name
    # e.g.:"COM1"
def set_baudrate(baudrate):
    global ser_baudrate
    ser_baudrate = baudrate
    return ser_baudrate
    # set baudrate
    # e.g.:"9600"


if __name__ == "__main__":
    if init_connection():
        print("串口连接成功")
