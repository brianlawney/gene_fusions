import sys
import tcga_constants as constants
import tcga_download_utils as tdu
import os

map_file=r'/home/tessella/gene_fusions/tss_to_cohort_abbr.csv'

def main(tcga_id, gene_id, data_directory):
  with open(map_file, 'r') as mapping:
    tss=tcga_id[5:7]
    found=False
    while not found:
      map_line=mapping.readline()
      if not map_line: 
        print 'could not map TCGA ID to a disease cohort'
        break
      tss_from_file, cohort=map_line.split(',')
      cohort=cohort[:-1] #get rid of \n
      if tss==tss_from_file:
	found=True
        search_directory=os.path.join(data_directory, cohort)
        data_file=tdu.get_file_list(constants.MERGED_FILE, search_directory)
        with open(list(data_file)[0], 'r') as merged_data:
          for line in merged_data:
            tcga_id_from_file, gene_from_file=line.split('\t')[0].split(':')
            if tcga_id_from_file==tcga_id and gene_from_file==gene_id:
              print str(os.path.join(data_directory, str(tcga_id)+'_'+str(gene_id)))
              with open(os.path.join(data_directory, str(tcga_id)+'_'+str(gene_id)),'w') as result_file:
                print line
                result_file.write(line)
      

if __name__=='__main__':
  if len(sys.argv)==4:
    tcga_id=sys.argv[1]
    gene_id=sys.argv[2]
    data_directory=sys.argv[3]
    #data_directory='/home/tessella/gene_fusions/tcga_data_20131018162538/'
    main(tcga_id, gene_id, data_directory)



