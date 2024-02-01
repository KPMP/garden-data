# tiff-to-ome-tiff Conversion for IMC Images

## How This Script Works
This script uses a provided _summary.txt file and converts a normal IMC tiff image to an -ome.tif image for use in Vitessce.
Currently this script does not determine which text file goes with each -ome.tif image.

The directory structure should look like this:

### /folder/with/images
* Sample1
  * Sample1-image-to-convert.tiff
  * Sample1-image-to-convert_summary.txt

* Sample2
  * Sample2-image-to-convert.tiff
  * Sample2-image-convert_summary.txt

## Usage
Currently this script takes in two files:
1. a .txt file with the channel names
2. a .tif file from IMC

There is a directory variable that should be modified to point at the directory where the .txt and .tif files are located.
`python3 tiff-to-ome-tiff.py -d /path/to/Sample1`