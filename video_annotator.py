import tkinter as tk
from tkinter import ttk, filedialog
import json
import os
import cv2
from PIL import Image, ImageTk
import time
from typing import Optional, Dict, List


class VideoAnnotator:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Annotator V2")

        # State variables
        self.video_files: List[str] = []
        self.video_folder: str = ""
        self.labels_file = "labels.json"
        self.labels_data: Dict[str, str] = {}
        self.current_video_idx = 0
        self.cap: Optional[cv2.VideoCapture] = None
        self.last_frame_time = 0
        self.target_fps = 30
        self.frame_delay = 1.0 / self.target_fps

        # Load labels and create UI
        self.load_labels()
        self.setup_ui()

    def setup_ui(self):
        # Bind keyboard events
        self.root.bind('<Left>', lambda e: self.prev_video())
        self.root.bind('<Right>', lambda e: self.next_video())
        self.root.bind('<Return>', lambda e: self.next_video())

        # Toolbar
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(toolbar, text="Select Folder", command=self.select_folder).pack(side=tk.LEFT)

        # Filter frame
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(filter_frame, text="Filter:").pack(side=tk.LEFT)
        self.prefix_var = tk.StringVar()
        prefix_entry = ttk.Entry(filter_frame, textvariable=self.prefix_var)
        prefix_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Apply", command=self.apply_filter).pack(side=tk.LEFT)
        ttk.Button(filter_frame, text="Clear", command=self.clear_filter).pack(side=tk.LEFT)

        # Video frame
        self.video_frame = ttk.Frame(self.root)
        self.video_frame.pack(padx=5, pady=5)
        self.video_label = ttk.Label(self.video_frame)
        self.video_label.pack()

        # Current annotation label
        self.current_label = ttk.Label(self.root, text="No Label", font=('Arial', 12, 'bold'))
        self.current_label.pack(pady=5)

        # Navigation frame
        nav_frame = ttk.Frame(self.root)
        nav_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(nav_frame, text="Previous", command=self.prev_video).pack(side=tk.LEFT)
        ttk.Button(nav_frame, text="Next", command=self.next_video).pack(side=tk.LEFT)

        # Direct video selection
        select_frame = ttk.Frame(self.root)
        select_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(select_frame, text="Go to video:").pack(side=tk.LEFT)
        self.video_select = ttk.Combobox(select_frame, state="readonly")
        self.video_select.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.video_select.bind('<<ComboboxSelected>>', self.on_video_select)

        # Status label
        self.status_label = ttk.Label(self.root, text="No folder selected")
        self.status_label.pack(pady=5)

        # Clean labels button
        ttk.Button(
            self.root,
            text="Clean Labels",
            command=self.clean_labels
        ).pack(pady=5)

        # Labels frame
        labels_frame = ttk.Frame(self.root)
        labels_frame.pack(fill=tk.X, padx=5, pady=5)
        self.create_label_buttons(labels_frame)

    def create_label_buttons(self, parent):
        style = ttk.Style()
        style.configure('Selected.TButton', background='green')

        labels = self.load_label_definitions()
        self.label_buttons = {}

        for i, label in enumerate(labels):
            btn = ttk.Button(
                parent,
                text=label,
                command=lambda l=label: self.apply_label(l),
                style='TButton'
            )
            btn.grid(row=i // 5, column=i % 5, padx=2, pady=2, sticky='ew')
            self.label_buttons[label] = btn

        for i in range(5):
            parent.grid_columnconfigure(i, weight=1)

    def load_label_definitions(self) -> List[str]:
        try:
            with open("label_definitions.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            default_labels = ["Label 1", "Label 2", "Label 3", "Label 4", "Label 5"]
            with open("label_definitions.json", 'w') as f:
                json.dump(default_labels, f)
            return default_labels

    def load_labels(self):
        try:
            with open(self.labels_file, 'r') as f:
                self.labels_data = json.load(f)
                # Convert existing single labels to lists
                for key in self.labels_data:
                    if isinstance(self.labels_data[key], str):
                        self.labels_data[key] = [self.labels_data[key]]
        except FileNotFoundError:
            self.labels_data = {}

    def save_labels(self):
        with open(self.labels_file, 'w') as f:
            json.dump(self.labels_data, f, indent=4)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.video_folder = folder
            self.apply_filter()

    def apply_filter(self):
        if not self.video_folder:
            return

        prefix = self.prefix_var.get().strip()
        files = [f for f in os.listdir(self.video_folder)
                 if f.lower().endswith(('.mp4', '.avi', '.mov'))
                 and not f.startswith('._')
                 and os.path.getsize(os.path.join(self.video_folder, f)) > 0]

        if prefix:
            files = [f for f in files if f.startswith(prefix)]

        self.video_files = sorted(files)
        self.update_video_select()

        if self.video_files:
            self.current_video_idx = 0
            self.play_current_video()
        else:
            self.status_label.config(text="No videos found")

    def clear_filter(self):
        self.prefix_var.set("")
        self.apply_filter()

    def update_video_select(self):
        self.video_select['values'] = self.video_files
        if self.video_files:
            self.video_select.set(self.video_files[self.current_video_idx])

    def on_video_select(self, event):
        selected = self.video_select.get()
        if selected in self.video_files:
            self.current_video_idx = self.video_files.index(selected)
            self.play_current_video()

    def play_current_video(self):
        if not self.video_files:
            return

        # Release previous capture
        self.cleanup_video()

        try:
            video_path = os.path.join(self.video_folder, self.video_files[self.current_video_idx])
            self.cap = cv2.VideoCapture(video_path)

            if not self.cap.isOpened():
                self.status_label.config(text=f"Error opening video: {self.video_files[self.current_video_idx]}")
                return

            self.update_status()
            self.update_labels()
            self.last_frame_time = time.time()
            self.update_video_frame()

        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

    def update_video_frame(self):
        if self.cap is None or not self.cap.isOpened():
            return

        current_time = time.time()
        elapsed = current_time - self.last_frame_time

        if elapsed < self.frame_delay:
            self.root.after(int((self.frame_delay - elapsed) * 1000), self.update_video_frame)
            return

        ret, frame = self.cap.read()
        if ret:
            frame = cv2.resize(frame, (854, 480))  # 16:9 ratio (480p)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
            self.last_frame_time = current_time
            self.root.after(1, self.update_video_frame)
        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.update_video_frame()

    def cleanup_video(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def update_labels(self):
        current_video = self.video_files[self.current_video_idx]
        current_labels = self.labels_data.get(current_video, [])

        for label, btn in self.label_buttons.items():
            if label in current_labels:
                btn.configure(style='Selected.TButton')
            else:
                btn.configure(style='TButton')

        if current_labels:
            self.current_label.config(text=f"Current Labels: {', '.join(current_labels)}")
        else:
            self.current_label.config(text="No Label")

    def apply_label(self, label: str):
        if not self.video_files:
            return

        current_video = self.video_files[self.current_video_idx]
        if current_video not in self.labels_data:
            self.labels_data[current_video] = []

        if label in self.labels_data[current_video]:
            self.labels_data[current_video].remove(label)
        else:
            self.labels_data[current_video].append(label)

        self.save_labels()
        self.update_labels()

    def clean_labels(self):
        if not self.video_files:
            return

        current_video = self.video_files[self.current_video_idx]
        if current_video in self.labels_data:
            del self.labels_data[current_video]
            self.save_labels()
            self.update_labels()

    def next_video(self):
        if not self.video_files:
            return
        self.current_video_idx = (self.current_video_idx + 1) % len(self.video_files)
        self.play_current_video()

    def prev_video(self):
        if not self.video_files:
            return
        self.current_video_idx = (self.current_video_idx - 1) % len(self.video_files)
        self.play_current_video()

    def update_status(self):
        if self.video_files:
            status = f"Video {self.current_video_idx + 1} of {len(self.video_files)}: {self.video_files[self.current_video_idx]}"
            self.status_label.config(text=status)
            self.video_select.set(self.video_files[self.current_video_idx])

    def __del__(self):
        self.cleanup_video()


def main():
    root = tk.Tk()
    app = VideoAnnotator(root)
    root.mainloop()


if __name__ == "__main__":
    main()