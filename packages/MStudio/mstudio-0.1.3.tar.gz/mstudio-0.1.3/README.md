# MStudio
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)\
A comprehensive toolkit for editing and managing 2D and 3D markers in motion capture and biomechanical studies. Designed to be compatible with [Pose2Sim](https://github.com/perfanalytics/pose2sim), and [Sports2D](https://github.com/davidpagnon/Sports2D), providing seamless integration for marker data processing and analysis.

> **Note:** This is an initial release. Automated tests are minimal and only basic smoke tests are included. More comprehensive tests will be added in future updates.

---

## 📦 Installation

**Step 1. Create a virtual environment using Anaconda (recommended):**
```bash
conda create -n mstudio python=3.10 -y
conda activate mstudio
```

**Step 2. Install MStudio from PyPI:**
```bash
pip install mstudio
```

**From source:**
```bash
git clone https://github.com/hunminkim98/MStudio.git
cd MStudio
pip install .
```

---

## 🚀 Quick Start

### The Easiest Way to Run MStudio (Recommended!)

Just open your terminal and run:
```bash
mstudio
```

That's it! This is the safest way to launch the app.

> **Heads up!**
> If you try to run `main.py` directly (like `python MStudio/main.py`), you might get an error like:
> `ModuleNotFoundError: No module named 'MStudio'`
> To avoid this, always use the command above from the root folder.

---

### Want to Run main.py Directly?

If you're actively developing and want to quickly test changes, you can add these lines at the very top of `MStudio/main.py`:

```python
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
```

Now you can run:

```bash
python MStudio/main.py
```

---

## 📚 Documentation & Support
- [Issue Tracker](https://github.com/hunminkim98/MStudio/issues)

---

## Features

### 🎯 3D Marker Visualization

- Interactive 3D viewport with real-time marker display

- Customizable marker colors and sizes (TODO)

- Toggle marker labels visibility

- Coordinate system switching (Z-up/Y-up)

- Zoom and pan controls

### 🦴 Skeleton 

- Multiple pre-defined skeleton models:

  - BODY_25B
  - BODY_25
  - BODY_135
  - BLAZEPOSE
  - HALPE (26/68/136)
  - COCO (17/133)
  - MPII
- Toggle skeleton visibility
- Color-coded connections for outlier detection
### 📊 Data Analysis Tools
- Marker trajectory visualization
- Multi-axis coordinate plots
- Frame-by-frame navigation
- Timeline scrubbing with time/frame display modes
- Outlier detection and highlighting
- **Analysis Mode:**
  - Activate via the "Analysis" button.
  - Left-click markers in the 3D view to select up to 3 markers.
  - Visualize Euclidean distance (m) between 2 selected markers directly in the 3D view.
  - Visualize joint angle (°) formed by 3 selected markers (using the second selected marker as the vertex) directly in the 3D view.
  - Selected markers are highlighted (green, thicker) for clear identification.
### 🔧 Data Processing
- Multiple filtering options:
  - Butterworth filter
  - Butterworth on speed
  - Median filter
- Customizable filter parameters
- Pattern-based marker interpolation
- Interactive data selection and editing
### 💾 File Operations
- Import TRC/C3D files
- Export to TRC/C3D files
- Original data preservation

---

## Future Enhancements / TODO

- [v] Add skeleton lines for trunk.
- [ ] Drag and select multiple markers (requires changing left-click logic).
- [ ] Choose the view by clicking the plane (inspired by OpenSim GUI).
- [ ] Customize marker size, color, and opacity.
- [v] Add an arc for visualizing the range of motion.

