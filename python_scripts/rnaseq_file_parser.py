

def main():

  chromosome='chr2'
  start=29415640
  end=30144432
  with open('LUAD_data.txt','r') as input_file:
    with open('ALK_data2.txt', 'w') as output_file:
      count=0
      for line in input_file:
        if count==0:
          sample_array=line.split('\t')
          size=len(sample_array)
          samples=(size-1)/3

          for i in range(samples):
            output_file.write(sample_array[3*i]+'\t')
          output_file.write(sample_array[size-1])
          count+=1
        try:
          split_line=line.split('\t')
          id=split_line[0]
          info=id.split(':')
          if info[0]==chromosome:
            base_range=info[1].split('-')
            if int(base_range[0])>=start:
              if int(base_range[1])<=end:
                for i in range(samples):
                  output_file.write(split_line[3*i]+'\t')
                output_file.write(split_line[size-1])
        except:
          pass


if __name__=='__main__':
  main()
