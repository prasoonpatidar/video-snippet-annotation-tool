# Video Snippet Annotator Tool (Implementation Details)

## Architecture Overview

### Core Components

1. `VideoAnnotator` Class
   - Main application class
   - Handles UI, video processing, and label management
   - Implements event-driven architecture

2. File Management
   - JSON-based configuration and storage
   - Dynamic file filtering
   - Memory-efficient video handling

3. UI Components
   - Tkinter-based interface
   - OpenCV video processing
   - Controlled frame rate display

## Application Flow

1. Initialization
   ```
   Load label definitions
   ↓
   Setup UI components
   ↓
   Initialize state variables
   ↓
   Bind keyboard events
   ```

2. Video Loading
   ```
   Select folder
   ↓
   Filter videos (if prefix set)
   ↓
   Update video selection dropdown
   ↓
   Load first video
   ↓
   Start playback loop
   ```

3. Label Management
   ```
   Load existing labels
   ↓
   Update UI state
   ↓
   Handle label toggling
   ↓
   Save to JSON
   ```

## Class Methods Documentation

### Core Methods

#### `__init__(self, root)`
- Initializes application state
- Sets up UI components
- Configures keyboard bindings

#### `setup_ui(self)`
- Creates all UI elements
- Configures layouts
- Sets up event bindings

### Video Handling

#### `play_current_video(self)`
- Opens video file
- Initializes playback
- Sets up frame timing
- Updates UI state

#### `update_video_frame(self)`
- Controls frame rate
- Handles frame resizing
- Manages memory efficiently
- Implements playback loop

### Label Management

#### `load_labels(self)`
- Reads labels.json
- Converts legacy format
- Initializes label state

#### `apply_label(self, label: str)`
- Toggles label state
- Updates UI
- Saves changes
- Handles multi-label logic

#### `clean_labels(self)`
- Removes all labels
- Updates UI state
- Saves changes

### Navigation

#### `next_video(self)/prev_video(self)`
- Handles video transitions
- Updates UI state
- Manages resources
- Called by keyboard/button events

### File Management

#### `filter_videos(self)`
- Applies prefix filter
- Updates video list
- Handles file validation
- Updates UI state

## Performance Considerations

### Memory Management
- Video cleanup on transitions
- Controlled frame buffer
- Resource release protocols

### UI Responsiveness
- Frame rate control
- Asynchronous updates
- Event-driven design

### File Operations
- Lazy loading
- Efficient JSON handling
- Optimized file filtering

## Data Structures

### Label Storage
```json
{
    "video_file.mp4": ["Label1", "Label2"],
    "another_video.mp4": ["Label3"]
}
```

### State Variables
```python
self.video_files: List[str]
self.labels_data: Dict[str, List[str]]
self.current_video_idx: int
```

## Error Handling

- Invalid file handling
- Resource cleanup
- User input validation
- File operation safety