
def read_file():
    with open('sim.txt', 'r') as reader:
        with open('sim.csv', 'w') as writer:
            lines = reader.readlines()
            #count = 0
            merged_line = "tick address bitflip_pos bitflip_amount will_recode curr_ecc next_ecc block_pos data_write data_rec fixed\n"
            writer.writelines(merged_line)
            has_one = False
            for line in lines:
                if line.startswith("RECODE 0 "):
                    merged_line = line[len("RECODE 0 "):].strip()
                    has_one = False
                elif line.startswith("RECODE 1"):
                    has_one = True
                    merged_line+=" "
                    merged_line += line[len("RECODE 1"):].strip()                    
                elif line.startswith("RECODE 2"):
                    if has_one == False:
                        merged_line += " False 0 0 -1"    
                    merged_line += line[len("RECODE 2"):]
                    writer.writelines(merged_line)
                else:
                    raise("FAIL")

read_file()


  
