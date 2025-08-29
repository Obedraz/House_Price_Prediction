# 1. Import Libraries
import pandas as pd
import numpy as np
from rdkit import Chem
from rdkit.Chem import Descriptors
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import RidgeClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, roc_auc_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# 2. Load Dataset
data = pd.read_csv('bioassay_data.csv')  # Ensure you have SMILES + Activity (1=active, 0=inactive)

# 3. Feature Extraction (Molecular Descriptors)
def calc_descriptors(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        return [Descriptors.MolWt(mol), Descriptors.MolLogP(mol), Descriptors.NumHDonors(mol), Descriptors.NumHAcceptors(mol)]
    else:
        return [np.nan, np.nan, np.nan, np.nan]

features = data['SMILES'].apply(calc_descriptors)
desc_df = pd.DataFrame(features.tolist(), columns=['MolWt', 'LogP', 'HDonors', 'HAcceptors'])
data = pd.concat([data, desc_df], axis=1).dropna()

X = data[['MolWt', 'LogP', 'HDonors', 'HAcceptors']]
y = data['Activity']

# 4. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5a. Decision Tree
dt = DecisionTreeClassifier()
dt.fit(X_train, y_train)
y_pred_dt = dt.predict(X_test)
print("Decision Tree Accuracy:", accuracy_score(y_test, y_pred_dt))
print("Decision Tree AUC:", roc_auc_score(y_test, dt.predict_proba(X_test)[:, 1]))

# 5b. Ridge Regression
ridge = RidgeClassifier()
ridge.fit(X_train, y_train)
y_pred_ridge = ridge.predict(X_test)
print("Ridge Accuracy:", accuracy_score(y_test, y_pred_ridge))

# 5c. ANN
model = Sequential([
    Dense(16, input_dim=X_train.shape[1], activation='relu'),
    Dense(8, activation='relu'),
    Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=20, batch_size=16, verbose=0)
ann_loss, ann_acc = model.evaluate(X_test, y_test)
y_pred_ann = model.predict(X_test).ravel()
print("ANN Accuracy:", ann_acc)
print("ANN AUC:", roc_auc_score(y_test, y_pred_ann))

# 5d. Clustering (KMeans)
kmeans = KMeans(n_clusters=2, random_state=42)
clusters = kmeans.fit_predict(X)
# Evaluate how clusters align with real labels
cluster_acc = accuracy_score(y, clusters)
print("KMeans Clustering Accuracy (approximation):", cluster_acc)