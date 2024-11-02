# train_model.py

import os
from data_preprocessing import load_data, preprocess_data
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout
import joblib

def build_model(input_shape, num_classes):
    model = Sequential()
    model.add(Dense(256, activation='relu', input_shape=(input_shape,)))
    model.add(Dropout(0.5))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))

    # Compile the model
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def main():
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'Guitar Chords V2'))
    train_file_paths, train_labels, test_file_paths, test_labels = load_data(data_dir)
    X_train, X_test, y_train, y_test, label_encoder = preprocess_data(train_file_paths, train_labels, test_file_paths, test_labels)

    num_classes = len(label_encoder.classes_)
    input_shape = X_train.shape[1]

    model = build_model(input_shape, num_classes)

    # Train the model
    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

    # Evaluate the model
    test_loss, test_acc = model.evaluate(X_test, y_test)
    print("Neural Network Test Accuracy:", test_acc)

    # Save the model and label encoder
    model.save('guitar_note_model.h5')
    joblib.dump(label_encoder, 'label_encoder.joblib')

if __name__ == '__main__':
    main()
