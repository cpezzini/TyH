ADR #3: Red Neuronal para Predicción de Riesgo Cardíaco

Estado: Aceptada

Contexto
Para el problema de predicción de riesgo cardíaco se utilizó un enfoque de machine learning para clasificar los datos de salud. Se empleó una red neuronal con TensorFlow y Keras.

Decisiones
Se optó por utilizar una red neuronal implementada con TensorFlow y Keras para resolver el problema de clasificación de riesgo cardíaco.

Modelo de Red Neuronal: Se utilizó un modelo secuencial con capas y funciones de activación ReLU.
Compilación y Entrenamiento: El modelo se compiló con la función de pérdida 'binary_crossentropy' y el optimizador Adam, y se entrenó durante 100 épocas con un tamaño de lote de 64.

Resultados y Evaluación
Se realizaron varias evaluaciones para medir el rendimiento del modelo:

Gráfica ROC: Se genera la curva ROC para evaluar la capacidad del modelo para distinguir entre clases.
Matriz de Confusión: Se visualiza la matriz de confusión para analizar el rendimiento en la clasificación.
Métricas de Evaluación: Se calculan métricas como precisión, recall, F1-score y accuracy para evaluar el desempeño del modelo.

Consecuencias
Rendimiento del Modelo: La red neuronal muestra una buena evaluación en métricas estándar de clasificación.

Aplicación Práctica: Este enfoque permite una identificación más precisa del riesgo cardíaco basado en datos de salud.

Consideraciones Futuras
Optimización del Modelo: Explorar estrategias de optimización para mejorar el rendimiento del modelo en la predicción de riesgo cardíaco.
Despliegue Eficiente: Planificar un despliegue eficiente del modelo para su uso práctico en entornos de producción.