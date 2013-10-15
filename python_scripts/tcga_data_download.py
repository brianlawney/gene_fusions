import tcga_download_utils as tdu
import tcga_constants
import datetime
import time
import os

def format_url(cohort):
  base_url=r"https://tcga-data.nci.nih.gov/tcga/damws/jobprocess/xml?"
  centers=tdu.create_csv_string(tcga_constants.CENTERS)
  platforms=tdu.create_csv_string(tcga_constants.PLATFORMS)
  
  disease_param=r'&disease='+str(cohort)
  center_param=r'&center='+str(centers)
  platform_param=r'&platform='+str(platforms)
  level_param=r'&level=3' #level 3 data
  url=str(base_url)+str(disease_param)+str(center_param)+str(platform_param)+str(level_param)

  temp_param='&sampleList=TCGA-67-6216-*'

  url+=str(temp_param)
  print str(url)
  return url

def get_data():

  FORMAT='%Y%m%d%H%M%S'
  new_directory_path='tcga_data_'+datetime.datetime.now().strftime(FORMAT)
  if not os.path.isdir(new_directory_path):
    os.makedirs(new_directory_path)

  cohorts=['LUAD']

  for cohort in cohorts:
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
    file_name=tdu.download_archive(archive_url, new_directory_path)
    os.rename(os.path.join(new_directory_path,file_name) ,os.path.join(new_directory_path, str(cohort))+'.tar.gz') 

if __name__=='__main__':
  get_data()
      
