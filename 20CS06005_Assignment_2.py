# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 19:28:47 2021

@author: Abhishek Maurya
"""
###-------------------------------Encyption-------------------------------------###

# Use wave package to read and write .wav audio file
import wave

# read wave audio file
song = wave.open("cover_audio.wav", 'rb')

# Read frames and convert to byte array
frame_bytes = bytearray(list(song.readframes(song.getnframes())))

# The "secret" text message
a="I wonder, after listening many great love stories of the word"
b=", what could be the greatest thing a lover can do for his/her partner?"
c=" Build a freaking bridge over ocean? Such was the love of Lord Ram for Mata Sita,"
d=" which no ocean, no ten headed Ravan, no million strength armies was able to bound."
e=" I certainly believe that if there is any true monument of love, then it is Ram Setu."
message=a+b+c+d+e
message=message*1000
n=len(message)*8
print(n//8) 
#print(len(frame_bytes))

# Convert text to bit array
bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in message])))

# Replace LSB of each byte of the audio data by one bit from the text bit array
for i, bit in enumerate(bits):
    frame_bytes[i] = (frame_bytes[i] & 254) | bit
    
# Get modified bytes
frame_modified = bytes(frame_bytes)

# Write bytes to a new wave audio file
with wave.open('Encrypted_song.wav', 'wb') as fd:
    fd.setparams(song.getparams())
    fd.writeframes(frame_modified)
song.close()
print("\nEncrytion Successful.\n")

###--------------------------------Decryption-----------------------------------###

song = wave.open("Encrypted_song.wav", mode='rb')
# Convert audio to byte array
frame_bytes = bytearray(list(song.readframes(song.getnframes())))

# Extracting the LSB of each byte
frame_bytes=frame_bytes[:n]
extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]

# Decrypt byte array to string
decoded_string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))


# Print the encrypted message
print("Sucessfully decoded:\n\n"+decoded_string)
song.close()