-- File: sdram_cntl.vhd
-- Generated by MyHDL 0.11
-- Date: Sat May 21 11:03:58 2022


library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.textio.all;

use work.pck_myhdl_011.all;

entity sdram_cntl is
    port (
        clk_i: in std_logic;
        host_intf_rst_i: in std_logic;
        host_intf_rd_i: in std_logic;
        host_intf_wr_i: in std_logic;
        host_intf_addr_i: in unsigned(23 downto 0);
        host_intf_data_i: in unsigned(15 downto 0);
        host_intf_data_o: out unsigned(15 downto 0);
        host_intf_done_o: out std_logic;
        host_intf_rdPending_o: out std_logic;
        host_intf_dftm_i: in std_logic;
        sd_intf_cke: out std_logic;
        sd_intf_cs: out std_logic;
        sd_intf_cas: out std_logic;
        sd_intf_ras: out std_logic;
        sd_intf_we: out std_logic;
        sd_intf_bs: out unsigned(1 downto 0);
        sd_intf_addr: out unsigned(12 downto 0);
        sd_intf_dqml: out std_logic;
        sd_intf_dqmh: out std_logic;
        sd_intf_dq: inout unsigned(15 downto 0)
    );
end entity sdram_cntl;


architecture MyHDL of sdram_cntl is


type t_enum_cntlstatetype_1 is (
	INITWAIT,
	INITPCHG,
	INITSETMODE,
	INITRFSH,
	RW,
	ACTIVATE,
	REFRESHROW,
	SELFREFRESH
	);

signal activate_in_progress_s: std_logic;
signal activebank_r: unsigned(1 downto 0);
signal activebank_x: unsigned(1 downto 0);
signal ba_r: unsigned(1 downto 0);
signal ba_x: unsigned(1 downto 0);
signal bank_s: unsigned(1 downto 0);
signal cmd_r: unsigned(2 downto 0);
signal cmd_x: unsigned(2 downto 0);
signal col_s: unsigned(8 downto 0);
signal doactivate_s: std_logic;
signal rastimer_r: unsigned(2 downto 0);
signal rastimer_x: unsigned(2 downto 0);
signal rd_in_progress_s: std_logic;
signal rdpipeline_r: unsigned(4 downto 0);
signal rdpipeline_x: unsigned(4 downto 0);
signal reftimer_r: unsigned(9 downto 0);
signal reftimer_x: unsigned(9 downto 0);
signal rfshcntr_r: unsigned(13 downto 0);
signal rfshcntr_x: unsigned(13 downto 0);
signal row_s: unsigned(12 downto 0);
signal saddr_r: unsigned(12 downto 0);
signal saddr_x: unsigned(12 downto 0);
signal sdata_r: unsigned(15 downto 0);
signal sdata_x: unsigned(15 downto 0);
signal sdatadir_r: std_logic;
signal sdatadir_x: std_logic;
signal sdramdata_r: unsigned(15 downto 0);
signal sdramdata_x: unsigned(15 downto 0);
signal sdriver: unsigned(15 downto 0);
signal state_r: t_enum_cntlstatetype_1;
signal state_x: t_enum_cntlstatetype_1;
signal timer_r: unsigned(10 downto 0);
signal timer_x: unsigned(10 downto 0);
signal wr_in_progress_s: std_logic;
signal wrpipeline_r: unsigned(4 downto 0);
signal wrpipeline_x: unsigned(4 downto 0);
signal wrtimer_r: unsigned(1 downto 0);
signal wrtimer_x: unsigned(1 downto 0);
type t_array_activeflag_r is array(0 to 4-1) of std_logic;
signal activeflag_r: t_array_activeflag_r;
type t_array_activeflag_x is array(0 to 4-1) of std_logic;
signal activeflag_x: t_array_activeflag_x;
type t_array_activerow_r is array(0 to 4-1) of unsigned(12 downto 0);
signal activerow_r: t_array_activerow_r;
type t_array_activerow_x is array(0 to 4-1) of unsigned(12 downto 0);
signal activerow_x: t_array_activerow_x;

begin



sd_intf_dq <= sdriver;

SDRAM_CNTL_COMB_FUNC: process (rfshcntr_r, timer_r, rd_in_progress_s, ba_r, host_intf_rd_i, activeflag_r, sdatadir_r, activebank_r, bank_s, rastimer_r, activerow_r, host_intf_wr_i, cmd_r, row_s, rdpipeline_r, col_s, saddr_r, wrtimer_r, wr_in_progress_s, ba_x, reftimer_r, doactivate_s, state_r, activate_in_progress_s) is
begin
    rdpipeline_x <= unsigned'('0' & rdpipeline_r((3 + 2)-1 downto 1));
    wrpipeline_x <= to_unsigned(0, 5);
    if (rastimer_r /= 0) then
        rastimer_x <= (rastimer_r - 1);
    else
        rastimer_x <= rastimer_r;
    end if;
    if (wrtimer_r /= 0) then
        wrtimer_x <= (wrtimer_r - 1);
    else
        wrtimer_x <= wrtimer_r;
    end if;
    if (reftimer_r /= 0) then
        reftimer_x <= (reftimer_r - 1);
        rfshcntr_x <= rfshcntr_r;
    else
        reftimer_x <= to_unsigned(782, 10);
        rfshcntr_x <= (rfshcntr_r + 1);
    end if;
    cmd_x <= cmd_r;
    state_x <= state_r;
    saddr_x <= saddr_r;
    activebank_x <= activebank_r;
    sdatadir_x <= sdatadir_r;
    for index in 0 to (2 ** 2)-1 loop
        activeflag_x(index) <= activeflag_r(index);
        activerow_x(index) <= activerow_r(index);
    end loop;
    if (timer_r /= 0) then
        timer_x <= (timer_r - 1);
        cmd_x <= to_unsigned(7, 3);
    else
        timer_x <= timer_r;
        case state_r is
            when INITWAIT =>
                timer_x <= to_unsigned(2000, 11);
                state_x <= INITPCHG;
            when INITPCHG =>
                cmd_x <= to_unsigned(2, 3);
                timer_x <= to_unsigned(2, 11);
                state_x <= INITRFSH;
                saddr_x <= to_unsigned(512, 13);
                rfshcntr_x <= to_unsigned(8, 14);
            when INITRFSH =>
                cmd_x <= to_unsigned(1, 3);
                timer_x <= to_unsigned(7, 11);
                rfshcntr_x <= (rfshcntr_r - 1);
                if (rfshcntr_r = 1) then
                    state_x <= INITSETMODE;
                end if;
            when INITSETMODE =>
                cmd_x <= to_unsigned(0, 3);
                timer_x <= to_unsigned(2, 11);
                state_x <= RW;
                saddr_x <= to_unsigned(48, 13);
            when RW =>
                if (rfshcntr_r /= 0) then
                    if ((not bool(activate_in_progress_s)) and (not bool(wr_in_progress_s)) and (not bool(rd_in_progress_s))) then
                        cmd_x <= to_unsigned(2, 3);
                        timer_x <= to_unsigned(2, 11);
                        state_x <= REFRESHROW;
                        saddr_x <= to_unsigned(512, 13);
                        for index in 0 to (2 ** 2)-1 loop
                            activeflag_x(index) <= '0';
                        end loop;
                    end if;
                elsif bool(host_intf_rd_i) then
                    if (ba_x = ba_r) then
                        if bool(doactivate_s) then
                            if ((not bool(activate_in_progress_s)) and (not bool(wr_in_progress_s)) and (not bool(rd_in_progress_s))) then
                                cmd_x <= to_unsigned(2, 3);
                                timer_x <= to_unsigned(2, 11);
                                state_x <= ACTIVATE;
                                saddr_x <= to_unsigned(0, 13);
                                activeflag_x(to_integer(bank_s)) <= '0';
                            end if;
                        elsif (not bool(rd_in_progress_s)) then
                            cmd_x <= to_unsigned(5, 3);
                            sdatadir_x <= '0';
                            saddr_x <= resize(col_s, 13);
                            rdpipeline_x <= unsigned'('1' & rdpipeline_r((3 + 2)-1 downto 1));
                        end if;
                    end if;
                elsif bool(host_intf_wr_i) then
                    if (ba_x = ba_r) then
                        if bool(doactivate_s) then
                            if ((not bool(activate_in_progress_s)) and (not bool(wr_in_progress_s)) and (not bool(rd_in_progress_s))) then
                                cmd_x <= to_unsigned(2, 3);
                                timer_x <= to_unsigned(2, 11);
                                state_x <= ACTIVATE;
                                saddr_x <= to_unsigned(0, 13);
                                activeflag_x(to_integer(bank_s)) <= '0';
                            end if;
                        elsif (not bool(rd_in_progress_s)) then
                            cmd_x <= to_unsigned(4, 3);
                            sdatadir_x <= '1';
                            saddr_x <= resize(col_s, 13);
                            wrpipeline_x <= to_unsigned(1, 5);
                            wrtimer_x <= to_unsigned(2, 2);
                        end if;
                    end if;
                else
                    cmd_x <= to_unsigned(7, 3);
                    state_x <= RW;
                end if;
            when ACTIVATE =>
                cmd_x <= to_unsigned(3, 3);
                timer_x <= to_unsigned(2, 11);
                state_x <= RW;
                rastimer_x <= to_unsigned(5, 3);
                saddr_x <= row_s;
                activebank_x <= bank_s;
                activerow_x(to_integer(bank_s)) <= row_s;
                activeflag_x(to_integer(bank_s)) <= '1';
            when REFRESHROW =>
                cmd_x <= to_unsigned(1, 3);
                timer_x <= to_unsigned(7, 11);
                state_x <= RW;
                rfshcntr_x <= (rfshcntr_r - 1);
            when others =>
                state_x <= INITWAIT;
        end case;
    end if;
end process SDRAM_CNTL_COMB_FUNC;

SDRAM_CNTL_SEQ_FUNC: process (clk_i, host_intf_rst_i) is
begin
    if (host_intf_rst_i = '1') then
        rfshcntr_r <= to_unsigned(0, 14);
        saddr_r <= to_unsigned(0, 13);
        timer_r <= to_unsigned(0, 11);
        sdata_r <= to_unsigned(0, 16);
        wrpipeline_r <= to_unsigned(0, 5);
        ba_r <= to_unsigned(0, 2);
        rastimer_r <= to_unsigned(0, 3);
        reftimer_r <= to_unsigned(782, 10);
        wrtimer_r <= to_unsigned(0, 2);
        activerow_r(0) <= to_unsigned(0, 13);
        activerow_r(1) <= to_unsigned(0, 13);
        activerow_r(2) <= to_unsigned(0, 13);
        activerow_r(3) <= to_unsigned(0, 13);
        state_r <= INITWAIT;
        activebank_r <= to_unsigned(0, 2);
        activeflag_r(0) <= '0';
        activeflag_r(1) <= '0';
        activeflag_r(2) <= '0';
        activeflag_r(3) <= '0';
        cmd_r <= to_unsigned(7, 3);
        sdatadir_r <= '0';
        rdpipeline_r <= to_unsigned(0, 5);
        sdramdata_r <= to_unsigned(0, 16);
    elsif rising_edge(clk_i) then
        state_r <= state_x;
        cmd_r <= cmd_x;
        saddr_r <= saddr_x;
        sdata_r <= sdata_x;
        sdatadir_r <= sdatadir_x;
        activebank_r <= activebank_x;
        sdramdata_r <= sdramdata_x;
        wrpipeline_r <= wrpipeline_x;
        rdpipeline_r <= rdpipeline_x;
        ba_r <= ba_x;
        timer_r <= timer_x;
        rastimer_r <= rastimer_x;
        reftimer_r <= reftimer_x;
        wrtimer_r <= wrtimer_x;
        rfshcntr_r <= rfshcntr_x;
        for index in 0 to (2 ** 2)-1 loop
            activerow_r(index) <= activerow_x(index);
            activeflag_r(index) <= activeflag_x(index);
        end loop;
    end if;
end process SDRAM_CNTL_SEQ_FUNC;

SDRAM_CNTL_SDRAM_PIN_MAP: process (saddr_r, bank_s, sdata_r, cmd_r, sdatadir_r) is
begin
    sd_intf_cke <= '1';
    sd_intf_cs <= '0';
    sd_intf_ras <= cmd_r(2);
    sd_intf_cas <= cmd_r(1);
    sd_intf_we <= cmd_r(0);
    sd_intf_bs <= bank_s;
    sd_intf_addr <= saddr_r;
    if (sdatadir_r = '1') then
        sdriver <= sdata_r;
    else
        sdriver <= "ZZZZZZZZZZZZZZZZ";
    end if;
    sd_intf_dqml <= '0';
    sd_intf_dqmh <= '0';
end process SDRAM_CNTL_SDRAM_PIN_MAP;


host_intf_done_o <= stdl(bool(rdpipeline_r(0)) or bool(wrpipeline_r(0)));
host_intf_data_o <= sdramdata_r;
host_intf_rdPending_o <= rd_in_progress_s;
sdata_x <= host_intf_data_i;


bank_s <= host_intf_addr_i(((2 + 13) + 9)-1 downto (13 + 9));
ba_x <= host_intf_addr_i(((2 + 13) + 9)-1 downto (13 + 9));
row_s <= host_intf_addr_i((13 + 9)-1 downto 9);
col_s <= host_intf_addr_i(9-1 downto 0);

SDRAM_CNTL_DO_ACTIVE: process (bank_s, rastimer_r, activerow_r, wrtimer_r, activeflag_r, sd_intf_dq, row_s, activebank_r, rdpipeline_r, sdramdata_r) is
begin
    if ((bank_s /= activebank_r) or (row_s /= activerow_r(to_integer(bank_s))) or (not bool(activeflag_r(to_integer(bank_s))))) then
        doactivate_s <= '1';
    else
        doactivate_s <= '0';
    end if;
    if (rdpipeline_r(1) = '1') then
        sdramdata_x <= sd_intf_dq;
    else
        sdramdata_x <= sdramdata_r;
    end if;
    if (rastimer_r /= 0) then
        activate_in_progress_s <= '1';
    else
        activate_in_progress_s <= '0';
    end if;
    if (wrtimer_r /= 0) then
        wr_in_progress_s <= '1';
    else
        wr_in_progress_s <= '0';
    end if;
    if (rdpipeline_r((3 + 2)-1 downto 1) /= 0) then
        rd_in_progress_s <= '1';
    else
        rd_in_progress_s <= '0';
    end if;
end process SDRAM_CNTL_DO_ACTIVE;

end architecture MyHDL;
