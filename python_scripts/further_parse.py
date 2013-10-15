

def main():

  with open('ALK_data.txt','r') as input_file:
    with open('ALK_data_num.txt', 'w') as output_file:
      count=0
      for line in input_file:
        if count>0:
          try:
            contents=line.split('\t')
            for i in range(col_count-1):
              output_file.write(contents[i+1]+'\t')
            output_file.write(contents[col_count])
          except:
            pass
        else:
          col_count=len(line.split('\t'))-1 #number of actual data cols
          count+=1


if __name__=='__main__':
  main()
