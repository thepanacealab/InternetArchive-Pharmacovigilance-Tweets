import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (brier_score_loss, precision_score, recall_score, f1_score)
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix,accuracy_score
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier

fO = open("predictions_all_RF.txt", "w")
filepath_dict = {'drugs':   'shuf_alltweets.csv'}

predict_sentences=[]
userIds=[]
tweetIds = []

predict_data=open('all_details.txt', encoding= 'UTF-8')
for sentence in predict_data:
    line = sentence.replace('\n','')
    #print(line)
    result = [x.strip() for x in line.split('\t')]
    tweetText = result[0]
    predict_sentences.append(tweetText.replace('\n',''))
    if result[1] is not None:
        tweetIds.append(result[1])          
    if result[2] is not None:
        userIds.append(result[2])   
    

df_list = []
for source, filepath in filepath_dict.items():
    df = pd.read_csv(filepath, names=['sentence', 'label'], sep=',', encoding='utf-8', quoting=3, error_bad_lines=False)
    df['source'] = source  # Add another column filled with the source name
    df_list.append(df)

df = pd.concat(df_list)
for source in df['source'].unique():
    df_source = df[df['source'] == source]
    sentences = df_source['sentence'].values.astype('U')
    y = df_source['label'].values

    sentences_train, sentences_test, y_train, y_test = train_test_split(sentences, y, test_size=0.25, random_state=1000)

    vectorizer = CountVectorizer()
    vectorizer.fit(sentences_train)
    X_train = vectorizer.transform(sentences_train)
    X_test  = vectorizer.transform(sentences_test)
    X_predict = vectorizer.transform(predict_sentences)
    
    
    input_dim = X_train.shape[1]
    classifier = RandomForestClassifier(bootstrap = True, max_depth = 100, max_features = 'auto', n_estimators = 50)
    classifier.fit(X_train, y_train)
    #score = classifier.score(X_test, y_test)
    rfc_cv_score = cross_val_score(classifier, X_train, y_train, verbose=False, cv = 10)
    print("=== All AUC Scores ===")
    print(rfc_cv_score)
    print('\n')
    print("=== Mean AUC Score ===")
    print("Mean AUC Score - RF: ", rfc_cv_score.mean())
    #print('Accuracy for {} data: {:.4f}'.format(source, score))

    print("starting predictions")
    #predictions = classifier.predict(X_predict)
    probabilities = classifier.predict_proba(X_predict)[:,1]
    
    for i in range(len(probabilities)):
    
        #fO.write( str(predictions[i]) + "\n")
        fO.write( predict_sentences[i]+ "\t" + tweetIds[i] + "\t" + userIds[i] + "\t" +  '{:.10f}'.format(float(probabilities[i])) + "\n")
	
print("predictions done")
