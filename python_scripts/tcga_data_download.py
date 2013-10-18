import tcga_download_utils as tdu
import tcga_constants
import datetime
import time
import os
import sys
import config
import subprocess

def format_url(cohort):
  """
  Create a properly formatted url for downloading data from the NCI
  """
  base_url=r"https://tcga-data.nci.nih.gov/tcga/damws/jobprocess/xml?"
  centers=tdu.create_csv_string(tcga_constants.CENTERS)
  platforms=tdu.create_csv_string(tcga_constants.PLATFORMS)
  
  disease_param=r'&disease='+str(cohort)
  center_param=r'&center='+str(centers)
  platform_param=r'&platform='+str(platforms)
  level_param=r'&level=3' #level 3 data
  url=str(base_url)+str(disease_param)+str(center_param)+str(platform_param)+str(level_param)

  if cohort=='LUAD':
    temp_param='&sampleList=TCGA-67-6216-*,TCGA-35-3615-*'
  if cohort=='LUSC':
    temp_param='&sampleList=TCGA-21-1077-*,TCGA-21-1078-*'

  url+=str(temp_param)
  print str(url)
  return url

def get_data(output_data_directory):
  """
  Downloads the TCGA data (a number of tar.gz's) and places them in the specified directorys
  """

  cohorts=['LUAD', 'LUSC']

  for cohort in cohorts:
    #create a directory for this cohort:
    cohort_specific_directory=os.path.join(output_data_directory, cohort)
    if not os.path.isdir(cohort_specific_directory):
      os.makedirs(cohort_specific_directory)
    url=format_url(cohort)
    response_xml=tdu.generate_request(url)
    status_check_url=tdu.get_element_value(response_xml, 'status-check-url')
    #wait for the archive to be built
    #check if it is done:
    while True:
      #sleep
      time.sleep(10)
      status_check_xml=tdu.generate_request(status_check_url)   
      status_code=tdu.get_element_value(status_check_xml, 'status-code')
      status_message=tdu.get_element_value(status_check_xml, 'status-message')
      if status_code=='200' and status_message=='OK':
        print 'completed'
        break
    archive_url=tdu.get_element_value(status_check_xml, 'archive-url')
    file_name=tdu.download_archive(archive_url, cohort_specific_directory)


def merge_all_output(cohort_directory): 
  files=tdu.get_file_list(tcga_constants.MAPPED_FILE_SUFFIX, cohort_directory)
  with open(os.path.join(cohort_directory, tcga_constants.MERGED_FILE),'w') as merged_file:
    for f in files:
      with open(f,'r') as inputfile:
        for line in inputfile:
          merged_file.write(line)
     
def remove_excess_files(cohort_directory): 
  files=tdu.get_file_list(tcga_constants.MAPPED_FILE_SUFFIX, cohort_directory)
  with open(os.path.join(cohort_directory, tcga_constants.MERGED_FILE),'w') as merged_file:
    for f in files:
      with open(f,'r') as inputfile:
        for line in inputfile:
          merged_file.write(line)


if __name__=='__main__':
  
  if len(sys.argv)==2:
    
    #create the directory to place the downloads into
    output_data_directory=sys.argv[1]
    FORMAT='%Y%m%d%H%M%S'
    new_directory_path=os.path.join(output_data_directory,'tcga_data_'+datetime.datetime.now().strftime(FORMAT))
    if not os.path.isdir(new_directory_path):
      os.makedirs(new_directory_path)
    get_data(new_directory_path)
    
    #temp
    #new_directory_path='/home/tessella/gene_fusions/tcga_data_20131015131033'

    #get a list of all the downloaded archives
    archive_list=tdu.get_file_list('tar.gz', new_directory_path)

    #unpack the archives
    tdu.unpack_all(archive_list)

    #get a list of the directories (the cohort directories):
    directory_list=[d for d in os.listdir(new_directory_path) if os.path.isdir(os.path.join(new_directory_path, d))]

    #within each directory(each disease cohort), merge the data files by calling a java process 
    for directory in directory_list:
      cohort_directory=os.path.join(new_directory_path, directory)
      subprocess.call(['java', '-jar', tcga_constants.FILE_MERGE_JAR, cohort_directory, tcga_constants.MAPPED_FILE_SUFFIX])
      merge_all_output(cohort_directory)

    

    
      
