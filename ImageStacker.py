# ImageStacker.py
'''
ImageStacker is a class that can take a selection
of ppm files/images and combine them and average
their values (an image stack), then output a
file with the stacked values.

The constructor takes a filename, which corresponds
to the 'root name' of the ppms; the ppms's root is
proceeded by an index from 1-999 or 1-XXX. By default
the foler they have to be located in is ./ppms/...
For example:
    './ppms/filename_001.ppm'
    './ppms/filename_002.ppm'
    ...
All of these can be tweaked in the constructor to
fit your use case.
'''
from dataclasses import dataclass
from os import path
from math import floor


class ImageStacker:

    # _pixel and _ppm_struct act like C-structs
    @dataclass
    class _pixel:
        r : int = 0
        g : int = 0
        b : int = 0
        
    @dataclass
    class _ppm_struct:
        magic_num : str = ''
        width : int = 0
        height : int = 0
        rgb_max : int = 0
        

    def __init__(self, filename: str, numOfImages: int, ppmFolderPath='ppms/', avg_num: int = None, out_path='out.ppm') -> None:
        # defines member variables
        self.filename = filename
        self.numOfImages = numOfImages
        self.ppmFolderPath = ppmFolderPath
        self.avg_num = avg_num
        self.out_path = out_path
        
        # creates a list of pixels
        self._pixels = []
        
        
    def __getPpm(self) -> _ppm_struct:
        # reads header from first ppm file to get ppm settings
        ppm = self._ppm_struct()
        with open(self.__getFilepath(self.filename, 1), 'r') as file:
            # reads first line: magic number only
            ppm.magic_num = file.readline().rstrip('\n')
            # reads second line: width height; converts both to int
            ppm.width, ppm.height = (int(n) for n in file.readline().rstrip('\n').split(' '))
            # third line: rgb max value only
            ppm.rgb_max = file.readline().rstrip('\n')
            #print(repr(ppm))
            
        for _ in range(ppm.width * ppm.height):
            temp = self._pixel()
            self._pixels.append(temp)
        return ppm
    
    def __readImage(self, fileNum) -> None:
        
        with open(self.__getFilepath(self.filename, fileNum)) as img:
            # clears header info
            img.readline()
            img.readline()
            img.readline()
            
            # read image by incrementing rgb values in each pixel
            for pixel in self._pixels:
                # converts strings of rgb values to three ints r, g, b
                r, g, b = (int(n) for n in img.readline().rstrip('\n').split(' '))
                pixel.r += r
                pixel.g += g
                pixel.b += b
            # print(self._pixels[0:10])
            
        
    def __getFilepath(self, name, fileNum) -> str:
        #filepath is the name of a specific .ppm file
        filepath = f'{name}_{fileNum:0>3}.ppm'
        # returns the complete file path (including folders)
        return path.join(self.ppmFolderPath, filepath)
    

    def __average(self) -> None:
        # if an avg_num was defined in the constructor, use it
        # else, just use the num of images to divide by.
        if avg_val := self.avg_num or self.numOfImages:
            # averages every rgb value in each pixel
            for pixel in self._pixels:
                pixel.r = floor(pixel.r / avg_val) 
                pixel.g = floor(pixel.g / avg_val)
                pixel.b = floor(pixel.b / avg_val)
            
            
    def __writePpm(self) -> None:
        # opens file to write ppm to
        with open(self.out_path, 'w') as out:
            # writes header
            out.write(self.ppm.magic_num + '\n')
            out.write(f'{self.ppm.width} {self.ppm.height}\n')
            out.write(self.ppm.rgb_max + '\n')
            # writes body (pixels)
            for pixel in self._pixels:
                out.write(f'{pixel.r} {pixel.g} {pixel.b}\n')


    def stack(self) -> None:
        # stack() performs the stack
        # gets ppm header info
        self.ppm = self.__getPpm()
        
        # reads in all images
        for i in range(1, self.numOfImages+1):
            self.__readImage(i)

        # calls average function to average every pixel's value
        self.__average()
        # write to file
        self.__writePpm()
