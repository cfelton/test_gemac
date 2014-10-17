module tb_m_fifo_2clock_cascade;

reg wclk;
reg [35:0] datain;
reg src_rdy_i;
wire dst_rdy_o;
reg [15:0] space;
reg rclk;
wire [35:0] dataout;
wire src_rdy_o;
reg dst_rdy_i;
reg [15:0] occupied;
reg reset;

initial begin
    $from_myhdl(
        wclk,
        datain,
        src_rdy_i,
        space,
        rclk,
        dst_rdy_i,
        occupied,
        reset
    );
    $to_myhdl(
        dst_rdy_o,
        dataout,
        src_rdy_o
    );
end

m_fifo_2clock_cascade dut(
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

endmodule
