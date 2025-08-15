🎨 Virtual Air Drawing using OpenCV

Virtual Air Drawing using OpenCV is a fun and interactive computer vision project that turns your hand into a virtual pen. Using just a webcam, the system detects your hand, tracks your index finger in real-time, and allows you to draw freely in the air. No physical pen or paper required — your movements are captured and displayed on a virtual canvas.

This project showcases the power of OpenCV for image processing and MediaPipe for accurate hand landmark detection. It’s a great example of how gesture recognition can be applied to creative applications such as virtual whiteboards, drawing tools, or even gesture-based games.

🔹 Features

✍️ Air Drawing – Draw anything in the air using just your fingertip

🎥 Real-Time Tracking – Smooth and fast hand tracking using a webcam

🖼️ Virtual Canvas – Your screen becomes a digital canvas

🧹 Clear Canvas Option – Reset the screen whenever you need a fresh start

💡 Hands-Free Creativity – No external hardware needed, just your hand

🛠 Tech Stack

Python

OpenCV → For image processing & drawing on frames

MediaPipe → For hand & fingertip landmark detection

NumPy → For handling coordinates and arrays

🚀 How It Works

Captures live video stream from the webcam.

Detects hand and finger landmarks using MediaPipe Hand Tracking.

Tracks the index fingertip position to determine the drawing point.

Continuously plots the tracked positions onto a virtual canvas.

The result is displayed in real-time, allowing you to draw letters, shapes, or anything you want.

🌟 Future Improvements

Add multiple color options for drawing 🎨

Support eraser tool to remove parts of the drawing

Add gesture shortcuts (e.g., ✌️ for clear screen, ✊ for pause)

Save the virtual drawing as an image file 🖼️
