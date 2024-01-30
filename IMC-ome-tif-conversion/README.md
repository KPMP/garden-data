# tiff-to-ome-tiff conversion for IMC images

## How does this work
This uses a _summary.txt file provided to us from IMC to convert their tiff image to a .ome.tif image that vitessce can understand.
Currently this script cannot determine which text file goes with each .ome.tif image. This will require another look in the future, but for now this is what we have
So to convert the image in a way that is functional for vitessce, the directory tree should look like this:

### /folder/with/images
* Sample1
  * Sample1-image-to-convert.tiff
  * Sample1-image-to-convert_summary.txt

* Sample2
  * Sample2-image-to-convert.tiff
  * Sample2-image-convert_summary.txt

## Usage
Install the packages in the requirements.txt file
`pip3 install -r requirements.txt`

Currently this takes in two files.
1. txt file with the channel names and the like
2. tif file from IMC
 There is a directory variable that should be modified to point at the direcotry where the .txt and .tif files are located

`python3 tiff-to-ome-tiff.py -d /path/to/directory`