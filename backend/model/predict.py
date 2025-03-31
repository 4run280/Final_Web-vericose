# import tensorflow as tf
# import numpy as np
# from keras.layers import TFSMLayer
# import cv2

# model = tf.keras.models.load_model("model/frozen_model/saved_model")

# def predict_varicose(image_path):
#     img = cv2.imread(image_path)
#     img = cv2.resize(img, (224, 224))
#     img = np.expand_dims(img, axis=0) / 255.0

#     prediction = model.predict(img)
#     return "Varicose Veins Detected" if prediction[0] > 0.5 else "No Varicose Veins"

import tensorflow as tf
import numpy as np
import cv2

# Load the TensorFlow SavedModel using TFSMLayer
model_path = "model/frozen_model/saved_model"
model = tf.keras.layers.TFSMLayer(model_path, call_endpoint='serving_default')

def preprocess_image(image_path):
    """Load and preprocess the image for the model."""
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB
    img = cv2.resize(img, (224, 224))  # Resize to match model input size
    img = img / 255.0  # Normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

def predict_varicose(image_path):
    """Perform prediction using the model."""
    img = preprocess_image(image_path)
    
    # Call the model instead of using `.predict()`
    prediction = model(img)  # Direct function call for TFSMLayer

    # Convert tensor to numpy array
    prediction = prediction.numpy()
    
    # Assuming it's a classification model with probabilities
    result = "Varicose Vein Detected" if prediction[0] > 0.5 else "No Varicose Vein Detected"
    
    return result
