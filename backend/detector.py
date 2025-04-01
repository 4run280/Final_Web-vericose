# detector.py
import cv2
import numpy as np
import tensorflow as tf

class DetectorTF2:
    def __init__(self, path_to_checkpoint, path_to_labelmap, class_id=None, threshold=0.5):
        self.class_id = class_id
        self.Threshold = threshold
        
        # Load labels from labelmap.pbtxt
        self.category_index = self.load_labelmap(path_to_labelmap)
        
        # Load model
        tf.keras.backend.clear_session()
        self.model = tf.saved_model.load(path_to_checkpoint)

    def load_labelmap(self, path_to_labelmap):
        category_index = {}
        try:
            with open(path_to_labelmap, 'r') as f:
                lines = f.readlines()
                
            current_item = {}
            for line in lines:
                line = line.strip()
                if line.startswith('item {'):
                    current_item = {}
                elif line.startswith('id:'):
                    current_item['id'] = int(line.split(':')[1].strip())
                elif line.startswith('name:'):
                    current_item['name'] = line.split(':')[1].strip().strip("'\"")
                elif line == '}' and current_item:
                    category_index[str(current_item['id'])] = current_item
                    
            return category_index
        except Exception as e:
            print(f"Error loading labelmap: {e}")
            # Return a default category index if loading fails
            return {'1': {'id': 1, 'name': 'varicose'}}

    def DetectFromImage(self, img):
        im_height, im_width, _ = img.shape
        # Expand dimensions
        input_tensor = np.expand_dims(img, 0)
        input_tensor = tf.convert_to_tensor(input_tensor)
        input_tensor = tf.cast(input_tensor, tf.float32)
        
        # Detection
        detections = self.model(input_tensor)

        # Process detections
        bboxes = detections['detection_boxes'][0].numpy()
        bclasses = detections['detection_classes'][0].numpy().astype(np.int32)
        bscores = detections['detection_scores'][0].numpy()
        
        det_boxes = self.ExtractBBoxes(bboxes, bclasses, bscores, im_width, im_height)
        return det_boxes

    def ExtractBBoxes(self, bboxes, bclasses, bscores, im_width, im_height):
        bbox = []
        for idx in range(len(bboxes)):
            if self.class_id is None or bclasses[idx] in self.class_id:
                if bscores[idx] >= self.Threshold:
                    y_min = int(bboxes[idx][0] * im_height)
                    x_min = int(bboxes[idx][1] * im_width)
                    y_max = int(bboxes[idx][2] * im_height)
                    x_max = int(bboxes[idx][3] * im_width)
                    class_label = self.category_index.get(str(bclasses[idx]), {}).get('name', 'unknown')
                    bbox.append([x_min, y_min, x_max, y_max, class_label, float(bscores[idx])])
        return bbox

    def DisplayDetections(self, image, boxes_list, det_time=None):
        if not boxes_list: return image
        img = image.copy()
        
        for box in boxes_list:
            x_min, y_min, x_max, y_max, detected_class, score = box
            
            text = f"{detected_class}: {score:.2f}"
            
            # Draw rectangle and text
            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            cv2.putText(img, text, (x_min, y_min - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        if det_time is not None:
            fps = round(1000. / det_time, 1)
            fps_txt = f"{fps} FPS"
            cv2.putText(img, fps_txt, (25, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

        return img