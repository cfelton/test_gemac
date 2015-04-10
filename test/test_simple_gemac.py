
from __future__ import division
from __future__ import print_function

import sys
import os
import argparse
from argparse import Namespace
from array import array

from myhdl import *

from mn.system import Global
from mn.system import Wishbone

from support import prep_cosim
from support import GMII
from support import StreamIntf


#=====================================================================
def test_simple_gemac(args):
    

    # clocks
    clk125 = Signal(bool(0))
    sys_clk = Signal(bool(0))
    clock = sys_clk
    reset = ResetSignal(0, active=1, async=True)
    glbl = Global(clock, reset)

    # intefaces
    gmii = GMII()
    stif = StreamIntf(eth_clk=clk125, sys_clk=sys_clk)
    wb = Wishbone(glbl, data_width=32, address_width=8, name='test')

    tbdut = prep_cosim(args, clk125, reset, gmii, sys_clk, stif, wb)

    force_error = Signal(bool(0))
    force_dat_err = Signal(intbv(0)[4:])

    # receive packet interface monitor
    tbmon = stif.m_rx_packets(sys_clk, reset)
    txmon = gmii.m_tx_monitor()
    rxmon = gmii.m_rx_monitor()
    
    def _test():
        NS = 1 #1000

        # note the time scale is 1ns/1ps (1ps)
        @always(delay(4*NS))
        def tbclk1():
            clk125.next = not clk125

        @always(delay(10*NS))
        def tbclk2():
            sys_clk.next = not sys_clk

        @always_comb
        def tb_loopback():
            gmii.rx_dv.next = gmii.tx_en
            gmii.rx_er.next = gmii.tx_er | force_error
            gmii.rxd.next = gmii.txd ^ force_dat_err
            gmii.rx_clk.next = gmii.tx_clk

        def _pause_ticks(N):
            for _ in range(N):
                yield clock.posedge

        def bytes_to_32(lst, idx):
            return concat(intbv(lst[idx+0])[8:],
                          intbv(lst[idx+1])[8:],
                          intbv(lst[idx+2])[8:],
                          intbv(lst[idx+3])[8:])

        pkt_test = Signal(0)
        @instance
        def tbstim():
            yield delay(13*NS)
            reset.next = reset.active
            yield delay(33*NS)
            reset.next = not reset.active
            yield clock.posedge

            try:
                print("  ~~~ setup ~~~")
                # addr 0: misc settings:
                #  {pause_reqeuest_en, pass_ucast, pass_mcast, pass_bcast,
                #   pass_pause, pass_all, pause_respect_en} = misc_settings
                yield wb.write(0x00, int('111101', 2))
                yield wb.write(0x04, 0xA0B0)      # ucast_addr_h
                yield wb.write(0x08, 0xC0D0A1B1)  # ucast_addr_l
                yield wb.write(0x0C, 0x0000)      # mcast_addr_h
                yield wb.write(0x10, 0x00000000)  # mcast_addr_l

                print("setting mii bits")
                wb.write(20, 0x08)          # set mdio divider to 8 and nopre to 0

                print("wait")
                yield _pause_ticks(1000)
                #for _ in range(1000):
                #    yield clock.posedge

                print("  ~~~ first packet  ~~~")
                # this packet will be recieved
                pkt_test.next = 1
                gmii.clear()
                # @todo: need to debug why the a len less than 4 fails
                nwords = 1  # number of words in the packet
                yield stif.t_tx_packet_sp(0xA0B0C0D0, nwords) # received
                #yield stif.t_tx_packet_sp(0xABBACDDC, nwords)  # dropped
                # @todo: wait till ?? words recieved or timeout
                yield _pause_ticks(2000)
                #gmii.dump_monitors()
                # length of epkt, 8 preamble, 4 crc
                assert len(gmii.txl) >= 10+8+2, "Incorrect number of bytes transmitted"  
                assert bytes_to_32(gmii.txl, 8) == 0xA0B0C0D0, "Invalid data transmitted"
                # @todo: include generic packet checking, preamble, crc, etc
                # @todo: check the received words in stif.pkt_buffer
                assert len(stif.pkt_buffer) >= nwords, \
                    "Invalid number of words received %d" % (len(stif.pkt_buffer))
                assert stif.pkt_buffer[0][32:] == 0xA0B0C0D0, \
                    "Invalid received data %08X" % (stif.pkt_buffer[0][32:])
                stif.clear_rx_packets()

                print("  ~~~ second packet ~~~")
                # this packet is dropped by the filters (verify)
                pkt_test.next = 2
                gmii.clear()
                yield stif.t_tx_packet_sp(0xAABBCCDD, 100)
                yield _pause_ticks(100)
                # the gmii monitor will capture all bytes (txd), verify
                # a certain number of bytes recieved
                assert len(gmii.txl) > 100+8, "Incorrect number of bytes transmitted"
                assert bytes_to_32(gmii.txl, 8) == 0xAABBCCDD, "Invalid data transmitted"

                yield _pause_ticks(2000)
                print("  ~~~ third (normal) packet ~~~")
                pkt_test.next = 3
                gmii.clear()
                yield _pause_ticks(10)
                nbytes,nwait = 60,0
                yield stif.t_tx_packet_from_file_sp(nbytes, nwait=nwait)
                yield _pause_ticks(2000*nwait + 2000)

                # @todo: the number of bytes ethernet preamble+header
                # the ethernet preamble has 8 bytes, the gmii monitors
                # should contain and extra 8 bytes
                l1,l2,l3 = len(stif.pkt_mem), len(gmii.txl), len(gmii.rxl)
                print("  %d, %d, %d" % (l1,l2,l3))

                assert len(gmii.txl) > (nbytes+8), "packet not send/recieved"
                for ii in range(8):
                    print("  xx  %02X  %02X " % (gmii.txl[ii], gmii.rxl[ii]))

                nerr = 0
                for ii in range(min((l1,l2,l3,))):
                    if (stif.pkt_mem[ii] != gmii.txl[ii+8] or 
                        stif.pkt_mem[ii] != gmii.rxl[ii+8]):
                        ec = '*'
                        nerr += 1
                    else:
                        ec = ' '
                    print("  %02X  %02X  %02X %s" % (stif.pkt_mem[ii],
                                                     gmii.txl[ii+8],
                                                     gmii.rxl[ii+8],
                                                     ec))

                print("%d byte mismatches for packet sent" % (nerr))

                # some extra ticks at the end
                print("end wait")
                yield _pause_ticks(1111)
                

            except AssertionError, err:
                print("@E: assertion error occurred")
                print("    %s" % (str(err)))
                yield delay(111*NS)
                raise err
            except Exception, err:
                print("@E: assertion error occurred")
                print("    %s" % (str(err)))
                yield delay(111*NS)
                raise err

            raise StopSimulation

        return tbclk1, tbclk2, tbstim, tb_loopback, tbmon, txmon, rxmon

    traceSignals.timescale = '1ps'
    traceSignals.name = 'vcd/_test'
    fn = traceSignals.name + '.vcd'
    if os.path.isfile(fn):
        os.remove(fn)

    Simulation((traceSignals(_test), tbdut,)).run()


#=====================================================================
if __name__ == '__main__':
    args = Namespace()
    test_simple_gemac(args)