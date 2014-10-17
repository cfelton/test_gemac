
from __future__ import division
from __future__ import print_function

from myhdl import *

from _sgem_eth import EthernetByteStream


class GMII(object):
    """
    """

    def __init__(self):
        # outputs (from DUT)
        self.tx_clk = Signal(bool(0))     # 125 MHz clock for GMII
        self.tx_en = Signal(bool(0))      # enable (data is valid)
        self.tx_er = Signal(bool(0))      # error (corrupt the packet)
        self.txd = Signal(intbv(0)[8:])   # data
        
        # inputs (to DUT)
        self.rx_clk = Signal(bool(0))     # recieve clock, 125 MHz
        self.rx_dv = Signal(bool(0))      # data valid
        self.rx_er = Signal(bool(0))      # error on data
        self.rxd = Signal(intbv(0)[8:])   # data

        self.force_error = Signal(bool(0))
        self.force_dat_err = Signal(intbv(0)[8:])

        # get the byte-streams to connect to Ethernet emulation
        self.tx_eth = EthernetByteStream(self.tx_clk, self.txd,
                                         self.tx_en,  self.tx_er)
        self.rx_eth = EthernetByteStream(self.rx_clk, self.rxd,
                                         self.rx_dv,  self.rx_er)
        self.txl = []
        self.rxl = []

    def clear(self):
        self.txl = []
        self.rxl = []

    def m_loopback(self):
        """ loopback the interface
        """
        force_error = self.force_error
        force_dat_err = self.force_dat_err

        @always_comb
        def mlp():
            self.rx_dv.next  = self.tx_en
            self.rx_er.next  = self.tx_er | force_error
            self.rxd.next    = self.txd ^ force_dat_err
            self.rx_clk.next = self.tx_clk

        return mlp

    def m_tx_monitor(self):    
        @always(self.tx_clk.posedge)
        def montx():
            if self.tx_en:
                self.txl.append(int(self.txd))

        return montx

    def m_rx_monitor(self):
        @always(self.rx_clk.posedge)
        def monrx():
            if self.rx_dv:
                self.rxl.append(int(self.rxd))

        return monrx

    def dump_monitors(self, pktb=None):
        """ dumpy the monitor buffers (lists)
        pktb : packet buffer (list)
        """
        ln = min(len(self.txl), len(self.rxl))
        print("  len(txl) %d,  len(rxl) %d  " % (len(self.txl), len(self.rxl)))
        for ii in range(ln):
            print("  [%4d]: %02X  %02X  " % (ii, self.txl[ii], self.rxl[ii]))

    