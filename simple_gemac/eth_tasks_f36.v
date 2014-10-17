//`timescale 1ns / 1ps -- this files is "tick-included"
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    14:12:55 02/18/2011 
// Design Name: 
// Module Name:    eth_tasks_f36 
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


task SendFlowCtrl;
   input [15:0] fc_len;
   begin
      $display("Sending Flow Control, quanta = %d, time = %d", fc_len,$time);
      pause_time <= fc_len;
      @(posedge eth_clk);
      pause_req <= 1;
      @(posedge eth_clk);
      pause_req <= 0;
      $display("Sent Flow Control");
   end
endtask // SendFlowCtrl

task SendPacket_to_fifo36;
   input [31:0] data_start;
   input [15:0] data_len;
   reg [15:0] 	count;
   begin
      $display("Sending Packet Len=%d, %d", data_len, $time);
      count   <= 2;
      tx_f36_data <= {2'b0, 1'b0, 1'b1, data_start};
      tx_f36_src_rdy  <= 1;
      #1;
      while(count < data_len)
	begin
	   while(~tx_f36_dst_rdy)
	     @(posedge sys_clk);
	   @(posedge sys_clk);
	   tx_f36_data[31:0] = tx_f36_data[31:0] + 32'h0101_0101;
	   count 	   = count + 4;
	   tx_f36_data[32] <= 0;
	end
      tx_f36_data[33] 	  <= 1;
      while(~tx_f36_dst_rdy)
	@(posedge sys_clk);
      @(posedge sys_clk);
      tx_f36_src_rdy <= 0;
   end
endtask // SendPacket_to_fifo36


task Waiter;
	input [31:0] wait_length;
	begin
		tx_f36_src_rdy <= 0;
		repeat(wait_length)
			@(posedge sys_clk);
		tx_f36_src_rdy <= 1;
	end
endtask // Waiter

task SendPacketFromFile_f36;
   input [31:0] data_len;
   input [31:0] wait_length;
   input [31:0] wait_time; // This must be a multiple of 4!
   
   integer 	count;
   begin
      $display("Sending Packet From File to LL8 Len=%d, %d",data_len,$time);
      $readmemh("test_packet.mem",pkt_rom );     
      
      while(~tx_f36_dst_rdy)
	@(posedge sys_clk);
      
      tx_f36_data[31:0] <= {pkt_rom[0], pkt_rom[1], pkt_rom[2], pkt_rom[3]};
      tx_f36_src_rdy <= 1;
      tx_f36_data[35:34]  <= 2'b00; // 4 bytes
      tx_f36_data[33]     <= 0;     // EOF
      tx_f36_data[32]     <= 1;     // SOF
      @(posedge sys_clk);
      
      // Note, this may not handle packets with sizes smaller than 8 well.
      for(i=4;i<data_len-3;i=i+4)
	begin
	   while(~tx_f36_dst_rdy)
	     @(posedge sys_clk);
	   tx_f36_data[31:0]   <= {pkt_rom[i], pkt_rom[i+1], pkt_rom[i+2], pkt_rom[i+3]};
	   tx_f36_data[35:34]  <= 2'b00; // 4 bytes
	   tx_f36_data[33]     <= 0; // EOF
	   tx_f36_data[32]     <= 0; // SOF	   
	   @(posedge sys_clk);
	   if(i==wait_time)
	     Waiter(wait_length);
	end
      
      while(~tx_f36_dst_rdy)
	@(posedge sys_clk);
      
      //
      tx_f36_data[33]     <= 1; // EOF
      tx_f36_data[35:34]  <= (data_len-i+1);
      tx_f36_data[31:0]   <=  {pkt_rom[i], pkt_rom[i+1], pkt_rom[i+2], pkt_rom[i+3]};
      @(posedge sys_clk);
      tx_f36_src_rdy <= 0;		
   end
endtask

