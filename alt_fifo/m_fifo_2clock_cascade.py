
from argparse import Namespace

from myhdl import *

from mn.system import FIFOBus
from mn.cores.fifo import m_fifo_async
from mn.cores.fifo import m_fifo_fast


def m_fifo_2clock_cascade(
    wclk,       # in:  write side clock
    datain,     # in:  write data
    src_rdy_i,  # in:  
    dst_rdy_o,  # out: 
    space,      # out: how many can be written
    
    rclk,       # in:  read side clock
    dataout,    # out: read data
    src_rdy_o,  # out: 
    dst_rdy_i,  # in:  
    occupied,   # out: number in the fifo

    reset,      # in:  system reset
):


    wr = Signal(bool(0))    # wr1
    #wr2 = Signal(bool(0))  # rd1
    wr3 = Signal(bool(0))
    rd1 = Signal(bool(0))
    rd2 = Signal(bool(0))
    rd = Signal(bool(0))    # rd3
    ed1 = Signal(bool(1))

    args = Namespace(width=36, size=128, name='fifo_2clock_cascade')
    fbus2 = FIFOBus(args=args)
    args.size = 16
    fbus1 = FIFOBus(args=args)
    fbus3 = FIFOBus(args=args)

    # need to update the fbus refernces to reference the Signals in
    # the moudule port list (function arguments).
    fbus1.wr = wr
    fbus1.wdata = datain
    fbus1.rd = rd1

    fbus2.wr = rd1
    fbus2.wdata = fbus1.rdata
    fbus2.rd = rd2

    fbus3.wr = wr3
    fbus3.wdata = fbus2.rdata
    fbus3.rd = rd
    fbus3.rdata = dataout

    @always_comb
    def rtl_assign1():
        wr.next = src_rdy_i and dst_rdy_o
        rd.next = dst_rdy_i and src_rdy_o
        rd1.next = not fbus1.empty and not fbus2.full
        rd2.next = not ed1 and not fbus3.full
        wr3.next = fbus2.rvld

    @always_comb
    def rtl_assign2():
        dst_rdy_o.next = not fbus1.full
        src_rdy_o.next = not fbus3.empty

    # @todo: fix the m_fifo_async bug!!!
    # hackery, need to fix the simultaneous write and read issue
    # with the async FIFO!
    @always_seq(rclk.posedge, reset=reset)
    def rtl_ed1():
        if ed1:
            ed1.next = fbus2.empty
        else:
            ed1.next = True


    # the original was a chain:
    #    m_fifo_fast  (16)
    #    m_fifo_async (64)tx, (512)rx
    #    m_fifo_fast  (16)
    # the two small FIFOs were used to simplify the interface to
    # the async FIFO, the async FIFOs have some odd behaviors, the
    # up front fast fifo wasn't really needed.
    # the small fast FIFOs have a simpler (reactive) interface
    # it works more like a register with enable(s).

    gfifo1 = m_fifo_fast(wclk, reset, fbus1)
    gfifo2 = m_fifo_async(reset, wclk, rclk, fbus2)
    gfifo3 = m_fifo_fast(rclk, reset, fbus3)
                

    return rtl_assign1, rtl_assign2, rtl_ed1, gfifo1, gfifo2, gfifo3

