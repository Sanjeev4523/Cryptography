from BitVector import *
import binascii
import sys
### Steps to run
### Call Encrypt.py adversary.txt adv_cipher.txt
### This step has to be done Differentially in order for code to work

#f = open('','r')
# call Encrypt.py input.txt output.txt

print('''
 Steps to run
 Call Encrypt.py adversary.txt adv_cipher.txt
''')
PassPhrase = "I want to learn cryptograph and network security"                            #(C)

BLOCKSIZE = 64                                                               #(D)
numbytes = BLOCKSIZE // 8                                                     #(E)

# Reduce the passphrase to a bit array of size BLOCKSIZE:
bv_iv = BitVector(bitlist = [0]*BLOCKSIZE)                                    #(F)
for i in range(0,len(PassPhrase) // numbytes):                                #(G)
    textstr = PassPhrase[i*numbytes:(i+1)*numbytes]                           #(H)
    bv_iv += BitVector( textstring = textstr ) 
bv_key = BitVector(size=0)

encrypted = open('adversary.txt','r')
msg_encrypted_bv = BitVector( textstring=encrypted.read() )    
encrypted.close()
decrypted = open('adv_cipher.txt','r')  
msg_decrypted_bv = BitVector(hexstring=decrypted.read())       
decrypted.close()
                         #(R)
#print(len(msg_decrypted_bv)==len(msg_encrypted_bv))
# Carry out differential XORing of bit blocks and encryption:
previous_block = bv_iv          
i=0
j=1
while i<len(msg_encrypted_bv):
    if j==-1:
        break;
    if i+BLOCKSIZE<=len(msg_decrypted_bv):
        #print("if:",i+BLOCKSIZE)
        bv_e_read = msg_encrypted_bv[i:i+BLOCKSIZE]
        bv_d_read = msg_decrypted_bv[i:i+BLOCKSIZE]
    else:
        bv_e_read = msg_encrypted_bv[i:len(msg_encrypted_bv)]
        bv_d_read = msg_decrypted_bv[i:len(msg_decrypted_bv)]
        #print("else:",len(bv_read))
        bv_e_read += BitVector(size = (BLOCKSIZE - len(bv_e_read)))     
        bv_d_read += BitVector(size = (BLOCKSIZE - len(bv_d_read)))   
    new_prev_block = bv_d_read.deep_copy()
    bv_key = bv_d_read^bv_e_read^previous_block
    # bv_read ^= key_bv
    # bv_read ^= previous_block
    previous_block = new_prev_block.deep_copy()
    # msg_decrypted_bv += bv_read
    # print(bv_key)
    # print(bv_key.get_text_from_bitvector())
    i = i +  BLOCKSIZE
    j=j-1


msg_decrypted_bv1 = BitVector( size = 0 )                                      #(R)

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
    bv_read ^= bv_key
    bv_read ^= previous_block
    previous_block = new_prev_block.deep_copy()
    msg_decrypted_bv1 += bv_read
    i = i +  BLOCKSIZE

#outputstr = msg_decrypted_bv.get_bitvector_in_ascii()
outputstr = str(msg_decrypted_bv1)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

outputstr = text_from_bits(outputstr)
FILEOUT = open('recoverytext.txt','w')
FILEOUT.write(outputstr)
FILEOUT.close()


