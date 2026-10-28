import re#Regualr expression

def normalize(code):#This funciton make sure all course codes look exactly the same
    return re.sub(r"\s+", " ", str(code)).strip().upper()#cleans whatever string you already extracted
