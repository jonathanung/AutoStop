from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer
import queue
import cv2

class MainWindow(QWidget):
    """
    MainWindow is responsible for creating and managing a GUI with multiple views for real-time
    display of camera or LIDAR outputs. It includes control buttons to navigate through different views
    and updates the views with new frame data at regular intervals.

    Attributes
    ----------
    layout : QVBoxLayout
        The main vertical layout of the window.
    grid_layout : QGridLayout
        Layout to arrange multiple view windows.
    views : list
        List to store QLabel widgets representing each view.
    image_queues : list
        List to store queue.Queue objects for frame data of each view.
    control_layout : QHBoxLayout
        Layout to arrange control buttons.
    next_button : QPushButton
        Button to switch to the next view.
    prev_button : QPushButton
        Button to switch to the previous view.
    current_view_index : int
        Index of the currently displayed view.
    timer : QTimer
        Timer to trigger updates for real-time frame display.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AutoStop")
        
        # Create main layout
        self.layout = QVBoxLayout()
        
        # Create grid layout for multiple views
        self.grid_layout = QGridLayout()
        self.views = []  # List to store QLabel widgets
        self.image_queues = []  # List to store corresponding queues
        self.last_frames = []  # Store last received frame for each view
        
        # Control buttons
        self.control_layout = QHBoxLayout()
        self.next_button = QPushButton("Next View")
        self.prev_button = QPushButton("Prev View")
        self.next_button.clicked.connect(self.next_view)
        self.prev_button.clicked.connect(self.prev_view)
        self.control_layout.addWidget(self.prev_button)
        self.control_layout.addWidget(self.next_button)
        
        self.layout.addLayout(self.control_layout)
        self.layout.addLayout(self.grid_layout)
        self.setLayout(self.layout)
        
        # Current view index
        self.current_view_index = -1
        
        # Set up the timer for real-time updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frames)
        self.timer.start(30)  # Update every 30 ms

    def add_view(self, name=""):
        """Add a new view window for camera/LIDAR output"""
        label = QLabel(self)
        label.setAlignment(Qt.AlignCenter)
        label.setText(name)
        
        # Calculate grid position (2 columns)
        pos = len(self.views)
        row = pos // 2
        col = pos % 2
        
        self.grid_layout.addWidget(label, row, col)
        self.views.append(label)
        self.image_queues.append(queue.Queue())
        self.last_frames.append(None)
        
        if self.current_view_index == -1:
            self.current_view_index = 0
            
        return len(self.views) - 1  # Return index of the new view

    def update_frame_for_view(self, index, frame):
        """Update specific view with new frame data"""
        if 0 <= index < len(self.image_queues):
            self.image_queues[index].put(frame)

    def next_view(self):
        if len(self.views) > 1:
            self.current_view_index = (self.current_view_index + 1) % len(self.views)

    def prev_view(self):
        if len(self.views) > 1:
            self.current_view_index = (self.current_view_index - 1) % len(self.views)

    def update_frames(self):
        """Update all views with latest frames"""
        for idx, q in enumerate(self.image_queues):
            try:
                while not q.empty():  # Process all available frames
                    frame = q.get_nowait()
                    if frame is not None:
                        self.last_frames[idx] = frame
                
                # Display the last received frame
                if self.last_frames[idx] is not None:
                    frame = self.last_frames[idx]
                    # Convert frame to QImage
                    if len(frame.shape) == 3:
                        # RGB image (camera)
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        height, width, channel = frame.shape
                        bytes_per_line = 3 * width
                        q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                    else:
                        # Grayscale image (LIDAR visualization)
                        height, width = frame.shape
                        q_img = QImage(frame.data, width, height, width, QImage.Format_Grayscale8)
                    
                    self.views[idx].setPixmap(QPixmap.fromImage(q_img))
            except queue.Empty:
                continue

    def closeEvent(self, event):
        self.timer.stop()



