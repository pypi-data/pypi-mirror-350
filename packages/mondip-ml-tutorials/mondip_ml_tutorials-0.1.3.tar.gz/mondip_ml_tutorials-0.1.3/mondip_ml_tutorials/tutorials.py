import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler
from sklearn.datasets import load_breast_cancer, load_iris, load_digits
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.cluster import KMeans
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB, CategoricalNB

def chapter_1_numpy():
    """Chapter 1: NumPy Fundamentals"""
    print("=== Chapter 1: NumPy ===")
    print(f"NumPy version: {np.__version__}")
    
    # Basic array creation and properties
    arr1 = np.array([1, 2, 3, 4, 5, 6])
    print(f"Array: {arr1}")
    print(f"Data type: {arr1.dtype}")
    print(f"Shape: {arr1.shape}")
    
    # 2D array
    arr2 = np.array([[1.1, 1.2, 3.4], [2.1, 7.2, 2.3]])
    print(f"2D Array:\n{arr2}")
    print(f"Data type: {arr2.dtype}")
    print(f"Shape: {arr2.shape}")
    
    # Array from list
    lst = [[1, 2, 3], [11, 12, 13], [21, 22, 23], [31, 32, 33]]
    arr = np.array(lst)
    print(f"Array from list:\n{arr}")
    
    # Indexing and slicing
    print(f"First row: {arr[0]}")
    print(f"Element [1,2]: {arr[1, 2]}")
    print(f"Second row: {arr[1, :]}")
    print(f"First column: {arr[:, 0]}")
    print(f"Slice [2, 1:3]: {arr[2, 1:3]}")
    
    # Advanced indexing
    x = arr[:, 0:2]
    y = arr[:, -1]
    print(f"First two columns:\n{x}")
    print(f"Last column: {y}")
    
    # Conditional indexing
    print(f"Elements divisible by 3: {arr[arr % 3 == 0]}")
    print(f"Elements > 10: {arr[arr > 10]}")
    
    # Statistical operations
    print(f"Sum: {np.sum(arr)}")
    print(f"Min: {np.min(arr)}")
    print(f"Mean: {np.mean(arr)}")
    print(f"Median: {np.median(arr)}")
    print(f"Standard deviation: {np.std(arr)}")
    print(f"50th percentile: {np.percentile(arr, 50)}")
    
    # Axis operations
    print(f"Sum of columns: {np.sum(arr, axis=0)}")
    print(f"Sum of rows: {np.sum(arr, axis=1)}")
    print(f"Mean of columns: {np.mean(arr, axis=0)}")

def chapter_2_pandas():
    """Chapter 2: Pandas Data Manipulation"""
    print("\n=== Chapter 2: Pandas ===")
    print(f"Pandas version: {pd.__version__}")
    
    # Create DataFrame
    df1 = pd.DataFrame([[1, 2, 3], [7, 4, 9], [3, 9, 2], [1, 8, 4], [2, 6, 5], [5, 8, 3]])
    print(f"DataFrame:\n{df1}")
    print(f"Shape: {df1.shape}")
    
    # Head and tail
    print(f"Head (3 rows):\n{df1.head(3)}")
    print(f"Tail (3 rows):\n{df1.tail(3)}")
    
    # Indexing
    print(f"First column:\n{df1[0]}")
    print(f"Element [1,2]: {df1.iloc[1, 2]}")
    print(f"Second row: {df1.iloc[2, :].values}")
    print(f"First column: {df1.iloc[:, 0].values}")
    print(f"Slice [1:4, 1:3]:\n{df1.iloc[1:4, 1:3]}")
    
    # Note: File operations would require actual CSV files
    print("Note: CSV file operations require actual files (income_expense.csv)")

def chapter_3_matplotlib():
    """Chapter 3: Matplotlib Visualization"""
    print("\n=== Chapter 3: Matplotlib ===")
    print(f"Matplotlib version: {plt.matplotlib.__version__}")
    
    # Line plot
    xpoints = np.array([0, 2, 4, 6])
    ypoints = np.array([0, 75, 100, 250])
    
    plt.figure(figsize=(12, 10))
    
    plt.subplot(2, 2, 1)
    plt.title("Basic Line Plot")
    plt.xlabel("X - Label")
    plt.ylabel("Y - Label")
    plt.plot(xpoints, ypoints)
    
    # Styled line plot
    x = np.array([1, 3, 5, 7])
    y = np.array([25, 85, 140, 240])
    plt.subplot(2, 2, 2)
    plt.title("Styled Line Plot")
    plt.plot(x, y, marker='o', ms=10, mec='r', mfc='r', linestyle='dotted', color='b', linewidth=3)
    
    # Scatter plot
    x_scatter = np.array([5, 7, 8, 7, 2, 17, 2, 9, 4, 11, 12, 9, 6])
    y_scatter = np.array([99, 86, 87, 88, 111, 86, 103, 87, 94, 78, 77, 85, 86])
    plt.subplot(2, 2, 3)
    plt.title("Scatter Plot")
    plt.scatter(x_scatter, y_scatter)
    
    # Bar plot
    x_bar = np.array(["A", "B", "C", "D"])
    y_bar = np.array([30, 58, 45, 60])
    plt.subplot(2, 2, 4)
    plt.title("Bar Plot")
    plt.bar(x_bar, y_bar)
    
    plt.tight_layout()
    plt.show()
    
    # Pie chart
    plt.figure(figsize=(6, 6))
    y_pie = np.array([15, 35, 20, 30])
    plt.pie(y_pie, labels=['A', 'B', 'C', 'D'], autopct='%1.1f%%')
    plt.title("Pie Chart")
    plt.show()

def chapter_4_sklearn_basics():
    """Chapter 4: Scikit-learn Basics"""
    print("\n=== Chapter 4: Scikit-learn Basics ===")
    
    # Note: This requires actual CSV file
    print("Linear Regression example (requires Linear_Simple_Salary_Data.csv)")
    
    # Label Encoding example
    mydata = pd.DataFrame([
        [21, 45000, "govt"],
        [33, 42000, "private"],
        [18, 30000, "semi-govt"],
        [36, 53000, "private"],
        [45, 55000, "govt"],
        [34, 48000, "semi-govt"]
    ], columns=["age", "salary", "job"])
    
    le = LabelEncoder()
    encoded = le.fit_transform(mydata["job"])
    print(f"Encoded jobs: {encoded}")
    print(f"Classes: {le.classes_}")
    
    # Breast cancer dataset
    bc = load_breast_cancer()
    x, y = bc.data, bc.target
    print(f"Features: {bc.feature_names[:5]}...")  # Show first 5 features
    print(f"Targets: {bc.target_names}")
    
    # Train-test split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)
    print(f"Training set size: {x_train.shape[0]}, Test set size: {x_test.shape[0]}")
    
    # Scaling examples
    print("MinMax Scaling:")
    print(MinMaxScaler().fit_transform(mydata[["age", "salary"]])[:3])  # Show first 3 rows
    print("Standard Scaling:")
    print(StandardScaler().fit_transform(mydata[["age", "salary"]])[:3])  # Show first 3 rows

def chapter_5_knn():
    """Chapter 5: K-Nearest Neighbors"""
    print("\n=== Chapter 5: KNN ===")
    
    iris = load_iris()
    X, Y = iris.data, iris.target
    
    # Visualization
    plt.figure(figsize=(10, 4))
    
    plt.subplot(1, 2, 1)
    colors = ["green", "blue", "red"]
    for i, c in enumerate(colors):
        plt.scatter(X[Y == i, 2], X[Y == i, 3], color=c, marker="+", label=f"Class {i}")
    plt.xlabel("Petal Length")
    plt.ylabel("Petal Width")
    plt.title("Iris Dataset")
    plt.legend()
    
    # Preprocessing and model training
    X_scaled = StandardScaler().fit_transform(X)
    x_train, x_test, y_train, y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=1)
    
    model = KNeighborsClassifier(n_neighbors=5).fit(x_train, y_train)
    y_pred = model.predict(x_test)
    print(f"Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}")
    print(f"Classification Report:\n{classification_report(y_test, y_pred)}")
    
    # Error rate vs K value
    errors = []
    k_range = range(1, 21)
    for k in k_range:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(x_train, y_train)
        y_pred_k = knn.predict(x_test)
        errors.append(np.mean(y_pred_k != y_test))
    
    plt.subplot(1, 2, 2)
    plt.plot(k_range, errors, 'ro--', markerfacecolor="blue")
    plt.title("Error Rate vs. K Value")
    plt.xlabel("K Value")
    plt.ylabel("Mean Error")
    plt.tight_layout()
    plt.show()

def chapter_6_decision_tree():
    """Chapter 6: Decision Tree Classifier"""
    print("\n=== Chapter 6: Decision Tree ===")
    
    x, y = load_iris(return_X_y=True)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)
    
    # Test different max_depth values
    accuracies = []
    depth_range = range(1, 11)
    for d in depth_range:
        dt = DecisionTreeClassifier(max_depth=d, random_state=0)
        dt.fit(x_train, y_train)
        pred = dt.predict(x_test)
        accuracies.append(accuracy_score(y_test, pred))
    
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(depth_range, accuracies, 'bo-')
    plt.title("Accuracy vs Max Depth")
    plt.xlabel("Max Depth")
    plt.ylabel("Accuracy")
    
    # Best model
    model = DecisionTreeClassifier(criterion='entropy', max_depth=4, random_state=0)
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    print(f"Accuracy: {accuracy_score(y_test, pred)*100:.2f}%")
    
    if len(x_test) > 3:
        print(f"Test sample: {x_test[3]}")
        print(f"Actual: {y_test[3]}, Predicted: {model.predict([x_test[3]])[0]}")
    
    # Visualize tree
    plt.subplot(1, 2, 2)
    plot_tree(model, filled=True, max_depth=2, fontsize=8)  # Limit depth for readability
    plt.title("Decision Tree Visualization")
    plt.tight_layout()
    plt.show()
    
    print("Note: Weather data example requires weather_play.csv file")

def chapter_7_kmeans():
    """Chapter 7: K-Means Clustering"""
    print("\n=== Chapter 7: K-Means ===")
    
    # Generate sample data (since CSV file is not available)
    np.random.seed(42)
    ages = np.random.uniform(20, 60, 100)
    incomes = np.random.uniform(20000, 80000, 100) + ages * 500  # Some correlation
    
    df = pd.DataFrame({'Age': ages, 'Income': incomes})
    
    # Normalize data
    scaler = MinMaxScaler()
    df[['Income', 'Age']] = scaler.fit_transform(df[['Income', 'Age']])
    
    plt.figure(figsize=(12, 4))
    
    # Original data
    plt.subplot(1, 3, 1)
    plt.scatter(df["Age"], df["Income"])
    plt.xlabel("Age (normalized)")
    plt.ylabel("Income (normalized)")
    plt.title("Original Data")
    
    # K-means clustering
    kmeans = KMeans(n_clusters=3, random_state=42)
    df['cluster'] = kmeans.fit_predict(df[['Age', 'Income']])
    
    # Clustered data
    plt.subplot(1, 3, 2)
    colors = ['green', 'red', 'blue']
    for i, c in enumerate(colors):
        cluster_data = df[df.cluster == i]
        plt.scatter(cluster_data.Age, cluster_data.Income, color=c, label=f'Cluster {i}')
    
    centroids = kmeans.cluster_centers_
    plt.scatter(centroids[:, 0], centroids[:, 1], color='purple', marker='*', s=200, label='Centroids')
    plt.xlabel("Age (normalized)")
    plt.ylabel("Income (normalized)")
    plt.title("K-Means Clustering")
    plt.legend()
    
    # Elbow method
    sse = []
    k_range = range(1, 10)
    for k in k_range:
        kmeans_temp = KMeans(n_clusters=k, random_state=42)
        kmeans_temp.fit(df[['Age', 'Income']])
        sse.append(kmeans_temp.inertia_)
    
    plt.subplot(1, 3, 3)
    plt.plot(k_range, sse, marker='o')
    plt.xlabel('K')
    plt.ylabel('SSE')
    plt.title('Elbow Method')
    plt.tight_layout()
    plt.show()

def chapter_8_svm():
    """Chapter 8: Support Vector Machine"""
    print("\n=== Chapter 8: SVM ===")
    
    digits = load_digits()
    X = digits.images.reshape(len(digits.images), -1)
    y = digits.target
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    
    models = [
        ("Linear SVM", svm.SVC(kernel='linear')),
        ("RBF SVM", svm.SVC(kernel='rbf')),
        ("RBF SVM (gamma=0.003)", svm.SVC(gamma=0.003)),
        ("RBF SVM (gamma=0.001, C=0.1)", svm.SVC(gamma=0.001, C=0.1))
    ]
    
    print("SVM Model Comparison:")
    for name, model in models:
        model.fit(X_train, y_train)
        accuracy = accuracy_score(y_test, model.predict(X_test))
        print(f"{name}: {accuracy*100:.2f}%")
    
    # Show a sample digit
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)
    plt.imshow(digits.images[0], cmap='gray')
    plt.title(f"Sample Digit: {digits.target[0]}")
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(digits.images[100], cmap='gray')
    plt.title(f"Sample Digit: {digits.target[100]}")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def chapter_9_random_forest():
    """Chapter 9: Random Forest"""
    print("\n=== Chapter 9: Random Forest ===")
    
    digits = load_digits()
    X, y = digits.data, digits.target
    
    # Show sample digit
    plt.figure(figsize=(6, 3))
    plt.subplot(1, 2, 1)
    plt.imshow(digits.images[109], cmap='gray')
    plt.title(f"Sample Digit: {digits.target[109]}")
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(digits.images[50], cmap='gray')
    plt.title(f"Sample Digit: {digits.target[50]}")
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    estimator_values = [10, 15, 20, 25, 50, 100]
    print("Random Forest Performance:")
    for n in estimator_values:
        model = RandomForestClassifier(n_estimators=n, random_state=42)
        model.fit(X_train, y_train)
        accuracy = accuracy_score(y_test, model.predict(X_test))
        print(f"Estimators={n}: Accuracy={accuracy*100:.2f}%")

def chapter_10_naive_bayes():
    """Chapter 10: Naive Bayes"""
    print("\n=== Chapter 10: Naive Bayes ===")
    
    # Generate sample data (since titanic.csv is not available)
    np.random.seed(42)
    n_samples = 1000
    
    sample_data = {
        'Pclass': np.random.choice([1, 2, 3], n_samples),
        'Sex': np.random.choice([0, 1], n_samples),  # 0=male, 1=female
        'Age': np.random.uniform(5, 80, n_samples),
        'SibSp': np.random.poisson(0.5, n_samples),
        'Parch': np.random.poisson(0.4, n_samples),
        'Fare': np.random.exponential(30, n_samples),
    }
    
    # Create survival based on some logical rules
    survival_prob = (sample_data['Sex'] * 0.7 + 
                    (sample_data['Pclass'] == 1) * 0.3 + 
                    (sample_data['Age'] < 15) * 0.2)
    sample_data['Survived'] = np.random.binomial(1, np.clip(survival_prob, 0, 1), n_samples)
    
    df = pd.DataFrame(sample_data)
    
    X = df.drop("Survived", axis=1)
    y = df["Survived"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=9)
    
    model = GaussianNB()
    model.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test))
    print(f"Gaussian Naive Bayes Accuracy: {accuracy*100:.2f}%")
    
    # Categorical Naive Bayes example
    print("\nCategorical Naive Bayes (requires weather_play.csv)")
    
    # Sample weather data
    weather_data = pd.DataFrame([
        ['sunny', 'hot', 'high', 'weak', 'no'],
        ['sunny', 'hot', 'high', 'strong', 'no'],
        ['overcast', 'hot', 'high', 'weak', 'yes'],
        ['rain', 'mild', 'high', 'weak', 'yes'],
        ['rain', 'cool', 'normal', 'weak', 'yes'],
        ['rain', 'cool', 'normal', 'strong', 'no'],
        ['overcast', 'cool', 'normal', 'strong', 'yes'],
        ['sunny', 'mild', 'high', 'weak', 'no'],
        ['sunny', 'cool', 'normal', 'weak', 'yes'],
        ['rain', 'mild', 'normal', 'weak', 'yes'],
        ['sunny', 'mild', 'normal', 'strong', 'yes'],
        ['overcast', 'mild', 'high', 'strong', 'yes'],
        ['overcast', 'hot', 'normal', 'weak', 'yes'],
        ['rain', 'mild', 'high', 'strong', 'no']
    ], columns=['outlook', 'temp', 'humidity', 'wind', 'play'])
    
    x_weather = weather_data.drop('play', axis=1)
    y_weather = weather_data['play']
    
    # Encode categorical variables
    le = LabelEncoder()
    x_weather_encoded = x_weather.apply(lambda col: le.fit_transform(col))
    
    model_cat = CategoricalNB()
    model_cat.fit(x_weather_encoded, y_weather)
    
    print(f"Weather Play Prediction Score: {model_cat.score(x_weather_encoded, y_weather):.3f}")
    
    # Make a prediction
    sample_prediction = model_cat.predict([[0, 1, 1, 0]])  # encoded features
    print(f"Sample prediction: {sample_prediction[0]}")

def run_all_chapters():
    """Run all chapters sequentially"""
    chapters = [
        chapter_1_numpy,
        chapter_2_pandas,
        chapter_3_matplotlib,
        chapter_4_sklearn_basics,
        chapter_5_knn,
        chapter_6_decision_tree,
        chapter_7_kmeans,
        chapter_8_svm,
        chapter_9_random_forest,
        chapter_10_naive_bayes
    ]
    
    for chapter in chapters:
        try:
            chapter()
            print("\n" + "="*50 + "\n")
        except Exception as e:
            print(f"Error in {chapter.__name__}: {e}")
            print("\n" + "="*50 + "\n")

def mondip():
    """Original function that now calls organized chapters"""
    print("Running all Data Science chapters...")
    run_all_chapters()
    print("mondip")

if __name__ == "__main__":
    # You can run individual chapters or all at once
    # mondip()  # Run all chapters
    
    # Or run individual chapters:
    # chapter_1_numpy()
    # chapter_3_matplotlib()
    pass
