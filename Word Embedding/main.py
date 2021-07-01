###### Imports ######

# unsupervised label generation
import nltk
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# sentiment analysis tools
import transformers
from transformers import BertForSequenceClassification, BertTokenizer, AdamW, get_linear_schedule_with_warmup, \
    TrainingArguments, Trainer, BertConfig
import torch
import numpy as np
import pandas as pd
import seaborn as sns
from pylab import rcParams
import matplotlib.pyplot as plt
from matplotlib import rc
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, precision_recall_fscore_support, accuracy_score
from collections import defaultdict
from textwrap import wrap
from torch import nn, optim
from torch.utils.data import Dataset, DataLoader

###### Load Data ######
df = pd.read_csv("./B2_P4.csv",
                 header=None,
                 names=['index', 'title', 'author', 'publisher', 'date', 'text'])

print(df.head())
print(df.columns)
print(f'shape: {df.shape}')

X_train, X_test = train_test_split(df.copy(), test_size=0.2, random_state=21, shuffle=True)
X_val, X_test = train_test_split(X_test.copy(), test_size=0.5, random_state=22, shuffle=True)
# steps:
# 1. generate labels for X_train
# 2. build BERT model
# 3. training
# 4. predictions

analyzer = SentimentIntensityAnalyzer()


def vader_sentiment_result(sent):
    scores = analyzer.polarity_scores(sent)

    if scores["neg"] > scores["pos"]:
        return 0
    elif abs(scores['neg'] - scores['pos']) <= 0.1:
        return 1

    return 2


X_train["vader_result"] = X_train['title'].apply(lambda x: vader_sentiment_result(x))
X_val["vader_result"] = X_val['title'].apply(lambda x: vader_sentiment_result(x))

print(X_train['vader_result'].value_counts())
print(X_train['title'][15])
print(X_train['vader_result'][15])
# neutral with what Vader suggested results with Vader and issues:
# 1 6945
# 2 51
# 0 6
# we need to filter out the unncessary stuff in the titles, clean spelling, find a good way to determine postive, negative, neutral with Vader

# 1    3409
# 2    2248
# 0    1345

###### Build Dataset ######

# sentiment analysis stuff

pretrained_model_name = 'bert-base-uncased'

tokenizer = BertTokenizer.from_pretrained(pretrained_model_name)
# token_lens = []
# for txt in df.title:
#     tokens = tokenizer.encode(txt,max_length=512)
#     token_lens.append(len(tokens))
#
# fig = plt.figure(figsize = (10,10))
# sns.distplot(token_lens)
# plt.title('Token Length Distribution')
# plt.xlim([0,256])
# plt.xlabel('Token Count')
# plt.show()

max_len = 200


class SentimentAnalysisDataset(Dataset):
    def __init__(self, titles, targets, tokenizer, max_len):
        self.titles = titles
        self.targets = targets
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.titles)

    def __getitem__(self, item):
        title = str(self.titles[item])
        target = self.targets[item]
        encoding = self.tokenizer.encode_plus(
            title,
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )
        return {
            'title_text': title,
            'input_ids': encoding['input_ids'][0],
            'attention_mask': encoding['attention_mask'][0],
            'labels': torch.tensor(target, dtype=torch.long)
        }


X_train_ds = SentimentAnalysisDataset(titles=X_train['title'].tolist(),
                                      targets=X_train['vader_result'].tolist(),
                                      tokenizer=tokenizer,
                                      max_len=max_len)

X_val_ds = SentimentAnalysisDataset(titles=X_val['title'].tolist(),
                                    targets=X_val['vader_result'].tolist(),
                                    tokenizer=tokenizer,
                                    max_len=max_len)

config = BertConfig.from_pretrained(pretrained_model_name)
config.num_labels = 3

model= BertForSequenceClassification(config)

for name, param in model.bert.named_parameters():
    if (not name.startswith('pooler')) and "layer.23" not in name:
        param.requires_grad=False

def compute_metrics(pred):
    labels=pred.label_ids
    preds= pred.predictions.argmax(-1)
    precision, recall, f1, _ =precision_recall_fscore_support(labels, preds, average='binary')
    acc=accuracy_score(labels,preds)
    return {'accucracy': acc, 'f1':f1, 'precision': precision, 'recall': recall}


training_args=TrainingArguments(
    output_dir = './BERT_output',
    num_train_epochs=10,
    per_device_train_batch_size=16,
    per_device_eval_batch_size= 64,
    warmup_steps= 500,
    weight_decay= 0.01,
    save_strategy= "epoch",
    evaluation_strategy= "steps"
)

trainer= Trainer(
    model= model,
    args= training_args,
    train_dataset= X_train_ds,
    eval_dataset= X_val_ds,
    compute_metrics= compute_metrics
)

print(torch.cuda.is_available())
#trainer.train()
