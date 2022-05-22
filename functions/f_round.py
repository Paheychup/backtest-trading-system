import math
#defined round functions
#------------------------------------------------------------------------------
def round_up(n, decimals=0): 
    multiplier = 10 ** decimals 
    return math.ceil(n * multiplier) / multiplier
def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

def roundPartial_down(value,resolution,round_down=round_down):
    return round_down(value/float(resolution))*resolution
#print(roundPartial_down(2.721,0.25))
def roundPartial_up(value,resolution,round_up=round_up):
    return round_up(value/float(resolution))*resolution
#------------------------------------------------------------------------------