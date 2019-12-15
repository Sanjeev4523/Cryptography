'''
This required pallier python library
Install Instructions : pip install phe
'''
# imports
from phe import paillier
# generating keys
public_key, private_key = paillier.generate_paillier_keypair()
keyring = paillier.PaillierPrivateKeyring()
keyring.add(private_key)
public_key1, private_key1 = paillier.generate_paillier_keypair(keyring)
public_key2, private_key2 = paillier.generate_paillier_keypair(keyring)

# print(public_key)
# print(public_key1)
# print(private_key1)
print('''
This examples takes the 10 day period Blood Pressure level of the patient
in an encrypted form amd then returns the Mean Blood pressure to the doctor
 ''')

bp = [80,81,82,83,84,85,96,87,98,69,80]

# encrypting blood pressure
encrypted_bp = [public_key.encrypt(x) for x in bp]
f = open("encrypted_bp.txt","w+")



# writing encrypted blooad presure to the file
for i in range(0,len(encrypted_bp)):
    f.write(str(encrypted_bp[i].ciphertext()))
    

sum  = encrypted_bp[0]
 # adding encypted values
for i in range(1,len(encrypted_bp)):
    sum += encrypted_bp[i]
    
# dividing encrypted values
mean_enc = sum / len(encrypted_bp)
mean =  private_key.decrypt(mean_enc)

print("Mean Blood Pressure")
print("encrypted : decrypted")
print(f"{mean_enc.ciphertext()}:{mean}")

print("The blood pressure's and corresponding encrpted values are stored in the file encyptedbp.txt for reference")
f.close()

