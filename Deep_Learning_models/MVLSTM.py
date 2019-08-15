import typing
from pathlib import Path
import pandas as pd
import matchzoo as mz
import keras
import numpy as np
import multiprocessing
import csv

def load_data(path: str = 'train.csv') -> typing.Union[mz.DataPack, typing.Tuple[mz.DataPack, list]]:
	data_pack = mz.pack(pd.read_csv(path, index_col=0,error_bad_lines=False))
	data_pack.relation['label'] = data_pack.relation['label'].astype(int)
	data_pack = data_pack.one_hot_encode_label(num_classes=2)
	return data_pack



######################
train_path='train.csv'
valid_path='dev.csv'
test_path='test.csv'
######################

train_pack = load_data(train_path)
valid_pack = load_data(valid_path)
test_pack = load_data(test_path)

preprocessor = mz.preprocessors.BasicPreprocessor(remove_stop_words=True)
ranking_task = mz.tasks.Classification(num_classes=2)

train_processed = preprocessor.fit_transform(train_pack)
valid_processed = preprocessor.transform(valid_pack)
test_processed = preprocessor.transform(test_pack)


model = mz.models.MVLSTM()
model.params.update(preprocessor.context)
model.params['task'] = ranking_task
model.params['embedding_output_dim'] = 300
model.params['lstm_units'] = 50
model.params['top_k'] = 20
model.params['mlp_num_layers'] = 2
model.params['mlp_num_units'] = 10
model.params['mlp_num_fan_out'] = 5
model.params['mlp_activation_func'] = 'relu'
model.params['dropout_rate'] = 0.5
model.params['optimizer'] = 'adam'
model.guess_and_fill_missing_params()
model.build()
model.compile()

pred_x, pred_y = valid_processed.unpack()
evaluate = mz.callbacks.EvaluateAllMetrics(model, x=pred_x, y=pred_y, batch_size=len(pred_y))
x = int(input('Enter number of batchs:'))
data_generator = mz.DataGenerator(train_processed, batch_size=x)

x = int(input('Enter number of epochs:'))
history= model.fit_generator(data_generator, epochs=x, callbacks=[evaluate], use_multiprocessing=True, workers=max(1, multiprocessing.cpu_count() - 1))


pred_x, pred_y = test_processed.unpack()
result = model.predict(pred_x)
final_res=[]
for x in result:
	final_res.append(x[1])

predicted=[1 if i[1] > 0.5 else 0 for i in result]

Relevant = open(test_path)
Rel = csv.reader(Relevant, delimiter=',')

#########################
Ranked= open('Ranked_tweets.txt','w')
output= open('predictions.txt','w')
########################
j =0
tweets={}
for row in Rel:
	if j ==0:
		j = j +1
		continue
	tweets[row[4]]=final_res[j-1]
	j = j +1
tweets = {k:v for k, v in sorted(tweets.items(), key=lambda t: t[1],reverse=True)}


for tweet in tweets:
	Ranked.write(tweet+'	'+str(tweets[tweet])+'\n')

for i in range(len(predicted)):
	output.write(str(predicted[i])+'\n')

Relevant.close()
Ranked.close()
output.close()

