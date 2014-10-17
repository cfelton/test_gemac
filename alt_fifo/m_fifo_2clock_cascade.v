// File: m_fifo_2clock_cascade.v
// Generated by MyHDL 0.9dev
// Date: Mon Jul 21 18:53:12 2014


`timescale 1ns/10ps

module m_fifo_2clock_cascade (
    wclk,
    datain,
    src_rdy_i,
    dst_rdy_o,
    space,
    rclk,
    dataout,
    src_rdy_o,
    dst_rdy_i,
    occupied,
    reset
);


input wclk;
input [35:0] datain;
input src_rdy_i;
output dst_rdy_o;
wire dst_rdy_o;
input [15:0] space;
input rclk;
output [35:0] dataout;
wire [35:0] dataout;
output src_rdy_o;
wire src_rdy_o;
input dst_rdy_i;
input [15:0] occupied;
input reset;

reg fbus3_empty;
reg fbus3_full;
reg fbus1_full;
wire fbus2_empty;
wire rd;
wire fbus2_full;
reg fbus1_empty;
reg ed1;
wire rd1;
wire rd2;
reg fbus2_rvld;
wire wr3;
wire wr;
reg [4:0] gfifo3_nvacant;
reg [3:0] gfifo3_addr;
wire gfifo3_fbus_rvld;
reg [4:0] gfifo3_ntenant;
wire [35:0] gfifo3_fbus_wdata;
wire gfifo3_fbus_clear;
reg gfifo2_wfull;
wire [6:0] gfifo2_raddr;
wire [6:0] gfifo2_waddr;
reg [7:0] gfifo2_rq2_wptr;
reg [7:0] gfifo2_wq2_rptr;
reg [7:0] gfifo2_wptr;
reg gfifo2_rrst;
reg gfifo2_rempty;
reg gfifo2_wrst;
wire gfifo2__we;
reg [7:0] gfifo2_rptr;
reg [7:0] gfifo2_rbin;
reg [7:0] gfifo2_wbin;
wire [35:0] gfifo2_g_fifomem_din;
reg [35:0] gfifo2_g_fifomem__din;
reg [6:0] gfifo2_g_fifomem__addr_w;
reg [35:0] gfifo2_g_fifomem__dout;
reg gfifo2_g_fifomem__wr;
reg [7:0] gfifo2_gs4_d1;
reg [7:0] gfifo2_gs3_d1;
reg [4:0] gfifo1_nvacant;
reg [3:0] gfifo1_addr;
wire gfifo1_fbus_rvld;
reg [4:0] gfifo1_ntenant;
wire gfifo1_fbus_clear;

reg [35:0] gfifo3_mem [0:16-1];
reg [35:0] gfifo2_g_fifomem_mem [0:128-1];
reg gfifo2_gs2_rsync [0:2-1];
reg gfifo2_gs1_rsync [0:2-1];
reg [35:0] gfifo1_mem [0:16-1];

assign gfifo3_fbus_clear = 0;
assign gfifo1_fbus_clear = 0;




assign wr = (src_rdy_i && dst_rdy_o);
assign rd = (dst_rdy_i && src_rdy_o);
assign rd1 = ((!fbus1_empty) && (!fbus2_full));
assign rd2 = ((!ed1) && (!fbus3_full));
assign wr3 = fbus2_rvld;



assign dst_rdy_o = (!fbus1_full);
assign src_rdy_o = (!fbus3_empty);


always @(posedge rclk, posedge reset) begin: M_FIFO_2CLOCK_CASCADE_RTL_ED1
    if (reset == 1) begin
        ed1 <= 1;
    end
    else begin
        if (ed1) begin
            ed1 <= fbus2_empty;
        end
        else begin
            ed1 <= 1'b1;
        end
    end
end


always @(posedge wclk) begin: M_FIFO_2CLOCK_CASCADE_GFIFO1_RTL_SRL_IN
    integer ii;
    if (wr) begin
        gfifo1_mem[0] <= datain;
        for (ii=1; ii<16; ii=ii+1) begin
            gfifo1_mem[ii] <= gfifo1_mem[(ii - 1)];
        end
    end
end



assign gfifo2_g_fifomem_din = gfifo1_mem[gfifo1_addr];



assign gfifo1_fbus_rvld = rd1;


always @(posedge wclk, posedge reset) begin: M_FIFO_2CLOCK_CASCADE_GFIFO1_RTL_FIFO
    if (reset == 1) begin
        fbus1_empty <= 1;
        fbus1_full <= 0;
        gfifo1_addr <= 0;
    end
    else begin
        if (gfifo1_fbus_clear) begin
            gfifo1_addr <= 0;
            fbus1_empty <= 1'b1;
            fbus1_full <= 1'b0;
        end
        else if ((rd1 && (!wr))) begin
            fbus1_full <= 1'b0;
            if ((gfifo1_addr == 0)) begin
                fbus1_empty <= 1'b1;
            end
            else begin
                gfifo1_addr <= (gfifo1_addr - 1);
            end
        end
        else if ((wr && (!rd1))) begin
            fbus1_empty <= 1'b0;
            if ((!fbus1_empty)) begin
                gfifo1_addr <= (gfifo1_addr + 1);
            end
            if (($signed({1'b0, gfifo1_addr}) == (16 - 2))) begin
                fbus1_full <= 1'b1;
            end
        end
    end
end


always @(posedge wclk, posedge reset) begin: M_FIFO_2CLOCK_CASCADE_GFIFO1_DBG_OCCUPANCY
    if (reset == 1) begin
        gfifo1_nvacant <= 16;
        gfifo1_ntenant <= 0;
    end
    else begin
        if (gfifo1_fbus_clear) begin
            gfifo1_nvacant <= 16;
            gfifo1_ntenant <= 0;
        end
        else if ((rd1 && (!wr))) begin
            gfifo1_nvacant <= (gfifo1_nvacant + 1);
            gfifo1_ntenant <= (gfifo1_ntenant - 1);
        end
        else if ((wr && (!rd1))) begin
            gfifo1_nvacant <= (gfifo1_nvacant - 1);
            gfifo1_ntenant <= (gfifo1_ntenant + 1);
        end
    end
end


always @(posedge rclk, posedge gfifo2_rrst) begin: M_FIFO_2CLOCK_CASCADE_GFIFO2_RTL_RPTRS
    integer rbn;
    integer rpn;
    if (gfifo2_rrst == 1) begin
        fbus2_rvld <= 0;
        gfifo2_rptr <= 0;
        gfifo2_rbin <= 0;
        gfifo2_rempty <= 1;
    end
    else begin
        rbn = (gfifo2_rbin + (rd2 && (!gfifo2_rempty)));
        gfifo2_rbin <= rbn;
        rpn = ($signed(rbn >>> 1) ^ rbn);
        gfifo2_rptr <= rpn;
        gfifo2_rempty <= (rpn == $signed({1'b0, gfifo2_rq2_wptr}));
        fbus2_rvld <= (rd2 && (!gfifo2_rempty));
    end
end


always @(posedge wclk, posedge gfifo2_wrst) begin: M_FIFO_2CLOCK_CASCADE_GFIFO2_RTL_WPTRS
    integer wbn;
    integer wpn;
    if (gfifo2_wrst == 1) begin
        gfifo2_wfull <= 0;
        gfifo2_wbin <= 0;
        gfifo2_wptr <= 0;
    end
    else begin
        wbn = (gfifo2_wbin + (rd1 && (!gfifo2_wfull)));
        gfifo2_wbin <= wbn;
        wpn = ($signed(wbn >>> 1) ^ wbn);
        gfifo2_wptr <= wpn;
        gfifo2_wfull <= (wpn == {(~gfifo2_wq2_rptr[(7 + 1)-1:(7 - 1)]), gfifo2_wq2_rptr[(7 - 1)-1:0]});
    end
end


always @(posedge wclk, posedge reset) begin: M_FIFO_2CLOCK_CASCADE_GFIFO2_GS1_RTL
    if (reset == 1) begin
        gfifo2_gs1_rsync[0] <= 1;
        gfifo2_gs1_rsync[1] <= 1;
        gfifo2_wrst <= 1;
    end
    else begin
        gfifo2_gs1_rsync[0] <= reset;
        gfifo2_gs1_rsync[1] <= gfifo2_gs1_rsync[0];
        gfifo2_wrst <= gfifo2_gs1_rsync[1];
    end
end



assign gfifo3_fbus_wdata = gfifo2_g_fifomem__dout;


always @(posedge rclk) begin: M_FIFO_2CLOCK_CASCADE_GFIFO2_G_FIFOMEM_RTL_RD
    gfifo2_g_fifomem__dout <= gfifo2_g_fifomem_mem[gfifo2_raddr];
end


always @(posedge wclk) begin: M_FIFO_2CLOCK_CASCADE_GFIFO2_G_FIFOMEM_RTL_WR
    gfifo2_g_fifomem__wr <= gfifo2__we;
    gfifo2_g_fifomem__addr_w <= gfifo2_waddr;
    gfifo2_g_fifomem__din <= gfifo2_g_fifomem_din;
end


always @(posedge wclk) begin: M_FIFO_2CLOCK_CASCADE_GFIFO2_G_FIFOMEM_RTL_MEM
    if (gfifo2_g_fifomem__wr) begin
        gfifo2_g_fifomem_mem[gfifo2_g_fifomem__addr_w] <= gfifo2_g_fifomem__din;
    end
end


always @(posedge rclk, posedge reset) begin: M_FIFO_2CLOCK_CASCADE_GFIFO2_GS2_RTL
    if (reset == 1) begin
        gfifo2_gs2_rsync[0] <= 1;
        gfifo2_gs2_rsync[1] <= 1;
        gfifo2_rrst <= 1;
    end
    else begin
        gfifo2_gs2_rsync[0] <= reset;
        gfifo2_gs2_rsync[1] <= gfifo2_gs2_rsync[0];
        gfifo2_rrst <= gfifo2_gs2_rsync[1];
    end
end


always @(posedge rclk, posedge gfifo2_rrst) begin: M_FIFO_2CLOCK_CASCADE_GFIFO2_GS4_RTL
    if (gfifo2_rrst == 1) begin
        gfifo2_rq2_wptr <= 0;
        gfifo2_gs4_d1 <= 0;
    end
    else begin
        gfifo2_gs4_d1 <= gfifo2_wptr;
        gfifo2_rq2_wptr <= gfifo2_gs4_d1;
    end
end



assign gfifo2__we = (rd1 && (!fbus2_full));



assign fbus2_empty = gfifo2_rempty;
assign fbus2_full = gfifo2_wfull;



assign gfifo2_waddr = gfifo2_wbin[7-1:0];
assign gfifo2_raddr = gfifo2_rbin[7-1:0];


always @(posedge wclk, posedge gfifo2_wrst) begin: M_FIFO_2CLOCK_CASCADE_GFIFO2_GS3_RTL
    if (gfifo2_wrst == 1) begin
        gfifo2_wq2_rptr <= 0;
        gfifo2_gs3_d1 <= 0;
    end
    else begin
        gfifo2_gs3_d1 <= gfifo2_rptr;
        gfifo2_wq2_rptr <= gfifo2_gs3_d1;
    end
end


always @(posedge rclk) begin: M_FIFO_2CLOCK_CASCADE_GFIFO3_RTL_SRL_IN
    integer ii;
    if (wr3) begin
        gfifo3_mem[0] <= gfifo3_fbus_wdata;
        for (ii=1; ii<16; ii=ii+1) begin
            gfifo3_mem[ii] <= gfifo3_mem[(ii - 1)];
        end
    end
end



assign dataout = gfifo3_mem[gfifo3_addr];



assign gfifo3_fbus_rvld = rd;


always @(posedge rclk, posedge reset) begin: M_FIFO_2CLOCK_CASCADE_GFIFO3_RTL_FIFO
    if (reset == 1) begin
        fbus3_empty <= 1;
        fbus3_full <= 0;
        gfifo3_addr <= 0;
    end
    else begin
        if (gfifo3_fbus_clear) begin
            gfifo3_addr <= 0;
            fbus3_empty <= 1'b1;
            fbus3_full <= 1'b0;
        end
        else if ((rd && (!wr3))) begin
            fbus3_full <= 1'b0;
            if ((gfifo3_addr == 0)) begin
                fbus3_empty <= 1'b1;
            end
            else begin
                gfifo3_addr <= (gfifo3_addr - 1);
            end
        end
        else if ((wr3 && (!rd))) begin
            fbus3_empty <= 1'b0;
            if ((!fbus3_empty)) begin
                gfifo3_addr <= (gfifo3_addr + 1);
            end
            if (($signed({1'b0, gfifo3_addr}) == (16 - 2))) begin
                fbus3_full <= 1'b1;
            end
        end
    end
end


always @(posedge rclk, posedge reset) begin: M_FIFO_2CLOCK_CASCADE_GFIFO3_DBG_OCCUPANCY
    if (reset == 1) begin
        gfifo3_nvacant <= 16;
        gfifo3_ntenant <= 0;
    end
    else begin
        if (gfifo3_fbus_clear) begin
            gfifo3_nvacant <= 16;
            gfifo3_ntenant <= 0;
        end
        else if ((rd && (!wr3))) begin
            gfifo3_nvacant <= (gfifo3_nvacant + 1);
            gfifo3_ntenant <= (gfifo3_ntenant - 1);
        end
        else if ((wr3 && (!rd))) begin
            gfifo3_nvacant <= (gfifo3_nvacant - 1);
            gfifo3_ntenant <= (gfifo3_ntenant + 1);
        end
    end
end

endmodule