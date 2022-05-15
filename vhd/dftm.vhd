-- File: dftm.vhd
-- Generated by MyHDL 0.11
-- Date: Sun May 15 14:11:21 2022


library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.textio.all;

use work.pck_myhdl_011.all;

entity dftm is
    port (
        clk_i: in std_logic;
        host_intf_rst_i: in std_logic;
        host_intf_rd_i: in std_logic;
        host_intf_wr_i: in std_logic;
        host_intf_addr_i: in unsigned(23 downto 0);
        host_intf_data_i: in unsigned(15 downto 0);
        host_intf_data_o: out unsigned(15 downto 0);
        host_intf_done_o: out std_logic;
        host_intf_rdPending_o: in std_logic;
        host_intf_sdram_rst_i: in std_logic;
        host_intf_sdram_rd_i: out std_logic;
        host_intf_sdram_wr_i: out std_logic;
        host_intf_sdram_addr_i: out unsigned(23 downto 0);
        host_intf_sdram_data_i: out unsigned(15 downto 0);
        host_intf_sdram_data_o: in unsigned(15 downto 0);
        host_intf_sdram_done_o: in std_logic;
        host_intf_sdram_rdPending_o: in std_logic
    );
end entity dftm;


architecture MyHDL of dftm is


type t_enum_OPERATION_MODE_1 is (
	NORMAL,
	RECODING_UP,
	RECODING_DOWN
	);
type t_enum_RECODING_MODE_2 is (
	READ,
	WAIT_READ,
	WRITE,
	WAIT_WRITE
	);

signal current_operation_mode: t_enum_OPERATION_MODE_1;
signal current_recoding_mode: t_enum_RECODING_MODE_2;
signal recode_count: unsigned(15 downto 0);
signal recode_data_o: unsigned(15 downto 0);
signal recode_from_ecc: unsigned(2 downto 0);
signal recode_position: unsigned(23 downto 0);
signal recode_to_ecc: unsigned(2 downto 0);
type t_array_ram is array(0 to 256-1) of unsigned(2 downto 0);
signal ram: t_array_ram;

function MYHDL2_get_position(
    addr: in unsigned;
    page_size: in natural
    ) return integer is
begin
    return to_integer(addr / page_size);
end function MYHDL2_get_position;

function MYHDL3_get_encode(
    mem: in unsigned
    ) return integer is
begin
    return to_integer(shift_right(mem, 1));
end function MYHDL3_get_encode;

function MYHDL4_encoder(
    data: in unsigned;
    type: in integer
    ) return unsigned is
begin
    return data;
end function MYHDL4_encoder;

function MYHDL5_decoder_check(
    data: in unsigned;
    type: in integer
    ) return std_logic is
begin
    return '1';
end function MYHDL5_decoder_check;

function MYHDL6_get_next_encode(
    enc: in integer
    ) return integer is
    variable L: line;
    variable LAST_ENCODE: natural;
begin
    LAST_ENCODE := 3;
    if (enc >= 3) then
        write(L, string'("more:"));
        write(L, string'(" "));
        write(L, to_string(enc));
        writeline(output, L);
        return enc;
    end if;
    write(L, string'("enc+1:"));
    write(L, string'(" "));
    write(L, to_string(enc));
    writeline(output, L);
    return (enc + 1);
end function MYHDL6_get_next_encode;

function MYHDL7_decoder(
    data: in std_logic;
    type: in integer
    ) return std_logic is
begin
    return data;
end function MYHDL7_decoder;

function MYHDL8_decoder(
    data: in std_logic;
    type: in integer
    ) return std_logic is
begin
    return data;
end function MYHDL8_decoder;

function MYHDL9_decoder(
    data: in std_logic;
    type: in integer
    ) return std_logic is
begin
    return data;
end function MYHDL9_decoder;

function MYHDL10_decoder(
    data: in unsigned;
    type: in unsigned
    ) return unsigned is
begin
    return data;
end function MYHDL10_decoder;

function MYHDL11_encoder(
    data: in unsigned;
    type: in unsigned
    ) return unsigned is
begin
    return data;
end function MYHDL11_encoder;

procedure MYHDL12_set_encode(
    signal mem: out unsigned;
    signal enc: in unsigned) is
begin
    mem(1) <= (enc and to_unsigned(1, 3))(0);
    mem(2) <= shift_right((enc and to_unsigned(2, 3)), 1)(0);
end procedure MYHDL12_set_encode;

begin




DFTM_MAIN: process (clk_i) is
    variable L: line;
    variable iram_current_position: integer;
    variable ram_inf: unsigned(2 downto 0);
    variable current_encode: integer;
    variable decode_ok: std_logic;
    variable next_encode: integer;
    variable recode: std_logic;
    variable recoding_current_address: integer;
    variable r_count: integer;
begin
    if rising_edge(clk_i) then
        if (current_operation_mode = NORMAL) then
            iram_current_position := MYHDL2_get_position(host_intf_addr_i, 1);
            ram_inf := ram(iram_current_position);
            current_encode := MYHDL3_get_encode(ram_inf);
            host_intf_sdram_addr_i <= host_intf_addr_i;
            host_intf_sdram_data_i <= MYHDL4_encoder(host_intf_data_i, current_encode);
            host_intf_sdram_rd_i <= host_intf_rd_i;
            host_intf_sdram_wr_i <= host_intf_wr_i;
            if bool(host_intf_sdram_done_o) then
                host_intf_data_o <= host_intf_sdram_data_o;
                decode_ok := MYHDL5_decoder_check(host_intf_data_i, current_encode);
                -- FAKE ERR WHEN 120 
                decode_ok := stdl((not (bool(host_intf_rd_i) and (host_intf_addr_i = 120))));
                write(L, string'("[DFTM] addr:"));
                write(L, string'(" "));
                write(L, to_hstring(host_intf_data_i));
                write(L, string'(" "));
                write(L, string'(", ecc:"));
                write(L, string'(" "));
                write(L, to_string(current_encode));
                writeline(output, L);
                if (decode_ok = '0') then
                    next_encode := MYHDL6_get_next_encode(current_encode);
                    recode := stdl(next_encode /= current_encode);
                    write(L, string'("will recode:"));
                    write(L, string'(" "));
                    write(L, to_string(bool(recode)));
                    writeline(output, L);
                    if bool(recode) then
                        current_operation_mode <= RECODING_UP;
                        current_recoding_mode <= READ;
                        recode_position <= to_unsigned(iram_current_position, 24);
                        recode_from_ecc <= to_unsigned(current_encode, 3);
                        recode_to_ecc <= to_unsigned(next_encode, 3);
                        recode_count <= to_unsigned(0, 16);
                        host_intf_done_o <= '0';
                        host_intf_sdram_rd_i <= '0';
                        host_intf_sdram_wr_i <= '0';
                    else
                        host_intf_done_o <= MYHDL7_decoder(host_intf_sdram_done_o, current_encode);
                    end if;
                else
                    host_intf_done_o <= MYHDL8_decoder(host_intf_sdram_done_o, current_encode);
                end if;
            else
                host_intf_done_o <= MYHDL9_decoder(host_intf_sdram_done_o, current_encode);
                host_intf_data_o <= host_intf_sdram_data_o;
            end if;
        else
            if ((recode_count = 0) and (current_recoding_mode = READ)) then
                write(L, string'("STATING RECODING pos:"));
                write(L, string'(" "));
                write(L, to_hstring(recode_position));
                write(L, string'(" "));
                write(L, string'(", FROM ECC "));
                write(L, string'(" "));
                write(L, to_hstring(recode_from_ecc));
                write(L, string'(" "));
                write(L, string'(", to:"));
                write(L, string'(" "));
                write(L, to_hstring(recode_to_ecc));
                writeline(output, L);
            end if;
            recoding_current_address := to_integer((recode_position * 1) + recode_count);
            write(L, string'("RECODING "));
            write(L, string'(" "));
            write(L, to_hstring(recode_position));
            write(L, string'(" "));
            write(L, string'(" - "));
            write(L, string'(" "));
            write(L, to_hstring(recode_count));
            write(L, string'(" "));
            write(L, string'(" - "));
            write(L, string'(" "));
            write(L, to_string(recoding_current_address));
            writeline(output, L);
            if (current_recoding_mode = READ) then
                write(L, to_string(current_recoding_mode));
                writeline(output, L);
                host_intf_sdram_addr_i <= to_unsigned(recoding_current_address, 24);
                host_intf_sdram_rd_i <= '1';
                current_recoding_mode <= WAIT_READ;
            end if;
            if (current_recoding_mode = WAIT_READ) then
                write(L, to_string(current_recoding_mode));
                writeline(output, L);
                host_intf_sdram_rd_i <= '0';
                if bool(host_intf_sdram_done_o) then
                    current_recoding_mode <= WRITE;
                    recode_data_o <= MYHDL10_decoder(host_intf_sdram_data_o, recode_from_ecc);
                    -- TODO IGNORING THE DECODE ERROR 
                    write(L, string'("RECODING READ "));
                    write(L, string'(" "));
                    write(L, to_hstring(host_intf_sdram_data_o));
                    writeline(output, L);
                end if;
            end if;
            if (current_recoding_mode = WRITE) then
                write(L, to_string(current_recoding_mode));
                writeline(output, L);
                host_intf_sdram_addr_i <= to_unsigned(recoding_current_address, 24);
                host_intf_sdram_data_i <= MYHDL11_encoder(recode_data_o, recode_to_ecc);
                current_recoding_mode <= WAIT_WRITE;
            end if;
            if (current_recoding_mode = WAIT_WRITE) then
                write(L, to_string(current_recoding_mode));
                writeline(output, L);
                host_intf_sdram_wr_i <= '1';
                if bool(host_intf_sdram_done_o) then
                    host_intf_sdram_rd_i <= '0';
                    host_intf_sdram_wr_i <= '0';
                    r_count := to_integer(recode_count + 1);
                    if (r_count < 1) then
                        current_recoding_mode <= READ;
                        recode_count <= to_unsigned(r_count, 16);
                    else
                        -- RECODING DONE
                        host_intf_done_o <= '1';
                        current_operation_mode <= NORMAL;
                        ram_inf := ram(to_integer(recode_position));
                        MYHDL12_set_encode(ram_inf, recode_to_ecc);
                        write(L, string'("Change encode pos:"));
                        write(L, string'(" "));
                        write(L, to_hstring(recode_position));
                        write(L, string'(" "));
                        write(L, string'(", from:"));
                        write(L, string'(" "));
                        write(L, to_hstring(recode_from_ecc));
                        write(L, string'(" "));
                        write(L, string'(",to:"));
                        write(L, string'(" "));
                        write(L, to_hstring(recode_to_ecc));
                        writeline(output, L);
                    end if;
                end if;
            end if;
        end if;
    end if;
end process DFTM_MAIN;

end architecture MyHDL;
