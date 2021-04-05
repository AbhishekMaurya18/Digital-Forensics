"""
Created on Tue Mar 23 12:41:01 2021

@author: Abhishek Maurya
"""
#--------Python library and module invocation

import numpy as np
import pywt
from PIL import Image
from scipy import fft
 

image = 'Jai_Mahakal.jpg'        #----original image
watermark = 'shivling.jpg'       #----watermarked image


#--------convert image to Gray Scale image

def convert_image(image_name, size):
    img = Image.open('C:\\Users\\DELL\\Downloads\\' + image_name).resize((size, size), 1)
    img = img.convert('L')
    img.save(image_name)
    img.show(title=image_name)

    image_array = np.array(img.getdata(), dtype=np.float).reshape((size, size))             

    return image_array



#--------DCT image coefficient processing usint pywt library

def process_coefficients(array, model, level):
    coeffs=pywt.wavedec2(data = array, wavelet = model, level = level)
    coeffs_H=list(coeffs) 
   
    return coeffs_H

           
#--------embed original image with watermark image 

def embed_watermark(watermark, origin):
    watermark_flat = watermark.ravel()  #convert watermark image 2-D array to flat 1-D array
    ind = 0
    n=len(origin)
    for x in range (0,n,8):
        for y in range (0,n,8):
            if ind < len(watermark_flat):
                subdct = origin[x:x+8, y:y+8]
                subdct[5][5] = watermark_flat[ind]
                origin[x:x+8, y:y+8] = subdct
                ind += 1 


    return origin
      

#--------Apply Descrete Cosine Transform

def DCT(image_array):
    size =len(image_array[0])
    total_dct = np.empty((size, size))
    for i in range (0, size, 8):
        for j in range (0, size, 8):
            subpixels = image_array[i:i+8, j:j+8]
            subdct = fft.dct(fft.dct(subpixels.T, norm="ortho").T, norm="ortho")
            total_dct[i:i+8, j:j+8] = subdct

    return total_dct



#--------Apply Inverse Descrete Cosine Transform

def inverse_DCT(total_dct):
    size =len(total_dct[0])
    total_idct = np.empty((size, size))
    for i in range (0, size, 8):
        for j in range (0, size, 8):
            subidct = fft.idct(fft.idct(total_dct[i:i+8, j:j+8].T, norm="ortho").T, norm="ortho")
            total_idct[i:i+8, j:j+8] = subidct

    return total_idct



#---------Get watermarked image

def get_watermark(dct_watermarked_coeff, size):
    
    marks = []                     #list to hold watermark subsets
    n=len(dct_watermarked_coeff)
    for x in range (0,n,8):
        for y in range (0,n,8):
            coeff_slice = dct_watermarked_coeff[x:x+8, y:y+8]
            marks.append(coeff_slice[5][5])

    watermark = np.array(marks).reshape(size, size)

    return watermark



#----------recover watermarked image


def recover_watermark(image_array, model, level):
    coeffs_watermarked_image = process_coefficients(image_array, model, level=level)
    dct_watermarked_coeff = DCT(coeffs_watermarked_image[0])
    
    watermark_array = get_watermark(dct_watermarked_coeff, 128).astype('uint8')

    #Save result
    img = Image.fromarray(watermark_array)
    img.save('recovered watermark.jpg')
    img.show(title='recovered image from watermark')



#--------Calculating PSNR value using numpy

def  PSNR(src, dst):
	mse = np.mean((dst - src)**2); print("\n\nMean Square Error is : ",'%.3f'%mse)

	psnr=10*np.log10(255.0**2/mse)
    
	return psnr



#--------Driver Method to execute DCT watermarking

def DCT_Watermarking():
    image_array = convert_image(image, 2048)
    watermark_array = convert_image(watermark, 128)

    coeffs_image = process_coefficients(image_array, 'haar', level=1)
    
    dct_array = DCT(coeffs_image[0])
    dct_array = embed_watermark(watermark_array, dct_array)
    coeffs_image[0] = inverse_DCT(dct_array)


    #----reconstruction
    image_H=pywt.waverec2(coeffs_image, 'haar')
    image_copy=image_H.clip(0,255).astype("uint8")
    dest=Image.fromarray(image_copy)
    dest.save('image with watermark.jpg')
    dest.show(title='image with watermark')

    print("\nPeak Signal-to-Noise Ratio (PSNR) value is : ",'%.3f'%(PSNR(image_array,dest)))


    #----recover watermark image
    recover_watermark(image_array = image_H, model='haar', level = 1)




DCT_Watermarking()

