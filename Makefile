test_dftm:
	python3 test/dftm.py

gen_vhdl_sdram_cntl:
	python3 conversion/sdram_cntl.py
	mv *.vhd vhd/

clean:
	rm *.vhd