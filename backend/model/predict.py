import cv2
import numpy as np
import tensorflow as tf
import os

# Load Model
model_path = r"C:\dev\Project2\backend\model\frozen_model\saved_model"
model = tf.saved_model.load(model_path) 
def predict_varicose(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (640, 640))
    img = img / 255.0  # Normalize

    input_tensor = tf.convert_to_tensor([img], dtype=tf.float32)

    # Run model
    outputs = model(input_tensor)

    # Extract confidence score (Example: You may need to modify this based on your model output)
    confidence = np.mean(outputs['output_layer'][0].numpy()) * 100  # Convert to percentage

    prediction = "Yes" if confidence > 60 else "No"

    # Save Processed Image with Bounding Boxes
    processed_img_path = image_path.replace(".jpg", "_processed.jpg")
    cv2.putText(img, f"Prediction: {prediction}, {confidence:.2f}%", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imwrite(processed_img_path, img)

    return prediction, confidence, processed_img_path
