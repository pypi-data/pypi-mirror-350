def chapter_1_numpy():
    import numpy as np
    print(np.__version__)

    arr1= np.array([1, 2, 3, 4, 5, 6])
    print(arr1)
    print(arr1.dtype)
    print(arr1.shape)

    arr2=np.array([[1.1, 1.2, 3.4],[2.1, 7.2, 2.3]])
    print(arr2)
    print(arr2.dtype)
    print(arr2.shape)

    lst=[[1,2,3],[11,12,13],[21,22,23],[31,32,33]]
    arr=np.array(lst)
    print(arr)
    print(arr.dtype)
    print(arr.shape)

    print(arr[0])
    print(arr[1,2])

    print(arr[1,:])
    print(arr[:,0])
    print(arr[2,1:3])

    x=arr[:,0:2]
    y=arr[:,-1]
    print(x)
    print(y)

    print(arr[arr%3==0])
    print(arr[arr>10])

    for x in arr:
        print(x)

    for x in arr:
        for v in x:
            print(v)

    ans= np.sum(arr)
    print("Sum:",ans)
    ans= np.min(arr)
    print("Min:",ans)
    ans= np.mean(arr)
    print("Mean:",ans)
    ans= np.median(arr)
    print("Median:",ans)
    ans= np.std(arr)
    print("Standard deviation:",ans)
    ans= np.percentile(arr, 50)
    print("Percentile:",ans)

    print(arr)
    ans= np.sum(arr, axis=0)
    print("Sum of Column:",ans)
    ans= np.sum(arr, axis=1)
    print("Sum of Rows:",ans)
    ans=np.mean(arr, axis=0)
    print("Mean of Colms")

def chapter_2_matplotlib():
    import matplotlib
    print(matplotlib.__version__)

    import matplotlib.pyplot as plt
    import numpy as np
    xpoints = np.array([0,2,4,6])
    ypoints = np.array([0,75,100,250])
    plt.title("Title of charts")
    plt.xlabel("X - Label")
    plt.ylabel("Y - Label")
    plt.plot(xpoints, ypoints)
    plt.show()

    x = np.array([1, 3, 5, 7])
    y = np.array([25, 85, 140, 240])

    plt.plot(x, y, marker = 'o', ms = 10, mec = 'r', mfc = 'r', linestyle = 'dotted', color = 'b', linewidth = '3')
    plt.show()

    x = np.array([5, 7, 8, 7, 2, 17, 2, 9, 4, 11, 12, 9, 6])
    y = np.array([99, 86, 87, 88, 111, 86, 103, 87, 94, 78, 77, 85, 86])
    plt.scatter(x, y)
    plt.show()

    x = np.array(["A", "B", "C", "D"])
    y = np.array([30, 58, 45, 60])

    plt.bar(x, y)
    plt.show()

    y = np.array([15, 35, 20, 30])

    plt.pie(y)
    plt.show()


def chapter_3_pandas():
    import pandas as pd
    print(pd.__version__)

    df1 = pd.DataFrame([[1, 2, 3],[7, 4, 9],[3, 9, 2],[1, 8, 4],[2, 6, 5],[5, 8, 3]])
    print(df1)
    print(df1.shape)

    df1.head()

    print(df1.head(3))

    print(df1.tail())
    print("Last Three recoerds")
    print(df1.tail(3))

    print(df1[0])

    print(df1.iloc[1,2])
    print(df1.iloc[2,:])
    print(df1.iloc[:,0])
    print(df1.iloc[1:4,1:3])

    mydata= pd.read_csv("C:/Users/Asus/Downloads/income-expense.csv")
    print(mydata.shape)
    print(mydata.head)

    print(mydata.isnull().sum())

    mydata.info()

    print(mydata.mean())
    print(mydata.median())
    print(mydata.quantile(0.5))

    mydata["Income"] = mydata["Income"].fillna(mydata["Income"].median())
    mydata.isnull().sum()

    print(mydata["Age"].mean())
    print(mydata["Income"].median())
    print(mydata["Expense"].quantile(0.75))

    mydata.describe()

    mydata.corr()



def chapter_4_sklearn():
    from sklearn.datasets import load_breast_cancer
    br_canc = load_breast_cancer()
    x = br_canc.data
    y = br_canc.target
    print(x.shape)
    print(y.shape)

    feature_names = br_canc.feature_names
    target_names = br_canc.target_names
    print("Feature nmaes:",feature_names)
    print("Target Names:", target_names)

    import pandas as pd
    df = pd.DataFrame(br_canc.data, columns=br_canc.feature_names)
    df.head()

    df["mean radius"].describe()

    from sklearn.model_selection import train_test_split

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size = 0.2, random_state = 1
    )

    print(x_train.shape)
    print(x_test.shape)

    print(y_train.shape)
    print(y_test.shape)

    import numpy as np
    data = [[21, 45000, "govt"],[33, 42000, "private"],[18, 30000, "semi-govt"],[36, 53000, "private"], [45, 55000, "govt"], [34, 48000, "semi-govt"]]
    mydata = pd.DataFrame(data, columns=["age", "salary", "job"])
    print(mydata)

    from sklearn.preprocessing import MinMaxScaler
    scaler=MinMaxScaler()
    numdata=mydata.iloc[:,0:2]
    scalar_num=scaler.fit_transform(numdata)
    scalar_num

    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    numdata = mydata.iloc[:,0:2]
    scaler_num = scaler.fit_transform(numdata)
    scaler_num

    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    catdata = mydata['job']
    data_encode=le.fit_transform(catdata)
    print(data_encode)
    print(le.classes_)

    data = pd.read_csv("C:/Users/Asus/Downloads/Linear_Simple_Salary_Data.csv")
    print(data.shape)
    data.head()

    from sklearn.linear_model import LinearRegression
    x=data.drop("Salary", axis="columns")
    y=data.Salary
    model=LinearRegression()
    model.fit(x,y)

    model.score(x,y)

    model.predict([[7.5]])

    print("Coefficient:=",model.coef_)
    print("Intercept:=",model.intercept_)
    print("Formula: y = " + str(model.coef_[0]) + " * X + " + str(model.intercept_))

def chapter_5_knn():
    import os
    import pandas as pd
    from sklearn.datasets import load_iris

    iris = load_iris()
    print(iris.data.shape)
    print(iris.target.shape)
    iris

    df = pd.DataFrame(iris.data,columns=iris.feature_names)
    df["target"] = iris.target
    df.head()

    df["flower_name"] = df.target.apply(lambda x: iris.target_names[x])
    df[45:55]

    df1 = df[:50]
    df2 = df[50:100]
    df3 = df[100:]

    import matplotlib.pyplot as plt

    plt.xlabel("Petal Length")
    plt.ylabel("Petal Width")
    plt.scatter(df1["petal length (cm)"],df1["petal width (cm)"],color="green",marker="+")
    plt.scatter(df2["petal length (cm)"],df2["petal width (cm)"],color="blue",marker="+")
    plt.scatter(df3["petal length (cm)"],df3["petal width (cm)"],color="red",marker="+")

    X = iris.data
    Y = iris.target
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(X,Y,test_size=0.20,random_state = 1)

    from sklearn.neighbors import KNeighborsClassifier
    model = KNeighborsClassifier(n_neighbors=33)
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)

    from sklearn.metrics import classification_report, confusion_matrix
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    import numpy as np
    error = []

    # Claculate error for K values between 1 to 60
    for i in range(1, 60):
        knn = KNeighborsClassifier(n_neighbors=i)
        knn.fit(x_train, y_train)
        pred_i = knn.predict(x_test)
        error.append(np.mean(pred_i != y_test))

    plt.figure(figsize=(16,8))
    plt.plot(range(1, 60), error, color="red", linestyle="dashed",marker="o",markerfacecolor="blue")
    plt.title("Error Rate K Value")
    plt.xlabel("K Value")
    plt.ylabel("Mean Error")

def chapter_6_1_decision_tree():
    import pandas as pd
    df = pd.read_csv("E:\Downloads\weather.csv")
    print(df.shape)
    df.head()

    x = df.drop('play',axis='columns')
    y = df['play']
    y

    from sklearn.preprocessing import LabelEncoder
    le_outlook = LabelEncoder()
    le_temp = LabelEncoder()
    le_humi = LabelEncoder()
    le_windy = LabelEncoder()

    x['outlook_n'] = le_outlook.fit_transform(x['outlook'])
    x['temprature_n'] = le_temp.fit_transform(x['temperature'])
    x['humidity_n'] = le_humi.fit_transform(x['humidity'])
    x['windy_n'] = le_windy.fit_transform(x['windy'])

    x_n = x.drop(['outlook', 'temperature', 'humidity', 'windy'], axis='columns')

    from sklearn import tree
    model = tree.DecisionTreeClassifier(criterion='entropy')
    model.fit(x_n, y)
    model.score(x_n, y)

    model.predict([[0, 1, 1, 0]])

    tree.plot_tree(model)

def chapter_6_2_decision_tree():
    import numpy as np
    import pandas as pd
    from sklearn.metrics import accuracy_score
    from sklearn.datasets import load_iris
    from sklearn import tree
    import matplotlib.pyplot as plt

    dataset=load_iris()
    x=dataset.data
    y=dataset.target
    print(x.shape)
    print(y.shape)

    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=0
    )
    print(x_train.shape)
    print(x_test.shape)
    print(y_train.shape)
    print(y_test.shape)

    accuracy = []

    # Loop over depths 1 to 10
    for i in range(1, 11):
        model = tree.DecisionTreeClassifier(max_depth=i, random_state=0)
        model.fit(x_train, y_train)
        pred = model.predict(x_test)
        score = accuracy_score(y_test, pred)
        accuracy.append(score)

    # Plot accuracy vs max_depth
    plt.plot(range(1, 11), accuracy, color='blue', marker='o', markersize=10)

    # Now — train one DecisionTree with entropy criterion and max_depth=4
    model = tree.DecisionTreeClassifier(criterion='entropy', max_depth=4, random_state=0)
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    score = accuracy_score(y_test, pred)
    print(f"Accuracy: {score * 100:.2f}%")

    # Print a specific test instance and its actual and predicted value
    print("Test sample:", x_test[3, :])
    print("Actual label:", y_test[3])
    ans = model.predict([x_test[3, :]])
    print("Predicted label:", ans[0])

    # Plot the trained decision tree
    plt.figure(figsize=(20, 10))
    tree.plot_tree(model)
    plt.show()

def chapter_7_kmeans():
    from sklearn.cluster import KMeans
    import pandas as pd
    from sklearn.preprocessing import MinMaxScaler
    from matplotlib import pyplot as plt

    df= pd.read_csv("C:/Users/Asus/Downloads/IncomeKMean.csv")
    df

    plt.scatter(df["Age"],df["Income"])
    plt.xlabel('Age')
    plt.ylabel('Income')

    df.head(8)

    """scaler=MinMaxScaler()
    scaler.fit(df[["Income"]])
    df['Income'] = scaler.transform(df[['Income']])

    scaler.fit(df[["Age"]])
    df['Age'] = scaler.transform(df[["Age"]])
    df.head(8)
    """

    km = KMeans(n_clusters=3)
    y_predict = km.fit_predict(df[['Age','Income']])
    y_predict

    df['cluster']=y_predict
    df.tail(15)

    km.cluster_centers_

    df1 = df[df.cluster == 0]
    df2 = df[df.cluster == 1]
    df3 = df[df.cluster == 2]
    plt.scatter(df1.Age, df1['Income'], color='green', label='Cluster 0')
    plt.scatter(df2.Age, df2['Income'], color='red', label='Cluster 1')
    plt.scatter(df3.Age, df3['Income'], color='blue', label='Cluster 2')
    plt.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1], color='purple', marker='*', s=200, label='Centroid')

    sse = []
    k_rng = range(1, 10)
    for k in k_rng:
        km = KMeans(n_clusters=k)
        km.fit(df[['Age', 'Income']])
        sse.append(km.inertia_)

    plt.xlabel('K')
    plt.ylabel('Sum of Squared Error (SSE)')
    plt.plot(k_rng, sse)
    plt.title('Elbow Method For Optimal K')
    plt.show()

def chapter_8_svm():
    import numpy as np
    import pandas as pd
    from sklearn.datasets import load_digits

    dataset = load_digits()
    x = dataset.data
    y = dataset.target
    print(x.shape)
    print(y.shape)

    print(dataset.images.shape)
    dataimglen = len(dataset.images)
    print(dataimglen)

    idx = 1109
    import matplotlib.pyplot as plt
    plt.gray()
    plt.matshow(dataset.images[idx])
    plt.show()

    dataset.images[idx]

    print(y[idx])

    x = dataset.images.reshape(dataimglen, -1)
    x
    y = dataset.target
    y

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=42)

    print(X_train.shape)
    print(X_test.shape)

    print(y_train.shape)
    print(y_test.shape)

    from sklearn import svm
    model = svm.SVC(kernel='linear')
    model.fit(X_train, y_train)

    idx=309
    result=model.predict(dataset.images[idx].reshape(1,-1))
    print(result)

    plt.gray()
    plt.matshow(dataset.images[idx])
    plt.show()

    y_pred=model.predict(X_test)
    arr=np.concatenate((y_pred.reshape(len(y_pred),1),y_test.reshape(len(y_test),1)),1)
    print(arr[111:114,:])

    from sklearn.metrics import accuracy_score
    acc = accuracy_score(y_test, y_pred)
    print("Accuracy:=", acc*100)

    model1 = svm.SVC(kernel='linear')
    model2 = svm.SVC(kernel='rbf')
    model3 = svm.SVC(gamma=0.003)
    model4 = svm.SVC(gamma=0.001, C=0.1)

    model1.fit(X_train, y_train)

def chapter_9_random_forest():
    import numpy as np
    import pandas as pd
    from sklearn.datasets import load_digits

    dataset=load_digits()
    X=dataset.data
    y=dataset.target
    print(X.shape)
    print(y.shape)

    idx=109
    import matplotlib.pyplot as plt
    plt.gray()
    plt.matshow(dataset.images[idx])
    plt.show()
    dataset.images[idx]

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
    print(X_train.shape)
    print(X_test.shape)
    print(y_train.shape)
    print(y_test.shape)

    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=20)
    model.fit(X_train, y_train)

    model.score(X_test, y_test)

    y_pred=model.predict(X_test)
    arr=np.concatenate((y_pred.reshape(len(y_pred),1),y_test.reshape(len(y_test),1)),1)
    print(arr[11:440,:])

    from sklearn.metrics import accuracy_score
    acc=accuracy_score(y_test,y_pred)
    print("Accuarcy:=",acc*100)

    model1 = RandomForestClassifier(n_estimators=10)
    model2 = RandomForestClassifier(n_estimators=15)
    model3 = RandomForestClassifier(n_estimators=20)
    model4 = RandomForestClassifier(n_estimators=25)
    model1.fit(X_train, y_train)
    model2.fit(X_train, y_train)
    model3.fit(X_train, y_train)
    model4.fit(X_train, y_train)
    y_pred1= model1.predict(X_test)
    y_pred2= model2.predict(X_test)
    y_pred3= model3.predict(X_test)
    y_pred4= model4.predict(X_test)
    print("Accuarcy of Model 1:=",(accuracy_score(y_test,y_pred1)*100))
    print("Accuarcy of Model 2:=",(accuracy_score(y_test,y_pred2)*100))

    print("Accuarcy of Model 3:=",(accuracy_score(y_test,y_pred3)*100))
    print("Accuarcy of Model 4:=",(accuracy_score(y_test,y_pred4)*100))


def chapter_10_1_naive_bayes():
    import pandas as pd
    import numpy as np

    import pandas as pd

    # Load the dataset
    myData = pd.read_csv("D:/Downloads/titanic.csv")

    # Map 'Sex' to 0 for male and 1 for female
    myData['Sex'] = myData['Sex'].map({'male': 0, 'female': 1})

    # Drop unnecessary columns
    myData.drop(columns=['Ticket', 'Cabin', 'Embarked'], inplace=True)

    # Remove rows with any null values
    myData.dropna(inplace=True)

    # Display the cleaned DataFrame
    print(myData.head())

    x=myData.drop(["Survived","Name"], axis=1)
    y=myData["Survived"]
    myData

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.20, random_state=9)

    print(X_train.shape)
    print(X_test.shape)

    print(y_train.shape)
    print(y_test.shape)

    from sklearn.naive_bayes import GaussianNB
    model = GaussianNB()
    model.fit(X_train, y_train)

    model.score(X_test, y_test)

    from sklearn.metrics import accuracy_score
    y_pred = model.predict(X_test)
    acc=accuracy_score(y_test,y_pred)
    print("Accuracy=",acc*100)


def chapter_10_2_naive_bayes():
    import pandas as pd
    df=pd.read_csv("D:\Downloads\weather_play.csv")
    print(df.shape)
    df

    x = df.drop('play',axis='columns')
    y=df['play']
    y

    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    x = x.apply(le.fit_transform)

    x

    from sklearn.naive_bayes import CategoricalNB
    model = CategoricalNB()
    model.fit(x,y)
    model.score(x,y)

    model.predict([[0,1,1,0]])

    print(y[12])