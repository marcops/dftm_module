from myhdl import *
class dftm_ram():  
    
    def get_position(addr, page_size):
        return addr // page_size 
  
    def get_previous_encode(enc):
        #FIRST_ENCODE = 0
        if enc <= 1:
            return 1
        else:
            return enc - 1

    def get_next_encode(enc):
        #LAST_ENCODE = 3
        if enc >= 3:
            return 3
        else:
            return enc + 1

    def set_cycle(mem, r_cycle):
        cycle = intbv(r_cycle)[32:]
        POS_CYCLE = 8
        mem.next[POS_CYCLE   ] = cycle[ 0]
        mem.next[POS_CYCLE+ 1] = cycle[ 1]
        mem.next[POS_CYCLE+ 2] = cycle[ 2]
        mem.next[POS_CYCLE+ 3] = cycle[ 3]
        mem.next[POS_CYCLE+ 4] = cycle[ 4]
        mem.next[POS_CYCLE+ 5] = cycle[ 5]
        mem.next[POS_CYCLE+ 6] = cycle[ 6]
        mem.next[POS_CYCLE+ 7] = cycle[ 7]
        mem.next[POS_CYCLE+ 8] = cycle[ 8]
        mem.next[POS_CYCLE+ 9] = cycle[ 9]
        mem.next[POS_CYCLE+10] = cycle[10]
        mem.next[POS_CYCLE+11] = cycle[11]
        mem.next[POS_CYCLE+12] = cycle[12]
        mem.next[POS_CYCLE+13] = cycle[13]
        mem.next[POS_CYCLE+14] = cycle[14]
        mem.next[POS_CYCLE+15] = cycle[15]
        mem.next[POS_CYCLE+16] = cycle[16]
        mem.next[POS_CYCLE+17] = cycle[17]
        mem.next[POS_CYCLE+18] = cycle[18]
        mem.next[POS_CYCLE+19] = cycle[19]
        mem.next[POS_CYCLE+20] = cycle[20]
        mem.next[POS_CYCLE+21] = cycle[21]
        mem.next[POS_CYCLE+22] = cycle[22]
        mem.next[POS_CYCLE+23] = cycle[23]
        mem.next[POS_CYCLE+24] = cycle[24]
        mem.next[POS_CYCLE+25] = cycle[25]
        mem.next[POS_CYCLE+26] = cycle[26]
        mem.next[POS_CYCLE+27] = cycle[27]
        mem.next[POS_CYCLE+27] = cycle[28]
        mem.next[POS_CYCLE+29] = cycle[29]
        mem.next[POS_CYCLE+30] = cycle[30]
        mem.next[POS_CYCLE+31] = cycle[31]
    
    def get_cycle(mem):
        POS_CYCLE = 8
        d = intbv(0)[32:]
        d[ 0] = mem[POS_CYCLE]
        d[ 1] = mem[POS_CYCLE+ 1]
        d[ 2] = mem[POS_CYCLE+ 2]
        d[ 3] = mem[POS_CYCLE+ 3]
        d[ 4] = mem[POS_CYCLE+ 4]        
        d[ 5] = mem[POS_CYCLE+ 5]
        d[ 6] = mem[POS_CYCLE+ 6]
        d[ 7] = mem[POS_CYCLE+ 7]
        d[ 8] = mem[POS_CYCLE+ 8]
        d[ 9] = mem[POS_CYCLE+ 9]
        d[10] = mem[POS_CYCLE+10]
        d[11] = mem[POS_CYCLE+11]
        d[12] = mem[POS_CYCLE+12]
        d[13] = mem[POS_CYCLE+13]
        d[14] = mem[POS_CYCLE+14]
        d[15] = mem[POS_CYCLE+15]
        d[16] = mem[POS_CYCLE+16]
        d[17] = mem[POS_CYCLE+17]
        d[18] = mem[POS_CYCLE+18]
        d[19] = mem[POS_CYCLE+19]
        d[20] = mem[POS_CYCLE+20]
        d[21] = mem[POS_CYCLE+21]
        d[22] = mem[POS_CYCLE+22]
        d[23] = mem[POS_CYCLE+23]
        d[24] = mem[POS_CYCLE+24]
        d[25] = mem[POS_CYCLE+25]
        d[26] = mem[POS_CYCLE+26]
        d[27] = mem[POS_CYCLE+27]
        d[28] = mem[POS_CYCLE+28]
        d[29] = mem[POS_CYCLE+29]
        d[30] = mem[POS_CYCLE+30]
        d[31] = mem[POS_CYCLE+31]
        return d

    def set_count_error(mem, count):
        csig = intbv(count)[5:]
        POS_COUNT_ERROR = 3
        mem.next[POS_COUNT_ERROR] = csig[0]
        mem.next[POS_COUNT_ERROR+1] = csig[1]
        mem.next[POS_COUNT_ERROR+2] = csig[2]
        mem.next[POS_COUNT_ERROR+3] = csig[3]
        mem.next[POS_COUNT_ERROR+4] = csig[4]
    def get_count_error(mem):
        POS_COUNT_ERROR = 3
        d = intbv(0)[5:]
        d[0] = mem[POS_COUNT_ERROR]
        d[1] = mem[POS_COUNT_ERROR+1]
        d[2] = mem[POS_COUNT_ERROR+2]
        d[3] = mem[POS_COUNT_ERROR+3]
        d[4] = mem[POS_COUNT_ERROR+4]
        return d

    def set_encode(mem, enc):
        POS_ENCODE = 1
        mem.next[POS_ENCODE] = enc[0]
        mem.next[POS_ENCODE+1] = enc[1]
    def get_encode(mem):
        POS_ENCODE = 1
        d = intbv(0)[2:]
        d[0] = mem[POS_ENCODE]
        d[1] = mem[POS_ENCODE+1]
        return int(d)

    def get_configuration(mem):
        return mem[0]
    def set_configuration(mem, config):
        mem.next[0] = config        
    
    
