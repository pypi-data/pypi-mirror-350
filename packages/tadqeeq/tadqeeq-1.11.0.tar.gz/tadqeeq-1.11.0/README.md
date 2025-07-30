# Tadqeeq – Image Annotator Tool

An interactive image annotation tool built with **PyQt5**, designed for efficient labeling of **segmentation masks** and **bounding boxes**.

> Developed by **Mohamed Behery** @ RTR Software Development - An "Orbits" Subsidiary
> 📅 April 30, 2025
> 🪪 Licensed under the MIT License

---

## 🚀 Widget Features

- ✅ **Minimalist Interactive Design**
- 🖌️ **Scroll through label classes / Adjust pen size** with the mouse wheel
- 🎨 **Supports segmentation masks (.png)** and **bounding boxes (.txt)**
- 🧠 **Dynamic label color generation** (HSV-based)
- 💬 **Floating labels** showing hovered and selected classes
- 💾 **Auto-save** and **manual save** (Ctrl+S)
- 🧽 **Flood-fill segmentation** with a postprocessing stage of **binary hole filling**
- 🚫 **Right-click erase mode** and **double-click to clear all**

## 🚀 CLI Features

- ✅ **Minimalist Design**
- 🎨 **Navigate through images** using A and D.

---

## 📦 Installation

### Option 1: Install via pip

```bash
pip install tadqeeq
```

### Option 2: Run from source

```bash
git clone https://github.com/orbits-it/tadqeeq.git
cd tadqeeq
pip install -r requirements.txt
```

---

## 🛠️ Usage

### Import in your code:

```python
from tadqeeq import ImageAnnotator
```
```python
from tadqeeq import ImageAnnotatorWindow
```

### Run CLI tool from command line (if installed via pip):

```bash
tadqeeq [--void_background|--verbose|--autosave|--use_bounding_boxes]* --images <images_directory_path> --classes <class_names_filepath> --bounding-boxes <bounding_boxes_directory_path> --semantic-segments <semantic_segments_directory_path>
```

**Notes:**
>1. Use A and D to navigate through images.</br>
>2. The annotation files could either be:</br>
>>a) PNG for **semantic segmentation masks** with class-labeled pixels on a white background.</br>
>>b) txt for **YOLO-style bounding boxes** formatted as: `label_index x_offset y_offset width height`.</br>
>3. <class_names_filepath> is a txt file containing a list of a class names used in annotating.</br>
>4. Tool Behavior in Segmentation:</br>
>>- If `void_background` is False:</br>
>>>- Increments all label values by 1, turning background (255) into 0 and shifting segment labels to start from 1.</br>
>>- If `void_background` is True:</br>
>>>- Leaves label values unchanged (255 remains as void).</br>
>>- Detects boundaries between segments and sets those boundary pixels to 255 (void label).

---

## 🧭 Controls

| Action                  | Mouse/Key |
|-------------------------|-----------|
| Draw / Fill segment     | Left-click / double-click |
| Erase (one object)      | Right-click + Left-click |
| Toggle erase mode       | Right-click |
| Clear all               | Double right-click |
| Scroll through labels / Adjust cursor size   | Mouse wheel |
| Save annotations        | Ctrl+S |
| Show label on hover     | Hover cursor |
| Navigate through images (CLI only) | A / D |

---

## 📁 Project Structure

```plaintext
root/
├── tadqeeq/
|   ├── __init__.py         # Entry point for importing
|   ├── widgets.py          # Contains ImageAnnotator class
|   ├── utils.py            # Helper methods (flood fill, bounding box logic)
|   ├── implementations.py  # Contains a working example of integrating the ImageAnnotator class within a full minimalist setup
|   ├── cli.py              # Entry point for a full annotation solution utilizing the code in `implementations.py`
├── README.md
├── LICENSE
├── setup.py
├── pyproject.toml
└── requirements.txt
```

---

## 🧑‍💻 Contributing

[Repository](https://github.com/orbits-it/tadqeeq.git)

Pull requests are welcome!  
If you add features (e.g. COCO export, brush tools, batch processing), please document them in the README.

---

## 📄 License

This project is licensed under the **MIT License**.  
See [LICENSE](./LICENSE) for the full license text.

---

## 💡 Acknowledgements

🎉 Built for computer vision practitioners needing fast, mouse-based labeling with clean overlays and autosave logic.

🌟 Special thanks to **PyQt5** for providing the powerful and flexible GUI toolkit that made the development of this interactive image annotator possible.

---

## 🔗 Related Resources

- [PyQt5 Docs](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [NumPy](https://numpy.org/)
- [scikit-image](https://scikit-image.org/)
- [SciPy](https://scipy.org/)
