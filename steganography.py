"""A program that encodes and decodes hidden messages in images through LSB steganography"""
from PIL import Image, ImageFont, ImageDraw
import textwrap

def decode_image(file_location="images/encoded_sample.png"):
    """Decodes the hidden message in an image

    file_location: the location of the image file to decode. By default is the provided encoded image in the images folder
    """
    encoded_image = Image.open(file_location)
    full_read = encoded_image.load()
    red_channel = encoded_image.split()[0]
    red_read = red_channel.load()

    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]

    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()

    """Ok, so what I to do is get the values for each pixel, take the red value and extract the LSB, then 
    store it in the new picture"""

    for x in range(x_size):
        for y in range(y_size):
            red_bin_val = bin(red_read[x,y])
            LSB = red_bin_val[-1]
            if LSB == '0':
                pixels[x,y] = (0,0,0)
            else:
                pixels[x,y] = (255,255,255)




    decoded_image.save("images/decoded_image2.png")

def write_text(text_to_write, image_size):
    """Writes text to an RGB image. Automatically line wraps

    text_to_write: the text to write to the image
    image_size: size of the resulting text image. Is a tuple (x_size, y_size)
    """
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    #Text wrapping. Change parameters for different text formatting
    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin,offset), line, font=font)
        offset += 10
    return image_text

def encode_image(text_to_encode, template_image="images/samoyed.jpg"):
    """Encodes a text message into an image

    text_to_encode: the text to encode into the template image
    template_image: the image to use for encoding. An image is provided by default.
    """
    image_to_encode = Image.open("images/Shakespeare.png")
    image_read = image_to_encode.load()

    x_size = image_to_encode.size[0]
    y_size = image_to_encode.size[1]

    written_text = write_text(text_to_encode, (x_size,y_size))
    read = written_text.load()



    coded_image = Image.new("RGB", (x_size,y_size))
    pixel_new_image = coded_image.load()
    
    for x in range(x_size):
        for y in range(y_size):
            text = read[x,y]
            LSB = bin(text[0])
            to_change_end = bin(image_read[x,y][0])# = LSB[-1]
            to_change = to_change_end[:-1] + str(LSB[-1])
            int_to_change = int(to_change,2)
            pixel_new_image[x,y] = (int_to_change,image_read[x,y][1],image_read[x,y][2])
            #to_change
            #decoded_image.save("images/coded_image.png")
            # LSB = red_bin_val[-1]
            # if LSB == '0':
            #     pixels[x,y] = (0,0,0)
            # else:
     
            #     pixels[x,y] = (255,255,255)


    coded_image.save("images/coded_image.png")


if __name__ == '__main__':
    print("Decoding the image...")
    decode_image("images/coded_image.png")

    #print("Encoding the image...")
    encode_image('Be not afraid of greatness: some are born great, some achieve greatness, and some have greatness thrust upon them.')
