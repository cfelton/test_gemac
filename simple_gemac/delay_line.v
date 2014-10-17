`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    11:29:42 02/18/2011 
// Design Name: 
// Module Name:    delay_line 
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
module delay_line
  #(parameter WIDTH=32)
   (input clk,
    input [3:0] delay,
    input [WIDTH-1:0] din,
    output [WIDTH-1:0] dout);
    
   genvar 	       i;
   generate
      for (i=0;i<WIDTH;i=i+1)
	begin : gen_delay
	   SRL16E
	     srl16e(.Q(dout[i]),
		    .A0(delay[0]),.A1(delay[1]),.A2(delay[2]),.A3(delay[3]),
		    .CE(1'b1),.CLK(clk),.D(din[i]));
	end
   endgenerate

endmodule
