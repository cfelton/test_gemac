#
# Copyright (c) 2014 Christopher L. Felton
#
# Permission is hereby granted, free of charge, to any person obtaining a 
# copy of this software and associated documentation files (the "Software"), 
# to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the 
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included 
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
# THE SOFTWARE.
#

from __future__ import division
from __future__ import print_function

import os
from argparse import Namespace

from myhdl import *

from m_fifo_2clock_cascade import m_fifo_2clock_cascade

def test_fifo_2cc(args=None):
    """ verify the synchronous FIFO
    """

    if args is None:
        args = Namespace(width=8, size=16, name='test')
    else:
        # @todo: verify args has the attributes needed for the FIFOBus
        pass 

    reset = ResetSignal(0, active=1, async=True)
    wclk,rclk = Signal(bool(0)), Signal(bool(0))
    
    src_rdy_i = Signal(bool(0))
    dst_rdy_o = Signal(bool(0))
    src_rdy_o = Signal(bool(0))
    dst_rdy_i = Signal(bool(0))

    datain = Signal(intbv(0)[36:])
    dataout = Signal(intbv(0)[36:])

    space = Signal(intbv(0, min=0, max=512))
    occupied = Signal(intbv(0, min=0, max=512))
    

    def _test():
        
        # @todo: use args.fast, args.use_srl_prim
        tbdut = m_fifo_2clock_cascade(wclk, datain, src_rdy_i, dst_rdy_o, space,
                                      rclk, dataout, src_rdy_o, dst_rdy_i, occupied, 
                                      reset)

        # Need to test with different clock rates
        WHD,RHD = 10,10  # 12,4

        @always(delay(WHD))
        def tbclk1():
            wclk.next = not wclk

        @always(delay(RHD))
        def tbclk2():
            rclk.next = not rclk

        
        @instance
        def tbstim():
            datain.next = 0xFE
            reset.next = reset.active
            yield delay(33)
            reset.next = not reset.active
            for ii in range(5):
                yield wclk.posedge

            # test the normal cases
            for num_bytes in range(1, 80):

                # write some bytes
                for ii in range(num_bytes):
                    #print('nbyte %x wdata %x' % (num_bytes, ii))
                    yield wclk.posedge
                    if dst_rdy_o:
                        datain.next = ii
                        src_rdy_i.next = True
                    else:
                        src_rdy_i.next = False
                        break

                yield wclk.posedge
                src_rdy_i.next = False
                datain.next = 0xFE

                # if 16 bytes written make sure FIFO is full
                yield wclk.posedge
                #if num_bytes == args.size:
                #    assert fbus.full, "FIFO should be full!"
                #    assert not fbus.empty, "FIFO should not be empty"
                
                for ii in range(num_bytes):
                    while not src_rdy_o:
                        dst_rdy_i.next = False
                        #yield rclk.posedge
                        yield delay(1)

                    dst_rdy_i.next = True
                    yield rclk.posedge
                    #print("rdata %x ii %x " % (fbus.rdata, ii))
                    assert dataout == ii, "rdata %x ii %x " % (dataout, ii)
                    yield delay(1)

                dst_rdy_i.next = False
                yield rclk.posedge

            # Test overflows        
            # Test underflows        
            # Test write / read same time

            raise StopSimulation

        
        return tbdut, tbclk1, tbclk2, tbstim

    traceSignals.name = 'vcd/test_fifo_fast_%d' % (args.size)
    if os.path.isfile(traceSignals.name+'.vcd'):
        os.remove(traceSignals.name+'.vcd')        
    #g = traceSignals(_test)
    g = _test()
    Simulation(g).run()

if __name__ == '__main__':
    for size in (4,8,16):
        args = Namespace(width=8, size=size, name='test')
        test_fifo_2cc(args=args)
