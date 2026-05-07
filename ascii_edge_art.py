import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cv2
import io
import random

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(page_title="Binary Edge Art", page_icon="⬛", layout="wide")

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

html, body, [class*="css"] {
    background-color: #0a0a0a;
    color: #e0e0e0;
    font-family: 'Share Tech Mono', monospace;
}

h1, h2, h3 {
    font-family: 'Orbitron', monospace;
    letter-spacing: 0.1em;
}

.stApp {
    background: #0a0a0a;
}

.block-container {
    padding-top: 2rem;
}

section[data-testid="stSidebar"] {
    background: #111;
    border-right: 1px solid #222;
}

.stSlider > div > div > div {
    background: #00ff88;
}

.stButton > button {
    background: #00ff88;
    color: #0a0a0a;
    font-family: 'Orbitron', monospace;
    font-weight: 700;
    border: none;
    border-radius: 2px;
    padding: 0.6rem 2rem;
    letter-spacing: 0.1em;
    transition: all 0.2s;
    width: 100%;
}

.stButton > button:hover {
    background: #00cc66;
    transform: translateY(-1px);
    box-shadow: 0 0 20px #00ff8855;
}

.stFileUploader {
    border: 1px dashed #333;
    border-radius: 4px;
    padding: 1rem;
}

.header-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.2rem;
    font-weight: 900;
    color: #00ff88;
    letter-spacing: 0.15em;
    margin-bottom: 0;
    text-shadow: 0 0 30px #00ff8844;
}

.header-sub {
    font-family: 'Share Tech Mono', monospace;
    color: #555;
    font-size: 0.85rem;
    letter-spacing: 0.2em;
    margin-top: 0.2rem;
}

.algo-box {
    background: #111;
    border: 1px solid #1a1a1a;
    border-left: 3px solid #00ff88;
    padding: 1rem 1.5rem;
    border-radius: 2px;
    margin-bottom: 1rem;
}

.algo-box h4 {
    color: #00ff88;
    font-family: 'Orbitron', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    margin-bottom: 0.5rem;
}

.algo-box p {
    color: #888;
    font-size: 0.82rem;
    line-height: 1.6;
    margin: 0;
}

.metric-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
}

.metric-box {
    background: #111;
    border: 1px solid #1a1a1a;
    padding: 0.5rem 1rem;
    border-radius: 2px;
    font-size: 0.75rem;
    color: #555;
}

.metric-box span {
    color: #00ff88;
    font-size: 1rem;
    display: block;
}

stImage > img {
    border-radius: 2px;
}
</style>
""", unsafe_allow_html=True)


# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown('<p class="header-title">BINARY EDGE ART</p>', unsafe_allow_html=True)
st.markdown('<p class="header-sub">// edge detection → binary character mapping //</p>', unsafe_allow_html=True)
st.markdown("---")


# ─── Algorithm explanation ───────────────────────────────────────────────────
with st.expander("⚙  HOW THE ALGORITHM WORKS", expanded=False):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="algo-box">
        <h4>01 // GRAYSCALE</h4>
        <p>Convert RGB image to single-channel luminance. Reduces computation while preserving structural information.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="algo-box">
        <h4>02 // SOBEL / CANNY</h4>
        <p>Compute gradient magnitude using Sobel kernels (Gx, Gy) or run Canny for cleaner, thinner edges. G = √(Gx²+Gy²).</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="algo-box">
        <h4>03 // THRESHOLD</h4>
        <p>Binarize the gradient map. Pixels above threshold = edge. Below = background. Controls character density.</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="algo-box">
        <h4>04 // CHAR MAP</h4>
        <p>Place '0' or '1' (or any chars) at edge pixels. Optionally colorize using original pixel RGB values.</p>
        </div>
        """, unsafe_allow_html=True)


# ─── Sidebar controls ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙ CONTROLS")
    st.markdown("---")

    uploaded = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png", "webp"])

    st.markdown("#### Edge Detection")
    detector = st.selectbox("Method", ["Canny", "Sobel", "Laplacian"], index=0)

    if detector == "Canny":
        low_thresh = st.slider("Canny Low Threshold", 10, 150, 50)
        high_thresh = st.slider("Canny High Threshold", 50, 300, 150)
    else:
        edge_thresh = st.slider("Edge Threshold", 0, 255, 80)

    st.markdown("#### Character Settings")
    char_set = st.selectbox("Character Set", [
        "Binary (0 & 1)",
        "Binary (0 only)",
        "Binary (1 only)",
        "Mixed (0,1,|,—)",
        "Custom"
    ])
    if char_set == "Custom":
        custom_chars = st.text_input("Your chars (no spaces)", value="01!@#")
    
    char_size = st.slider("Character Size (px)", 4, 20, 8)
    density = st.slider("Character Density", 0.1, 1.0, 0.7, step=0.05)

    st.markdown("#### Color Mode")
    color_mode = st.selectbox("Color", [
        "Green on Black (Matrix)",
        "White on Black",
        "Original Colors",
        "Red on Black",
        "Cyan on Black",
    ])

    st.markdown("#### Output")
    output_scale = st.slider("Output Scale", 0.5, 2.0, 1.0, step=0.25)
    bg_opacity = st.slider("Background Image Blend", 0.0, 0.5, 0.0, step=0.05)

    generate = st.button("⬛ GENERATE")


# ─── Core functions ──────────────────────────────────────────────────────────
def get_char_set(name, custom=""):
    sets = {
        "Binary (0 & 1)": list("01"),
        "Binary (0 only)": ["0"],
        "Binary (1 only)": ["1"],
        "Mixed (0,1,|,—)": list("01|—\\/_"),
        "Custom": list(custom) if custom else list("01"),
    }
    return sets.get(name, list("01"))


def get_colors(mode, orig_pixel=None):
    """Returns (fg_color, bg_color) as RGB tuples."""
    bg = (0, 0, 0)
    if mode == "Green on Black (Matrix)":
        return (0, 255, 136), bg
    elif mode == "White on Black":
        return (220, 220, 220), bg
    elif mode == "Original Colors":
        if orig_pixel is not None:
            r, g, b = int(orig_pixel[0]), int(orig_pixel[1]), int(orig_pixel[2])
            # Boost brightness a bit
            factor = 1.4
            r = min(255, int(r * factor))
            g = min(255, int(g * factor))
            b = min(255, int(b * factor))
            return (r, g, b), bg
        return (0, 255, 136), bg
    elif mode == "Red on Black":
        return (255, 60, 60), bg
    elif mode == "Cyan on Black":
        return (0, 220, 255), bg
    return (0, 255, 136), bg


def detect_edges(gray_np, method, **kwargs):
    if method == "Canny":
        edges = cv2.Canny(gray_np, kwargs.get("low", 50), kwargs.get("high", 150))
    elif method == "Sobel":
        sx = cv2.Sobel(gray_np, cv2.CV_64F, 1, 0, ksize=3)
        sy = cv2.Sobel(gray_np, cv2.CV_64F, 0, 1, ksize=3)
        mag = np.sqrt(sx**2 + sy**2)
        mag = np.uint8(np.clip(mag / mag.max() * 255, 0, 255))
        _, edges = cv2.threshold(mag, kwargs.get("thresh", 80), 255, cv2.THRESH_BINARY)
    elif method == "Laplacian":
        lap = cv2.Laplacian(gray_np, cv2.CV_64F)
        lap = np.uint8(np.clip(np.abs(lap) / np.abs(lap).max() * 255, 0, 255))
        _, edges = cv2.threshold(lap, kwargs.get("thresh", 80), 255, cv2.THRESH_BINARY)
    return edges


def generate_ascii_art(img_pil, edges_np, chars, char_size, density, color_mode, bg_blend, scale):
    orig_w, orig_h = img_pil.size
    out_w = int(orig_w * scale)
    out_h = int(orig_h * scale)

    # Resize source data to output size
    img_resized = img_pil.resize((out_w, out_h), Image.LANCZOS)
    orig_np = np.array(img_resized)

    edges_resized = cv2.resize(edges_np, (out_w, out_h), interpolation=cv2.INTER_NEAREST)

    # Create output canvas
    canvas = Image.new("RGB", (out_w, out_h), (0, 0, 0))

    # Optional: blend original image in background
    if bg_blend > 0:
        dark_orig = Image.blend(Image.new("RGB", (out_w, out_h), (0, 0, 0)), img_resized, bg_blend)
        canvas.paste(dark_orig)

    draw = ImageDraw.Draw(canvas)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", char_size)
    except Exception:
        font = ImageFont.load_default()

    # Determine char bounding box
    try:
        bbox = font.getbbox("0")
        cw = bbox[2] - bbox[0]
        ch = bbox[3] - bbox[1]
    except Exception:
        cw, ch = char_size, char_size

    # Iterate in grid steps
    for y in range(0, out_h - ch, max(1, ch)):
        for x in range(0, out_w - cw, max(1, cw)):
            # Check if this region has an edge
            region = edges_resized[y:y+ch, x:x+cw]
            edge_ratio = np.count_nonzero(region) / (ch * cw + 1e-6)

            if edge_ratio > (1 - density) * 0.5 and random.random() < density:
                char = random.choice(chars)
                orig_pixel = orig_np[min(y, out_h-1), min(x, out_w-1)]
                fg, _ = get_colors(color_mode, orig_pixel if color_mode == "Original Colors" else None)
                draw.text((x, y), char, font=font, fill=fg)

    return canvas


# ─── Main area ──────────────────────────────────────────────────────────────
if uploaded is None:
    st.markdown("""
    <div style="
        border: 1px dashed #222;
        border-radius: 4px;
        padding: 4rem 2rem;
        text-align: center;
        color: #333;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.9rem;
        letter-spacing: 0.15em;
    ">
        <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.3;">⬛</div>
        UPLOAD AN IMAGE TO BEGIN<br>
        <span style="font-size: 0.7rem; color: #222;">// supported: jpg, png, webp //</span>
    </div>
    """, unsafe_allow_html=True)
else:
    img_pil = Image.open(uploaded).convert("RGB")
    img_np = np.array(img_pil)
    gray_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

    # Always show original
    col_orig, col_edge, col_result = st.columns([1, 1, 1])

    with col_orig:
        st.markdown("**// ORIGINAL**")
        st.image(img_pil, use_container_width=True)

    # Compute edges
    if detector == "Canny":
        edges = detect_edges(gray_np, "Canny", low=low_thresh, high=high_thresh)
    else:
        edges = detect_edges(gray_np, detector, thresh=edge_thresh)

    with col_edge:
        st.markdown("**// EDGE MAP**")
        st.image(edges, use_container_width=True, clamp=True)

    # Generate art on button press or auto if already generated
    if generate or "result_img" in st.session_state:
        if generate:
            with st.spinner("Rendering binary edge art..."):
                chars = get_char_set(char_set, custom_chars if char_set == "Custom" else "")
                result = generate_ascii_art(
                    img_pil, edges, chars, char_size, density,
                    color_mode, bg_opacity, output_scale
                )
                st.session_state["result_img"] = result

        result = st.session_state["result_img"]

        with col_result:
            st.markdown("**// BINARY EDGE ART**")
            st.image(result, use_container_width=True)

        # Download
        buf = io.BytesIO()
        result.save(buf, format="PNG")
        st.download_button(
            label="⬇ DOWNLOAD PNG",
            data=buf.getvalue(),
            file_name="binary_edge_art.png",
            mime="image/png",
        )

        # Stats
        edge_pixels = int(np.count_nonzero(edges))
        total_pixels = edges.size
        st.markdown(f"""
        <div style="display:flex; gap:1rem; margin-top:1rem;">
            <div class="metric-box">EDGE PIXELS<span>{edge_pixels:,}</span></div>
            <div class="metric-box">TOTAL PIXELS<span>{total_pixels:,}</span></div>
            <div class="metric-box">EDGE DENSITY<span>{100*edge_pixels/total_pixels:.1f}%</span></div>
            <div class="metric-box">METHOD<span>{detector.upper()}</span></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        with col_result:
            st.markdown("**// BINARY EDGE ART**")
            st.markdown("""
            <div style="border:1px dashed #1a1a1a; border-radius:4px; padding:3rem;
                        text-align:center; color:#333; font-size:0.8rem; letter-spacing:0.15em;">
                PRESS GENERATE →
            </div>
            """, unsafe_allow_html=True)