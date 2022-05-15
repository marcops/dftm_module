test_dftm:
	python3 test/test_dftm.py

gen_vhdl_dftm:
	python3 conversion/conv_dftm.py
	mv *.vhd vhd/

clean:
	rm *.vhd