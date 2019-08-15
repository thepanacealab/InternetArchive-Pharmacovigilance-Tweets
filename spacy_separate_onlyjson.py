#!/usr/bin/env python
import json
import time
import csv
import argparse
import datetime
import spacy
import os
import sys
import threading
import tarfile
import bz2
import glob
from bz2 import BZ2File
from xtract import xtract
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span

drugsList=[]
jsonFilesList = []
# creates list of lists of json files to be processed in a thread and length of list is n.
def ChunkIt(a, n):  # n = number of items to be divided into
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

def ProcessFilesInThread(filesList, nlp, matcher, fO):
    for file in filesList:
        with open(file, 'r') as f:
            cnt = 0
            for line in f:
                if line.strip().startswith('{'):
                    tweet = json.loads(line)
                    if 'lang' in tweet and str(tweet["lang"]) == "en" and 'retweeted_status' not in tweet:
                        try:
                            tweetText = str(tweet["text"]).lower()
                        except:
                            tweetText = 'NULL'
                        doc = nlp(tweetText)
                        matches = matcher(doc)
                        cnt += 1                    
                        if len(matches) > 0:
                            fO.write(str(line))

def jsonParse(inputPath):
    jsonFiles = glob.glob(inputPath + '/**/*.json', recursive=True)
    for file in jsonFiles:
        jsonFilesList.append(file)
    return jsonFilesList

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--drugdictionary", help="Drug dictionary file with extension")
    parser.add_argument("-o", "--outputfile", help="Output file name with extension", required = False, default= "")
    parser.add_argument("-i", "--inputmonthfolder", help="Input file name with extension")
    

    args = parser.parse_args()
    if args.drugdictionary is None or args.inputmonthfolder is None:
        parser.error("please add necessary arguments")
        
    starttime = datetime.datetime.now()
    
    print(starttime)
    with open(args.drugdictionary) as f:
        reader = csv.reader(f, delimiter=",", quotechar="\"")
        next(reader)
        for drugRow in reader:
            drugsList.append(drugRow[1].lower())
    print("completed loading drug dictionary")
    nlp = spacy.load('en_core_web_sm',disable=['ner', "tagger"])
    drugPatterns = [nlp(drug) for drug in drugsList]  # process each word to create phrase pattern
    matcher = PhraseMatcher(nlp.vocab)
    matcher.add('DRUG', None, *drugPatterns)  # add patterns to matcher
    fO = open(args.outputfile, "w", encoding="utf-8")

    jsonFilesList = jsonParse(args.inputmonthfolder)   
    print("Completed parsing tar files and found " + str(len(jsonFilesList)) + " json files.")
    jsonFiles = list(ChunkIt(jsonFilesList, 30))
    threads = []
    print("Initiating threads!!")
    for filesList in jsonFiles:
        threads.append(threading.Thread(target=ProcessFilesInThread, args=(filesList, nlp, matcher,fO)))
        threads[-1].start()
    print("Created " + str(len(threads)) + " threads to process json files.")
    for t in threads:
        t.join()
    while True:
        currentThreads = [t for t in threads if t.is_alive()]
        if len(currentThreads) == 0:
            fO.close()
            stoptime = datetime.datetime.now()
            timedifference = stoptime - starttime
            print("Completed processing of tar file and created a new json file with separated tweets.")
            print(stoptime)
            print(timedifference)
            break  
  
# main invoked here    
main()