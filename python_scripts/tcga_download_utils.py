from xml.dom import minidom
import urllib2
import os
import tarfile
import tcga_constants
import config
from gene import gene
from exon import exon

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


def get_file_list(file_suffix, root_directory='.'):
  """
  @Summary:  beginning from the directory (default from which the module is originated), walk the directory structure and
             find all files with the desired suffix
  @Param root_directory:  a string denoting the root directory to start the walk
  @Param file_suffix: a string denoting the desired file suffix (e.g. '.txt').
  """

  #keep the file paths in a set
  all_files=set()

  for root, dirs, files in os.walk(root_directory):
    for file in files:
      if file.endswith(str(file_suffix)):
        #construct the fully resolved file path
        path=os.path.join(root,file)
        all_files.add(path)
  return all_files


def unpack_all(file_list):
  """
  @Summary: unpacks compressed directories/files
  @Parameter file_list: a set of absolute file paths

  """  
  #progress through the list of compressed files and unzip to the desired directory
  for file in file_list:
    if file.endswith('tar.gz'):
      tf=tarfile.open(str(file),'r:gz')
      tf.extractall(os.path.dirname(file))
 
   
def traverse_upwards(directory, level):
  """
  walks up directory tree to get parent paths
  """  
  if level==1:
    return os.path.dirname(directory)
  else:
    return traverse_upwards(os.path.dirname(directory), level-1)



  
def create_sample_mapping(cohort_specific_directory):
  """
  For the directory passed as argument, map the file names to the TCGA-XX-XXXX sample barcodes they correspond to
  """
  map_file_path=os.path.join(cohort_specific_directory, 'FILE_SAMPLE_MAP.txt')
  with open(map_file_path, 'r') as map_file:
    #read the contents into a dictionary
    line_num=0
    file_to_sample_mapping={}
    for line in map_file:
      if line_num>0: #ignore header line
        split_line=line.split('\t')
        if split_line[0].endswith(tcga_constants.EXON_FILE_EXTENSION):  
          file_to_sample_mapping[split_line[0]]=split_line[1][0:12] #extract the TCGA-XX-XXXX sample id
      else:
        line_num+=1
  return file_to_sample_mapping
  


def determine_gene(this_exon):
  try:
    genes_on_chromosome=config.genomic_position_to_gene_map[this_exon.chromosome()] #list of genes on this chromosome
    for a_gene in genes_on_chromosome:
      if a_gene.contains(this_exon):
        return a_gene
  except KeyError:
    print 'could not map for exon:'+str(this_exon)
    
  
def write_to_file(directory, gene_name, sample_id, exon_list):
  filename=os.path.join(directory, str(sample_id)+'_merged.txt')
  with open(filename, 'a') as outfile:
    outfile.write(str(sample_id)+':'+str(gene_name)+'\t')
    for this_exon in exon_list:
      outfile.write(str(this_exon.rpkm())+'\t')
    outfile.write('\n')



def merge_exon_files(containing_directory):
  """
  Merge the exon_quantification files in the directory passed as an argument
  """

  #get the directory for this cohort
  cohort_specific_directory=traverse_upwards(containing_directory,3)
  print 'merging files in '+str(cohort_specific_directory)
  #get all the exon files in a list
  exon_files=[f for f in os.listdir(containing_directory) if f.endswith(tcga_constants.EXON_FILE_EXTENSION)]

  #get a mapping from the center's ID to the TCGA ID
  sample_mapping=create_sample_mapping(cohort_specific_directory)
  
  for input_file in exon_files:
    sample_id=sample_mapping[input_file]
    input_file_path=os.path.join(containing_directory, input_file)
    current_gene=None
    exon_list=[]
    with open(input_file_path, 'r') as infile:
      line_count=0
      while True:
        line=infile.readline()
        if not line: break
        if line_count>0:
          new_exon=exon(line)
          if current_gene:
            if not current_gene.contains(new_exon):
              if len(exon_list)>0:
                write_to_file(containing_directory, current_gene.name(), sample_id, exon_list)
              current_gene=determine_gene(new_exon)
              exon_list=[]
          else:
            current_gene=determine_gene(new_exon)
            exon_list=[]
          exon_list.append(new_exon) 
        else:
          line_count+=1
      #have to write the remnants (since writes normally only happen when a new genomic region is encountered
      if current_gene:
        write_to_file(containing_directory, current_gene.name(), sample_id, exon_list) 
    

def create_genomic_mapping():
  mapping={}
  
  with open(tcga_constants.GTF_FILE,'r') as gtf_file:

    for line in gtf_file:
      split_line=line.split('\t')
      chromosome=split_line[0]
      start_pos=int(split_line[3])
      end_pos=int(split_line[4])
      extra_field=split_line[8]

      extras=[field.strip() for field in extra_field.split(';')]
      for e in extras:
        if e.startswith('gene_name'):
          gene_name=e.split()[1][1:-1]

      this_gene=gene(chromosome, start_pos, end_pos, gene_name)
     
      if chromosome in mapping:
        existing_list=mapping[chromosome]
        existing_list.append(this_gene)
        mapping[chromosome]=existing_list
      else:
        new_list=[]
        new_list.append(this_gene)
        mapping[chromosome]=new_list
  return mapping

