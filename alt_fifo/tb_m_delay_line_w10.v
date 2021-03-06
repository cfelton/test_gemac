module tb_m_delay_line_w10;

reg clk;
reg [3:0] delay;
reg [9:0] din;
wire [9:0] dout;

initial begin
    $from_myhdl(
        clk,
        delay,
        din
    );
    $to_myhdl(
        dout
    );
end

m_delay_line_w10 dut(
    clk,
    delay,
    din,
    dout
);

endmodule
