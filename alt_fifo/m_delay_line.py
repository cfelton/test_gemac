
from myhdl import *

def m_delay_line(clk, delay, din, dout):

    dline = [Signal(intbv(0, min=din.min, max=din.max)) for _ in range(16)]

    @always(clk.posedge)
    def rtl():
        dline[0].next = din
        for ii in range(1,16):
            dline[ii].next = dline[ii-1]

    @always_comb
    def rtlo():
        dout.next = dline[delay]

    return rtl, rtlo
