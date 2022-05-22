class Parity():
	def odd(x):
		x ^= x >> 8
		x ^= x >> 4
		x ^= x >> 2
		x ^= x >> 1
		return (~x) & 1

	def encode(data):
		x = Parity.odd(data)
		data = data << 1
		return data + x

	def check(data):
		c = data & 0x1	
		data = data >> 1	
		x = Parity.odd(data)
		return c == x
        
	def decode(data):
		return data >> 1


#def test():
#	val = 2
	#enc = Parity.encode(val)
	#dec = Parity.decode(enc)
	#print("check data " , Parity.check(enc))
	#print("enc/dec is ok? " , val == dec)