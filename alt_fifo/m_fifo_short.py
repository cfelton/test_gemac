
from argparse import Namespace

from myhdl import *

from mn.system import FIFOBus
from mn.cores.fifo import m_fifo_async
from mn.cores.fifo import m_fifo_fast


def m_fifo_short(clock, reset, clear, 
                 datain, src_rdy_i, dst_rdy_o,
                 dataout, src_rdy_o, dst_rdy_i):

    wr = Signal(bool(0))
    rd = Signal(bool(0))

    args = Namespace(width=36, size=16, name='fifo_2clock_cascade')
    fbus = FIFOBus(args=args)
    # need to update the fbus refernces to reference the Signals in
    # the moudule port list (function arguments).
    fbus.wr = wr
    fbus.wdata = datain
    fbus.rd = rd
    fbus.rdata = dataout
    fbus.clear = clear

    @always_comb
    def rtl_assign1():
        wr.next = src_rdy_i & dst_rdy_o
        rd.next = dst_rdy_i & src_rdy_o

    @always_comb
    def rtl_assign2():
        dst_rdy_o.next = not fbus.full
        src_rdy_o.next = not fbus.empty

    gfifo = m_fifo_fast(clock, reset, fbus)

    return rtl_assign1, rtl_assign2, gfifo
    
