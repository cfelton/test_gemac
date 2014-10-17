`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    11:46:55 02/18/2011 
// Design Name: 
// Module Name:    ll8_shortfifo 
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
module ll8_shortfifo
  (input clk, input reset, input clear,
   input [7:0] datain, input sof_i, input eof_i, input error_i, input src_rdy_i, output dst_rdy_o,
   output [7:0] dataout, output sof_o, output eof_o, output error_o, output src_rdy_o, input dst_rdy_i);

   //fifo_short #(.WIDTH(11)) fifo_short
   //  (.clk(clk), .reset(reset), .clear(clear),
   //   .datain({error_i,eof_i,sof_i,datain}), .src_rdy_i(src_rdy_i), .dst_rdy_o(dst_rdy_o),
   //   .dataout({error_o,eof_o,sof_o,dataout}), .src_rdy_o(src_rdy_o), .dst_rdy_i(dst_rdy_i));

   m_fifo_short_w11 u_fifo_short
     (.clock(clk), .reset(reset), .clear(clear),
      .datain({error_i,eof_i,sof_i,datain}), .src_rdy_i(src_rdy_i), .dst_rdy_o(dst_rdy_o),
      .dataout({error_o,eof_o,sof_o,dataout}), .src_rdy_o(src_rdy_o), .dst_rdy_i(dst_rdy_i));



endmodule
