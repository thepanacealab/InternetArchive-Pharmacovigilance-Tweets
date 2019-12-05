# Mining Archive.org's Twitter Stream Grab for Pharmacovigilance Research Gold


This repository contains the code and data from the following paper -  Mining Archive.org's Twitter Stream Grab for Pharmacovigilance Research Gold - https://www.biorxiv.org/content/10.1101/859611v1

Please use the following instructions if you intend to reproduce the results. If you are looking for the dataset, scroll all the way down!!

1) The Internet Archive's files must be first downloaded from - https://archive.org/details/twitterstream.

Example - wget https://archive.org/download/archiveteam-twitter-stream-2018-10/twitter-2018-10-01.tar. 

2) Unzip the files using - sh separate.sh 
Note: Please change the source directly location on the first line of separate.sh

3) Use spacy_separate_onlyjson.py to filter drug tweets using the dictionary. 

Eg: python spacy_separate_onlyjson.py -i Oct -d drug_dict_singlestr.csv -o oct_singlestr_tweets.json

4) To train the deep learning or classical models, please download data as given under the Claassification Section of the paper.
Once you obtain the training data, you can use the code for training Classical Models and Deep Learning models. 
Please follow the readme instructions on Classical and Deep Learning models for specific instructions and examples


# Dataset
The 3,346,758 tweet ids dataset is currently available by email request. 

Contact Information
Ramya Tekumalla - rtekumalla1@student.gsu.edu 
Juan M Banda  -  jbanda@gsu.edu
