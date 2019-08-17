# InternetArchive-Pharmacovigilance-Tweets
This repository contains the code of Mining archive.org’s Twitter stream grab for Pharmacovigilance research gold paper.

The Internet Archive's files must be first downloaded from - https://archive.org/details/twitterstream.

Example - wget https://archive.org/download/archiveteam-twitter-stream-2018-10/twitter-2018-10-01.tar. 

Unzip the files using - sh separate.sh 
Note: Please change the source directly location on the first line of separate.sh

Use spacy_separate_onlyjson.py to filter drug tweets using the dictionary. 
Eg: python spacy_separate_onlyjson.py -i Oct -d drug_dict_singlestr.csv -o oct_singlestr_tweets.json


Please use the TweetIds_IA_panacea.zip to access drug related Tweet Ids.
