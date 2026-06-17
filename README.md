# 🐍 Hand-Controlled Snake Game with MediaPipe & Pygame

Welcome to the **Hand-Controlled Snake Game**! 🎮 This is a modern twist on the classic retro Snake game. Instead of bashing your keyboard arrows, you control the snake's direction in real-time by **moving your index finger** captured by your webcam! 

Powered by **Pygame** for smooth 2D rendering and **Google MediaPipe** for robust, real-time hand landmark tracking.

---

## ✨ Features

* 🙌 **Gesture Control:** Control the snake using simple, intuitive movements of your **index finger**.
* 🎥 **Live Camera Overlay:** See your hand landmarks, skeleton connections, and detected directions rendered dynamically.
* ⚡ **Smooth Mechanics:** Responsive grid-based movement with visual indicators.
* 🎮 **Classic Arcade Experience:** Score tracking, retro visuals, and easy restart options.

---

## 🕹️ How to Play

The rules are simple: guide the snake to eat the apples 🍎, grow your score, and avoid hitting the walls or your own tail!

### ☝️ The Controls: Index Finger Navigation
You control the snake simply by **moving your index finger** (Point 8) up, down, left, or right in the camera frame relative to your hand:

* ⬆️ **Move UP:** Move your index finger upwards.
* ⬇️ **Move DOWN:** Move your index finger downwards.
* ⬅️ **Move LEFT:** Move your index finger to the left.
* ➡️ **Move RIGHT:** Move your index finger to the right.

> 💡 **Tip:** Keep your hand stable, then shift your index finger towards the direction you want the snake to go!

### ⌨️ Keyboard Shortcuts
* `Space` / `Enter` / `R`: Restart the game after a Game Over 🔄
* `Esc`: Quit the game instantly ❌

---

## 🚀 Getting Started

### 📦 Prerequisites
Make sure you have Python 3.8+ installed. You can install all the required modules using `requirements.txt`:

```bash
pip install -r requirements.txt
