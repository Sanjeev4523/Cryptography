'''
This required pallier python library
Install Instructions : pip install phe
                        pip install pycryptodome
'''
# imports 
from phe import paillier
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

# key generation
public_key, private_key = paillier.generate_paillier_keypair()
keyring = paillier.PaillierPrivateKeyring()
keyring.add(private_key)
public_key1, private_key1 = paillier.generate_paillier_keypair(keyring)
public_key2, private_key2 = paillier.generate_paillier_keypair(keyring)


# key for nonPID data
password = "crypto"

# PID -> data which doesnt need to be preprocesses

def nonPID_encrypt(key, source, encode=True):
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = Random.new().read(AES.block_size)  # generate IV
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
    source += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
    data = IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
    return base64.b64encode(data).decode("latin-1") if encode else data

def nonPID_decrypt(key, source, decode=True):
    if decode:
        source = base64.b64decode(source.encode("latin-1"))
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = source[:AES.block_size]  # extract the IV from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])  # decrypt
    padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
    if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
        raise ValueError("Invalid padding...")
    return data[:-padding]  # remove the padding


print('''
This examples takes the normal patient form and encrypts the data 
 ''')

# digital copy of the physical from filled at visit
# firstName:
# lastName:
# age:
# height:
# bloodPressure:

class PatientForm:
    def __init__(self,firstName, lastName , age , height, bloodPressure):
        self.firstName = firstName
        self.lastName = lastName
        self.age = age
        self.height = height
        self.bloodPressure = bloodPressure
    
    def encrypt_data(self,public_key):
        self.encrypted_data = {
            "firstname": str(nonPID_encrypt(bytes(password,'utf-8'),bytes(self.firstName,'utf-8'))),
            "lastname": str(nonPID_encrypt(bytes(password,'utf-8'),bytes(self.lastName,'utf-8'))),
            "age": str(public_key.encrypt(self.age).ciphertext()),
            "height": str(public_key.encrypt(self.height).ciphertext()),
            "bloodPressure": str(public_key.encrypt(self.bloodPressure).ciphertext())
        }
    
# creating an instance of the patient

print("Please enter the required Details: \n")
fn = input("Please Enter your firstname: \n")
ln = input("Please Enter your lastname: \n")
a = int(input("Please Enter your age: \n"))
h = int(input("Please Enter your height(in cm): \n"))
bp = int(input("Please Enter your Blood Pressure (Distolic): \n"))




patient1 = PatientForm(fn,ln,a,h,bp)
patient1.encrypt_data(public_key)

f = open("formdata.txt","w+")
# print("The Encrypted Data :")
# print(patient1.encrypt_data)


f.write(str(patient1.encrypted_data))
# for x in patient1.encrypt_data:
#     f.write(x)
print("Encypted Data is available in the file formdata.txt")
f.close()


