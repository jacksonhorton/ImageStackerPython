# ImageConvert.py
'''
The Image convert class contains functionality
to convert an image to a ppm file format (Only
tested with png's and jpg's). Intended to be used
in conjunction with the ImageStacker class; converts
regular images into a format that ImageStacker can use.

The format parameter is whatever is after the '.'
in the extension, so if the file(s) is called
'image.png', the format is just 'png'.

Target dir is where a file is located, or the path
to that directory, default is the local directory ./

Output dir is the path/folder the resultant images
will be outputted to. Default for convert() is local
dir(./) and for convertDir() is './out/', so a local
folder named 'out'
'''
#!TODO make the convert function dual-functional: jpg->ppm and ppm->jpg
from PIL import Image
from numpy import array
import glob, os
from dataclasses import dataclass

@dataclass
class image_data:
    filename : str
    img : array
    width : int
    height : int

# returns a directory with the output images
def convertDir(targetDir, targetFormat='JPG', outputDir='out', outputName: str = None) -> str:
    # gets all files in dir that matches the given (or defaultm 'JPG') format
    files = glob.glob(os.path.join(targetDir, f'*.{targetFormat}'))
    # converts each file in dir
    for i, file in enumerate(files):
        file = os.path.split(file)[1] # gets rid of target directory in filename/path
        print( convert(file, targetDir=targetDir, outputDir=outputDir, imageNum=i+1, outputName=outputName) )
    
    return os.path.join(outputDir)



def convert(file: str, targetDir='', outputDir='', imageNum: int = None, outputName: str = None) -> str:
    files = glob.glob(os.path.join(targetDir, file))
    for file in files:
        # creates preImage, which is PIL's image
        filename = os.path.splitext(file)[0]
        filename = os.path.split(filename)[1]
        # if output name is given, use it
        if outputName is not None:
            filename = outputName
        # if image numbers are give format filename accordingly
        if imageNum is not None:
            filename = f'{filename}_{imageNum:0>3}'# like 'filename_001'
        preImage = Image.open(file)
        
        # converts image data to 2d array of pixels with rgb values
        pixels = array(preImage)
        preImage.close()
        # gets width and height based on size of 2d array
        width = len(pixels[0])
        height = len(pixels)
        # print(f'{width=} {height=}')
        
        # passes all image information to write function
        imageDataObject = image_data(filename, pixels, width, height)
        __writeImageData(imageDataObject, outputDir=outputDir)
        
        
        return os.path.join(outputDir, filename + '.ppm')
        
        
        
        
def __writeImageData(imageDataObject: image_data, outputDir='') -> None:
    # makes sure outputDir exists if used
    if outputDir != '' and not os.path.isdir(outputDir):
        os.makedirs(outputDir)
    
    # writes pixels to the output file
    path = os.path.join(outputDir, imageDataObject.filename + '.ppm')
    with open(path, 'w') as out:
        # writes header
        out.write('P3\n')
        out.write(f'{imageDataObject.width} {imageDataObject.height}\n')
        out.write('255\n')
        # writes body (pixels)
        for row in imageDataObject.img:
            for column in row:
                out.write(
                    f'{column[0]} {column[1]} {column[2]}\n')



if __name__ == "__main__":
    # convert('ss.png')
    # convert('IMG_8072.JPG')
    convertDir('./test', 'png')
