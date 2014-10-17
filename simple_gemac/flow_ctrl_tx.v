`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    11:32:46 02/18/2011 
// Design Name: 
// Module Name:    flow_control_tx 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module flow_ctrl_tx 
(input        rst,
   input        tx_clk,
   //host processor
   input        tx_pause_en,
   // From MAC_rx_ctrl
   input [15:0] pause_quanta,
   input        pause_quanta_val,
   // MAC_tx_ctrl
   output       pause_apply,
   input        paused);
     
   // ******************************************************************************        
   // Inhibit our TX from transmitting because they sent us a PAUSE frame
   // ******************************************************************************

   // Pauses are in units of 512 bit times, or 64 bytes/clock cycles, and can be
   //   as big as 16 bits, so 22 bits are needed for the counter
   
   reg [15+6:0] pause_quanta_counter;
   reg 		pqval_d1, pqval_d2;		

   always @(posedge tx_clk) pqval_d1 <= pause_quanta_val;
   always @(posedge tx_clk) pqval_d2 <= pqval_d1;

   always @ (posedge tx_clk or posedge rst)
     if (rst)
       pause_quanta_counter <= 0;
     else if (pqval_d1 & ~pqval_d2)
       pause_quanta_counter <= {pause_quanta, 6'b0}; 
     else if((pause_quanta_counter!=0) & paused)
       pause_quanta_counter <= pause_quanta_counter - 1'b1;

   assign	pause_apply = tx_pause_en & (pause_quanta_counter != 0);
   

endmodule
