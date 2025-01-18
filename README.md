# Video Snippet Annotator Tool (Usage)

A Python-based tool for efficient video annotation with customizable labels for videos in a given directory.

### Installation

```bash
# Install dependencies
pip install opencv-python pillow
```

### Configuration

1. Create `label_definitions.json` in the tool directory:
```json
[
    "Label 1",
    "Label 2",
    "Label 3",
    "Label 4",
    "Label 5"
]
```

2. The tool will create `labels.json` automatically to store annotations.

### Usage

1. Run the tool:
```bash
python video_annotator.py
```

2. Interface Elements:
   - Select Folder: Choose directory containing videos
   - Filter: Enter prefix to filter video files
   - Video Player: 16:9 ratio video display
   - Navigation: Previous/Next buttons and direct video selection
   - Label Buttons: Click to apply label and auto-advance
   - Status Bar: Shows current video information

### File Management

- Supported formats: .mp4, .avi, .mov
- Labels stored in labels.json:
```json
{
    "video1.mp4": "Label 1",
    "video2.mp4": "Label 2"
}
```

