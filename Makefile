test_sdram_cntl:
	python3 test/sdram_cntl.py

vhdl_sdram_cntl:
	python3 conversion/sdram_cntl.py

clean:
	rm *.vhd