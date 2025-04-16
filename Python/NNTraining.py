from keras import Input
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import dataPreProcessing
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


def trainNN(data, plotData=None):
    excludeColumns = ["activeCube", "activeCubeX", "activeCubeY", "GoalGesture"]
    dfNormalized = dataPreProcessing.standardizeDataframe(data, excludeColumns)

    X = dfNormalized.drop(columns=excludeColumns)
    Y = dfNormalized['GoalGesture']

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42, stratify=Y)

    Y_train = to_categorical(Y_train)
    Y_test = to_categorical(Y_test)

    model = Sequential([
        Input(shape=(X_train.shape[1],)),
        Dense(128, activation='relu'),
        Dropout(0.3),
        Dense(64, activation='relu'),
        Dropout(0.3),
        Dense(Y_train.shape[1], activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    history = model.fit(X_train, Y_train, validation_split=0.2, epochs=50, batch_size=32, verbose=1)

    if plotData:
        # Plot the learning curve (accuracy)
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.plot(history.history['accuracy'], label='Training Accuracy')
        plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
        plt.title('Accuracy over Epochs')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend()

        # Plot the learning curve (loss)
        plt.subplot(1, 2, 2)
        plt.plot(history.history['loss'], label='Training Loss')
        plt.plot(history.history['val_loss'], label='Validation Loss')
        plt.title('Loss over Epochs')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()

        plt.show()

    yPredProbs = model.predict(X_test)
    yPred = yPredProbs.argmax(axis=1)
    yTrue = Y_test.argmax(axis=1)

    print("Test Accuracy:", accuracy_score(yTrue, yPred))
    print("Confusion Matrix:")
    print(confusion_matrix(yTrue, yPred))
    print("Classification Report:")
    print(classification_report(yTrue, yPred))

    model.save("NeuralNetworkModel.h5")
    print("trained and saved neural network model")
