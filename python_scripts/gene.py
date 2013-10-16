import exon

class gene(object):

  def __init__(self, chromosome, start, end, name):
    self.__chromosome=chromosome
    self.__start_pos=start
    self.__end_pos=end
    self.__name=name

  def name(self):
    return self.__name

  def chromosome(self):
    return self.__chromosome
  
  def start_pos(self):
    return self.__start_pos

  def end_pos(self):
    return self.__end_pos

  def contains(self, this_exon):
    """
    returns True if the exon (object) passed to this method is contained in teh current gene. else, false
    """
    if this_exon.chromosome()==self.__chromosome:
      if this_exon.start_pos()>=self.__start_pos and this_exon.end_pos()<=self.__end_pos:
        return True
    return False

  def __str__(self):
    return str(self.__name)+','+str(self.__chromosome)+','+str(self.__start_pos)+','+str(self.__end_pos)
