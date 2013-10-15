import sys


def parse_gtf(infile, outfile):
  with open(infile, 'r') as in_file:
    with open(outfile, 'w') as out_file:
      for line in in_file:
        if not line.startswith('##'):
          split_line=line.split('\t')
          if split_line[2]=='gene':
            out_file.write(line)
    


if __name__=='__main__':
  
  if len(sys.argv)==3:
    parse_gtf(sys.argv[1], sys.argv[2])
  else:
    print 'Supply an input file and an output file as arguments'
