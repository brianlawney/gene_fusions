def make_delimited_string(cols, delimiter):
    """
    @summary: Makes a delimiter-separated list out of the database columns- used for the sql insert statement
    """
    delimited_string=''
    for column in cols:
      delimited_string=delimited_string+str(column)+str(delimiter)
    ds=delimited_string.rstrip(str(delimiter))  #remove the final delimiter
    return ds