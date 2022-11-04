# Image Stacker
*Image stacking* is a photography technique that combines multiple pictures (usually taken at different focuses) into one picture. The result is typically a higher quality photograph. This technique is often used to remove distortion or just to improve the overall quality of an image.

This is my implementation of an image stacker program in python. My program creates stacked images in the [ppm image format](https://netpbm.sourceforge.net/doc/ppm.html), specifically P3 ppm images because of how easy it is to write these images.

*Note: I will be implementing a method in the ImageConvert module to convert ppm's to more acessible image formats, like PNG or JPG. This will make the resultant, stacked images easier to distribute and won't require a special program to view.*

# ImageStacker.py
ImageStacker is a class that stacks a collection of PPM image files into one PPM file.
It extracts the RGB values from each pixel from each PPM image and sums, then averages the values.
Then, it writes the resulting pixel data to an output PPM file.

In order to stack typical image formats, like JPG's or PNG's, use the ImageConvert module.

# ImageConvert.py
ImageConvert is a module to assist with the ImageStacker class. It currently facilitates the conversion of typical image formats, like JPG or PNG, to the PPM(P3) file format, the format that [ImageStacker](./ImageStacker.py) uses. P3 is a version of the PPM that stores an RGB value for every pixel in an image, which is easy to use in the case of combining the pixel data from multiple images.

ImageConvert can be used by running: 
```
ImageConvert.convertToPpm(filename)
```

You can also specify the directory the file is in, output directory (where converted image should be saved), and an output name.

You can also convert an entire directory of images using:
```
ImageConvert.convertDir(targetDir)
```
