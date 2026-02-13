import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model

# ===============================
# 1. DATA PATH
# ===============================

base_path = "data"

train_path = os.path.join(base_path, "train")
val_path = os.path.join(base_path, "val")
test_path = os.path.join(base_path, "test")

# ===============================
# 2. IMAGE PREPROCESSING
# ===============================

train_datagen = ImageDataGenerator(rescale=1./255)
val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_path,
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary'
)

val_generator = val_datagen.flow_from_directory(
    val_path,
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary'
)

# ===============================
# 3. LOAD PRETRAINED MODEL
# ===============================

base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224,224,3))
base_model.trainable = False

model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(1, activation='sigmoid')
])

model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# ===============================
# 4. TRAIN MODEL
# ===============================

history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=5
)

# ===============================
# 5. SAVE MODEL
# ===============================

model.save("accident_model.keras")
print("Model saved successfully!")

# ===============================
# 6. TEST ON VIDEO
# ===============================

model = load_model("accident_model.keras")

video_path = "test_video.mp4"   # Put your video in project folder
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    img = cv2.resize(frame, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)

    if prediction[0][0] > 0.5:
        label = "Accident"
        color = (0, 0, 255)
    else:
        label = "Non-Accident"
        color = (0, 255, 0)

    cv2.putText(frame, label, (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, color, 2)

    cv2.imshow("Accident Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
