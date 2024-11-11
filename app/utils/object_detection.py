import cv2
import os
class ObjectDetection:
    def __init__(self):

        cfg_path = os.path.abspath("app/resources/yolov3.cfg")
        weights_path = os.path.abspath("app/resources/yolov3.weights")

        self.model = cv2.dnn.readNetFromDarknet(cfg_path, weights_path )
        self.layer_names = self.model.getLayerNames()
        self.output_layers = [self.layer_names[i-1] for i in self.model.getUnconnectedOutLayers()]

    def detect_objects_from_webcam(self):
        """Detect objects from the webcam feed."""
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            self.model.setInput(blob)
            outs = self.model.forward(self.output_layers)
            
            # Process detections
            for out in outs:
                for detection in out:
                    # Object detection logic here...
                    pass
            
            # Display the frame
            cv2.imshow("Webcam Object Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
