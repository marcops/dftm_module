#IRAM_DATA_SIZE = 1 + 2 + 5 + 32
IRAM_SIZE_DYNAMIC = 1
IRAM_SIZE_ECC = 2
INIT_COUNT = IRAM_SIZE_DYNAMIC + IRAM_SIZE_ECC
IRAM_SIZE_COUNT_ERROR = 5
IRAM_DATA_SIZE = IRAM_SIZE_DYNAMIC + IRAM_SIZE_ECC + IRAM_SIZE_COUNT_ERROR


WORD_SIZE = 64
WORD_SIZE_WITH_ECC = 72
WORD_DOUBLE_SIZE = 128
WORD_DOUBLE_SIZE_WITH_ECC = 144
DISTANCE_ECC_ONE_MODULE = 8

ECC_NONE = 0
ECC_PARITY = 1
ECC_HAMMING = 2
ECC_LPC_WITHOUT_PARITY = 3
#ECC_DOUBLE_XOR = 4