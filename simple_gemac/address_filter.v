`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    11:31:03 02/18/2011 
// Design Name: 
// Module Name:    address_filter 
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
module address_filter
  (input clk,
   input reset,
   input go,
   input [7:0] data,
   input [47:0] address,
   output match,
   output done);

   reg [2:0] af_state;

   always @(posedge clk)
     if(reset)
       af_state     <= 0;
     else
       if(go)
	 af_state <= (data == address[47:40]) ? 3'd1 : 3'd7;
       else
	 case(af_state)
	   1 : af_state <= (data == address[39:32]) ? 3'd2 : 3'd7;
	   2 : af_state <= (data == address[31:24]) ? 3'd3 : 3'd7;
	   3 : af_state <= (data == address[23:16]) ? 3'd4 : 3'd7;
	   4 : af_state <= (data == address[15:8])  ? 3'd5 : 3'd7;
	   5 : af_state <= (data == address[7:0]) ? 3'd6 : 3'd7;
	   6, 7 : af_state <= 0;
	 endcase // case (af_state)

   assign match  = (af_state==6);
   assign done 	 = (af_state==6)|(af_state==7);
   

endmodule
