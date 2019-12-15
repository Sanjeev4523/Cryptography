   --------------SANJEEV SINGLA -------------------
   --------------2017A7PS0152P --------------------

   Problem Statement :
   S-DES is a reduced version of the DES algorithm. It has similar properties to DES but deals with a much smaller block and key size (operates on 8-bit message blocks with a 10-bit key). It has 2 rounds. The 10-bit key is used to generate 2 different blocks of 8-bit subkeys where each block is used in a particular iteration. For your reference, you can take help from the given link  https://eprint.iacr.org/2002/045.pdf.

	Objective: You need to perform differential cryptanalysis on Simplified S-Box. Your goal is to extract the main key, round1 subkey, and round2 subkey.
	Submission:  You need to submit  Encryption code, Decryption code differential cryptanalysis crack code along with the necessary auxiliary files and finally in the form of a single Zip file. Your crack code should print main key, round1 subkey and round2 subkey.

	Note: Your encryption code should prompt for entering the key. Plaintext should be taken from a file.

	
   There are 3 .c files in the folder:
   	(1) encrypt.c
   		This is the encryption file . 
   		run -> encrypt (executable)
   		Inputs:
   			Key : User Prompt
   			Plaintext : file already in the Folder called 'plaintext.c'
   		Output:
   			Ciphertext : In the file 'ciphertext.txt'

   	(2) decrypt.c
   		This is the decryption file . 
   		run -> decrypt (executable)
   		Inputs:
   			Key : User Prompt
   			Ciphertext : file already in the Folder called 'ciphertext.c'
   		Output:
   			Plaintext : In the file 'plaintext.txt'

   	(3) crack.c
   		This is the crack
   		Inputs:
   			Key : User Promt
   			( For generating Chosen Plaintext - Ciphertext Pairs )
   			Output :
   			Differential Tables
   			Key frequencies
   			Guessed Subkey
   			



