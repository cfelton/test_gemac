`timescale 1ps / 1ps

module tb_simple_gemac;

   /*input */  reg  clk125;             
   /*input */  reg  reset;
   // GMII
   /*output*/  wire GMII_GTX_CLK  ;
   /*output*/  wire GMII_TX_EN 	  ;
   /*output*/  wire GMII_TX_ER 	  ;
   /*output*/  wire [7:0] GMII_TXD;
   /*input */  reg  GMII_RX_CLK	  ;
   /*input */  reg  GMII_RX_DV 	  ;
   /*input */  reg  GMII_RX_ER 	  ;
   /*input */  reg  [7:0] GMII_RXD;
    
    // Client FIFO Interfaces
    /*input */ reg  sys_clk           ;
    /*output*/ wire [35:0] rx_f36_data;
    /*output*/ wire rx_f36_src_rdy    ;
    /*input */ reg  rx_f36_dst_rdy    ;
    /*input */ reg  [35:0] tx_f36_data;
    /*input */ reg  tx_f36_src_rdy    ;
    /*output*/ wire tx_f36_dst_rdy    ;   
    
    // Wishbone Interface
    /*input */ reg  wb_clk         ;
    /*input */ reg  wb_rst 	   ;
    /*input */ reg  wb_stb 	   ;
    /*input */ reg  wb_cyc 	   ;
    /*output*/ wire wb_ack 	   ;
    /*input */ reg  wb_we	   ;
    /*input */ reg  [7:0] wb_adr   ;
    /*input */ reg  [31:0] wb_dat_i;
    /*output*/ wire [31:0] wb_dat_o;
    
   // MIIM
   /*inout */  wire mdio;   
   /*output*/  wire mdc;   
   /*output*/  wire [79:0] debug;       
   
   initial begin
      $dumpfile("vcd/_tb_simple_gemac.vcd");
      $dumpvars(0, tb_simple_gemac);
   end

   initial begin
      $from_myhdl(
	 clk125, reset,
	 GMII_RX_CLK, GMII_RX_DV, GMII_RX_ER, GMII_RXD,
	 sys_clk,
	 rx_f36_dst_rdy, tx_f36_data, tx_f36_src_rdy,
	 wb_clk, wb_rst, wb_stb, wb_cyc, wb_we, wb_adr,
	 wb_dat_i
	 );
      
      $to_myhdl(
	 GMII_GTX_CLK, GMII_TX_EN, GMII_TX_ER, GMII_TXD,
	 rx_f36_data, rx_f36_src_rdy, tx_f36_dst_rdy,
	 wb_ack, wb_dat_o
	 );
   end
   
   simple_gemac_wrapper 
     DUT
       (.clk125              (clk125           ),   /*input */
	.reset               (reset            ),   /*input */            
	// ethernet phy interface   		    
	.GMII_GTX_CLK        (GMII_GTX_CLK     ),   /*output*/  
	.GMII_TX_EN          (GMII_TX_EN       ),   /*output*/  
	.GMII_TX_ER          (GMII_TX_ER       ),   /*output*/  
	.GMII_TXD            (GMII_TXD         ),   /*output*/  
	.GMII_RX_CLK         (GMII_RX_CLK      ),   /*input */  
	.GMII_RX_DV          (GMII_RX_DV       ),   /*input */  
	.GMII_RX_ER          (GMII_RX_ER       ),   /*input */  
	.GMII_RXD            (GMII_RXD         ),   /*input */  
	// streaming interfaces          
	.sys_clk             (sys_clk          ),   /*input */
	.rx_f36_data         (rx_f36_data      ),   /*output*/
	.rx_f36_src_rdy      (rx_f36_src_rdy   ),   /*output*/
	.rx_f36_dst_rdy      (rx_f36_dst_rdy   ),   /*input */
	.tx_f36_data         (tx_f36_data      ),   /*input */
	.tx_f36_src_rdy      (tx_f36_src_rdy   ),   /*input */
	.tx_f36_dst_rdy      (tx_f36_dst_rdy   ),   /*output*/
	// wishbone interface              
	.wb_clk              (wb_clk           ),   /*input */ 
	.wb_rst              (wb_rst           ),   /*input */
	.wb_stb              (wb_stb           ),   /*input */
	.wb_cyc              (wb_cyc           ),   /*input */
	.wb_ack              (wb_ack           ),   /*output*/
	.wb_we               (wb_we            ),   /*input */
	.wb_adr              (wb_adr           ),   /*input */
	.wb_dat_i            (wb_dat_i         ),   /*input */
	.wb_dat_o            (wb_dat_o         ),   /*output*/
	//                   
	.mdio                (mdio             ),   /*inout */            
	.mdc                 (mdc              ),   /*output*/             
	.debug               (debug            )    /*output*/
	);
       	
     
endmodule
