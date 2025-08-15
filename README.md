🎨 Virtual Air Drawing using OpenCV & MediaPipe

This project demonstrates gesture-controlled air drawing using OpenCV and MediaPipe.
By tracking hand landmarks via webcam, you can draw in the air using your thumb + index finger pinch gesture, select colors, clear the canvas, and even save your artwork.

🚀 Project Levels


🖌️ 1. Basic Drawing

Webcam opens.

Draw freely in the air using pinch gesture (thumb + index).

Only one default color is available.

🎨 2. Multi-Color Drawing

Webcam opens.

Draw with multiple colors.

Change colors by pointing your index finger to the palette at the top of the screen.

🧹 3. Advanced Drawing (Final Version)

Webcam opens.

Draw with multiple colors.

Color selection via index finger.

🧹 Clear Button to reset canvas.

🖼 Save Image Button to export your drawing as drawing.png.

🛠️ Tech Stack

Python

OpenCV

MediaPipe

NumPy

Streamlit (for interactive UI in final version)

📂 Project Structure
📁 Virtual-Air-Drawing
 ┣ 📄 basic_drawing.py      # 1st code (single color)
 ┣ 📄 multicolor_drawing.py # 2nd code (color selection)
 ┣ 📄 final_app.py          # 3rd code (color, clear, save)
 ┣ 📄 README.md             # Documentation

▶️ How to Run
1️⃣ Install dependencies
pip install opencv-python mediapipe numpy streamlit

2️⃣ Run Basic Version
python basic_drawing.py

3️⃣ Run Multi-Color Version
python multicolor_drawing.py

4️⃣ Run Final Streamlit App
streamlit run final_app.py

✋ Controls

Draw → Pinch gesture (Thumb + Index finger close).

Change Color → Point index finger to color palette.

🧹 Clear Canvas → Click Clear button.

🖼 Save Image → Click Save button → Download drawing.

🎯 Future Improvements

✨ Brush size control (slider).

🧽 Eraser tool.

🖌️ Different brush styles.

💾 Save multiple drawings with custom filenames.
