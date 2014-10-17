
import os

from myhdl import *
from _sgem_filelist import filelist

#=====================================================================
# @todo: move to a separate file
def prep_cosim(
    args,
    clk125=None,
    reset=None,
    gmii=None,
    sys_clk=None,
    stintf=None,
    wb=None,
    #mdio=None,
    #mdc=None            
):
    """
    """
    global filelist
    files = filelist + ['tb_simple_gemac.v']
    print("compiling ...")
    cmd = "iverilog -o simple_gemac %s " % (" ".join(files))
    os.system(cmd)

    if not os.path.exists('vcd'):
        os.makedirs('vcd')

    print("cosimulation setup ...")
    cmd = "vvp -m ./myhdl.vpi simple_gemac"

    gcosim = Cosimulation(cmd,
        clk125=clk125, 
        reset=reset,
        # ethernet phy interface
        GMII_GTX_CLK=gmii.tx_clk, 
        GMII_TX_EN=gmii.tx_en, 
        GMII_TX_ER=gmii.tx_er, 
        GMII_TXD=gmii.txd,
        GMII_RX_CLK=gmii.rx_clk, 
        GMII_RX_DV=gmii.rx_dv, 
        GMII_RX_ER=gmii.rx_er, 
        GMII_RXD=gmii.rxd,
        # internal logic 
        sys_clk=sys_clk,
        rx_f36_data=stintf.rx_data, 
        rx_f36_src_rdy=stintf.rx_src_rdy, 
        rx_f36_dst_rdy=stintf.rx_dst_rdy,
        tx_f36_data=stintf.tx_data, 
        tx_f36_src_rdy=stintf.tx_src_rdy, 
        tx_f36_dst_rdy=stintf.tx_dst_rdy,

        # wishbone interface (device perspective)
        wb_clk=wb.clk_i,
        wb_rst=wb.rst_i,
        wb_stb=wb.stb_i,
        wb_cyc=wb.cyc_i,
        wb_ack=wb.ack_o,
        wb_we=wb.we_i,
        wb_adr=wb.adr_i,
        wb_dat_i=wb.dat_i,
        wb_dat_o=wb.dat_o

        # miim
        #mdio=mdi, mdc=mdc 
    )

    return gcosim

