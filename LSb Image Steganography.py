# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 18:50:36 2021

@author: Abhishek Maurya
"""

import numpy as np
from PIL import Image

def Encode(src, message, dest):

    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
        m = 0
    elif img.mode == 'RGBA':
        n = 4
        m = 1

    total_pixels = array.size//n

    message += "$stegano"
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)

    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")

    else:
        index=0
        for p in range(total_pixels):
            for q in range(m, n):
                if index < req_pixels:
                    array[p][q] = int(bin(array[p][q])[2:9] + b_message[index], 2)
                    index += 1

        array=array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest)
        print("Image Encoding Successful")


def Decode(src):

    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
        m = 0
    elif img.mode == 'RGBA':
        n = 4
        m = 1

    total_pixels = array.size//n

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(m, n):
            hidden_bits += (bin(array[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

    message = ""
    for i in range(len(hidden_bits)):
        if message[-8:] == "$stegano":
            break
        else:
            message += chr(int(hidden_bits[i], 2))
            
    if "$stegano" in message:
        print("Hidden Message:", message[:-8])
    else:
        print("No Hidden Message Found")
        

def LSB_Steganography():
    print("--Welcome to $steganography$--")
    print("Enter 1 for Encoding purpose.")
    print("For Decoding enter 2.")

    opt = input()

    if opt == '1':
        print("Enter Source Image Path")
        src = input()
        print("Enter Message to Hide")
        message = input()
        print("Enter Destination Image Path")
        dest = input()
        print("Encoding...")
        Encode(src, message, dest)

    elif opt == '2':
        print("Enter Source Image Path") #Encoded destination path to be enter
        src = input()
        print("Decoding...")
        Decode(src)

    else:
        print("ERROR : Invalid option chosen")
        
LSB_Steganography()
