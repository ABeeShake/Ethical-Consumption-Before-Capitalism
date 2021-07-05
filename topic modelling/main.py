import subprocess
import os
import re

# for filename in os.listdir("/Users/shubaprasadh/Downloads/ethics_csv"):
#     if filename.endswith(".csv"):
#         file1 = filename;
#         print(file1)
#         subprocess.call(['Rscript',
#                          '/Users/shubaprasadh/Downloads/topicmodeling1.R',
#                          file1])
#     else:
#         continue

for filename in os.listdir("/Users/shubaprasadh/Downloads/ethics_csv"):
    if filename.endswith(".txt"):
        with open('/Users/shubaprasadh/Downloads/ethics_csv/'+filename,'r') as file:
            data=file.read().replace(','," ")

        lexicon = re.compile('god|church|saint|lord')
        if(re.search(lexicon, data)!=None):
            print(filename + ' Success')        #file is relevant
        else:
            print('Failure')        #file is not relevant
    else:
        continue