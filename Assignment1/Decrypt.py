#!/usr/bin/env python



###  Call syntax:
###
###      Decrypt.py  encryptedFile.txt  DecryptedFile.txt
###
###  The Decrypted output is deposited in the file `DecryptedFile.txt'

import sys
from BitVector import *   
import binascii                                             #(A)

if len(sys.argv) is not 3:                                                    #(B)
    sys.exit('''Needs two command-line arguments, one for '''
             '''the message file and the other for the '''
             '''encrypted output file''')

PassPhrase = "I want to learn cryptograph and network security"    
#PassPhrase = "Sanjeev SIngla is great"                        #(C)

BLOCKSIZE = 64                                                                #(D)
numbytes = BLOCKSIZE // 8                                                     #(E)

# Reduce the passphrase to a bit array of size BLOCKSIZE:
bv_iv = BitVector(bitlist = [0]*BLOCKSIZE)                                    #(F)
for i in range(0,len(PassPhrase) // numbytes):                                #(G)
    textstr = PassPhrase[i*numbytes:(i+1)*numbytes]                           #(H)
    bv_iv ^= BitVector( textstring = textstr )                                #(I)

# Get key from user:
key = None
if sys.version_info[0] == 3:                                                  #(J)
    key = input("\nEnter key: ")                                              #(K)
else:                                                                         
    key = raw_input("\nEnter key: ")                                          #(L)
key = key.strip()                                                             #(M)

# Reduce the key to a bit array of size BLOCKSIZE:
key_bv = BitVector(bitlist = [0]*BLOCKSIZE)                                   #(N)
for i in range(0,len(key) // numbytes):                                       #(O)
    keyblock = key[i*numbytes:(i+1)*numbytes]                                 #(P)
    key_bv ^= BitVector( textstring = keyblock )                              #(Q)

# Create a bitvector for storing the ciphertext bit array:
msg_decrypted_bv = BitVector( size = 0 )                                      #(R)

f = open(sys.argv[1])
encrypted_msg = f.read()
f.close()
bv_encrypted = BitVector(hexstring=encrypted_msg)
previous_block = bv_iv   
#print(len(bv_encrypted))
while i<len(bv_encrypted):
    if i+BLOCKSIZE<=len(bv_encrypted):
        #print("if:",i+BLOCKSIZE)
        bv_read = bv_encrypted[i:i+BLOCKSIZE]
    else:
        bv_read = bv_encrypted[i:len(bv_encrypted)]
        #print("else:",len(bv_read))
        bv_read += BitVector(size = (BLOCKSIZE - len(bv_read)))     
    new_prev_block = bv_read.deep_copy()
    bv_read ^= key_bv
    bv_read ^= previous_block
    previous_block = new_prev_block.deep_copy()
    msg_decrypted_bv += bv_read
    i = i +  BLOCKSIZE

#outputstr = msg_decrypted_bv.get_bitvector_in_ascii()
outputstr = str(msg_decrypted_bv)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

outputstr = text_from_bits(outputstr)
FILEOUT = open(sys.argv[2],'w')
FILEOUT.write(outputstr)
FILEOUT.close()

        

    
    


                                                       #(f)
