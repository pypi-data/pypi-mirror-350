from commands import set_model, set_lock, set_ptt, set_freq, set_mode
from serials import init_connection, set_port, set_baudrate


#__all__ = ['commands', 'serials']
def init_connection():
    return serials.init_connection()

def set_port(port):
    return serials.set_port(port)

def set_baudrate(baudrate):
    return serials.set_baudrate(baudrate)

def set_model(model):
    return commands.set_model(model)

def set_lock(lock_state):
    return commands.set_lock(lock_state)

def set_ptt(ptt_state):
    return commands.set_ptt(ptt_state)

def set_freq(freq):
    return commands.set_freq(freq)

def set_mode(mode):
    return commands.set_mode(mode)
