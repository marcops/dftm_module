test_dftm:
	rm -rf *.vcd
	sh test/run_all_dftm.sh

gen_dftm:
	rm -rf *.vcd
	python3 conversion/conv_dftm.py
	mv *.vhd vhd/
	mv *.v vhd/
	python3 test/test_dftm.py tst_1BF_CD_NONE
	mv *.vcd vhd/

test_gen_dftm:
	rm -rf *.vcd
	python3 conversion/conv_dftm.py
	rm -rf *.vhd 
	rm -rf *.vcd

clean:
	rm -rf *.vhd 
	rm -rf *.vcd

make yosys:
	yosys dftm.ys