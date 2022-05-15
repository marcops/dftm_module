test_dftm:
	python3 test/dftm.py

gen_vhdl_dftm:
	python3 conversion/dftm.py
	mv *.vhd vhd/

clean:
	rm *.vhd