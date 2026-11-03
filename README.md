# 👁️ BlindAssist
### See the World Through Sound.

BlindAssist is an assistive vision application designed to help visually impaired individuals understand their surroundings through real-time object detection and audio-based alerts.

Using a camera and computer vision, BlindAssist identifies objects in the user's environment, estimates their approximate distance and position, and communicates relevant information through voice alerts.

Our goal is to make everyday navigation more informed and accessible through affordable, AI-powered technology.

---

## 🌟 Key Features

- **Real-Time Object Detection:** Identifies objects in the user's surroundings using computer vision.
- **Audio-Based Alerts:** Communicates detected objects through spoken notifications.
- **Distance Estimation:** Estimates the approximate distance of detected objects.
- **Directional Awareness:** Classifies detected objects into different regions of the camera frame, such as left, centre and right.
- **Hazard Detection:** Explores additional detection capabilities for potholes, stairs and doors.
- **Multiple Alert Languages:** Supports language-based voice notifications.
- **Quiet Mode:** Provides a less intrusive alert experience by filtering selected object notifications.
- **Live Camera Processing:** Processes camera frames to provide continuous environmental awareness.

## ⚙️ How It Works

1. **Camera Input:** The application captures live video from a connected camera.
2. **Frame Processing:** Selected video frames are passed to the object detection system.
3. **Object Detection:** YOLO-based computer vision models identify objects in the surroundings.
4. **Position and Distance Estimation:** Detected objects are analysed to estimate their position and approximate distance.
5. **Alert Generation:** The alert manager determines which detections require notifications.
6. **Audio Feedback:** The application communicates relevant information through spoken alerts.
7. **Live Dashboard:** Detection information and camera output are displayed through the application interface.

## 🧠 Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Computer Vision | OpenCV |
| Object Detection | Ultralytics YOLO |
| Deep Learning | PyTorch |
| Application Interface | Streamlit |
| Audio Notifications | Text-to-Speech |
| Version Control | Git and GitHub |
| Model File Management | Git LFS |

## 📁 Project Structure

```text
BlindAssist/
│
├── alerts/
│   ├── alert_manager.py
│   ├── phrases.py
│   └── speech.py
│
├── vision/
│   ├── detector.py
│   ├── logic.py
│   ├── quality.py
│   └── stream.py
│
├── P3_Data_Model/
│   ├── eval/
│   ├── model/
│   ├── p3_detector.py
│   ├── free_space.py
│   └── model_failures.md
│
├── tests/
├── tools/
├── docs/
│
├── app.py
├── config.py
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or compatible version
- Git
- Git LFS
- A connected webcam or camera

### 1. Clone the repository

```bash
git clone https://github.com/ishitasanger/BlindAssist.git
cd BlindAssist
```

### 2. Install Git LFS

Install Git LFS and initialise it:

```bash
git lfs install
git lfs pull
```

This downloads the large model-weight files managed through Git LFS.

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows:**
```powershell
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

Make sure your camera is connected and accessible.

## 🧪 Hazard Detection & Model Development

BlindAssist explores additional computer vision capabilities to identify environmental hazards and important surroundings.

The project includes experimental models for:

- **Pothole Detection**
- **Stair Detection**
- **Door Detection**

Supporting components include:

- Custom model-training scripts.
- Model evaluation scripts.
- A preliminary free-space estimation approach.
- Documentation of model performance, challenges and limitations.
- A separate detector module for running the additional models.

These models are being developed to extend the application's environmental awareness capabilities and are intended for integration with the existing detection and alert pipeline.

## ⚠️ Limitations & Safety Disclaimer

BlindAssist is an assistive technology prototype under development.

- Object detection may produce false positives and false negatives.
- Distance estimates are approximate and may not reflect actual physical distances.
- Experimental hazard-detection models have limited evaluation performance and require further training and validation.
- Door detection class labels are provisional.
- Free-space estimation is based on image regions and does not establish that a path is physically safe.

**BlindAssist should not be used as a replacement for a white cane, guide dog, or other established mobility aids. Users should continue to rely on their existing mobility and safety practices.**

## 🔮 Future Improvements

- Integration of additional hazard-detection models into the main application.
- Improved detection accuracy through larger and more diverse datasets.
- More reliable distance estimation and depth awareness.
- Improved free-space and obstacle analysis.
- Enhanced multilingual voice assistance.
- Real-world testing and accessibility feedback.
- Performance optimisation for real-time operation on accessible hardware.

## 👥 Team

Developed as a collaborative project focused on building accessible technology through computer vision and assistive AI.

Team Members:-

Ishita Sanger

Kashish Gupta

Nikita Gupta

Bhawana Gautam 


## ❤️ Our Vision

We believe technology should make the world more accessible.

**BlindAssist — Turning Visual Information into Audio Awareness.**
