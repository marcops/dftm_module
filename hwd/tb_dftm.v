module tb_dftm;

reg clk_i;
reg host_intf_rst_i;
reg host_intf_rd_i;
reg host_intf_wr_i;
reg [23:0] host_intf_addr_i;
reg [15:0] host_intf_data_i;
wire [15:0] host_intf_data_o;
wire host_intf_done_o;
reg host_intf_rdPending_o;
reg host_intf_dftm_i;
reg host_intf_sdram_rst_i;
wire host_intf_sdram_rd_i;
wire host_intf_sdram_wr_i;
wire [23:0] host_intf_sdram_addr_i;
wire [15:0] host_intf_sdram_data_i;
wire [15:0] host_intf_sdram_data_o;
reg host_intf_sdram_done_o;
reg host_intf_sdram_rdPending_o;
reg host_intf_sdram_dftm_i;

initial begin
    $from_myhdl(
        clk_i,
        host_intf_rst_i,
        host_intf_rd_i,
        host_intf_wr_i,
        host_intf_addr_i,
        host_intf_data_i,
        host_intf_rdPending_o,
        host_intf_dftm_i,
        host_intf_sdram_rst_i,
        host_intf_sdram_done_o,
        host_intf_sdram_rdPending_o,
        host_intf_sdram_dftm_i
    );
    $to_myhdl(
        host_intf_data_o,
        host_intf_done_o,
        host_intf_sdram_rd_i,
        host_intf_sdram_wr_i,
        host_intf_sdram_addr_i,
        host_intf_sdram_data_i,
        host_intf_sdram_data_o
    );
end

dftm dut(
    clk_i,
    host_intf_rst_i,
    host_intf_rd_i,
    host_intf_wr_i,
    host_intf_addr_i,
    host_intf_data_i,
    host_intf_data_o,
    host_intf_done_o,
    host_intf_rdPending_o,
    host_intf_dftm_i,
    host_intf_sdram_rst_i,
    host_intf_sdram_rd_i,
    host_intf_sdram_wr_i,
    host_intf_sdram_addr_i,
    host_intf_sdram_data_i,
    host_intf_sdram_data_o,
    host_intf_sdram_done_o,
    host_intf_sdram_rdPending_o,
    host_intf_sdram_dftm_i
);

endmodule
