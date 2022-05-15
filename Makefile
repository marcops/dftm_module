test_dftm:
	rm -rf *.vcd
	python3 test/test_dftm.py

gen_vhdl_dftm:
	rm -rf *.vcd
	python3 conversion/conv_dftm.py
	mv *.vhd vhd/
	python3 test/test_dftm.py
	mv *.vcd vhd/

clean:
	rm *.vhd