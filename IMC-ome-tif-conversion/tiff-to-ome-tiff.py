from tifffile import TiffWriter, imread
import pandas as pd
import os
import sys
import argparse
from os.path import join

parser = argparse.ArgumentParser()
parser.add_argument(
  "-d",
  "--dir",
  required=True,
  help="The directory where the .tiff and .txt file you want to convert are located"
)
args = parser.parse_args()
if os.path.isdir(args.dir):

  channel_names = None
  directory = args.dir
  for filename in os.scandir(directory):
    extension = os.path.splitext(filename)[1]
    if extension == ".tiff":
      img_path = join("raw", filename.path)
      output_path = join("processed", os.path.splitext(filename)[0] + ".ome" + extension)
    elif extension == ".txt":
      channel_names_path = join("raw", filename.path)
      df = pd.read_csv(channel_names_path, sep="\t")
      channel_names = df['Label'].tolist()
    else:
      print("Only .tiff and .txt files are supported.")
      sys.exit()
    img_arr = imread(img_path)
    img_arr.shape
    img_arr.dtype
    
    tiff_writer = TiffWriter(output_path, ome=True)
    tiff_writer.write(
      img_arr,
      metadata={
          'axes': "CYX",
          'Channel': {'Name': channel_names},
      }
    )
    tiff_writer.close()
    
else:
  print('Directory is not valid')
  sys.exit()