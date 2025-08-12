# 🚀 Space Invaders V2

**Author:** Ibtasaam Amjad  
**Semester:** 2nd (Developed between classes)  
**Language:** Python (Pygame)  
**Core Feature:** Mask-based collision detection module for precise hit registration

---

## 📖 Overview

Space Invaders V2 is a modernized version of the classic **Space Invaders** arcade game, built entirely in Python using **Pygame**.

This isn't just a clone — it integrates:

* A **modular collision detection system** using pixel-perfect **mask collisions**.
* **Multiple alien types**, each with unique health values.
* **Randomized power-ups and power-downs** that affect firepower.
* **Animated explosions** using a frame-by-frame sprite system.
* **Multi-channel audio** with custom sound mixing for overlapping effects.
* **Level loading from external text files** for easy stage customization.

---

## 🕹 Features

### 1. **Spaceship Mechanics**

* Smooth horizontal control using mouse movement.
* Adjustable bullet count via power-ups (1, 2, or 3 simultaneous shots).
* Health bar with visual depletion.

### 2. **Alien Types**

| Enemy Type | Health | Sprite       |
|------------|--------|--------------|
| 1          | 1      | `alien1.png` |
| 2          | 3      | `alien2.png` |
| 3          | 5      | `alien3.png` |
| 4          | 9      | `alien4.png` |
| 5          | 15     | `alien5.png` |

* All enemies move horizontally in sync and reverse on screen edge collision.
* Randomized shooting behavior for unpredictability.

### 3. **Bullets & Firing**

* **Player bullets**: Fire upwards with a cooldown timer.
* **Alien bullets**: Fire downwards randomly.
* Collision checks against both enemies and player.

### 4. **Drops (Power-Ups / Power-Downs)**

* Type 1: Increase bullet count (up to triple shot).
* Type 2: Decrease bullet count (minimum single shot).
* Random drop generation on enemy death.

### 5. **Collision Detection**

* Implemented in **`collision_detection.py`**:
  * Pixel-perfect mask-based detection.
  * Handles collisions between:
    * Player & alien bullets
    * Player & drops
    * Player bullets & aliens
* Returns collision state + coordinates for spawning explosions/drops.

### 6. **Explosion Animation**

* Frame-by-frame rendering of explosion sprites.
* Cooldown-controlled animation playback for smooth visuals.

### 7. **Levels**

* Stored in `data/levels/levelX.txt` files.
* Each file contains a comma-separated grid representing enemy placement & type.
* Easy to create/modify without touching the main game logic.

---

## 🗂 Project Structure

```
SpaceInvadersV2/
│
├── data/
│   ├── audio/               # Sound effects
│   ├── images/              # Sprites & backgrounds
│   ├── levels/              # Level text files
│
├── collision_detection.py   # Separate collision module (mask-based)
├── main.py                  # Game entry point
```

---

## ⚙️ How It Works

### **Level Loading**

* The `load_level()` function reads a `.txt` file and maps integers to enemy types.
* Automatically centers the alien formation.

### **Collision Handling**

* All collisions are delegated to the `collision_detection` module.
* Mask-based detection ensures that only visible pixels register hits.
* Example:

```python
collided, x, y, score = cd.handle_list_collision(enemies, bullets, score)
```

### **Power-Up System**

* On enemy death, a random check spawns a power-up/down.
* These are handled with separate collision functions to alter spaceship attributes.

---

## 🔊 Audio System

* Uses `pygame.mixer.set_num_channels(100)` for simultaneous overlapping sound effects.
* Sounds:
  * Shooting (player & alien)
  * Explosion
  * Game Over
  * Power-Up / Power-Down
  * Level-Up
  * Health Down

---

## 🖥 How to Run

```bash
# 1. Clone repository
git clone <repo-url>
cd SpaceInvadersV2

# 2. Install dependencies
pip install pygame

# 3. Run the game
python main.py
```

**Requirements:**

* Python 3.8+
* Pygame 2.0+

---

## 🎯 Gameplay Controls

| Action     | Control               |
|------------|-----------------------|
| Move ship  | Mouse movement        |
| Shoot      | Left mouse click      |
| Start Game | Click `Start` in menu |
| Quit Game  | Click `Quit` in menu  |

---

## 🛠 Customization

* **Levels:** Edit text files in `data/levels/`.
* **Sprites:** Replace `.png` files in `data/images/`.
* **Sounds:** Replace `.wav` files in `data/audio/`.

---

## 📌 Notes

* **No physics engine** — all movement is manually coded for precise arcade behavior.
* Explosion frames are preloaded for performance.
* Power-up drop chance: 1 in 3 enemies killed.

---

* Ibtasaam Mughal (August, 2025)
