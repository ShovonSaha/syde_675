import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score

def print_evaluation_metrics(y_true, y_pred, model_name):
    """Prints common evaluation metrics for binary classification."""
    print(f"Model: {model_name}")
    print("Accuracy:", accuracy_score(y_true, y_pred))
    print("Classification Report:")
    print(classification_report(y_true, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_true, y_pred))
    try:
        # ROC-AUC score is only applicable for binary classification tasks
        # and when the true outcomes have a binary encoding.
        print("ROC-AUC Score:", roc_auc_score(y_true, y_pred))
    except ValueError as e:
        print(f"ROC-AUC score calculation not applicable: {e}")
    print("---------------------------------------------------\n")

# Load the dataset
csv_file_path = os.path.expanduser('~/SYDE675_project/syde_675_data/processed_pointclouds_combined/pca_features_with_labels.csv')
print("Loading dataset...")
data = pd.read_csv(csv_file_path)
print("Dataset loaded successfully.")

# Prepare the features (X) and the target (y)
X = data.drop(['label'], axis=1)
y = data['label']
print(f"Dataset shape: {X.shape}. Feature columns: {list(X.columns)}")

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Data split into training and testing sets. Training size: {X_train.shape[0]}, Testing size: {X_test.shape[0]}")

# Feature scaling
print("Applying feature scaling...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("Feature scaling applied.")

# Train and evaluate Random Forest Classifier
print("Training Random Forest Classifier...")
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train_scaled, y_train)
rf_predictions = rf_classifier.predict(X_test_scaled)
print_evaluation_metrics(y_test, rf_predictions, "Random Forest Classifier")

# # Train and evaluate Gradient Boosting Classifier
# print("Training Gradient Boosting Classifier...")
# gb_classifier = GradientBoostingClassifier(random_state=42)
# gb_classifier.fit(X_train_scaled, y_train)
# gb_predictions = gb_classifier.predict(X_test_scaled)
# print_evaluation_metrics(y_test, gb_predictions, "Gradient Boosting Classifier")
