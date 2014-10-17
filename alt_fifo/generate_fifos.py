

from argparse import Namespace

from myhdl import *
import myhdl_tools as tlz

from m_fifo_2clock_cascade import m_fifo_2clock_cascade
from m_fifo_short import m_fifo_short
from m_delay_line import m_delay_line

def convert(args=None):
    wclk = Signal(bool(0))
    datain = Signal(intbv(0)[36:])
    src_rdy_i = Signal(bool(0))
    dst_rdy_o = Signal(bool(0))
    space = Signal(intbv(0)[16:])
    
    rclk = Signal(bool(0))
    dataout = Signal(intbv(0)[36:])
    src_rdy_o = Signal(bool(0))
    dst_rdy_i = Signal(bool(0))
    occupied = Signal(intbv(0)[16:])

    reset = ResetSignal(0, active=1, async=True)


    toVerilog(m_fifo_2clock_cascade, 
              wclk, datain, src_rdy_i, dst_rdy_o, space,
              rclk, dataout, src_rdy_o, dst_rdy_i, occupied,
              reset)

    clock = Signal(bool(0))
    clear = Signal(bool(0))
    datain = Signal(intbv(0)[36:])
    dataout = Signal(intbv(0)[36:])
    toVerilog.name = 'm_fifo_short_w36'
    toVerilog(m_fifo_short,
              clock, reset, clear,
              datain, src_rdy_i, dst_rdy_o,
              dataout, src_rdy_o, dst_rdy_i)

    datain = Signal(intbv(0)[11:])
    dataout = Signal(intbv(0)[11:])
    toVerilog.name = 'm_fifo_short_w11'
    toVerilog(m_fifo_short,
              clock, reset, clear,
              datain, src_rdy_i, dst_rdy_o,
              dataout, src_rdy_o, dst_rdy_i)


    delay = Signal(intbv(0, min=0, max=16))
    di = Signal(intbv(0)[10:])
    do = Signal(intbv(0)[10:])
    toVerilog.name = 'm_delay_line_w10'
    toVerilog(m_delay_line, clock, delay, di, do)

if __name__ == '__main__':
    convert()