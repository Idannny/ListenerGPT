from app.utils.object_detection import ObjectDetection

class ImageAgent:
    def __init__(self):
        self.object_detection = ObjectDetection()

    def recognize_objects(self):
        """Recognizes objects from a webcam feed."""
        print("Recognizing objects...")
        self.object_detection.detect_objects_from_webcam()
