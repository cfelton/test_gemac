
from __future__ import division
from __future__ import print_function

from myhdl import *


class StreamIntf(object):
    def __init__(self, eth_clk, sys_clk, W=36):
        # out of 
        self.eth_clk = eth_clk
        self.sys_clk = sys_clk

        self.rx_data = Signal(intbv(0)[W:])
        self.rx_src_rdy = Signal(bool(0))
        self.rx_dst_rdy = Signal(bool(0))
        
        # into
        self.tx_data = Signal(intbv(0)[W:])
        self.tx_src_rdy = Signal(bool(0))
        self.tx_dst_rdy = Signal(bool(0))

    def clear_rx_packets(self):
        self.pkt_buffer = []    

    def m_rx_packets(self, clock, reset):
        # recieve packets into a buffer
        self.pkt_buffer = []        
        word_cnt = Signal(0)

        @always_seq(clock.posedge, reset=reset)
        def mon_rx_pkts():
            # always ready to receive packet words
            self.rx_dst_rdy.next = True

            # if a new packet word arrives print and save (for now)
            if self.rx_src_rdy:
                print("::%08d:: new pkt word %02d,%01d,%01d:%08X, words %4d" % (
                    now(), self.rx_data[36:34], self.rx_data[33], self.rx_data[32],
                    self.rx_data[32:0], word_cnt)) 

                # need a copy of the value, leave an intbv so it can
                # be bit sliced later
                x = intbv(self.rx_data[:])[len(self.rx_data):]
                self.pkt_buffer.append(x)
                word_cnt.next = word_cnt + 1

        return mon_rx_pkts

    def t_tx_packet_sp(self, data_start, data_len):
        """ send a simple packet
        This is a replication of the original testbench send
        packet task.  This should be made genericer in the future!
        
        data_len is the number of 32 bit words to send, this function
        is limited to sending multiple of 4 bytes.

        36 bit bus
          35:34 : empty bytes (if 4 bytes used == 00)
          33    : end of frame (end of packet), EOF
          32    : start of frame (start of packet), SOF
          31:0  : 4 bytes of data
          
        Currently use the _sp to indicate this is a replication of 
        the original tasks.
        """
        # transmit a packet, the packet should be in a Python byte
        # array pkt = array.array('B', ...)
        #txd = int('00' + '0' + '1' + bin(data_start, 32), 2)
        if data_len < 8:
            print("@W: minimum payload size 8 words, setting data_len to 8")
            data_len = 8

        txd = concat('00', '0', '1', intbv(data_start)[32:])
        self.tx_data.next = txd
        self.tx_src_rdy.next = True
        count = 1
        while count < data_len:
            while not self.tx_dst_rdy:
                yield self.sys_clk.posedge
            yield self.sys_clk.posedge
            #print("@D: TX[%04d]: 0x%09X" % (count, self.tx_data))
            txd[32:0] = (txd[32:0] + 0x01010101) & 0xFFFFFFFF
            count = count + 1
            txd[32] = 0
            self.tx_data.next = txd

        txd[33] = 1
        self.tx_data.next = txd
        while not self.tx_dst_rdy:
            yield self.sys_clk.posedge
        yield self.sys_clk.posedge
        #print("@D: TX[%04d]: 0x%09X" % (count, self.tx_data))
        self.tx_src_rdy.next = False

    def t_tx_packet_from_file_sp(self, data_len, nwait=0, fn='test_packet.mem'):
        """ send a packet from a file
        This is a replication of the original testbench task to send
        a packet from a file.

        Currently use the _sp to indicate this is a replication of 
        the original tasks.
        """
        
        fp = open(fn, 'r')
        N = data_len + (data_len % 4)
        pkt_mem = [intbv(0)[8:] for _ in range(N)]
        for ii in range(data_len):
            byte = fp.readline()
            pkt_mem[ii][:] = int(byte, 16)
            
        self.pkt_mem = pkt_mem

        # wait for the destination (gemac TX FIFO) to be ready
        while not self.tx_dst_rdy:
            yield self.sys_clk.posedge

        txd = concat(pkt_mem[0], pkt_mem[1], pkt_mem[2], pkt_mem[3])
        self.tx_data.next[32:0] = txd
        self.tx_data.next[36:34] = intbv('00')   # 4 bytes are valid
        self.tx_data.next[33] = 0                # EOF
        self.tx_data.next[32] = 1                # SOF
        self.tx_src_rdy.next = True
        yield self.sys_clk.posedge
        #print("@D: TX[%04d]: 0x%09X" % (0, self.tx_data))
        self.tx_src_rdy.next = False

        for ii in range(4, data_len-4, 4):
            while not self.tx_dst_rdy:
                yield self.sys_clk.posedge
            txd = concat(pkt_mem[ii], pkt_mem[ii+1], pkt_mem[ii+2], pkt_mem[ii+3])
            self.tx_data.next[32:0] = txd
            self.tx_data.next[36:32] = 0
            self.tx_src_rdy.next = True
            yield self.sys_clk.posedge
            #print("@D: TX[%04d]: 0x%09X" % (ii, self.tx_data))
            self.tx_src_rdy.next = False

            for jj in range(nwait):
                yield self.sys_clk

        while not self.tx_dst_rdy:
            yield self.sys_clk.posedge

        # ok, should be at the end of the packet now, if the packet len
        # is not a multiple of four need to indicate the number of empty
        # bytes, this appears to be data_len-ii+1
        ii = ii + 4
        Ne = (data_len-ii) % 4        
        #print("@D: last index %d, data_len %d, N %d, Ne %d" % (ii, data_len, N, Ne))
        txd = concat(pkt_mem[ii], pkt_mem[ii+1], pkt_mem[ii+2], pkt_mem[ii+3])
        self.tx_data.next[32:0] = txd
        self.tx_data.next[36:34] = Ne
        self.tx_data.next[33] = 1    # EOF
        self.tx_data.next[32] = 0    # SOF
        self.tx_src_rdy.next = True
        yield self.sys_clk.posedge
        #print("@D: TX[%04d]: 0x%09X" % (ii, self.tx_data))
        self.tx_src_rdy.next = False
        
