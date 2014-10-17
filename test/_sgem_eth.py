
from __future__ import division
from __future__ import print_function

from myhdl import *

MinPktLen = (8 + 6 + 6 + 4 + 2 + 4)

class EthernetByteStream(object):
    """
    Each Ethernet interface (MII, RMII, GMII) needs to create a 
    byte-stream to connect to the Ethernet network emulation.
    """
    def __init__(self, clk, bs, dv, er):
        self.clk = clk
        self.bs = bs
        self.dv = dv
        self.er = er

class EthernetPacket(object):
    """
    """
    def __init__(self):
        # @todo: max ethernet packet is ??? bytes, use array.array('B')
        #        instead (less memory, unless numerous outstanding pkts).
        self.bytes = []   # the raw bytes
        self.crc = None   # packet crc
        self.mac_dst = None
        self.mac_src = None
        self.tag = None
        self.complete = False

    def calc_crc(self):
        assert len(self.bytes) >= MinPktLen
        
    def captured(self):
        """ when a complete packet is captured, generate the fields 
        """
        assert len(self.bytes) >= MinPktLen

        self.complete = True

    def append(self, byte):
        if not self.complete:
            self.bytes.append(byte)

# @todo: create an Ethernet object that takes various interfaces (GMII,
#        RMII, MII) and creates byte streams and has various methods 
#        to decode packets etc.
class Ethernet(object):
    """
    This is a simple ethernet emulation, it works on byte-streams and 
    not single differential lines.  This can connect different Ethernet
    interfaces (MII, RMII, GMII) as long as the generate the byte streams
    (Ethernet standard define on octets (bytes) should always be complete
     bytes).
    """
    def __init__(self, delay=3):
        self.nif = 0        # number of interfaces
        self.delay = delay  # a time-of-flight delay

        # list of all the interfaces (EthernetByteStreams) connected
        self.txif = []
        self.rxif = []

        # currently transmitting interface (only one at a time)
        self.txbs = txbs
        self.txdv = txdv
        self.txer = txer
        self.txck = txck

        # only one transmitter at a time, if the packetizer is enabled
        # all captured packets will be added to the list
        self.pkts = []
        
    def info(self):
        """
        """
        # @todo generate a string with a ton of info about the number
        #   of connections etc.
        pass

    def add(self, intf):
        assert isinstance(intf, (MII, RMII, GMII))
        assert hasattr(intf, tx_eth)
        assert hasattr(intf, rx_eth)
        # @todo: connect the interfaces

        self.txif.append(intf.tx_eth)
        self.rxif.append(intf.rx_eth)
        self.nif += 1
        
    def m_route(self, clock):
        """
        currently all the interfaces are connected, the byte-streams (bs)
        from each interface, including looping back to itself, broadcast
        to all.
        """
        
        # find a transmitting interface
        # currently the method to resolve collisions is winner take
        # all the first tx inteface 
        c_txi = Signal(-1) # current transmiting interface
        @always_comb
        def emu_find_tx():
            for ii,txi in enumerate(self.txif):
                if txi.dv:
                    c_txi.next = ii
        
        # currently transmitting interface
        txbs = Signal(intbv(0)[8:], delay=self.delay)
        txdv = Signal(bool(0),      delay=self.delay)
        txer = Signal(bool(0),      delay=self.delay)
        txck = Signal(bool(0),      delay=self.delay)

        # object refernces so the packet decoder can do its job
        self.txbs = txbs
        self.txdv = txdv
        self.txer = txer
        self.txck = txck

        # map the tranmitting byte-stream to all recievers
        @always_comb
        def emu_map_tx():
            txck.next = self.txif[c_txi].clk
            txbs.next = self.txif[c_txi].bs

        @always_comb
        def emu_route_rx():
            if c_txi >= 0 and c_txi < len(self.rxif):
                for rxi in self.rxif:
                    rxi.bs.next = txbs
                    rxi.dv.next = txdv
                    rxi.er.next = txer
                    rxi.clk.next = txck
                

        return emu_find_tx, emu_map_tx, emu_route_rx

    def packetize_byte_stream(self, clock):
        """ monitor a bytes stream and decode the packets
                
        given a byte-stream (bs), data valid (dv) and errror (er) this
        will monitor and capture packets.  A packet 
        summary of imporant ethernet standard/information:
        """
        assert isinstance(pkt_lst, list)
        assert len(bs) == 8

        states = enum("START",     # wait for a packet
                      "PREAMBLE",  # get the preamble
                      "HEADER",    # get the header
                      "PAYLOAD",   # get the payload
                      "TIMEOUT",   # timeout occurred 
                      "ERROR",     # some kind of error occurred
                      "IDELAY",    # wait for 
        )

        bs = self.txbs

        @instance
        def mon_decode_pkt():
            state = states.START
            nbytes = 0
            idelay = 0
            pkt = None

            while True:
                yield clock.posedge
                      
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                if state == states.START:
                    # wait for a packet to start arriving
                    if dv and bs == 0x55:
                        pkt = EthernetPacket()
                        pkt.append(bs)
                        nbytes += 1
                        state = states.PREAMBLE

                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif state == states.PREAMBLE:
                    # need to get 6 more 0x55 and SOF
                    if dv:
                        if nbytes < 7 and bs == 0x55:
                            pkt.append(bs)
                            nbytes += 1
                        elif nbytes == 8:
                            pkt.append(bs)
                            nbytes += 1
                            state = states.HEADER
                        else:
                            # error, unexpected wait for intergap
                            state = states.ERROR

                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif state == states.HEADER:
                    pass
                        

        return mon_decode_pkt

