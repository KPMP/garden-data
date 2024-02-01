from tifffile import TiffWriter, imread
import pandas as pd
import os
import sys
from os.path import join

directory = "/home/zwright/Documents/KPMP/CODEX_2024/data"
if os.path.isdir(directory):

  channel_names = None
  img_path = None
  for filename in os.scandir(directory):
    extension = os.path.splitext(filename)[1]
    if extension == ".tif" or extension == ".tiff":
      img_path = join("raw", filename.path)
      output_path = join("processed", os.path.splitext(filename)[0] + ".ome" + extension)
    elif extension == ".csv" or extension == ".txt":
      channel_names_path = join("raw", filename.path)
      df = pd.read_csv(channel_names_path, sep=",")
      if 'Marker' in df:
          channel_names = df['Marker'].tolist()
      elif 'Label' in df:
          channel_names = df['Label'].tolist()
    else:
      print("Only .tiff and .txt files are supported.")
      sys.exit()

    if (img_path and channel_names_path):  
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