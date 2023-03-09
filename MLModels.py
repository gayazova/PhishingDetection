from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

#вероятность обнаружения фишинга, когда он является фишингом.
def Pd(predicted, actual):
    numberOfPhishing = sum(i for i in actual if i == 1)
    numberOfDetectedPhishing = 0
    for i in range(len(actual)):
        if (actual[i] == 1 and actual[i] == predicted[i]):
            numberOfDetectedPhishing += 1
    return numberOfDetectedPhishing / numberOfPhishing

#это вероятность обнаружения фишинга, в то время как он является законным
def Pfd(predicted, actual):
    numberOfPhishing = sum(i for i in actual if i == 1)
    numberOfFalseDetectedPhishing = 0
    for i in range(len(actual)):
        if (actual[i] == 0 and predicted[i] == 1):
            numberOfFalseDetectedPhishing += 1
    return numberOfFalseDetectedPhishing / numberOfPhishing

#это вероятность помечания письма законным, в то время как он фишингом
def Pmd(predicted, actual):
    numberOfPhishing = sum(i for i in actual if i == 1)
    numberOfMissDetectedPhishing = 0
    for i in range(len(actual)):
        if (actual[i] == 1 and predicted[i] == 0):
            numberOfMissDetectedPhishing += 1
    return numberOfMissDetectedPhishing / numberOfPhishing

df = pd.read_csv(r'C:\Users\ASUS\Desktop\phishing-dataset-version2.csv', delimiter=',')

#df Нормализация столбца time_domain_activation по max/min
df.loc[df['time_domain_activation'] >= 0, 'time_domain_activation'] = (df.loc[df['time_domain_activation'] >= 0, 'time_domain_activation'] - df.loc[df['time_domain_activation'] >= 0, 'time_domain_activation'].min()) / (df.loc[df['time_domain_activation'] >= 0, 'time_domain_activation'].max() - df.loc[df['time_domain_activation'] >= 0, 'time_domain_activation'].min())
x = df.iloc[:, :7].values.tolist()
y = df['phishing'].values.tolist()
train_set_x = x[:2800]
train_set_y = y[:2800]

test_set_x = x[2800:]
test_set_y = y[2800:]

kernels = ['linear', 'poly', 'rbf', 'sigmoid']
for kern in kernels:
    clf = svm.SVC(kernel=kern)
    clf.fit(train_set_x, train_set_y)
    svm_predict = clf.predict(test_set_x)
    print('for', kern, ':')
    print(Pd(svm_predict,test_set_y))
    print(Pfd(svm_predict, test_set_y))
    print(Pmd(svm_predict, test_set_y))
    print(accuracy_score(test_set_y, svm_predict))
    print('--------------------------------------')

param_variants = [
    {'activation': 'relu', 'hidden_layer_size': (100) },
    {'activation': 'relu', 'hidden_layer_size': (100, 100) },
    {'activation': 'tanh', 'hidden_layer_size': (100) },
    {'activation': 'tanh', 'hidden_layer_size': (100, 100) },
    {'activation': 'logistic', 'hidden_layer_size': (100) },
    {'activation': 'logistic', 'hidden_layer_size': (100, 100) }
]
for param in param_variants:
    clf_neur = MLPClassifier(activation=param['activation'], solver='lbfgs', max_iter=500, hidden_layer_sizes=param['hidden_layer_size'], random_state=1)
    clf_neur.fit(train_set_x, train_set_y)
    neur_predict = clf_neur.predict(test_set_x)
    print('for', param['activation'], param['hidden_layer_size'], ':')
    print(Pd(neur_predict, test_set_y))
    print(Pfd(neur_predict, test_set_y))
    print(Pmd(neur_predict, test_set_y))
    print(accuracy_score(test_set_y, neur_predict))
    print('--------------------------------------')


max_depths = list(range(1, 11))
for depth in max_depths:
    clf = DecisionTreeClassifier(max_depth=depth)
    clf.fit(train_set_x, train_set_y)
    des_tree_predict = clf.predict(test_set_x)
    print('for', depth, ':')
    print(Pd(des_tree_predict,test_set_y))
    print(Pfd(des_tree_predict, test_set_y))
    print(Pmd(des_tree_predict, test_set_y))
    print(accuracy_score(test_set_y, des_tree_predict))
    print('--------------------------------------')

neighbors_array = list(range(1, 21))
for neigbor_number in neighbors_array:
    clf = KNeighborsClassifier(n_neighbors=neigbor_number)
    clf.fit(train_set_x, train_set_y)
    kneigbot_predict = clf.predict(test_set_x)
    print('for', neigbor_number, ':')
    print(Pd(kneigbot_predict,test_set_y))
    print(Pfd(kneigbot_predict, test_set_y))
    print(Pmd(kneigbot_predict, test_set_y))
    print(accuracy_score(test_set_y, kneigbot_predict))
    print('--------------------------------------')