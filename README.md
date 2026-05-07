# binary-edge-art

> Transform any image into viral binary ASCII art using edge detection algorithms.

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=flat-square&logo=opencv&logoColor=white)

---

## What is this?

**Binary Edge Art** is the viral image effect you've seen all over the internet — where a photo is converted into a dense grid of `0`s and `1`s that traces the edges and contours of the original subject. The result looks like a hacker aesthetic or a glitch art piece, but it's actually grounded in classical computer vision.

This repo gives you a fully interactive **Streamlit app** to generate the effect on any image, with manual controls for every parameter.

```
Original Image → Grayscale → Edge Detection → Threshold → 0/1 Character Mapping → Output
```

---

## Algorithm

The pipeline consists of 4 stages:

### 1. Grayscale Conversion
The input image is collapsed from 3-channel RGB into a single luminance channel. This reduces computational complexity while preserving the structural information needed for edge detection.

### 2. Edge Detection
Three methods are available:

| Method | Description | Best For |
|--------|-------------|----------|
| **Canny** | Two-threshold hysteresis filter. Produces thin, clean, connected edges. | Portraits, clean subjects |
| **Sobel** | Computes gradient magnitude: `G = √(Gx² + Gy²)` using 3×3 kernels | General use |
| **Laplacian** | Second-order derivative. Detects zero-crossings for very fine edges. | Textures, detail-heavy images |

### 3. Thresholding
The gradient map is binarized. Pixels above the threshold become **edge pixels** (candidates for characters). Below the threshold = background (empty space). This directly controls character density.

### 4. Character Mapping
The output canvas is iterated in a grid matching the chosen character size. At each grid cell that overlaps an edge pixel, a character (`0`, `1`, or any custom set) is placed with a randomly selected color — or sampled from the original image's RGB at that coordinate.

---

## Features

- **3 edge detection methods** — Canny, Sobel, Laplacian
- **Fully adjustable thresholds** for fine-grained edge control
- **Multiple character sets** — Binary `01`, mixed symbols, or fully custom
- **5 color modes** — Matrix green, white, original image colors, red, cyan
- **Density control** — How many edge pixels actually receive a character
- **Character size slider** — Controls the "resolution" of the ASCII grid
- **Background blend** — Ghost the original image behind the characters
- **Output scale** — Upscale/downscale the final render
- **Live edge map preview** alongside the original and result
- **One-click PNG download**

---

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/binary-edge-art.git
cd binary-edge-art
pip install -r requirements.txt
streamlit run ascii_edge_art.py
```

### Requirements

```
streamlit
opencv-python
pillow
numpy
```

Or install directly:

```bash
pip install streamlit opencv-python pillow numpy
```

---

## Usage

1. Run the app with `streamlit run ascii_edge_art.py`
2. Upload any image (JPG, PNG, WEBP) via the sidebar
3. Choose your edge detection method and tune the threshold
4. Pick a character set and color mode
5. Hit **GENERATE**
6. Download the result as PNG

---

## Examples

| Original | Edge Map | Binary Edge Art |
|----------|----------|-----------------|
| Portrait photo | Canny edges | Green `01` on black |
| Architecture | Sobel gradient | Original colors |
| Animal | Laplacian | White on black |

<img width="2286" height="1502" alt="image" src="https://github.com/user-attachments/assets/70a2cb79-223a-423f-8dad-d7cb3aed6bd8" />


---

## How the Viral Effect Works

The reason this effect went viral is simple: it turns any recognizable image into something that looks **hand-coded** — like a matrix of data that happens to form a face. The brain fills in the gaps between the sparse characters and reconstructs the original subject. It's a visual illusion rooted in **pareidolia** and **edge-based perception** — the same reason we can recognize line drawings as faces.

The key insight is that human vision relies primarily on **edges and contours**, not color or fill. Strip an image down to just its edges, map those edges to characters, and the subject is still instantly recognizable.

---

## Project Structure

```
binary-edge-art/
├── ascii_edge_art.py     # Main Streamlit app
├── requirements.txt      # Python dependencies
├── README.md
└── examples/             # Example input/output images (optional)
```
