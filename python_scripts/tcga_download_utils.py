from xml.dom import minidom
import urllib2
import os

def create_csv_string(iterable_item):
  """
  Given something iterable, create a csv string and return it.  For example, given the list [0, 1, 2] return '0,1,2'
  """
  s=''
  for item in iterable_item:
    s+=str(item)+','
  return s[0:-1]

def get_element_value(xml_string, tag_name):
  """
  Given an xml string, find the text inside the specified tag
  e.g. if tag_name='item', then this will return whatever is between <item>...</item>
  """
  xmldoc=minidom.parseString(xml_string)
  target_element=xmldoc.getElementsByTagName(tag_name)
  for element in target_element:
    children=element.childNodes
    for child in children:
      if child.nodeType==child.TEXT_NODE:
        return child.data

def generate_request(url):
  """
  open the url given as argument and return the whole thing
  """
  f=urllib2.urlopen(url)
  return f.read()

def download_archive(url, directory_path):
  """
  Given the url, download the tar.gz archive to the specified directory
  """

  #if the specified path is not a directory, just place the downloaded file into the current working directory
  if not os.path.isdir(directory_path):
    directory_path=os.getcwd()

  file_name = url.split('/')[-1]
  file_path=os.path.join(directory_path, file_name)
  u = urllib2.urlopen(url)
  with open(file_path, 'wb') as f:
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
      buffer = u.read(block_sz)
      if not buffer:
        break

      file_size_dl += len(buffer)
      f.write(buffer)
      status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
      status = status + chr(8)*(len(status)+1)
      print status,
  
  return file_name

  
