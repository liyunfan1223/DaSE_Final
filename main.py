# 设置和训练模型
import re
import numpy as np
import pandas as pd
from keras.utils import np_utils, plot_model
from keras.layers import LSTM, Dense, Embedding, Dropout
from keras.models import Sequential
from keras.preprocessing import sequence
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from keras import optimizers
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv1D, MaxPooling1D
import keras

textstr = 'reviewList'
scorestr = 'status'
bounddn = 0.5
boundup = 0.5

def createDict(data): # data是一个文本Series
    Dict = {}
    sents = data
    tot = 0
    for sent in sents:
        words = sent.split()
        for word in words:
            if word not in Dict:
                tot += 1
                Dict[word] = tot
    print("字典已生成。共包含 {} 个单词。".format(tot))
    return Dict

def dataReader(filepath):
    with open(filepath,'r',encoding='utf-8') as f:
        data = pd.read_csv(f)
    # data = data.dropna()
    print("数据加载完成。数据长度为 {} 。".format(len(data)))
    return data

def dataLoader(data, Dict, maxWords):
    X = []
    Y = []
    for index, row in data.iterrows():
        review = row[textstr]
        score = row[scorestr]
        if score <= bounddn:
            X.append(review)
            Y.append(0)
        if score >= boundup:
            X.append(review)
            Y.append(1)
    vocab_size = len(Dict)
    label_size = 2
    x = [[Dict[word] for word in sent.split()] for sent in X]
    X = sequence.pad_sequences(x, maxlen = maxWords)
    Y = np_utils.to_categorical(Y)
    train_x, test_x, train_y, test_y = train_test_split(X, Y, test_size = 0.4, random_state = 242)
    test_x, valid_x, test_y, valid_y = train_test_split(test_x, test_y, test_size = 0.5, random_state = 242)
    return train_x, test_x, valid_x, train_y, test_y, valid_y, vocab_size, label_size

def dataLoader_Tfidf(data, Dict):
    X = []
    Y = []
    for index, row in data.iterrows():
        review = row[textstr]
        score = row[scorestr]
        if score <= bounddn:
            X.append(review)
            Y.append(0)
        if score >= boundup:
            X.append(review)
            Y.append(1)
    train_x, test_x, train_y, test_y = train_test_split(X, Y, test_size = 0.4, random_state = 432)
    return train_x, test_x, train_y, test_y

def createModel_LSTM(units, input_shape, output_dim, maxWords, vocab_size, label_size):
    model = Sequential()
    model.add(Embedding(input_dim = vocab_size + 1,
                        output_dim = output_dim,
                        input_length = maxWords,
                        mask_zero = True))
    model.add(LSTM(units, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units, input_shape = input_shape))
    model.add(Dropout(0.2))
    model.add(Dense(label_size, activation='softmax'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.summary()
    return model

def createModel_CNN(units, input_shape, output_dim, maxWords, vocab_size, label_size):
    model = Sequential()
    model.add(Embedding(input_dim = vocab_size + 1,
                        output_dim = output_dim,
                        input_length = maxWords,
                        mask_zero = True))
    model.add(Conv1D(filters = 64, kernel_size = 3, padding = 'same', activation = 'relu'))
    model.add(MaxPooling1D(pool_size = 2))
    model.add(Dropout(0.25))
    model.add(Conv1D(filters = 128, kernel_size = 3, padding = 'same',activation = 'relu'))
    model.add(MaxPooling1D(pool_size = 2))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(64, activation = 'relu'))
    model.add(Dense(32, activation = 'relu'))
    model.add(Dense(2, activation = 'sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.summary()
    
    return model

def createModel_Dense(units, input_shape, output_dim, maxWords, vocab_size, label_size):
    model = Sequential()
    model.add(Embedding(input_dim = vocab_size + 1,
                        output_dim = output_dim,
                        input_length = maxWords,
                        mask_zero = True))
    model.add(Flatten())
    model.add(Dense(500, activation = 'relu'))
    model.add(Dense(500, activation = 'relu'))
    model.add(Dense(200, activation = 'relu'))
    model.add(Dense(50, activation = 'relu'))
    model.add(Dense(2, activation = 'sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.summary()
    
    return model


def getMeanScore(test_x, test_y):
    pred_y = np.linspace(1, 1, len(test_y))
    yy = [np.argmax(i) for i in test_y]
    print('mean score:', accuracy_score(pred_y, yy))

def modelTrain_LSTM(data, Dict):
    maxWords = 1000
    train_x, test_x, valid_x, train_y, test_y, valid_y, vocab_size, label_size= dataLoader(data, Dict, maxWords)
    input_shape = (train_x[0], train_x[1])
    print(input_shape)
    print(train_y)
    units = 100
    batch_size = 32
    output_dim = 20
    epochs = 5
    model = createModel_LSTM(units, input_shape, output_dim, maxWords, vocab_size, label_size)
    getMeanScore(test_x, test_y)
    print(train_y)
    model.fit(train_x, train_y, epochs = epochs, batch_size = batch_size, validation_data=(valid_x, valid_y))
    print(model.evaluate(test_x, test_y))
    return model

def modelTrain_CNN(data, Dict):
    maxWords = 1000
    train_x, test_x, valid_x, train_y, test_y, valid_y, vocab_size, label_size= dataLoader(data, Dict, maxWords)
    input_shape = (train_x[0], train_x[1])
    print(input_shape)
    print(train_y)
    units = 100
    batch_size = 32
    output_dim = 20
    epochs = 5
    model = createModel_CNN(units, input_shape, output_dim, maxWords, vocab_size, label_size)
    getMeanScore(test_x, test_y)
    print(train_y)
    model.fit(train_x, train_y, epochs = epochs, batch_size = batch_size, validation_data=(valid_x, valid_y))
    print(model.evaluate(test_x, test_y))
    print(model.predict(test_x))
    return model

def modelTrain_Dense(data, Dict):
    maxWords = 1000
    train_x, test_x, valid_x, train_y, test_y, valid_y, vocab_size, label_size= dataLoader(data, Dict, maxWords)
    input_shape = (train_x[0], train_x[1])
    print(input_shape)
    print(train_y)
    units = 100
    batch_size = 32
    output_dim = 20
    epochs = 5
    model = createModel_Dense(units, input_shape, output_dim, maxWords, vocab_size, label_size)
    getMeanScore(test_x, test_y)
    print(train_y)
    model.fit(train_x, train_y, epochs = epochs, batch_size = batch_size, validation_data=(valid_x, valid_y))
    print(model.evaluate(test_x, test_y))
    return model

def createModel_Tfidf():
    model = LogisticRegression(random_state = 0)
    return model

def modelTrain_Tfidf(data, Dict):
    train_x, test_x, train_y, test_y = dataLoader_Tfidf(data, Dict)
    getMeanScore(test_x, test_y)
    max_features = 5000
    vec = TfidfVectorizer(max_features = max_features).fit(train_x)
    train_x = vec.transform(train_x)
    test_x = vec.transform(test_x)
    model = createModel_Tfidf()
    print(train_x, train_y)
    model.fit(train_x, train_y)
    print(model.coef_)
    print(model.intercept_)
    y_pred = model.predict(test_x)
    print(y_pred)
    print(accuracy_score(y_pred, test_y))
    return model

if __name__ == '__main__':
    filepath = 'datasets/tagged_total.csv'
    data = dataReader(filepath)

    Dict = createDict(data[textstr])    
    model = modelTrain_LSTM(data, Dict)
    
    # model = modelTrain_Tfidf(data, Dict) 
    # model = modelTrain_CNN(data, Dict)
    # model = modelTrain_Dense(data, Dict)
    # model.save('my_model.h5')
    # np.save('dictionary.npy', Dict)