import serial
import serial.tools.list_ports

def ports():
    return serial.tools.list_ports.comports()

class CardConnection:

    __serial = serial.Serial()

    def __init__(self, port):
        self.__serial.port = port
        self.__serial.timeout = 3
        self.__serial.baudrate = 115200
        self.__serial.open()
    
    def __del__(self):
        self.__serial.close()

    def reset(self):
        return self.__RE()

    def disable(self):
        self.__CD()

    def enable(self):
        self.__CE()

    def data_delay(self, delay=None):
        if delay:
            self.__WT(0x01, 0x00)
            self.__WT(0x02, delay)
        else:
            return int(self.__DT()[18:20], 16)

    def coincidence_level(self, level=None):
        if level:
            mask = int(self.__DC()[7], 16)
            self.__WC(0x00, (level - 1) * 0x10 + mask)
        else:
            return int(self.__DC()[6], 16) + 1

    def channel_mask(self, mask=None):
        if mask:
            level = int(self.__DC()[6], 16) + 1
            self.__WC(0x00, (level - 1) * 0x10 + mask)
        else:
            return '{:04b}'.format(int(self.__DC()[7], 16))

    def gate_width(self, width=None):
        if width:
            width = '{:04X}'.format(width)
            self.__WC(0x02, int(width[2:4], 16))
            self.__WC(0x03, int(width[0:2], 16))
        else:
            line = self.__DC()
            return int(line[24:26] + line[18:20], 16)

    def threshold(self, channel=None, threshold=None):
        if channel is not None and threshold is not None:
            self.__TL(channel - 1, threshold)
        else:
            return self.__TL()

    def counters(self):
        pass

    def scalars(self):
        return self.__DS()

    def help(self):
        return self.__HE()

    def status(self, n):
        return self.__ST(n)

    def setup(self):
        return self.__V1()

    def poll(self):
        return self.__read()

    def __validate_echo(self, line):
        line_prefix = line[:2]
        echo_prefix = self.__read()[:2]
        if line_prefix != echo_prefix:
            raise SignalError(line_prefix)

    def __write(self, line):
        self.__serial.write(line.encode())
        if line != 'CE\r' and line != 'CD\r':
            self.__validate_echo(line)

    def __read(self, lines=1):
        if lines:
            return self.__serial.readline().decode() + self.__read(lines - 1)
        else:
            return ''

    def __CE(self):
        self.__write('CE\r')

    def __CD(self):
        self.__write('CD\r')

    def __DC(self):
        self.__write('DC\r')
        return self.__read()

    def __DF(self):
        self.__write('DF\r')
        return self.__read()

    def __DG(self):
        self.__write('DG\r')
        return self.__read()

    def __DS(self):
        self.__write('DS\r')
        return self.__read()

    def __DT(self):
        self.__write('DT\r')
        return self.__read()

    def __GP(self):
        pass

    def __HE(self):
        self.__write('HE\r')
        return self.__read(21)

    def __HF(self):
        pass

    def __HS(self):
        self.__write('HS\r')
        return self.__read(28)

    def __HB(self):
        pass

    def __NA(self, n):
        pass

    def __NM(self, n):
        pass

    def __RB(self):
        pass

    def __RE(self):
        self.__write('RE\r')
        return self.__read(9)

    def __SA(self, n=None):
        pass

    def __SB(self, n):
        pass

    def __SN(self, nnnn=None):
        pass

    def __ST(self, n):
        self.__write('ST\r')
        return self.__read()

    def __TH(self):
        pass

    def __TL(self, m=None, nnnn=None):
        if m is not None and nnnn is not None:
            self.__write('TL {:d} {:d}\r'.format(m, nnnn))
        else:
            self.__write('TL\r')
            return self.__read()

    def __V1(self):
        self.__write('V1\r')
        return self.__read(19)

    def __WC(self, mm, nn):
        self.__write('WC {:02X} {:02X}\r'.format(mm, nn))
        return self.__read()

    def __WT(self, mm, nn):
        self.__write('WT {:02X} {:02X}\r'.format(mm, nn))
        return self.__read()

class SignalError(Exception):
    
    def __init__(self, command):
        self.command = command
        self.message = 'Card failed to acknowledge {} signal'.format(self.command)
