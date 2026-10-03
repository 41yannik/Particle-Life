"""
Renders an animated GIF of the simulation without opening a window.
Used for the README preview. Requires Pillow (pip install pillow).

Usage: python scripts/render_gif.py docs/assets/particle-life.gif 3
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import particle_life.config as config
from particle_life.simulation import ParticleSystem

SIZE = 400  # output edge length in pixels
WARMUP_STEPS = 800  # let structures form before recording
TOTAL_STEPS = 1400
FRAME_EVERY = 6


def main() -> None:
    out = sys.argv[1] if len(sys.argv) > 1 else "particle-life.gif"
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else config.SEED
    np.random.seed(seed)
    system = ParticleSystem()
    scale = SIZE / config.WINDOW_WIDTH
    frames = []
    for step in range(TOTAL_STEPS):
        system.update()
        if step < WARMUP_STEPS or step % FRAME_EVERY:
            continue
        img = Image.new("RGB", (SIZE, SIZE), config.BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)
        for (x, y), t in zip(system.get_positions() * scale, system.get_types()):
            color = config.COLOR_PALETTE[t % len(config.COLOR_PALETTE)]
            draw.ellipse([x - 1.3, y - 1.3, x + 1.3, y + 1.3], fill=color)
        frames.append(img.quantize(colors=16))
    frames[0].save(
        out, save_all=True, append_images=frames[1:], duration=50, loop=0
    )
    print(f"{len(frames)} frames written to {out}")


if __name__ == "__main__":
    main()
