import subprocess
import os
import re
import pandas as pd
import csv
import string
from boxsdk import DevelopmentClient

          # This area runs the R script on all files in a folder; here
          # the folder is ethics_csv in my case
dir1 = "/Users/shubaprasadh/Downloads/ethics_csv"
og_file = 'A8_P4.csv'

#               SPLITTING large CSV file into smaller ones

data = pd.read_csv(dir1+"/"+og_file)
k = 10      #of csv files         10 is PLACEHOLDER, REPLACE WITH NUMBER OF ROWS IN DATAFRAME
for i in range(k):
    df = data[i:(i+1)]

    curr_file_name = (og_file.rsplit('.', 1)[0]) +'_'+str(i) + ('.csv')
    fullname = dir1+'/'+curr_file_name

    df.to_csv(fullname, index=False)

#           CALLS R SCRIPT

for filename in os.listdir(dir1):
    if (filename.endswith(".csv")) & (filename!=og_file):
        subprocess.call(['Rscript',
                         '/Users/shubaprasadh/Downloads/topicmodeling1.R',
                         filename])
    else:
        continue

#               automatically enters the developer token
def run(csv_file1):
    import sys
    f1 = sys.stdin
    f = open('input.txt','r')       #input.txt is text file that contains the developer key
    sys.stdin = f
    box_upload(csv_file1)
    f.close()
    sys.stdin = f1

#               uploads to Box
def box_upload(csv_file):
    '''
    Notes: Create a text file named app.cfg in pycharm. Add the following info in order:
            1. Client ID
            2. Client Secret
            3. Developer Token
            On the Box API site, go to your app and change settings:
            1. read and write all files and folders to Box - should be activated
            2. Manage users and manage groups - should be activated
            3. Make API calls using as-user header - should be activated
    '''
    client = DevelopmentClient()

    root_folder = client.folder('0').get()
    child_folders = root_folder.get_items(limit=100, offset=0)

    for child in child_folders:
        if child['name'] == 'Data+ Relevant Files':
            folder = client.folder(child['id']).get()
            break

    new_file = folder.upload(csv_file)

    print(f'File {new_file.name} was uploaded to {folder.name}')



#           This checks whether file is relevant against a lexicon
for filename in os.listdir("/Users/shubaprasadh/Downloads/ethics_csv"):
    if (filename.endswith(".txt")) & (filename!=".txt"):
        with open('/Users/shubaprasadh/Downloads/ethics_csv/'+filename,'r') as file:
            data=file.read().replace(','," ")

        lexicon = re.compile('god|church|saint|lord')
        filename_csv = (filename.rsplit('.', 1)[0])+('.csv')
        if(re.search(lexicon, data)!=None):
            print(filename_csv + ' Success')        #file is relevant
            run("/Users/shubaprasadh/Downloads/ethics_csv/"+filename_csv)
        else:
            print(filename_csv + ' Failure')        #file is not relevant
    else:
        continue


