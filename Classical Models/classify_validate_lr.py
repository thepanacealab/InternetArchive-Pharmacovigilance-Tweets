import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (brier_score_loss, precision_score, recall_score, f1_score)
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix,accuracy_score
from sklearn import metrics
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from matplotlib import pyplot

#fO = open("predictions_lg.txt", "w")
filepath_dict = {'drugs':   'shuf_alltweets.csv'}

predict_sentences=[]

for sentence in predict_data:
    predict_sentences.append(sentence.replace('\n',''))
    

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
    X_predict = vectorizer.transform(sentences_test)
    
    
    input_dim = X_train.shape[1]
    classifier = LogisticRegression(penalty= 'l2', C= 1)
    classifier.fit(X_train, y_train)
    #score = classifier.score(X_test, y_test)
    probabilities = classifier.predict_proba(X_predict)[:,1]
    rfc_cv_score = cross_val_score(classifier, X_train, y_train, verbose=False, cv = 10)
    print("=== All AUC Scores ===")
    print(rfc_cv_score)
    print('\n')
    print("=== Mean AUC Score ===")
    print("Mean AUC Score - LogisticRegression: ", rfc_cv_score.mean())
    auc = roc_auc_score(y_test, probabilities)
    print('AUC: %.4f' % auc)
    #print('Accuracy for {} data: {:.4f}'.format(source, score))

    print("starting predictions")
    #predictions = classifier.predict(X_predict)
    
    for i in range(len(predictions)):
    
        fO.write( str(predictions[i]) + "\n")
	
print("predictions done")
