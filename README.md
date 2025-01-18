# Video Snippet Annotator Tool

A Python tool for efficient multi-label video annotation with keyboard controls and filtering capabilities.

## Installation

```bash
pip install opencv-python pillow
```

## Quick Start

1. Configure labels in `label_definitions.json`:
```json
[
    "Walking",
    "Running",
    "Sitting",
    "Standing",
    "Jumping"
]
```

2. Launch:
```bash
python video_annotator_v2.py
```

## Features

- Multi-label support with toggle functionality
- Filename prefix filtering
- Direct video selection dropdown
- FPS-controlled 16:9 playback
- Automatic label saving
- Keyboard navigation

## Controls

### Keyboard
- `←` Previous video
- `→` or `Enter` Next video
- `Space` Pause/Play

### Mouse
- Click labels to toggle on/off
- "Clean Labels" removes all labels from current video
- Filter textbox for prefix search
- Video dropdown for direct navigation

## Data Storage

Labels are automatically saved in `labels.json`:
```json
{
    "video1.mp4": ["Walking", "Running"],
    "video2.mp4": ["Sitting"]
}
```

## Interface Guide

1. **Top Bar**
   - "Select Folder" opens video directory
   - Filter box for filename search
   - Apply/Clear filter buttons

2. **Video Display**
   - 16:9 aspect ratio playback
   - Current label display below video
   - Navigation controls

3. **Label Section**
   - Toggle buttons for each label
   - Green highlight for active labels
   - "Clean Labels" button

## Tips

- Use keyboard shortcuts for faster navigation
- Filter large directories with filename prefix
- Multiple labels can be applied per video
- Labels auto-save on every change
- Clean Labels resets to "No Label" state