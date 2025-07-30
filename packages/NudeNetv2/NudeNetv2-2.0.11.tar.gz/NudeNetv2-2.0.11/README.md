# NudeNet: Neural Nets for Nudity Classification, Detection and selective censoring

This is a fork of the `v2` branch of [https://github.com/notAI-tech/NudeNet](https://github.com/notAI-tech/NudeNet).

This fork exists since the original branch is no longer functional, as it relies upon downloading the classifier model from the github release page, which now requires the user to be logged in.

The emphasis of this fork is to maintain a simple working nudenet python package for easy use, primarily for classification purposes. I also removed the indecent images from the readme, as in my probably prude opinion they do not belong onto the page of a project that's about censoring it.


**Classifier classes:**
|class name   |  Description    |
|--------|:--------------:
|safe | Image/Video is not sexually explicit     |
|unsafe | Image/Video is sexually explicit|



# As Python module
**Installation**:
```bash
pip install --upgrade NudeNetv2
```

**Classifier Usage**:
```python
# Import module
from NudeNetv2 import NudeClassifier

# initialize classifier (downloads the checkpoint file automatically the first time)
classifier = NudeClassifier()

# Classify single image
classifier.classify('path_to_image_1')
# Returns {'path_to_image_1': {'safe': PROBABILITY, 'unsafe': PROBABILITY}}
# Classify multiple images (batch prediction)
# batch_size is optional; defaults to 4
classifier.classify(['path_to_image_1', 'path_to_image_2'], batch_size=BATCH_SIZE)
# Returns {'path_to_image_1': {'safe': PROBABILITY, 'unsafe': PROBABILITY},
#          'path_to_image_2': {'safe': PROBABILITY, 'unsafe': PROBABILITY}}

# Classify video
# batch_size is optional; defaults to 4
classifier.classify_video('path_to_video', batch_size=BATCH_SIZE)
# Returns {"metadata": {"fps": FPS, "video_length": TOTAL_N_FRAMES, "video_path": 'path_to_video'},
#          "preds": {frame_i: {'safe': PROBABILITY, 'unsafe': PROBABILITY}, ....}}

```

Thanks to [Johnny Urosevic](https://github.com/JohnnyUrosevic), NudeClassifier is also available in tflite.

**TFLite Classifier Usage**:
```python
# Import module
from nudenet import NudeClassifierLite

# initialize classifier (downloads the checkpoint file automatically the first time)
classifier_lite = NudeClassifierLite()

# Classify single image
classifier_lite.classify('path_to_image_1')
# Returns {'path_to_image_1': {'safe': PROBABILITY, 'unsafe': PROBABILITY}}
# Classify multiple images (batch prediction)
# batch_size is optional; defaults to 4
classifier_lite.classify(['path_to_image_1', 'path_to_image_2'])
# Returns {'path_to_image_1': {'safe': PROBABILITY, 'unsafe': PROBABILITY},
#          'path_to_image_2': {'safe': PROBABILITY, 'unsafe': PROBABILITY}}

```

Using the tflite classifier from flutter: **https://github.com/ndaysinaiK/nude-test** 

**Detector Usage**:
```python
# Import module
from NudeNetv2 import NudeDetector

# initialize detector (downloads the checkpoint file automatically the first time)
detector = NudeDetector() # detector = NudeDetector('base') for the "base" version of detector.

# Detect single image
detector.detect('path_to_image')
# fast mode is ~3x faster compared to default mode with slightly lower accuracy.
detector.detect('path_to_image', mode='fast')
# Returns [{'box': LIST_OF_COORDINATES, 'score': PROBABILITY, 'label': LABEL}, ...]

# Detect video
# batch_size is optional; defaults to 2
# show_progress is optional; defaults to True
detector.detect_video('path_to_video', batch_size=BATCH_SIZE, show_progress=BOOLEAN)
# fast mode is ~3x faster compared to default mode with slightly lower accuracy.
detector.detect_video('path_to_video', batch_size=BATCH_SIZE, show_progress=BOOLEAN, mode='fast')
# Returns {"metadata": {"fps": FPS, "video_length": TOTAL_N_FRAMES, "video_path": 'path_to_video'},
#          "preds": {frame_i: {'box': LIST_OF_COORDINATES, 'score': PROBABILITY, 'label': LABEL}, ...], ....}}



```

# Notes:
- detect_video and classify_video first identify the "unique" frames in a video and run predictions on them for significant performance improvement.
- V1 of NudeDetector (available in master branch of this repo) was trained on 12000 images labelled by the good folks at cti-community.
- V2 (current version) of NudeDetector is trained on 160,000 entirely auto-labelled (using classification heat maps and various other hybrid techniques) images. 
- The entire data for the classifier is available at https://archive.org/details/NudeNet_classifier_dataset_v1
- A part of the auto-labelled data (Images are from the classifier dataset above) used to train the base Detector is available at https://github.com/notAI-tech/NudeNet/releases/download/v0/DETECTOR_AUTO_GENERATED_DATA.zip
