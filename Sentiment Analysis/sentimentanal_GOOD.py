import subprocess
import shutil, os
import re
import pandas as pd
from csv import writer
import numpy as np
import string
from boxsdk import DevelopmentClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# This area runs the R script on all files in a folder; here
# the folder is ethics_csv in my case
dir = "/Users/shubaprasadh/Downloads/"
dir1 = dir + "ethics_csv"

windowdata_fp = dir + "topicmodel_sent"

# THIS METHOD analyzes sentiment using vader
def sentiment_scores(sentence):
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)
    return sentiment_dict['compound']

    # print("Overall sentiment dictionary is : ", sentiment_dict)
    # print("Text was rated as ", sentiment_dict['neg'] * 100, "% Negative")
    # print("Text was rated as ", sentiment_dict['neu'] * 100, "% Neutral")
    # print("Text was rated as ", sentiment_dict['pos'] * 100, "% Positive")
    #
    # print("Text Overall Rated As", end=" ")
    #
    # # decide sentiment as positive, negative and neutral
    # if sentiment_dict['compound'] >= 0.05:
    #     print("Positive")
    #
    # elif sentiment_dict['compound'] <= - 0.05:
    #     print("Negative")
    #
    # else:
    #     print("Neutral")

#           DOING SENTIMENT ANALYSIS
for f in os.listdir(windowdata_fp):
    fullname = windowdata_fp+"/"+f
    if (f.endswith(".csv")) and (f!="template.csv") and (f!=".csv"):
        df = pd.read_csv(windowdata_fp + "/" + f, header=None)

        df.columns = ["ratio","window"]
        scoresList = []                     #note that this func will throw an error if the csv if empty, but we can safely assume that none of these will be
        for row, i in df.iterrows():
            text = df._get_value(row,'window')
            scoresList.append(sentiment_scores(text))
        df['sent_scores'] = scoresList
        df.to_csv(fullname, index=False)
