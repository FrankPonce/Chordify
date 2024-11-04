# train_model.py

import os
from data_preprocessing import load_data, preprocess_data
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout, Conv1D, MaxPooling1D, Flatten, BatchNormalization
import joblib
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

def build_cnn_model(input_shape, num_classes):
    model = Sequential()
    model.add(Conv1D(32, kernel_size=3, activation='relu', input_shape=input_shape))
    model.add(BatchNormalization())
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.25))

    model.add(Conv1D(64, kernel_size=3, activation='relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))

    model.add(Dense(num_classes, activation='softmax'))
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def main():
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'Guitar Chords V2'))
    train_file_paths, train_labels, test_file_paths, test_labels = load_data(data_dir)
    X_train, X_test, y_train, y_test, label_encoder = preprocess_data(train_file_paths, train_labels, test_file_paths, test_labels)

    # Feature scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Reshape for Conv1D
    X_train_scaled = X_train_scaled.reshape(-1, X_train_scaled.shape[1], 1)
    X_test_scaled = X_test_scaled.reshape(-1, X_test_scaled.shape[1], 1)

    num_classes = len(label_encoder.classes_)
    input_shape = (X_train_scaled.shape[1], 1)

    model = build_cnn_model(input_shape, num_classes)

    # Callbacks
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    model_checkpoint = ModelCheckpoint('guitar_note_model.h5', save_best_only=True)

    # Train the model
    model.fit(X_train_scaled, y_train, epochs=50, batch_size=32, validation_data=(X_test_scaled, y_test), callbacks=[early_stopping, model_checkpoint])

    # Evaluate the model
    test_loss, test_acc = model.evaluate(X_test_scaled, y_test)
    print("CNN Test Accuracy:", test_acc)

    # Save the label encoder and scaler
    joblib.dump(label_encoder, 'label_encoder.joblib')
    joblib.dump(scaler, 'scaler.joblib')

if __name__ == '__main__':
    main()
