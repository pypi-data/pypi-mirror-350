
# hieuvision

A modular computer vision toolkit with built-in data augmentation and extensible tools.

---

## 📦 Installation

To install the latest version from PyPI:

```bash
pip install hieuvision
```

This will also install all necessary dependencies:

- `opencv-python`
- `albumentations`
- `tqdm`

---

## 🚀 Usage

### 🧰 Supported Tools

Currently available tool:

- `augment`: Perform brightness and contrast augmentation on image datasets with YOLO-style `.txt` labels.

More tools will be added in future updates.

---

### ✨ Example: Image Augmentation

Assume your dataset is structured like this:

```
dataset/
├── image1.jpg
├── image1.txt
├── image2.jpg
├── image2.txt
...
```

You can apply augmentation using:

```python
from hieuvision import HieuVision
from hieuvision.tools.augmenter import ImageAugmenter

augmenter = ImageAugmenter(
    input_dir="dataset",
    output_dir="dataset_augmented"
)

hv = HieuVision()
hv.add_tool("augment", augmenter)
hv.run_tool("augment")
```

What this does:

- Applies random brightness and contrast adjustments to each image.
- Saves the augmented image in the output directory.
- Copies corresponding YOLO `.txt` label files.
- Logs a warning if any label or image is missing.

---

## 🔧 Developer Guide

### Extend with custom tools

You can register your own tools in `HieuVision`:

```python
class MyCustomTool:
    def run(self):
        print("Running my custom tool")

tool = MyCustomTool()
hv = HieuVision()
hv.add_tool("custom", tool)
hv.run_tool("custom")
```

Each tool must implement a `.run()` method.

---

## 🛠 Requirements

These are installed automatically via `pip install hieuvision`:

- `opencv-python`
- `albumentations`
- `tqdm`

---

## 📁 Project Structure (for developers)

```
hieuvision/
├── hieuvision/
│   ├── __init__.py
│   ├── core.py
│   └── tools/
│       ├── __init__.py
│       └── augmenter.py
├── README.md
├── pyproject.toml
├── LICENSE
└── .github/
    └── workflows/
        └── publish.yml
```

---

## 📤 Publishing to PyPI

This project supports GitHub Actions for automatic publishing. Just push a Git tag like `v0.1.0`, and the package will be published to [https://pypi.org/project/hieuvision](https://pypi.org/project/hieuvision).

Make sure to:

- Create a PyPI token and add it to your repo secrets as `PYPI_API_TOKEN`
- Push your tag:

```bash
git tag v0.1.0
git push origin v0.1.0
```

---

## 📝 License

MIT License © 2025 Your Name
