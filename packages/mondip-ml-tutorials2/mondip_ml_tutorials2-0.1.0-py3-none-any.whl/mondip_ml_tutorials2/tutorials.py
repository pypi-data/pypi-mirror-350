# 1. NumPy Operations
def numpy_ops():
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

# 2. Matplotlib Plotting
def plot_charts():
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

# 3. Pandas Data Analysis
def pandas_analysis():
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

    mydata= pd.read_csv("C:/Users/Asus/Desktop/College/GJK/csv/income_expense.csv")
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

# 4. Data Preprocessing and Linear Regression
def linear_reg():
    from sklearn.datasets import load_breast_cancer
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder
    from sklearn.linear_model import LinearRegression
    import pandas as pd

    # Load dataset
    bc = load_breast_cancer()
    x, y = bc.data, bc.target
    print("Features:", bc.feature_names)
    print("Targets:", bc.target_names)
    df = pd.DataFrame(x, columns=bc.feature_names)
    print(df["mean radius"].describe())

    # Train-test split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

    # Sample data
    mydata = pd.DataFrame([[21,45000,"govt"],[33,42000,"private"],[18,30000,"semi-govt"],
                           [36,53000,"private"],[45,55000,"govt"],[34,48000,"semi-govt"]],
                          columns=["age", "salary", "job"])

    # Scaling
    print("MinMax:\n", MinMaxScaler().fit_transform(mydata.iloc[:, :2]))
    print("Standard:\n", StandardScaler().fit_transform(mydata.iloc[:, :2]))

    # Label encoding
    le = LabelEncoder()
    encoded = le.fit_transform(mydata["job"])
    print("Encoded jobs:", encoded)
    print("Classes:", le.classes_)

    # Linear Regression
    data = pd.read_csv("C:/Users/Asus/Desktop/College/GJK/csv/Linear_Simple_Salary_Data.csv")
    x, y = data.drop("Salary", axis=1), data["Salary"]
    model = LinearRegression().fit(x, y)
    print("Score:", model.score(x, y))
    print("Predict 7.5:", model.predict([[7.5]]))
    print("Coef:", model.coef_, "Intercept:", model.intercept_)
    print(f"Formula: y = {model.coef_[0]} * x + {model.intercept_}")

# 5. KNN Classification
def knn_model():
    import matplotlib.pyplot as plt
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.metrics import confusion_matrix, classification_report
    import numpy as np

    iris = load_iris()
    X, Y = iris.data, iris.target

    plt.xlabel("Petal Length")
    plt.ylabel("Petal Width")
    colors = ["green", "blue", "red"]
    for i, c in enumerate(colors):
        plt.scatter(X[Y==i, 2], X[Y==i, 3], color=c, marker="+")
    plt.show()

    X = StandardScaler().fit_transform(X)
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=1)

    model = KNeighborsClassifier(n_neighbors=33).fit(x_train, y_train)
    y_pred = model.predict(x_test)
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    errors = [np.mean(KNeighborsClassifier(n_neighbors=k).fit(x_train, y_train).predict(x_test) != y_test) for k in range(1,60)]
    plt.plot(range(1, 60), errors, 'ro--', markerfacecolor="blue")
    plt.title("Error Rate vs. K Value")
    plt.xlabel("K Value")
    plt.ylabel("Mean Error")
    plt.show()

# 6. Decision Trees - Weather Data
def dt_weather():
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.preprocessing import LabelEncoder
    from sklearn import tree

    # Load data
    df = pd.read_csv("C:/Users/Asus/Desktop/College/GJK/csv/weather_play.csv")
    X = df.drop('play', axis=1)
    y = df['play']

    # Encode features
    for col in X.columns:
        X[col] = LabelEncoder().fit_transform(X[col])

    # Train decision tree
    model = tree.DecisionTreeClassifier(criterion='entropy')
    model.fit(X, y)

    # Predict and plot
    print("Prediction:", model.predict([[0, 1, 1, 0]]))  # Example input
    tree.plot_tree(model, feature_names=X.columns, class_names=model.classes_, filled=True)
    plt.show()

# 7. Decision Trees - Iris Dataset
def dt_iris():
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    from sklearn.tree import DecisionTreeClassifier, plot_tree
    from sklearn.metrics import accuracy_score
    import matplotlib.pyplot as plt

    x, y = load_iris(return_X_y=True)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)

    # Accuracy vs. max_depth
    acc = [accuracy_score(y_test, DecisionTreeClassifier(max_depth=i, random_state=0).fit(x_train, y_train).predict(x_test)) for i in range(1, 11)]
    plt.plot(range(1, 11), acc, 'bo-')

    # Final model
    model = DecisionTreeClassifier(criterion='entropy', max_depth=4, random_state=0)
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    print(f"Accuracy: {accuracy_score(y_test, pred)*100:.2f}%")
    print("Test sample:", x_test[3])
    print("Actual:", y_test[3], "Predicted:", model.predict([x_test[3]])[0])

    # Plot tree
    plt.figure(figsize=(12, 6))
    plot_tree(model, filled=True)
    plt.show()

# 8. K-Means Clustering
def kmeans_cluster():
    import pandas as pd
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import MinMaxScaler
    import matplotlib.pyplot as plt

    # Load and scale data
    df = pd.read_csv("C:/Users/Asus/Desktop/College/GJK/csv/IncomeKMean.csv")
    for col in ['Income', 'Age']:
        df[col] = MinMaxScaler().fit_transform(df[[col]])

    # Initial scatter plot
    plt.scatter(df["Age"], df["Income"])
    plt.xlabel("Age")
    plt.ylabel("Income")
    plt.show()

    # KMeans clustering
    kmeans = KMeans(n_clusters=3)
    df['cluster'] = kmeans.fit_predict(df[['Age', 'Income']])

    # Clustered plot
    colors = ['green', 'red', 'blue']
    for i in range(3):
        plt.scatter(df[df.cluster == i].Age, df[df.cluster == i].Income, color=colors[i], label=f'Cluster {i}')
    plt.scatter(*kmeans.cluster_centers_.T, color='purple', marker='*', s=200, label='Centroids')
    plt.legend()
    plt.show()

    # Elbow method
    sse = [KMeans(n_clusters=k).fit(df[['Age', 'Income']]).inertia_ for k in range(1, 10)]
    plt.plot(range(1, 10), sse, marker='o')
    plt.xlabel('K')
    plt.ylabel('SSE')
    plt.title('Elbow Method')
    plt.show()

# 9. SVM Classification
def svm_model():
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.datasets import load_digits
    from sklearn.model_selection import train_test_split
    from sklearn import svm
    from sklearn.metrics import accuracy_score

    # Load and reshape data
    digits = load_digits()
    X, y = digits.images.reshape(len(digits.images), -1), digits.target

    # Display a digit
    idx = 1109
    plt.gray()
    plt.matshow(digits.images[idx])
    plt.show()
    print("Label:", y[idx])

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    # Train linear SVM and predict one sample
    model = svm.SVC(kernel='linear').fit(X_train, y_train)
    idx = 309
    print("Predicted:", model.predict([digits.images[idx].ravel()])[0])
    plt.matshow(digits.images[idx])
    plt.show()

    # Accuracy and sample prediction comparison
    y_pred = model.predict(X_test)
    print("Sample preds vs actual:\n", np.c_[y_pred[111:114], y_test[111:114]])
    print("Accuracy: {:.2f}%".format(accuracy_score(y_test, y_pred) * 100))

    # Multiple SVM models with different kernels/settings
    models = [
        svm.SVC(kernel='linear'),
        svm.SVC(kernel='rbf'),
        svm.SVC(gamma=0.003),
        svm.SVC(gamma=0.001, C=0.1)
    ]
    for i, m in enumerate(models, 1):
        m.fit(X_train, y_train)
        acc = accuracy_score(y_test, m.predict(X_test)) * 100
        print(f"Model {i} accuracy: {acc:.2f}%")

# 10. Random Forest
def rf_model():
    import matplotlib.pyplot as plt
    from sklearn.datasets import load_digits
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score

    # Load data
    digits = load_digits()
    X, y = digits.data, digits.target

    # Display one sample
    plt.gray()
    plt.matshow(digits.images[109])
    plt.show()

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Train base model
    model = RandomForestClassifier(n_estimators=20).fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("Accuracy =", accuracy_score(y_test, y_pred) * 100)

    # Compare models with different estimators
    for n in [10, 15, 20, 25]:
        m = RandomForestClassifier(n_estimators=n).fit(X_train, y_train)
        acc = accuracy_score(y_test, m.predict(X_test)) * 100
        print(f"Accuracy with {n} estimators: {acc:.2f}%")

# 11. Naive Bayes - Titanic
def nb_titanic():
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.naive_bayes import GaussianNB
    from sklearn.metrics import accuracy_score

    df = pd.read_csv("C:/Users/Asus/Desktop/College/GJK/csv/titanic.csv")
    df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})
    df.drop(columns=['Ticket', 'Cabin', 'Embarked', 'Name'], inplace=True)
    df.dropna(inplace=True)

    x, y = df.drop("Survived", axis=1), df["Survived"]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=9)

    model = GaussianNB().fit(x_train, y_train)
    pred = model.predict(x_test)
    print("Accuracy =", accuracy_score(y_test, pred) * 100)

# 12. Naive Bayes - Weather
def nb_weather():
    import pandas as pd
    from sklearn.preprocessing import LabelEncoder
    from sklearn.naive_bayes import CategoricalNB

    df = pd.read_csv("C:/Users/Asus/Desktop/College/GJK/csv/weather_play.csv")
    x, y = df.drop('play', axis=1), df['play']
    x = x.apply(LabelEncoder().fit_transform)

    model = CategoricalNB().fit(x, y)
    print("Score:", model.score(x, y))
    print("Prediction:", model.predict([[0,1,1,0]]))
    print("Actual:", y.iloc[12])