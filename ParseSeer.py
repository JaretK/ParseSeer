'''
Created on Dec 13, 2016

@author: KARNUTJ

Parses a sinuglar SEER directory into JSON with the following hierarchy:

Seer (root)
Archetype (Breast, etc)
Age @ diagnosis
Race / Ethnicity
Sex
AJCC Stage Group (0-4)
#reported cancers
#reported deaths
'''
from os import walk
import json
import sys
import traceback
from ParseLine import parseLine

archetypeTitles = {
    "OTHER":"OTHER",
    "RESPIR" : "RESPIRATORY",
    "BREAST":"BREAST",
    "COLRECT":"COLON / RECTUM",
    "MALEGEN":"MALE GENITAL",
    "DIGOTHR":"OTHER DIGESTIVE",
    "URINARY":"URINARY",
    "FEMGEN":"FEMALE GENITAL",
    "LYMYLEUK":"LYMPHOMA / LEUKEMIA"
    }

hierarchy = [
    "AGE_DX",
    "RACE",
    "HISP",
    "SEX",
    "STAGE"
    ]

#sep bins every 10 years
age_bins = [
    "10",
    "20",
    "30",
    "40",
    "50",
    "60",
    "70",
    "80",
    "90",
    "100",
    "110",
    "120",
    "130",
    "Unknown"
    ]
race_bins = [
    "White",
    "Black",
    "Native American / Alaskan Native",
    "Asian / Pacific Islander",
    "Other Specified",
    "Unknown"]

sex_bins = ["Male", "Female"]
stage_bins = [
    "In Situ",
    "Localized",
    "Regional",
    "Distant",
    "Local / Regional (Prostate Only)",
    "Unstaged"
    ]

container = {"name":"SEER ARCHETYPE",
             "children":[]}

iarch = {}
iage = {}
isex = {}
irace = {}
istage = {}

def parseDirectory(dir):
    dirs = []
    files = set()
    for (dirpath, dirnames, filenames) in walk(dir):
        [files.add(s) for s in filenames if s.endswith(".TXT")]
        dirs.extend(dirnames)
    #populate container
    for i, f in enumerate(files):
        #archetype
        d = {"name": archetypeTitles[f[:-4]],
             "children" : []}
        container["children"].append(d)
        iarch[f[:-4]] = i
        #age
        for i1, e1 in enumerate(age_bins):
            d = {"name": strAgeBin(e1),
             "children" : []}
            container["children"][i]["children"].append(d)
            iage[e1] = i1
            #race
            for i2, e2 in enumerate(race_bins):
                d = {"name": e2,
                     "children" : []}
                container["children"][i]["children"][i1]["children"].append(d)
                irace[e2]=i2
                #sex
                for i3, e3 in enumerate(sex_bins):
                    d = {"name": e3,
                         "children" : []}
                    container["children"][i]["children"][i1]["children"][i2]["children"].append(d)
                    isex[e3]=i3
                    #stage
                    for i4, e4 in enumerate(stage_bins):
                        d = {"name": e4,
                             "children" : [
                                 {"name": "Alive", "value":0},
                                 {"name" : "Dead", "value":0}]}
                        istage[e4]=i4
                        container["children"][i]["children"][i1]["children"][i2]["children"][i3]["children"].append(d)
    #populate dict   
    for d in dirs:
        print("Starting: "+d)          
        for f in files:
            print('\t Starting: ' + f)
            with open(dir+"/"+d +"/"+ f, "r") as fn:
                for line in fn:
                    parsed = parseLine(line)
                    e1 = convertToAgeBin(parsed["AGE_DX"])
                    e2 = parsed["RACE"]
                    e3 = parsed["SEX"]
                    e4 = parsed["STAGE"]
                    dead = parsed["DEAD"]
                    addToContainer(container, f[:-4], e1,e2,e3,e4,dead)
        
    print(json.dumps(container))
    saveDict(container, "seer-data.json")

def addToContainer(d, archtype, age, race, sex, stage, dead):
    archIndex = iarch[archtype]
    ageIndex = iage[age]
    raceIndex = irace[race]
    sexIndex = isex[sex]
    stageIndex = istage[stage]
    currentObj = d["children"][archIndex]["children"][ageIndex]["children"][raceIndex]["children"][sexIndex]["children"][stageIndex]["children"]
    prevAlive = currentObj[0]["value"];
    prevDead = currentObj[1]["value"];
    if(dead):
        currentObj[1]["value"] = prevDead + 1
    else:
        currentObj[0]["value"] = prevAlive + 1
#     for ele in d:
#         if (ele["name"] == archtype):
#             temp = ele["children"]
#             break

def strAgeBin(strAge):
    if(strAge == "Unknown"):
        return strAge
    if(strAge == "10"):
        return "0-10"
    i = int(strAge)
    lower = i-9
    return str(lower)+"-"+str(i)
    
def convertToAgeBin(intAge):
    if (intAge == 999):
        return "Unknown"
    for ele in age_bins:
        if (ele == "Unknown"):
            pass
        if intAge <= int(ele):
            return str(ele)

def saveDict(d, file):
    with open(file, "w") as f:
        json.dump(d, f)
    
if __name__ == "__main__":
    parseDirectory("C://Users/karnutj/Desktop/SEER_1973_2013_TEXTDATA.d04122016/SEER_1973_2013_TEXTDATA/incidence/")
    



