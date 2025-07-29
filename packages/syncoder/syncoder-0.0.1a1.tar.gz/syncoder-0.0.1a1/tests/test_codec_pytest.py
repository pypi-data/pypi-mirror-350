#write a test for codec.py

import random
import numpy as np
from itertools import product

import syncoder as codec

#logging.basicConfig(level=logging.DEBUG,stream=sys.stdout)
#numba_logger = logging.getLogger('numba')
#numba_logger.setLevel(logging.WARNING)

def test_encode_decode(): 
  c = codec.BaseNBlockCodec(inner_alphabet_size=32,inner_d=5,inner_n=30)

  in_text = (codec.lipsum + codec.lipsum)[0:c.block_capacity_bytes]

  coded = c.encode( in_text )
  random.shuffle(coded)
  #coded = coded[:-4] #erase a random strands
  corrupt_index = random.randint(0,len(coded[0])) 
  coded[0][corrupt_index] = 6 

  out_text = c.decode( coded )[0]
  assert in_text == out_text

def test_coded_to_bases():
  #TODO: test optimize too

  test_encoded_data = np.random.randint(0,32,(10,31),dtype=np.uint8)
  DNA_with_scores = codec.b32_to_DNA_optimize(test_encoded_data,codec._default_b32_alphabet,codec._default_b32_alphabet_alt)
  DNA = [x[0] for x in DNA_with_scores]
  test_decoded_data  = codec.dna_to_b32(DNA,codec._default_b32_alphabet,codec._default_b32_alphabet_alt) 
  print(test_encoded_data.flatten())
  print( np.array(test_decoded_data).flatten())
  assert np.array_equal( test_encoded_data.flatten(), np.array(test_decoded_data).flatten() )


def test_dna_to_bN():
  base = 47
  length = 4 # length>= log4(2*base)
  allwords = list(product("ACTG", repeat=length))
  allwords = [''.join(w) for w in allwords]
  words = allwords[:base]
  altwords = allwords[base:(2*base)]
  data_seq = np.random.randint(0,base*2,(10,base-1))
  data = np.mod(data_seq,base)
  
  #"encode"
  lut = np.array(words+altwords)
  seqs = [lut[d] for d in data_seq]
  seqs = [''.join(seq) for seq in seqs]
  decode_data = np.array(codec.dna_to_bN(seqs,words,altwords))
  assert np.array_equal(data, decode_data)

def test_dna_to_bytes():
  _int_to_baseN = codec.codec._int_to_baseN

  #TODO: adapt to workwith not b32 too.
  #answer = [64, 79, 231, 126, 228, 124, 3]
  alphabet =codec._default_b32_alphabet
  alphabet_alt = codec._default_b32_alphabet_alt
  full_alphabet = np.array(alphabet + alphabet_alt)
  
  #generate some DNA
  _t = np.random.randint(0,2*len(alphabet),size=3*10)
  _t_dna = full_alphabet[_t]
  DNA = ''.join(_t_dna)  
  #DNA = "GCTCTTCCCACCACCATTGCCTTCTTCTTG"

  answer32 = codec.dna_to_bN([DNA],alphabet,alphabet_alt)[0]

  dna_bytes, mask = codec.dna_to_bytes(DNA,alphabet,alphabet_alt)
  
  dna_baseN = _int_to_baseN(int.from_bytes(dna_bytes,"little"),len(alphabet))
  assert dna_baseN == answer32

  _t = np.array(dna_baseN)
  dna_baseN_with_alt = _t + len(alphabet)*np.array(mask)
  generated_dna = "".join(full_alphabet[dna_baseN_with_alt])
 
  assert generated_dna == DNA

def test_inserts():
  coder = codec.BaseNBlockCodec(inner_alphabet_size=32,inner_d=5,inner_n=29,n_strands=2000,n_redundant_strands=100)
  n_inserts = 200
  insert = "GCTCTTCCCACCACCATTGCCTTCTTCTTG"
  insert_bytes, imask = codec.dna_to_bytes(insert,codec._default_b32_alphabet,codec._default_b32_alphabet_alt)
  total_ibytes = len(insert_bytes)*n_inserts
  data_size = coder.block_capacity_bytes - total_ibytes 


  test_data = np.random.randint(0,255,data_size,dtype=np.uint8).tobytes()

  inserted_data = codec.insert_bytes(test_data,insert_bytes,coder.data_chunk_size,n_inserts)
  assert len(inserted_data)  == coder.block_capacity_bytes

  enc_d = coder.encode(inserted_data)
  data_decodec,__oe,__oer,__ie = coder.decode(enc_d)
  assert data_decodec == inserted_data

  test_dna_out = codec.b32_to_DNA_optimize(enc_d,codec._default_b32_alphabet,codec._default_b32_alphabet_alt,mask=imask,nmasked=n_inserts)
  test_dna = [x[0] for x in test_dna_out]
  for strand in test_dna[:n_inserts]:
    assert strand.decode().startswith(insert)

  assert codec.dna_to_bN(test_dna,codec._default_b32_alphabet,codec._default_b32_alphabet_alt) == enc_d
