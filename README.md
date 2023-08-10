# PhotoMosaic Maker

A [Photomosaic](https://en.wikipedia.org/wiki/Photographic_mosaic) generator written in python

![result](https://github.com/ReedGoldsworthy/Photomosaic-maker/assets/59662986/4dac3a66-eca9-48f1-866b-a5d1b569643a)


## Dependencies

This project uses two external python libraries: opencv-python and numpy.
These can be downloaded by entering pip install opencv-python in the terminal if pip is installed

## Usage

1). Add the image you want to turn into a mosaic into the project directory. Then change the variables _main_image_ and _photo_type_ to be the name and file type of your input image respectively. For example, using "input.jpg" as the main photo would have _main_image_ = "input" and _photo_type_ = ".jpg".

2). To add the sub-images that make up the mosaic, add a folder of images into the directory and change the variable _images_folder_ to be the name of your folder. The program currently uses a folder of folders of animal images called "animals", so _images_folder_ is currently set as "animals". In order to just use a folder of images, you will have to tweak the code in main.py.

3). In order to set the size of each sub-image in the mosaic, change the _TILE_HEIGHT_ and _TILE_WIDTH_ variables to the desired value.

4). Run main.py. This will create a json cache which stores a dictionary mapping rgb values from our folder of images to a list of strings representing image file paths with that rgb value. This saves us from having to compute these values every time we run our program. The program will then write the finished mosaic to "output.jpg".

&nbsp;

![result2](https://github.com/ReedGoldsworthy/Photomosaic-maker/assets/59662986/299616e7-5908-4f54-b892-029dce7e5c7a)
