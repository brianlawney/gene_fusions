import tarfile
import filesystem_utils
import os
from Constants import Constants

def unpack_all(file_list, output_directory='.'):
  """
  @Summary: unpacks compressed directories/files
  @Parameter file_list: a set of absolute file paths
  @Parameter output_directory: a path to a desired output directory
  """
  
  #progress through the list of compressed files and unzip to the desired directory
  for file in file_list:
    if file.endswith(Constants.TAR_GZ):
      tf=tarfile.open(str(file),'r:gz')
      tf.extractall(output_directory)
      