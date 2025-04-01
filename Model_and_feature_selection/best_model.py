import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.feature_selection import SelectFromModel
from imblearn.over_sampling import SMOTE
import joblib

# Load the data
data = pd.read_csv('../datas/final_heart_datas.csv')

# Drop the index column and separate features and target
data = data.drop('Unnamed: 0', axis=1)
X = data.iloc[:, :-1]  # All columns except the last one
y = data.iloc[:, -1]   # Last column is the target

# Convert to binary classification (high risk vs low risk)
# Values above 85 are considered high risk
y_binary = (y > 85).astype(int)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y_binary, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Apply SMOTE to balance the dataset
smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train_scaled, y_train)

# Initialize Random Forest for feature selection
rf_selector = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    random_state=42
)
rf_selector.fit(X_train_balanced, y_train_balanced)

# Select important features
selector = SelectFromModel(rf_selector, threshold='mean', prefit=True)
feature_idx = selector.get_support()
feature_names = X.columns[feature_idx]
print(f"\nNumber of selected features: {len(feature_names)}")

# Transform data with selected features
X_train_selected = selector.transform(X_train_balanced)
X_test_selected = selector.transform(X_test_scaled)

# Train the final model with selected features and optimized parameters
final_model = RandomForestClassifier(
    n_estimators=1000,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    max_features='sqrt',
    bootstrap=True,
    class_weight='balanced_subsample',  # Giving higher importance to class 1
    random_state=42,
    n_jobs=-1
)

# Perform cross-validation
cv_scores = cross_val_score(final_model, X_train_selected, y_train_balanced, cv=5)
print("\nCross-validation scores:", cv_scores)
print("Mean CV Score:", cv_scores.mean())
print("Standard deviation:", cv_scores.std())

# Train the final model
final_model.fit(X_train_selected, y_train_balanced)

# Make predictions
y_pred = final_model.predict(X_test_selected)
y_pred_proba = final_model.predict_proba(X_test_selected)[:, 1]

# Print results
print("\nSelected Features:")
print(feature_names.tolist())
print("\nFeature Importances:")
importances = dict(zip(feature_names, final_model.feature_importances_))
for feat, imp in sorted(importances.items(), key=lambda x: x[1], reverse=True):
    print(f"{feat}: {imp:.4f}")

print("\nModel Performance:")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"ROC AUC Score: {roc_auc_score(y_test, y_pred_proba):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# # Save the models and scaler
# joblib.dump(scaler, 'heart_attack_scaler.joblib')
# joblib.dump(selector, 'heart_attack_feature_selector.joblib')
# joblib.dump(final_model, 'heart_attack_model.joblib')
