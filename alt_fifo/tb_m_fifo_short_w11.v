module tb_m_fifo_short_w11;

reg clock;
reg reset;
reg clear;
reg [10:0] datain;
reg src_rdy_i;
wire dst_rdy_o;
wire [10:0] dataout;
wire src_rdy_o;
reg dst_rdy_i;

initial begin
    $from_myhdl(
        clock,
        reset,
        clear,
        datain,
        src_rdy_i,
        dst_rdy_i
    );
    $to_myhdl(
        dst_rdy_o,
        dataout,
        src_rdy_o
    );
end

m_fifo_short_w11 dut(
    clock,
    reset,
    clear,
    datain,
    src_rdy_i,
    dst_rdy_o,
    dataout,
    src_rdy_o,
    dst_rdy_i
);

endmodule