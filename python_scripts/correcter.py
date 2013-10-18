


def main():
  with open('/home/tessella/gene_fusions/tss_to_cohort_abbr.csv', 'r') as infile:
    with open('/home/tessella/gene_fusions/corrected.csv', 'w') as outfile:
      for line in infile:
        outfile.write(line[:-2]+'\n')
    

if __name__=='__main__':
  main()
