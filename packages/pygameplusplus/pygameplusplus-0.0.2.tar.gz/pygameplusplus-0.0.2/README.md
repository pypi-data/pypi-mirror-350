# pygame++

**Enhanced utilities and tools for Pygame development.**

`pygame++` (pygameplusplus) is a lightweight Python library that extends the capabilities of [Pygame](https://www.pygame.org/) by offering extra features, simplified patterns, and useful abstractions to speed up game development and UI creation.

---

## ✨ Features

- 🚀 Simplified object and scene management
- 🖱️ Advanced input handling and events
- 🎮 UI helpers and overlays (works great with `pygame_gui`)
- 🧠 Modular and easy-to-extend structure
- 🔧 Designed for use with `pygame` projects and tools like `pygame_gui`

---

## 📦 Installation

Install via pip:

```bash
pip install pygamepp
```
## 🛠️ Usage Example
```python
import pygame
import pygamepp as ppp

# Example: Create a game window and run a basic loop
window = ppp.Game(title="Hello Pygame++")
def update(window):
  print("Update!!!")
window.update = update
window.run()
```

---

## 🧪 Requirements
- Python 3.7+
- pygame
- cairosvg (for converting .svg files)
- cairo c library

---

## 🤝 Contributing

Contributions are welcome! If you’d like to suggest a feature or submit a pull request, please open an issue or fork the project.

