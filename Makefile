test_dftm:
	python3 test/test_dftm.py

gen_vhdl_dftm:
	python3 conversion/convert_dftm.py
	mv *.vhd vhd/

clean:
	rm *.vhd