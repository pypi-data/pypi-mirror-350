# 修改导入方式为相对导入
from .serials import cat_ser  # 添加点号表示当前包
import serial


# 假设 cat_ser 是已经初始化的串口对象
cat_serial = cat_ser
sat_data_rx = "0000000000"
sat_data_tx = "0000000000"
real_data = "0000000000"
# x_freq, tx_freq, rx_mode, tx_mode = "0", "0", "0", "0"

# 在模块顶部定义模式映射字典
MODE_MAP = {
    "00": "USB",
    "01": "LSB",
    "02": "CW",
    "03": "CWR",
    "04": "AM",
    "08": "FM",
    "88": "FMN",
    "0A": "DIG",
    "0C": "SPEC"
}


def set_model(model):
    global spe_format
    if model == "FT-847":
        spe_format = True
    elif model == "others":
        spe_format = False


def set_lock(lock_status):
    # Type:bool
    # FT_847 do not support this action
    global cat_serial
    if lock_status:
        cat_serial.write(bytes.fromhex("00 00 00 00 00"))
    elif not lock_status:
        cat_serial.write(bytes.fromhex("00 00 00 00 08"))


def set_ptt(status):
    # Type:bool
    global cat_serial
    if status:
        cat_serial.write(bytes.fromhex("00 00 00 00 08"))
    elif not status:
        cat_serial.write(bytes.fromhex("00 00 00 00 88"))


def set_freq(freq):
    # 144/430 freq e.g.:435.12345MHz = "43512345"
    # HF/50MHz freq e.g.:50.31300MHz = "05031300"
    # Type:String
    global cat_serial
    cat_serial.write(bytes.fromhex(freq))


def set_mode(mode):
    # mode e.g.:USB(Type:String)
    # opera code = 07
    global cat_serial
    mode_code = ""
    if mode == "USB":
        mode_code = "01 00 00 00 07"
    elif mode == "LSB":
        mode_code = "00 00 00 00 07"
    elif mode == "CW":
        mode_code = "02 00 00 00 07"
    elif mode == "CWR":
        mode_code = "03 00 00 00 07"
    elif mode == "AM":
        mode_code = "04 00 00 00 07"
    elif mode == "FM":
        mode_code = "08 00 00 00 07"
    elif mode == "FMN":
        mode_code = "88 00 00 00 07"
    elif mode == "DIG":
        mode_code = "0A 00 00 00 07"
    elif mode == "SPEC":
        mode_code = "0C 00 00 00 07"
    cat_serial.write(bytes.fromhex(mode_code))


def set_clar(status):
    # Type:bool
    # opera code = 05
    global cat_serial
    if status:
        cat_serial.write(bytes.fromhex("00 00 00 00 05"))
    elif not status:
        cat_serial.write(bytes.fromhex("00 00 00 00 85"))


def set_clar_freq(freq):
    # e.g.:-12.34KHz = "-12 34"
    # e.g.:+12.34KHz = "+12 34"
    # Type:String
    # opera code = F5
    global cat_serial
    if freq[1] == "+":
        str_freq = freq[1:]
        cat_serial.write(bytes.fromhex("00 00" + str_freq + "F5"))
        cat_serial.write(bytes.fromhex(freq))
    elif freq[1] == "-":
        str_freq = freq[1:]
        cat_serial.write(bytes.fromhex("01 00" + str_freq + "F5"))
        cat_serial.write(bytes.fromhex(freq))


def set_vfo():
    # opera code = 81
    # use it to change vfo
    global cat_serial
    cat_serial.write(bytes.fromhex("00 00 00 00 81"))


def set_split(status):
    # Type:bool
    # opera code = 02, 08
    global cat_serial
    if status:
        cat_serial.write(bytes.fromhex("00 00 00 00 02"))
    elif not status:
        cat_serial.write(bytes.fromhex("00 00 00 00 08"))


def set_repeater_offset(freq):
    # e.g.:+5.432100MHz = "+05432100"
    # e.g.:-5.432100MHz = "-05432100"
    # e.g.:OFF = "0"
    # Freq max = +-99 99 99 99 99(99.99999999MHz)
    # Type:String
    # opera code = 09, 49, 89
    global cat_serial
    if freq[1] == "+":
        str_freq = freq[1:]
        cat_serial.write(bytes.fromhex("00 00 00 00 09"))
        cat_serial.write(bytes.fromhex(str_freq))
    elif freq[1] == "-":
        str_freq = freq[1:]
        cat_serial.write(bytes.fromhex("00 00 00 00 49"))
        cat_serial.write(bytes.fromhex(str_freq))
    elif freq == "0":
        cat_serial.write(bytes.fromhex("00 00 00 00 89"))


def set_ctcss_status(status):
    # Type:bool
    # opera code = 0A
    global cat_serial
    if status:
        cat_serial.write(bytes.fromhex("0A 00 00 00 2A"))
    elif not status:
        cat_serial.write(bytes.fromhex("0A 00 00 00 8A"))


def set_dcs_status(status):
    # Type:bool
    # opera code = 0A
    global cat_serial
    if status:
        cat_serial.write(bytes.fromhex("0A 00 00 00 0A"))
    elif not status:
        cat_serial.write(bytes.fromhex("0A 00 00 00 8A"))


def set_ctcss_coder(coder):
    # Type:String
    # opera code:0A
    # e.g.:Decoder on = dec
    # e.g.:Encoder on = enc
    # If want to turn it off,please see set_ctcss_status.
    global cat_serial
    if coder == "dec":
        cat_serial.write(bytes.fromhex("0A 00 00 00 3A"))
    elif coder == "enc":
        cat_serial.write(bytes.fromhex("0A 00 00 00 4A"))


def set_dcs_coder(coder):
    # Type:String
    # opera code:0A
    # e.g.:Decoder on = dec
    # e.g.:Encoder on = enc
    # If want to turn it off,please see set_dcs_status.
    global cat_serial
    if coder == "dec":
        cat_serial.write(bytes.fromhex("0A 00 00 00 0B"))
    elif coder == "enc":
        cat_serial.write(bytes.fromhex("0A 00 00 00 0C"))


def set_ctcss_freq(tx, rx):
    # Type:int
    # opera code:0B
    # e.g.:tx = 0885(88.5Hz), rx = 1000(100.0Hz)
    global cat_serial
    cat_serial.write(bytes.fromhex(str(tx) + str(rx) + "0B"))


def set_dcs_freq(tx, rx):
    # Type:int
    # opera code:0C
    # e.g.:tx = 0023(023), rx = 0371(371)
    global cat_serial
    cat_serial.write(bytes.fromhex(str(tx) + str(rx) + "0C"))


def read_freq():
    # operaq code:P1
    global cat_serial, sat_data_rx, sat_data_tx, real_data  # , rx_freq, tx_freq, rx_mode, tx_mode
    cat_serial.write(bytes.fromhex("00 00 00 00 03"))
    print("1")
    data_byte = cat_serial.read(5)
    data = data_byte.hex()
    print(data)
    if data == "":
        cat_serial.write(bytes.fromhex("00 00 00 00 03"))
        real_data_byte = cat_serial.read(5)
        real_data = real_data_byte.hex()
        sat = False
    else:
        cat_serial.write(bytes.fromhex("00 00 00 00 13"))
        sat_data_rx_byte = cat_serial.read(5)
        sat_data_rx = sat_data_rx_byte.hex()
        cat_serial.write(bytes.fromhex("00 00 00 00 23"))
        sat_data_tx_byte = cat_serial.read(5)
        sat_data_tx = sat_data_tx_byte.hex()
        sat = True
    if sat:
        rx_freq = sat_data_rx[0:6]
        tx_freq = sat_data_tx[0:6]
        ord_rx_mode = sat_data_rx[7:9]
        ord_tx_mode = sat_data_tx[7:9]
        rx_mode = MODE_MAP.get(ord_rx_mode, "unknown")
        tx_mode = MODE_MAP.get(ord_tx_mode, "unknown")
    elif not sat:
        rx_freq = real_data[0:6]
        tx_freq = real_data[0:6]
        ord_rx_mode = real_data[7:9]
        ord_tx_mode = real_data[7:9]
        rx_mode = MODE_MAP.get(ord_rx_mode, "unknown")
        tx_mode = MODE_MAP.get(ord_tx_mode, "unknown")
    return rx_freq, tx_freq, rx_mode, tx_mode, sat


def read_rx_status():
    global cat_serial, rx_status, spe_format
    cat_serial.write(bytes.fromhex("00 00 00 00 E7"))
    data_byte = cat_serial.read(1)
    data = data_byte.hex()
    data_10 = int(data, 16)
    data_bin = '{:08b}'.format(data_10)
    if spe_format:
        if data_bin[0] == "1":
            ptt_status = True
        elif data_bin[0] == "0":
            ptt_status = False
        dummy_data = data_bin[1:3]
        po_alc_data = data_bin[2:7]
        return ptt_status, po_alc_data, dummy_data
    if spe_format is None:
        if data_bin[0] == "1":
            sql_status = True
        elif data_bin[0] == "0":
            sql_status = False
        if data_bin[1] == "1":
            tone_status = False  # Un-Matched
        elif data_bin[1] == "0":
            tone_status = True  # Matched
        if data_bin[2] == "0":
            disc_status = True  # Centered
        elif data_bin[2] == "1":
            disc_status = False  # Un-Centered
        dummy_data = data_bin[3]
        s_metre = data_bin[4:7]
        return sql_status, tone_status, disc_status, dummy_data, s_metre


def read_tx_status():
    global cat_serial, rx_status, spe_format
    cat_serial.write(bytes.fromhex("00 00 00 00 F7"))
    data_byte = cat_serial.read(1)
    data = data_byte.hex()
    data_10 = int(data, 16)
    data_bin = '{:08b}'.format(data_10)
    if spe_format:
        if data_bin[0] == "1":
            sql_status = True
        elif data_bin[0] == "0":
            sql_status = False
        if data_bin[1] == "1":
            tone_status = False  # Un-Matched
        elif data_bin[1] == "0":
            tone_status = True  # Matched
        if data_bin[2] == "0":
            disc_status = True  # Centered
        elif data_bin[2] == "1":
            disc_status = False  # Un-Centered
        s_meter_data = data_bin[3:7]
        return sql_status, tone_status, disc_status, s_meter_data
    if spe_format is None:
        if data_bin[0] == "1":
            ptt_status = True
        elif data_bin[0] == "0":
            ptt_status = False
        if data_bin[1] == "1":
            hi_swr = True  # High
        elif data_bin[1] == "0":
            hi_swr = False  # Low
        if data_bin[2] == "1":
            split_status = False  # Off
        elif data_bin[2] == "0":
            po_alc = True  # On
        dummy_data = data_bin[3]
        po_alc_data = data_bin[4:7]
        return ptt_status, hi_swr, split_status, dummy_data, po_alc_data