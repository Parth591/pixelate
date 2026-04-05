"""
Generates the three memory fragments using 3-of-3 additive secret sharing.

Message: Deathly Hallows symbol + "COMPUTER VISION" (white on black, 800×500)

Secret sharing (mod 256):
    share1 = random noise N1
    share2 = random noise N2
    share3 = (message − N1 − N2) mod 256

Each share on its own is uniformly random (pure noise) — no visual information
whatsoever is present in any individual fragment.

Reconstruction (done by solution.cpp):
    (share1 + share2 + share3) mod 256 = message

Charm transforms applied before saving (from tasks.md):
    fragment_a  ←  share1  :  horizontal flip, then invert (255 − value)
    fragment_b  ←  share2  :  no charm
    fragment_c  ←  share3  :  vertical flip
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
import math

BASE = os.path.dirname(os.path.abspath(__file__))
W, H = 800, 500

# ---------------------------------------------------------------------------
# 1. Draw the message: Deathly Hallows symbol + "COMPUTER VISION"
# ---------------------------------------------------------------------------
msg = Image.new("L", (W, H), 0)   # black canvas
draw = ImageDraw.Draw(msg)

# --- Deathly Hallows geometry (centered horizontally, upper half) ---
cx, tri_top, tri_h = W // 2, 40, 230
tri_bot = tri_top + tri_h
half_base = tri_h / math.sqrt(3)          # half-width of equilateral base
apex  = (cx, tri_top)
bl    = (cx - half_base, tri_bot)
br    = (cx + half_base, tri_bot)

# triangle outline
LW = 4   # line width
draw.polygon([apex, bl, br], outline=255, fill=0)
# thicken manually by drawing at ±1
for d in range(1, LW):
    draw.polygon(
        [(apex[0], apex[1]-d), (bl[0]-d, bl[1]+d), (br[0]+d, br[1]+d)],
        outline=255, fill=0
    )

# inscribed circle (incircle of equilateral: radius = tri_h / 3)
ic_r  = int(tri_h / 3)
ic_cx = cx
ic_cy = tri_bot - ic_r      # sits on the base, tangent to all three sides
for d in range(LW):
    r = ic_r - d
    draw.ellipse([ic_cx - r, ic_cy - r, ic_cx + r, ic_cy + r],
                 outline=255, fill=0)

# vertical line from apex to base mid
for d in range(-(LW//2), LW//2 + 1):
    draw.line([(cx + d, tri_top), (cx + d, tri_bot)], fill=255, width=1)

# --- "COMPUTER VISION" text below the symbol ---
font_paths = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
font = None
for fp in font_paths:
    if os.path.exists(fp):
        font = ImageFont.truetype(fp, 42)
        break
if font is None:
    font = ImageFont.load_default()

text = "COMPUTER VISION"
bb   = draw.textbbox((0, 0), text, font=font)
tw   = bb[2] - bb[0]
tx   = (W - tw) // 2
ty   = tri_bot + 28
draw.text((tx, ty), text, font=font, fill=255)

message = np.array(msg, dtype=np.uint8)   # 0 (black) or 255 (white)

# Save for visual reference (not used by solution)
Image.fromarray(message).save(os.path.join(BASE, "message_reference.png"))
print("Saved message_reference.png  (the secret — don't show this!)")

# ---------------------------------------------------------------------------
# 2. Additive secret sharing  mod 256
#    share1 + share2 + share3 ≡ message  (mod 256)
# ---------------------------------------------------------------------------
secret_rng = np.random.default_rng(42)

share1 = secret_rng.integers(0, 256, (H, W), dtype=np.uint8)   # pure noise
share2 = secret_rng.integers(0, 256, (H, W), dtype=np.uint8)   # pure noise
share3 = ((message.astype(np.int32)
           - share1.astype(np.int32)
           - share2.astype(np.int32)) % 256).astype(np.uint8)

# Sanity check
assert np.all(((share1.astype(np.int32)
                + share2.astype(np.int32)
                + share3.astype(np.int32)) % 256).astype(np.uint8) == message), \
    "Secret sharing sanity check failed!"

# ---------------------------------------------------------------------------
# 3. Apply charm transforms and save fragments
#    fragment_a  ←  share1  :  hflip then invert
#    fragment_b  ←  share2  :  no charm
#    fragment_c  ←  share3  :  vflip
# ---------------------------------------------------------------------------
frag_a = 255 - np.fliplr(share1)
frag_b = share2
frag_c = np.flipud(share3)

Image.fromarray(frag_a).save(os.path.join(BASE, "fragment_a.png"))
Image.fromarray(frag_b).save(os.path.join(BASE, "fragment_b.png"))
Image.fromarray(frag_c).save(os.path.join(BASE, "fragment_c.png"))

print("Saved fragment_a.png  (share1 → hflip → invert)")
print("Saved fragment_b.png  (share2 → as-is)")
print("Saved fragment_c.png  (share3 → vflip)")
print("\nAll three fragments are pure noise — message only visible after reconstruction.")
