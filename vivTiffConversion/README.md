# Processing tiff to ome-tiff
[This documentation](http://viv.gehlenborglab.org/#data-preparation) describes the process for installing the necessary tools to do the conversion of a tiff into an ome-tiff that Vitessce can use.

Note: There is a section mentioning converting to the zarr format, however the bioformats2raw doesn't support the --file_type parameter any longer. It says it automatically generates a zarr format, however, when following the Pyramid Generation portion of the instructions, I did not see a zarr file generated.

All in all, we will need conda installed, as well as bioformats2raw, ome and raw2ometiff (all covered in the instructions linked).

Strangely, it seems that the image size is reduced through this process. The input file I used was 25G and the outputs were less than 10G total (there are two steps, one to tile the image and the other to generate the ome tiff). We could likely remove the intermediate files generated after we have the ome.tiff.
