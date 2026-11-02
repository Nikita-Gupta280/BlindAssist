
# Blind Assist – Vision System Limitations

## 1. Incorrect Object Detection

**Problem:**
The YOLO model may misclassify objects that look similar.

**Example:**
An air conditioner may sometimes be detected as a microwave.

**Possible Fix:**
Fine-tune the model using a custom dataset containing more relevant objects and environmental conditions.

---

## 2. Poor Lighting Conditions

**Problem:**
The camera may not capture objects properly in dark environments.

**Current Handling:**
The system checks frame brightness and identifies low-light conditions. Detection is skipped when lighting is insufficient.

**Possible Fix:**
Improve camera quality, use better lighting, or explore image enhancement techniques.

---

## 3. Blurry Camera Frames

**Problem:**
Camera movement or sudden motion can make frames blurry, affecting object detection.

**Current Handling:**
The system uses Laplacian variance to estimate blur and skips frames classified as blurry.

**Possible Fix:**
Use a more stable camera mount and improve camera focus.

---

## 4. Inaccurate Distance Estimation

**Problem:**
Distance is estimated using the height of an object's bounding box. Different objects have different physical dimensions, so the estimate may be inaccurate.

**Current Handling:**
The system uses a focal-length-based calculation to classify objects as close, medium, or far.

**Possible Fix:**
Use class-specific object dimensions or depth-estimation models such as MiDaS.

---

## 5. Partially Visible Objects

**Problem:**
Objects that are partially outside the camera frame may not be detected correctly.

**Possible Fix:**
Train or fine-tune the model with images containing partially visible objects.

---

## 6. Approaching Detection Limitations

**Problem:**
The system identifies approaching objects by comparing bounding-box heights across frames. Sudden camera movement can also cause bounding boxes to grow.

**Current Handling:**
Object tracking IDs and bounding-box growth are used to estimate whether an object is approaching.

**Possible Fix:**
Use temporal smoothing and more reliable motion estimation.

---

## 7. Unknown Obstacles

**Problem:**
The YOLO model can miss obstacles that do not belong to its trained classes.

**Current Handling:**
Unknown obstacle detection is not yet fully implemented in the current vision pipeline.

**Possible Fix:**
Integrate free-space and depth-based obstacle detection.

---

## 8. Real-World Reliability

**Problem:**
The system may behave differently in crowded, outdoor, or unpredictable environments compared to controlled testing conditions.

**Possible Fix:**
Test in different environments, lighting conditions, and camera positions before real-world deployment.

---

## Future Improvements

- Custom obstacle detection model.
- Improved distance estimation using MiDaS.
- More reliable approaching detection.
- Unknown obstacle detection.
- Testing across different environments.
- Improved camera performance and stability.

**Note:** Blind Assist is designed as an assistive prototype that supplements a traditional white cane. It is not a replacement for a white cane or other mobility aids.
