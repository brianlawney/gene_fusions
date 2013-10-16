
class exon(object):

  def parse_exon_info(self, line):
    fields=line.split('\t')
    genomic_position=fields[0] #in the form chr?:XXX-XXX:+/-
    self.__rpkm=fields[3][:-1]
    self.__chromosome, pos_range, self.__strand=genomic_position.split(':')
    pos_range=pos_range.split('-')
    self.__start_pos=int(pos_range[0])
    self.__end_pos=int(pos_range[1])

  def __init__(self, data):
    self.parse_exon_info(data)

  def rpkm(self):
    return self.__rpkm

  def chromosome(self):
    return self.__chromosome
  
  def start_pos(self):
    return self.__start_pos

  def end_pos(self):
    return self.__end_pos

  def strand(self):
    return self.__strand

  def __str__(self):
    return str(self.__chromosome)+','+str(self.__start_pos)+','+str(self.__end_pos)

