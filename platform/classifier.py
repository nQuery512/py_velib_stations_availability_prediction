import numpy
import pandas

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib

def get_model(filename):
    mdl = joblib.load(filename)
    return mdl

def get_test_features(filename):
    df = pandas.read_table(filename,delimiter=',', names=('nbBike','heure', 'nom_de_station'))

    labels = df['nom_de_station'].values
    featureNames = ['nbBike', 'heure']
    features = df[featureNames].values
    trainingFeatures, testFeatures, trainingLabels, testLabels = train_test_split(features, labels, test_size=0.3,random_state=1)
    return testFeatures

def get_training_features(filename):
    df = pandas.read_table(filename,delimiter=',', names=('nbBike','heure', 'nom_de_station'))

    labels = df['nom_de_station'].values
    featureNames = ['nbBike', 'heure']
    features = df[featureNames].values
    trainingFeatures, testFeatures, trainingLabels, testLabels = train_test_split(features, labels, test_size=0.3,random_state=1)
    return trainingFeatures

def classify(hour):

    filename = str('data_h\\'+'data.txt') 
    df = pandas.read_table(filename, delimiter=',', names=('nbBike','heure', 'nom_de_station'))

    labels = df['nom_de_station'].values
    featureNames = ['nbBike', 'heure']
    features = df[featureNames].values

    trainingFeatures, testFeatures, trainingLabels, testLabels = train_test_split(features, labels, test_size=0.3,random_state=1)
    print('size of label:', len(trainingLabels))

    model = RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
                max_depth=None, max_features='auto', max_leaf_nodes=None,
                min_impurity_decrease=0.0, min_impurity_split=None,
                min_samples_leaf=1, min_samples_split=2,
                min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=4,
                oob_score=False, random_state=None, verbose=0,
                warm_start=False)
    

    model.fit(features,labels)
    print('\n\n\nsize of label', len(labels))
    print('\n\n\nsize of features', len(features))
    #print('\n\n',trainingLabels)
    #print(model)
    #print(model.feature_importances_)
    #print(model.score(testFeatures,testLabels))
    #print(model.predict_proba(testFeatures))
    #print(accuracy_score(testLabels, testLabels))

    proba_list={}
    count_all = 0
    res= model.predict(features)
    #ress = model.predict(features)

    print('\nsize of res of model: ', len(res))
    for element in res:
        count_all +=1
        if element not in proba_list:
            proba_list[element] = 1
        else:
            proba_list[element] += 1
            
    summ = 0
    for key in proba_list:
        
        summ += ((proba_list[key]*100)/count_all)
        proba_list[key] = ((proba_list[key]*100)/count_all)
    print(summ)
    return proba_list

def predict(model, features):
    new_features = []
    for array in features:
        new_features.append(array)
        new_features.append(array)
        new_features.append(array)
        new_features.append(array)
        new_features.append(array)
        new_features.append(array)
        new_features.append(array)
        new_features.append(array)
        new_features.append(array)
        new_features.append(array)
        new_features.append(array)
        new_features.append(array)
        new_features.append(array)
        new_features.append(array)
        new_features.append(array)
        new_features.append(array)
        new_features.append(array)
        new_features.append(array)
        new_features.append(array)
    print('\n\n',len(new_features),'\n\n')
    res= model.predict(new_features)
    
    proba_list={}
    count_all =0
    for element in res:
        count_all +=1
        if element not in proba_list:
            proba_list[element] = 1
        else:
            proba_list[element] += 1
    sum = 0
    for key in proba_list:
        
        sum += ((proba_list[key]*100)/count_all)
        proba_list[key] = ((proba_list[key]*100)/count_all)
    #print("BEST IS: ",max(proba_list),"\n\n")
    return proba_list
