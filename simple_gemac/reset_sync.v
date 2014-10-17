`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    11:35:39 02/18/2011 
// Design Name: 
// Module Name:    reset_sync 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Synchronises an async reset signal to the clock, asserting it for a minimum
// of 2 clock cycles.
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module reset_sync
  (input clk,
   input reset_in,
   output reg reset_out);

   reg 	      reset_int;

   always @(posedge clk or posedge reset_in)
     if(reset_in)
       {reset_out,reset_int} <= 2'b11;
     else
       {reset_out,reset_int} <= {reset_int,1'b0};
   

endmodule
