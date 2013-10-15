

def main():

  chromosome='chr2'
  start=29415640
  end=30144432
  with open('/home/brian/tessella/tcga_78_exon_quantification.txt','r') as input_file:
    with open('TCGA_78_data.txt', 'w') as output_file:
      count=0
      for line in input_file:
        if count<1:
          count+=1
        else:
          try:
            split_line=line.split('\t')
            id=split_line[0]
            info=id.split(':')
            if info[0]==chromosome:
              base_range=info[1].split('-')
              if int(base_range[0])>=start:
                if int(base_range[1])<=end:	
                  output_file.write(split_line[3])
          except:
            pass


if __name__=='__main__':
  main()
