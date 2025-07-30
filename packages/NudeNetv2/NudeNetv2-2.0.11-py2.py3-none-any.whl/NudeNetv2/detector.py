import os
from pathlib import Path
import cv2
import numpy as np
import pydload
import logging
import onnxruntime
from progressbar import progressbar

from .detector_utils import preprocess_image
from .video_utils import get_interest_frames_from_video

FILE_URLS = {
    "default": {
        "checkpoint": "https://github.com/notAI-tech/NudeNet/releases/download/v0/detector_v2_default_checkpoint.onnx",
        "classes": "https://github.com/notAI-tech/NudeNet/releases/download/v0/detector_v2_default_classes",
    },
    "base": {
        "checkpoint": "https://github.com/notAI-tech/NudeNet/releases/download/v0/detector_v2_base_checkpoint.onnx",
        "classes": "https://github.com/notAI-tech/NudeNet/releases/download/v0/detector_v2_base_classes",
    },
}


def dummy(x):
    return x


class Detector:
    detection_model = None
    classes = None

    def __init__(self, model_name: str = "default", model_dir: str = None):
        """
        Initialize the Detector.

        Args:
            model_name: Key of FILE_URLS to select which model to load ('default' or 'base').
            model_dir: Optional path to directory where models should be stored.
                       If not provided, will use the NUDENET_MODEL_DIR environment variable,
                       or fall back to '~/.NudeNet'.
        """
        checkpoint_url = FILE_URLS[model_name]["checkpoint"]
        classes_url = FILE_URLS[model_name]["classes"]

        # Determine base directory: parameter > env var > default
        if model_dir:
            base_dir = Path(model_dir)
        elif os.getenv("NUDENET_MODEL_DIR"):
            base_dir = Path(os.getenv("NUDENET_MODEL_DIR"))
        else:
            base_dir = Path.home() / ".NudeNet"

        base_dir.mkdir(parents=True, exist_ok=True)

        checkpoint_name = Path(checkpoint_url).name
        checkpoint_path = base_dir / checkpoint_name
        classes_path = base_dir / "classes"

        if not checkpoint_path.exists():
            print(f"Downloading checkpoint to {checkpoint_path}")
            pydload.dload(checkpoint_url, save_to_path=str(checkpoint_path), max_time=None)

        if not classes_path.exists():
            print(f"Downloading classes list to {classes_path}")
            pydload.dload(classes_url, save_to_path=str(classes_path), max_time=None)

        # Load model
        self.detection_model = onnxruntime.InferenceSession(str(checkpoint_path))
        with classes_path.open() as f:
            self.classes = [c.strip() for c in f if c.strip()]

    def detect_video(
        self,
        video_path: str,
        mode: str = "default",
        min_prob: float = 0.6,
        batch_size: int = 2,
        show_progress: bool = True,
    ):
        frame_indices, frames, fps, video_length = get_interest_frames_from_video(video_path)
        logging.debug(
            f"VIDEO_PATH: {video_path}, FPS: {fps}, Important frame indices: {frame_indices}, Video length: {video_length}"
        )
        if mode == "fast":
            frames = [preprocess_image(frame, min_side=480, max_side=800) for frame in frames]
        else:
            frames = [preprocess_image(frame) for frame in frames]

        scale = frames[0][1]
        frames = [frame[0] for frame in frames]
        all_results = {"metadata": {"fps": fps, "video_length": video_length, "video_path": video_path}, "preds": {}}

        progress_func = progressbar if show_progress else dummy

        for _ in progress_func(range(int(len(frames) / batch_size) + 1)):
            batch = frames[:batch_size]
            batch_indices = frame_indices[:batch_size]
            frames = frames[batch_size:]
            frame_indices = frame_indices[batch_size:]
            if batch_indices:
                outputs = self.detection_model.run(
                    [s.name for s in self.detection_model.get_outputs()],
                    {self.detection_model.get_inputs()[0].name: np.asarray(batch)},
                )

                labels = [op for op in outputs if op.dtype == "int32"][0]
                scores = [op for op in outputs if isinstance(op[0][0], np.float32)][0]
                boxes = [op for op in outputs if isinstance(op[0][0], np.ndarray)][0]

                boxes /= scale
                for frame_index, frame_boxes, frame_scores, frame_labels in zip(
                    batch_indices, boxes, scores, labels
                ):
                    preds = all_results["preds"].setdefault(frame_index, [])
                    for box, score, label in zip(frame_boxes, frame_scores, frame_labels):
                        if score < min_prob:
                            continue
                        preds.append({
                            "box": [int(c) for c in box.astype(int).tolist()],
                            "score": float(score),
                            "label": self.classes[label],
                        })

        return all_results

    def detect(self, img_path: str, mode: str = "default", min_prob: float = None):
        if mode == "fast":
            image, scale = preprocess_image(img_path, min_side=480, max_side=800)
            min_prob = min_prob or 0.5
        else:
            image, scale = preprocess_image(img_path)
            min_prob = min_prob or 0.6

        outputs = self.detection_model.run(
            [s.name for s in self.detection_model.get_outputs()],
            {self.detection_model.get_inputs()[0].name: np.expand_dims(image, axis=0)},
        )

        labels = [op for op in outputs if op.dtype == "int32"][0]
        scores = [op for op in outputs if isinstance(op[0][0], np.float32)][0]
        boxes = [op for op in outputs if isinstance(op[0][0], np.ndarray)][0]

        boxes /= scale
        processed_boxes = []
        for box, score, label in zip(boxes[0], scores[0], labels[0]):
            if score < min_prob:
                continue
            processed_boxes.append({
                "box": [int(c) for c in box.astype(int).tolist()],
                "score": float(score),
                "label": self.classes[label],
            })

        return processed_boxes

    def censor(self, img_path: str, out_path: str = None, visualize: bool = False, parts_to_blur: list = []):
        if not out_path and not visualize:
            print("No out_path passed and visualize is set to false. Aborting.")
            return

        image = cv2.imread(img_path)
        boxes = self.detect(img_path)
        if parts_to_blur:
            boxes = [b for b in boxes if b["label"] in parts_to_blur]
        else:
            boxes = [b for b in boxes]

        for b in boxes:
            x0, y0, x1, y1 = b["box"]
            image[y0:y1, x0:x1] = cv2.rectangle(image, (x0, y0), (x1, y1), (0, 0, 0), cv2.FILLED)

        if visualize:
            cv2.imshow("Censored", image)
            cv2.waitKey(0)

        if out_path:
            cv2.imwrite(out_path, image)


if __name__ == "__main__":
    # Example usage:
    detector = Detector(model_dir=os.getenv("NUDENET_MODEL_DIR", None))
    print(detector.detect("/path/to/image.jpg"))
