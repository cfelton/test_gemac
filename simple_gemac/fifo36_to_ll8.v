`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    11:47:46 02/18/2011 
// Design Name: 
// Module Name:    fifo36_to_ll8 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Convert a 36-bit word, f36_data to four 8-bit outputs
// Special inputs are:
// f36_data[35:34] = f36_occ - number of bytes (2'b00 = 4 bytes)
// f36_data[33]    = f36_sof - signal that this is the first byte of the data stream
// f36_data[32]    = f36_eof - signal that this group of four bytes contains the end of
//										 the data stream (ll_eof_n will be signalled once
//										 f36_occ bytes have been pushed through)
//
// Pushes a byte every clk if src (f36_src_rdy_i) and dst (ll_dst_rdy) are ready.
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module fifo36_to_ll8
  (input clk, input reset, input clear,
   input [35:0] f36_data,
   input f36_src_rdy_i,
   output f36_dst_rdy_o,

   output reg [7:0] ll_data,
   output ll_sof_n,
   output ll_eof_n,
   output ll_src_rdy_n,
   input ll_dst_rdy_n,

   output [2:0] debug);

   wire  ll_sof, ll_eof, ll_src_rdy;
   assign ll_sof_n = ~ll_sof;
   assign ll_eof_n = ~ll_eof;
   assign ll_src_rdy_n = ~ll_src_rdy;
   wire ll_dst_rdy = ~ll_dst_rdy_n;

   wire   f36_sof = f36_data[32];
   wire   f36_eof = f36_data[33];
   wire   f36_occ = f36_data[35:34];
   wire advance, end_early;
   reg [1:0] state;

   always @(posedge clk)
     if(reset)
       state 	  <= 0;
     else
       if(advance)
			 if(ll_eof)
				state  <= 0;
			 else
				state  <= state + 1'b1;

   always @*
     case(state)
       0 : ll_data = f36_data[31:24];
       1 : ll_data = f36_data[23:16];
       2 : ll_data = f36_data[15:8];
       3 : ll_data = f36_data[7:0];
       default : ll_data = f36_data[31:24];
       endcase // case (state)
   
   assign ll_sof 	 = (state==0) & f36_sof;
   assign ll_eof 	 = f36_eof & (((state==0)&(f36_occ==1)) |
			       ((state==1)&(f36_occ==2)) |
			       ((state==2)&(f36_occ==3)) |
			       (state==3));
   
   assign ll_src_rdy 	 = f36_src_rdy_i;

   assign advance 	 = ll_src_rdy & ll_dst_rdy;
   assign f36_dst_rdy_o  = advance & ((state==3)|ll_eof);
   assign debug 	 = {advance, state};
   
endmodule // ll8_to_fifo36
