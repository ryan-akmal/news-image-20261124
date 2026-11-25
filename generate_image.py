#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news front page (1024x1024 PNG).

Original artwork drawn for this entry: every pictogram is built from flat
Pillow shapes, every word set in DejaVu. No photograph, no borrowed art,
no network. Run:  python3 generate_image.py   (writes entry.png here)
"""
import math
from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 1024, 1024
PAPER = (248, 244, 235)
INK = (22, 30, 46)
NAVY = (18, 32, 60)
GOLD = (232, 194, 104)
CRIMSON = (176, 32, 32)
MUTED = (96, 96, 96)
CARD_LINE = (203, 198, 188)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_PLAIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def fold(draw, text, face, width):
    """Split text into lines no wider than `width` pixels."""
    words = text.split()
    rows, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=face) <= width:
            current = trial
        else:
            if current:
                rows.append(current)
            current = word
    if current:
        rows.append(current)
    return rows


def paragraph(draw, x, y, text, face, colour, width, step):
    for line in fold(draw, text, face, width):
        draw.text((x, y), line, font=face, fill=colour)
        y += step
    return y


def burst(draw, cx, cy, r_out, r_in, points, colour):
    """Starburst polygon centred on (cx, cy)."""
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=colour)


# ---------- pictograms, each drawn inside a square box ----------
def pic_tower(d, x, y, s):
    # A tall tower with setbacks, an antenna, and an impact burst.
    bx, by = x + s * 0.30, y + s * 0.34
    bw, bh = s * 0.40, s * 0.60
    d.rectangle([bx, by, bx + bw, by + bh], fill=(52, 68, 96),
                outline=NAVY, width=3)
    d.rectangle([bx + bw * 0.18, by - s * 0.12, bx + bw * 0.82, by],
                fill=(70, 88, 120), outline=NAVY, width=3)
    d.line([(bx + bw / 2, by - s * 0.12), (bx + bw / 2, by - s * 0.26)],
           fill=NAVY, width=4)
    d.ellipse([bx + bw / 2 - 4, by - s * 0.30, bx + bw / 2 + 4,
               by - s * 0.30 + 8], fill=CRIMSON)
    for row in range(5):
        for col in range(3):
            wx = bx + 8 + col * (bw - 16) / 3
            wy = by + 10 + row * 16
            d.rectangle([wx, wy, wx + 7, wy + 9], fill=(232, 194, 104))
    burst(d, bx + bw + 14, by + 6, 26, 12, 8, (230, 126, 34))
    burst(d, bx + bw + 14, by + 6, 14, 6, 8, (255, 220, 120))


def pic_ruin(d, x, y, s):
    # Two buildings, one with a jagged broken top and drifting smoke.
    bx, by = x + s * 0.10, y + s * 0.40
    d.rectangle([bx, by, bx + s * 0.34, by + s * 0.54],
                fill=(96, 104, 122), outline=NAVY, width=3)
    d.polygon([(bx + s * 0.40, by + s * 0.10), (bx + s * 0.48, by),
               (bx + s * 0.56, by + s * 0.12), (bx + s * 0.64, by + s * 0.02),
               (bx + s * 0.74, by + s * 0.14), (bx + s * 0.74, by + s * 0.54),
               (bx + s * 0.40, by + s * 0.54)],
              fill=(70, 78, 96), outline=NAVY, width=3)
    for wy in (by + 14, by + 34, by + 54):
        d.rectangle([bx + 8, wy, bx + 22, wy + 8], fill=(232, 194, 104))
        d.rectangle([bx + s * 0.46, wy, bx + s * 0.46 + 14, wy + 8],
                    fill=(232, 194, 104))
    for cx, cy, r in ((x + s * 0.62, y + s * 0.16, 12),
                      (x + s * 0.72, y + s * 0.08, 15),
                      (x + s * 0.84, y + s * 0.14, 10)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(160, 160, 160))


def pic_warning(d, x, y, s):
    # A warning triangle over a closed border barrier.
    cx, cy = x + s / 2, y + s * 0.42
    d.polygon([(cx, y + s * 0.06), (cx + s * 0.38, y + s * 0.72),
               (cx - s * 0.38, y + s * 0.72)],
              fill=(244, 196, 66), outline=(20, 20, 20), width=4)
    d.text((cx, y + s * 0.24), "!", font=load(SANS_BOLD, 64),
           fill=(20, 20, 20), anchor="ma")
    d.rectangle([x + s * 0.10, y + s * 0.80, x + s * 0.90, y + s * 0.88],
                fill=(200, 60, 60))
    for fx in (0.20, 0.45, 0.70):
        d.rectangle([x + s * fx, y + s * 0.80, x + s * fx + 8,
                     y + s * 0.94], fill=(40, 40, 40))


def pic_fire(d, x, y, s):
    # An apartment block with flames licking one corner.
    bx, by = x + s * 0.16, y + s * 0.30
    bw, bh = s * 0.56, s * 0.64
    d.rectangle([bx, by, bx + bw, by + bh], fill=(122, 96, 78),
                outline=NAVY, width=3)
    for row in range(3):
        for col in range(3):
            wx = bx + 10 + col * (bw - 20) / 3
            wy = by + 12 + row * (bh - 24) / 3
            d.rectangle([wx, wy, wx + 12, wy + 12],
                        fill=(232, 194, 104) if (row + col) % 2 else (60, 60, 60))
    fx = bx + bw - 6
    d.polygon([(fx - 26, by + 30), (fx - 4, by - 18), (fx + 10, by + 12),
               (fx + 26, by - 6), (fx + 20, by + 34), (fx + 2, by + 44)],
              fill=(230, 126, 34))
    d.polygon([(fx - 12, by + 34), (fx + 2, by + 8), (fx + 14, by + 30),
               (fx + 4, by + 44)], fill=(244, 196, 66))


def pic_fall(d, x, y, s):
    # A falling market line over axes, with an arrowhead pointing down.
    d.line([(x + s * 0.14, y + s * 0.12), (x + s * 0.14, y + s * 0.86)],
           fill=INK, width=4)
    d.line([(x + s * 0.14, y + s * 0.86), (x + s * 0.90, y + s * 0.86)],
           fill=INK, width=4)
    pts = [(x + s * 0.20, y + s * 0.26), (x + s * 0.38, y + s * 0.34),
           (x + s * 0.56, y + s * 0.30), (x + s * 0.74, y + s * 0.58),
           (x + s * 0.86, y + s * 0.76)]
    d.line(pts, fill=CRIMSON, width=6, joint="curve")
    d.polygon([(pts[-1][0], pts[-1][1] + 14), (pts[-1][0] - 14, pts[-1][1] - 4),
               (pts[-1][0] + 2, pts[-1][1] - 12)], fill=CRIMSON)
    for px, py in pts:
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=CRIMSON)


def pic_cup(d, x, y, s):
    # A gold winners' cup with handles, stem and base.
    cx = x + s / 2
    d.ellipse([cx - s * 0.30, y + s * 0.10, cx + s * 0.30, y + s * 0.52],
              fill=(232, 194, 104), outline=(150, 110, 40), width=3)
    d.rectangle([cx - s * 0.30, y + s * 0.10, cx + s * 0.30, y + s * 0.24],
                fill=(244, 210, 130))
    for side in (-1, 1):
        d.arc([cx + side * s * 0.30 - s * 0.16, y + s * 0.16,
               cx + side * s * 0.30 + s * 0.16, y + s * 0.44],
              270 if side < 0 else 90, 90 if side < 0 else 270,
              fill=(150, 110, 40), width=6)
    d.rectangle([cx - 6, y + s * 0.52, cx + 6, y + s * 0.72],
                fill=(150, 110, 40))
    d.rectangle([cx - s * 0.22, y + s * 0.72, cx + s * 0.22, y + s * 0.84],
                fill=(232, 194, 104), outline=(150, 110, 40), width=3)
    burst(d, cx, y + s * 0.06, 10, 4, 6, (255, 220, 120))


PANELS = [
    # (tag, accent, headline, caption, pictogram)
    ("GAZA", (178, 34, 34), "ISRAEL KILLS HAMAS SECURITY CHIEF",
     "Israeli airstrikes kill Hamas internal security director Naeem Abu "
     "Nahel and six others in Gaza.", pic_ruin),
    ("EUROPE", (29, 53, 87), "RUSSIA WARNS ESTONIA OF WAR",
     "Russia warns Estonia: closing the border risks 'open war'.",
     pic_warning),
    ("UKRAINE", (42, 110, 143), "FLAT HIT IN ZAPORIZHZHIA",
     "An overnight Russian strike hits an apartment block: 2 killed, 40 "
     "wounded, including four children.", pic_fire),
    ("MARKETS", (155, 34, 38), "STOCKS SLIP ON RATE FEARS",
     "The S&P 500 falls 0.95% and the Euro Stoxx 50 1.16% as a Fed "
     "official signals higher rates may come.", pic_fall),
]


def main():
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, CANVAS_W, 138], fill=NAVY)
    d.text((CANVAS_W // 2, 14), "THE WORLD IN ONE DAY",
           font=load(SERIF_BOLD, 56), fill=(255, 255, 255), anchor="ma")
    d.text((CANVAS_W // 2, 88), "TUESDAY  \u2022  24 NOVEMBER 2026",
           font=load(SANS_BOLD, 32), fill=GOLD, anchor="ma")
    d.rectangle([0, 138, CANVAS_W, 144], fill=GOLD)

    # Standfirst
    paragraph(d, 28, 158,
              "Six stories that defined the day: missiles over Riyadh, a "
              "Hamas chief killed in Gaza, Russia's warning to Estonia, a "
              "flat hit in Zaporizhzhia, markets sliding \u2014 and Senegal "
              "champions again.",
              load(SANS_PLAIN, 20), INK, CANVAS_W - 56, 27)

    # Lead story, full width
    lx, ly, lw, lh = 24, 212, CANVAS_W - 48, 158
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=(255, 255, 255),
                outline=CARD_LINE, width=2)
    d.rectangle([lx, ly, lx + lw, ly + 32], fill=(120, 40, 32))
    d.text((lx + 14, ly + 4), "YEMEN  \u2022  SAUDI ARABIA",
           font=load(SANS_BOLD, 19), fill=(255, 255, 255))
    pic_tower(d, lx + lw - 158, ly + 38, 112)
    tx = lx + 16
    paragraph(d, tx, ly + 44, "HOUTHIS STRIKE RIYADH TOWER",
              load(SANS_BOLD, 33), INK, lw - 190, 40)
    paragraph(d, tx, ly + 96,
              "Houthi missiles hit Riyadh's tallest tower for the second "
              "time in five days; 11 people injured. Fighters close in "
              "on Aden.",
              load(SANS_PLAIN, 19), (62, 62, 62), lw - 190, 25)

    # Four panels: 2 columns x 2 rows
    gx, gy = 24, 386
    pw, ph, gap = 480, 176, 16
    for i, (tag, accent, head, cap, pic) in enumerate(PANELS):
        col, row = i % 2, i // 2
        x0 = gx + col * (pw + gap)
        y0 = gy + row * (ph + gap)
        d.rectangle([x0, y0, x0 + pw, y0 + ph], fill=(255, 255, 255),
                    outline=CARD_LINE, width=2)
        d.rectangle([x0, y0, x0 + pw, y0 + 32], fill=accent)
        d.text((x0 + 14, y0 + 4), tag, font=load(SANS_BOLD, 19),
               fill=(255, 255, 255))
        pic(d, x0 + 10, y0 + 42, 118)
        tx = x0 + 142
        paragraph(d, tx, y0 + 44, head, load(SANS_BOLD, 25), INK,
                  pw - 158, 31)
        paragraph(d, tx, y0 + 110, cap, load(SANS_PLAIN, 17),
                  (62, 62, 62), pw - 158, 22)

    # Sport panel, full width
    sx, sy, sw, sh = 24, 770, CANVAS_W - 48, 84
    d.rectangle([sx, sy, sx + sw, sy + sh], fill=(255, 255, 255),
                outline=CARD_LINE, width=2)
    d.rectangle([sx, sy, sx + 150, sy + sh], fill=(28, 92, 58))
    d.text((sx + 75, sy + 26), "SPORT", font=load(SANS_BOLD, 22),
           fill=(255, 255, 255), anchor="ma")
    pic_cup(d, sx + 158, sy + 6, 66)
    paragraph(d, sx + 232, sy + 10, "SENEGAL CHAMPIONS AGAIN",
              load(SANS_BOLD, 26), INK, sw - 250, 32)
    paragraph(d, sx + 232, sy + 44,
              "Senegal are reinstated as 2025 Africa Cup of Nations "
              "champions after the sport's top court rules in their favour.",
              load(SANS_PLAIN, 17), (62, 62, 62), sw - 250, 22)

    # Also in the news
    ay = 868
    d.rectangle([24, ay, CANVAS_W - 24, ay + 78], fill=(233, 227, 213),
                outline=CARD_LINE, width=2)
    paragraph(d, 40, ay + 8,
              "ALSO IN THE NEWS:  Putin admits Ukraine's oil strikes strain "
              "Russia's fuel market  \u2022  Iraq orders takeover of Kurdish "
              "oilfields  \u2022  UN seeks probe into Benghazi port attacks  "
              "\u2022  Nepal hit by a 5.6 earthquake  \u2022  Jensen Huang "
              "back as Nvidia chief  \u2022  Spain amnesties Puigdemont",
              load(SANS_BOLD, 17), INK, CANVAS_W - 80, 23)

    # Footer
    d.text((CANVAS_W // 2, CANVAS_H - 26),
           "Sources: Just Security, Reuters, The Guardian, ISW, AP \u2014 "
           "reported 24 November 2026",
           font=load(SANS_PLAIN, 15), fill=MUTED, anchor="ma")

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
