from ROOT import *
import os
import math
import argparse
import numpy as np
from array import array
import pprint 
import json
import itertools
from itertools import islice
import collections




#main
fnameGdml = "gdml/CRTTxt/p3.txt"
with open(fnameGdml, 'r') as f:
    
    name = "\"Module"
    for line in f.readlines():
        if  name in line:
            words     = line.split("\"")
            AlTop = words[0]+"\""+words[1]+"\""+words[2]+"\""+words[3]+"_10\""+words[4]+"\""+words[5]+"\""+words[6]+"\""+words[7]+"\""+words[8]+"\""+words[9]+"\""+words[10]
            AlBot = words[0]+"\""+words[1]+"\""+words[2]+"\""+words[3]+"_01\""+words[4]+"\""+words[5]+"\""+words[6]+"\""+words[7]+"\""+words[8]+"\""+words[9]+"\""+words[10]

            print AlTop,
            print AlBot,
        else:
            print line,


