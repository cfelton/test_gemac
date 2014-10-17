
filelist = [

    '../simple_gemac/miim/eth_miim.v',
    '../simple_gemac/miim/eth_clockgen.v',
    '../simple_gemac/miim/eth_outputcontrol.v',
    '../simple_gemac/miim/eth_shiftreg.v',

    # myhdl fifo replacements
    '../alt_fifo/m_fifo_2clock_cascade.v',
    '../alt_fifo/m_fifo_short_w36.v',
    '../alt_fifo/m_fifo_short_w11.v',
    '../alt_fifo/m_delay_line_w10.v',

    '../simple_gemac/ll8_shortfifo.v',
    '../simple_gemac/ll8_to_fifo36.v',
    '../simple_gemac/fifo36_to_ll8.v',
    '../simple_gemac/ll8_to_txmac.v',
    '../simple_gemac/rxmac_to_ll8.v',
    '../simple_gemac/oneshot_2clk.v',
    '../simple_gemac/reset_sync.v',
    '../simple_gemac/crc.v',
    '../simple_gemac/address_filter.v',
    '../simple_gemac/flow_ctrl_rx.v',
    '../simple_gemac/flow_ctrl_tx.v',
    '../simple_gemac/simple_gemac_rx.v',
    '../simple_gemac/simple_gemac_tx.v',
    '../simple_gemac/simple_gemac_wb.v',
    '../simple_gemac/simple_gemac.v',
    '../simple_gemac/simple_gemac_wrapper.v',
    
    ]
