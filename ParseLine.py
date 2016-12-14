'''
Created on Dec 13, 2016

@author: KARNUTJ

Parses a single line of SEER data and returns map with pertinent values
'''
#dict of id:[start pos, length]
voi = {
    "AGE_DX":[25,3],
    "RACE":[234, 1],
    "HISP":[23,1],
    "SEX":[24,1],
    "STAGE":[236,1],
    "DEAD":[272,1],
    "YEAR":[39, 4]
    }

raceDict = {
    1:"White",
    2:"Black",
    3:"Native American / Alaskan Native",
    4:"Asian / Pacific Islander",
    7:"Other Specified",
    9:"Unknown"
    }

stageDict = {
    0:"In Situ",
    1:"Localized",
    2:"Regional",
    4:"Distant",
    8:"Local / Regional (Prostate Only)",
    9:"Unstaged"
    }

def parseLine(lineIn):
    d = {}
    for ele in voi:
        pos = voi[ele][0] - 1 #convert from 0 to 1 based indexing
        length = voi[ele][1] 
        strVal = str(lineIn[pos:pos+length])
        if ele == "DEAD":
            d[ele] = (strVal == "1")
        elif ele == "AGE_DX":
            d[ele] = int(strVal)
        elif ele == "RACE":
            d[ele] = raceDict[int(strVal)]
        elif ele == "HISP":
            d[ele] = strVal != "0"
        elif ele == "STAGE":
            if strVal == ' ':
                strVal = 9;
            d[ele] = stageDict[int(strVal)]
        elif ele == "SEX":
            d[ele] = "Male" if (strVal == "1") else "Female"
        elif ele == "YEAR":
            d[ele] = int(strVal)
    return d
    
    
if __name__ == "__main__":
    ln= "070000030000001502201 020601932   02111992C5052850038500391100810  00015                   4119                                                                      009020    01             213     260001745C505      1161023 099801311011010    009011    000000000010 369999   11158                   02381                  15000010         99     8    100000";
    print(parseLine(ln))