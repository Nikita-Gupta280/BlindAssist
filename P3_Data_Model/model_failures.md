
# Model Limitations and Failure Cases

## 1. Current Model
- Model: YOLOv8n pretrained on the COCO dataset.
- Current testing: Live webcam detection.
- Successfully detected examples of persons and chairs during testing.

## 2. Known Limitations

1. Potholes: Not included in the standard COCO classes.
2. Stairs: Not included in the standard COCO classes.
3. Doors: Not included in the standard COCO classes.
4. Auto-rickshaws: No dedicated COCO class; they may be classified incorrectly.
5. Small or distant objects: May be missed by the model.
6. Occluded objects: Partially hidden objects may not be detected reliably.

## 3. Free-Space Limitations
- Current free-space logic is experimental.
- It divides the image into left, centre and right regions.
- It does not calculate actual distance from obstacles.
- An undetected object does not mean the path is safe.

## 4. Future Improvements
- Collect and label custom images for potholes, stairs, doors and auto-rickshaws.
- Train and test a custom object-detection model.
- Evaluate using a labelled validation dataset.
- Test in different lighting and outdoor conditions.
- Improve obstacle distance and free-space estimation.

## 5. Safety Note
This is an experimental prototype and must not be relied upon as a standalone navigation or safety device.


## 6. Pothole Model Evaluation

- Model: Custom YOLOv8n pothole model.
- Training dataset: 1,041 images.
- Validation dataset: 130 images.
- Test dataset: 131 images.
- Successfully evaluated images: 129.

### Test Results
- Precision: 0.448
- Recall: 0.383
- mAP50: 0.370
- mAP50-95: 0.156

### Observed Dataset Issues
- Two test images were ignored because their labels mixed segmentation and detection formats.
- YOLO reported mixed segmentation and bounding-box annotations.
- Results are preliminary and indicate room for improvement.


## 7. Stairs Model Evaluation

- Model: Custom YOLOv8n stairs detection model.
- Training dataset: 340 images.
- Validation dataset: 42 images.
- Test dataset: 43 images.
- Training duration: 6 epochs.
- Number of labelled test instances: 47.

### Test Results
- Precision: 0.347 (34.7%)
- Recall: 0.234 (23.4%)
- mAP50: 0.168 (16.8%)
- mAP50-95: 0.086 (8.6%)

### Dataset Limitations
- The downloaded training folder did not contain annotation files.
- The 425 labelled images from the downloaded test folder were therefore split into training, validation and test subsets.
- The resulting test set is not an independent test set from the original dataset.
- One duplicate annotation was removed during evaluation.

### Observed Model Limitations
- The current model has low detection performance.
- It may miss stairs or produce incorrect detections.
- More labelled training images and additional training are required.
- It must not be relied upon for real-world navigation or safety.


## 8. Door Model Evaluation

- Model: Custom YOLOv8n door detection model.
- Training dataset: 896 images.
- Validation dataset: 112 images.
- Test dataset: 112 images.
- Training duration: 6 epochs.
- Number of labelled test instances: 61.
- Number of classes: 2 (door_class_0 and door_class_1).

### Test Results

- Precision: 0.360 (36.03%)
- Recall: 0.502 (50.18%)
- mAP50: 0.390 (39.04%)
- mAP50-95: 0.286 (28.60%)

### Class-wise Results

- door_class_0: 56 images, 56 instances, mAP50 = 0.668.
- door_class_1: 5 images, 5 instances, mAP50 = 0.113.

### Dataset Limitations

- The downloaded training folder did not contain annotation files.
- The 1,120 labelled images from the downloaded test folder were split into training, validation and test subsets.
- Therefore, the resulting test set is not an independent test set from the original dataset.
- The original class names were unclear, so provisional names were used.
- Class 1 has only 5 test instances, making its evaluation unreliable.

### Observed Model Limitations

- The model performs considerably better on class 0 than class 1.
- More labelled examples are needed, especially for class 1.
- Training was stopped after 6 epochs.
- The model requires further dataset verification and training.
- It must not be relied upon for real-world navigation or safety.
