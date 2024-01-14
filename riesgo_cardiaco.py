import numpy as np
import pandas as pd
import json 

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    precision_recall_curve,
    roc_curve,
    auc
)
from tensorflow.keras.models import Sequential, save_model
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Cargamos los datos desde el archivo CSV
data = pd.read_csv('riesgocardiaco.csv')

# Corregir los nombres de las columnas para la normalización
columns_to_normalize = ['colesterol', 'presion', 'glucosa', 'edad']

# Escalamos solo las características seleccionadas
scaler = MinMaxScaler()
data[columns_to_normalize] = scaler.fit_transform(data[columns_to_normalize])

# Separamos los datos de las etiquetas
X = data.drop(['riesgo_cardiaco'], axis=1)
y = data['riesgo_cardiaco']

# Dividimos el conjunto de datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Creamos y compilamos el modelo de red neuronal
model = Sequential([
    Dense(100, input_shape=(X.shape[1],), activation='relu'),
    Dense(50, activation='relu'),
    Dense(25, activation='relu'),
    Dense(10, activation='relu'),
    Dense(5, activation='relu'),
    Dropout(0.2),
    Dense(1, activation='sigmoid')  # Usamos 'sigmoid' para la clasificación binaria
])

# Compilamos el modelo
model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.01), metrics=['accuracy'])
model.summary()

# Entrenamos la red neuronal
model.fit(X_train, y_train, verbose=2, batch_size=64, epochs=100)

# Evaluamos la red neuronal en el conjunto de prueba
y_pred = model.predict(X_test)
y_pred_classes = (y_pred > 0.5).astype("int32")  # Convertimos las probabilidades en clases binarias

# Calcular la probabilidad de pertenecer a la clase positiva
y_probs = model.predict(X_test)
# Calcular la tasa de verdaderos positivos y la tasa de falsos positivos
fpr, tpr, thresholds = roc_curve(y_test, y_probs)

# Calcular el área bajo la curva ROC
roc_auc = auc(fpr, tpr)

# Graficar la curva ROC
plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC)')
plt.legend(loc="lower right")
plt.show()

# Matriz de confusión y visualización
matriz_confusion = confusion_matrix(y_test, y_pred_classes)
sns.heatmap(matriz_confusion, annot=True, cmap='Blues', fmt='g')
plt.xlabel('Etiquetas Predichas')
plt.ylabel('Etiquetas Verdaderas')
plt.title('Matriz de Confusión')
plt.show()

# Calculamos y mostramos las métricas de evaluación
accuracy = accuracy_score(y_test, y_pred_classes)
precision = precision_score(y_test, y_pred_classes)
recall = recall_score(y_test, y_pred_classes)
f1 = f1_score(y_test, y_pred_classes)

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)

# Curva de Precisión-Recall
precision, recall, thresholds = precision_recall_curve(y_test, y_pred)
plt.figure(figsize=(8, 6))
plt.plot(recall, precision, marker='.')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Curva de Precisión-Recall')
plt.grid(True)
plt.show()

# Guardar el modelo en formato nativo de Keras
model.save('c:/topicos2/riesgo_cardiaco.keras')
