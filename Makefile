# .VCD = Testbench file

HWD_OUTPUT = hwd/
CONV_CMD = python3 conversion/
TEST_CMD = python3 test/
MOVE_HWD = make mv_hwd

mv_hwd:
	mv *.vhd $(HWD_OUTPUT)
	mv *.v $(HWD_OUTPUT)

test_dftm:
	sh test/run_all_dftm.sh
	mv *.vcd $(HWD_OUTPUT)

test_sdram_cntl:
	$(TEST_CMD)test_sdram_cntl.py

test_sdram:
	$(TEST_CMD)test_sdram.py

gen_dftm_tb:
	$(TEST_CMD)test_dftm.py tst_1BF_CD_NONE
	mv *.vcd $(HWD_OUTPUT)/dftm.vcd

gen_sdram_hwd:
	$(CONV_CMD)conv_sdram_cntl.py
	$(MOVE_HWD)

gen_dftm_hwd:
	$(CONV_CMD)conv_dftm.py
	$(MOVE_HWD)

gen_sdram_cntl: test_sdram_cntl gen_sdram_hwd

gen_dftm: gen_dftm_tb gen_dftm_hwd

all_dftm: test_dftm gen_dftm_hwd

all: test_sdram gen_sdram_cntl all_dftm


clean :
	rm -rf *.vhd 
	rm -rf *.vcd
	rm -rf *.v

yosys:
	yosys dftm.ys