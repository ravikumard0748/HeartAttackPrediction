# Import required libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
print("Loading data...")
data = pd.read_csv('datas/final_heart_data.csv')
print(f"Dataset shape: {data.shape}")

# Prepare features and target
print("\nPreparing features and target...")
X = data.drop(['Heart Attack Risk'], axis=1)
y = data['Heart Attack Risk']

# Split the data
print("\nSplitting data into train and test sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
print("\nScaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Create the model
print("\nCreating neural network model...")
model = models.Sequential([
    layers.Dense(32, activation='relu', input_shape=(X_train.shape[1],)),
    layers.Dropout(0.2),
    layers.Dense(16, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Calculate class weights
class_weights = dict(zip(
    np.unique(y_train),
    1 / np.bincount(y_train)
))
# Adjust weight for class 1 (multiply by 1.5 to give it more importance)
class_weights[1] *= 1.5

print("\nClass weights:", class_weights)

# Train the model with class weights
print("\nTraining the model...")
history = model.fit(
    X_train_scaled, 
    y_train,
    epochs=20,
    batch_size=32,
    validation_split=0.2,
    class_weight=class_weights,
    verbose=1
)

# Evaluate the model
print("\nEvaluating the model...")
test_loss, test_accuracy = model.evaluate(X_test_scaled, y_test)
print(f'Test accuracy: {test_accuracy:.4f}')

# Make predictions
y_pred = model.predict(X_test_scaled)
y_pred_classes = (y_pred > 0.5).astype(int)

# Print classification report
from sklearn.metrics import classification_report
print('\nClassification Report:')
print(classification_report(y_test, y_pred_classes))

# Plot results
plt.figure(figsize=(10, 4))

# Plot training history - Loss
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

# Plot training history - Accuracy
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.tight_layout()
plt.show()
