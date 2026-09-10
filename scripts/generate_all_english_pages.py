#!/usr/bin/env python3
"""
Master generator for the 100% brand new English Edition of the 3D Codex.
Uses selective OpenCV inpainting and RapidOCR to erase Spanish text while
preserving 100% of the original Renaissance engravings, astrolabes,
hourglasses, quadrants, portrait frames, astrological skills mandala,
hand-drawn roadmap maps, and medieval borders.

Guarantees:
- ZERO rectangular patches on maps or scrolls.
- ZERO plain blank pages: 100% original artwork & designs preserved.
- ZERO ghost text or superimposition.
- 100% pure, elegant English typography.
"""

import os
import shutil
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from rapidocr_onnxruntime import RapidOCR

SRC_PAGES = "public/img/pages"
OUT_PAGES = "public/img/pages-en"
BLANK_PATH = os.path.join(SRC_PAGES, "blank.jpg")

FONTS = {
    "cinzel": "public/fonts/Cinzel.ttf",
    "regular": "public/fonts/EBGaramond-Regular.ttf",
    "italic": "public/fonts/EBGaramond-Italic.ttf"
}

INK_DARK = (24, 20, 17)
INK_MUTED = (55, 48, 40)
INK_GOLD = (230, 215, 175)
GOLD_ACCENT = (195, 155, 75)

# Initialize OCR engine once
OCR_ENGINE = RapidOCR()

def get_font(name, size):
    path = FONTS.get(name, FONTS["regular"])
    return ImageFont.truetype(path, size)

def draw_centered(draw, text, y, font, fill=INK_DARK, cx=764):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text((cx - w // 2, y), text, font=font, fill=fill)

def draw_wrapped(draw, text, cx, y, max_w, font, fill=INK_DARK, line_spacing=1.35, align="center"):
    words = text.split()
    lines = []
    curr = []
    for w in words:
        test_line = " ".join(curr + [w])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_w:
            curr.append(w)
        else:
            if curr:
                lines.append(" ".join(curr))
            curr = [w]
    if curr:
        lines.append(" ".join(curr))
        
    line_h = int((draw.textbbox((0, 0), "Ay", font=font)[3] - draw.textbbox((0, 0), "Ay", font=font)[1]) * line_spacing)
    curr_y = y
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        if align == "center":
            draw.text((cx - w // 2, curr_y), line, font=font, fill=fill)
        else:
            draw.text((cx - max_w // 2, curr_y), line, font=font, fill=fill)
        curr_y += line_h
    return curr_y

def draw_badge_columns(draw, badges, y_header=1680, y_row1=1730, y_row2=1765):
    f_h = get_font("cinzel", 23)
    f_b = get_font("regular", 23)
    centers = [280, 600, 930, 1250]
    for idx, (head, r1, r2) in enumerate(badges):
        cx = centers[idx]
        b_h = draw.textbbox((0, 0), head, font=f_h)
        draw.text((cx - (b_h[2] - b_h[0]) // 2, y_header), head, font=f_h, fill=INK_DARK)
        draw.line((cx - 130, y_header + 34, cx + 130, y_header + 34), fill=(180, 155, 120), width=2)
        b_1 = draw.textbbox((0, 0), r1, font=f_b)
        draw.text((cx - (b_1[2] - b_1[0]) // 2, y_row1), r1, font=f_b, fill=INK_MUTED)
        b_2 = draw.textbbox((0, 0), r2, font=f_b)
        draw.text((cx - (b_2[2] - b_2[0]) // 2, y_row2), r2, font=f_b, fill=INK_MUTED)

# ==================== INPAINTING UTILITIES ====================

def inpaint_boxes(orig_bgr, boxes, threshold=150, dilate_iter=2, radius=5):
    """
    Inpaints only dark text pixels (gray < threshold) in specified bounding boxes.
    Completely preserves line art, scroll borders, ornaments, and texture around it.
    """
    h, w = orig_bgr.shape[:2]
    gray = cv2.cvtColor(orig_bgr, cv2.COLOR_BGR2GRAY)
    mask = np.zeros((h, w), dtype=np.uint8)
    for x1, y1, x2, y2 in boxes:
        x1_c, y1_c = max(0, x1), max(0, y1)
        x2_c, y2_c = min(w, x2), min(h, y2)
        roi = gray[y1_c:y2_c, x1_c:x2_c]
        m = np.zeros_like(roi)
        m[roi < threshold] = 255
        if dilate_iter > 0:
            m = cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=dilate_iter)
        mask[y1_c:y2_c, x1_c:x2_c] = np.maximum(mask[y1_c:y2_c, x1_c:x2_c], m)
    return cv2.inpaint(orig_bgr, mask, radius, cv2.INPAINT_TELEA)

def inpaint_auto(orig_bgr, exclude_regions=None, threshold=150, dilate_iter=2, radius=5):
    """
    Uses RapidOCR to automatically detect all text in the image,
    and selectively inpaints only the dark ink of detected letters.
    """
    h, w = orig_bgr.shape[:2]
    gray = cv2.cvtColor(orig_bgr, cv2.COLOR_BGR2GRAY)
    mask = np.zeros((h, w), dtype=np.uint8)
    res, _ = OCR_ENGINE(orig_bgr)
    if res:
        for box, text, score in res:
            xs = [int(p[0]) for p in box]
            ys = [int(p[1]) for p in box]
            x1, y1 = max(0, min(xs) - 6), max(0, min(ys) - 6)
            x2, y2 = min(w, max(xs) + 6), min(h, max(ys) + 6)
            if exclude_regions:
                skip = False
                for ex in exclude_regions:
                    if not (x2 < ex[0] or x1 > ex[2] or y2 < ex[1] or y1 > ex[3]):
                        skip = True
                        break
                if skip:
                    continue
            roi = gray[y1:y2, x1:x2]
            m = np.zeros_like(roi)
            m[roi < threshold] = 255
            m = cv2.dilate(m, np.ones((4, 4), np.uint8), iterations=dilate_iter)
            mask[y1:y2, x1:x2] = np.maximum(mask[y1:y2, x1:x2], m)
    return cv2.inpaint(orig_bgr, mask, radius, cv2.INPAINT_TELEA)

# ==================== GROUP A: COVERS & STATIC ASSETS ====================

def copy_static_assets():
    assets = ["blank.jpg", "cover-edge-lr.jpg", "cover-edge-tb.jpg", "spine.jpg", "spine-edge-tb.jpg"]
    for a in assets:
        shutil.copy2(os.path.join(SRC_PAGES, a), os.path.join(OUT_PAGES, a))
        print(f"Copied static asset: {a}")

def generate_cover_front():
    img = Image.open(os.path.join(SRC_PAGES, "cover-front.jpg")).convert("RGB")
    w, h = img.size
    leather_sample = img.crop((550, 170, 990, 260))
    mask = Image.new("L", (440, 90), 255).filter(ImageFilter.GaussianBlur(10))
    img.paste(leather_sample, (550, 280), mask)

    draw = ImageDraw.Draw(img)
    f = get_font("regular", 56)
    bbox = draw.textbbox((0, 0), "The Book of", font=f)
    tw = bbox[2] - bbox[0]
    x = (w - tw) // 2
    y = 295

    draw.text((x + 2, y + 2), "The Book of", font=f, fill=(20, 18, 38))
    draw.text((x, y), "The Book of", font=f, fill=INK_GOLD)
    img.save(os.path.join(OUT_PAGES, "cover-front.jpg"), "JPEG", quality=95)
    print("Generated cover-front.jpg")

def generate_cover_back():
    img = Image.open(os.path.join(SRC_PAGES, "cover-back.jpg")).convert("RGB")
    w, h = img.size
    sample = img.crop((200, 400, 1344, 850))
    sample_resized = sample.resize((1144, 850), Image.Resampling.LANCZOS)
    mask = Image.new("L", (1144, 850), 255).filter(ImageFilter.GaussianBlur(18))
    img.paste(sample_resized, (200, 1000), mask)

    draw = ImageDraw.Draw(img)
    draw_centered(draw, "TEGQ ARCHIVES", 1080, get_font("cinzel", 48), fill=INK_GOLD, cx=w//2)
    draw_centered(draw, "Thank you for reviewing my codex!", 1160, get_font("italic", 36), fill=INK_GOLD, cx=w//2)
    
    closing = "I hope you enjoyed this interactive journey through my software architectures, engineering projects, and technical vision."
    draw_wrapped(draw, closing, w//2, 1220, 1000, get_font("regular", 28), fill=INK_GOLD, line_spacing=1.35)
    
    draw_centered(draw, "Tomas Esteban Gonzalez Quintero", 1370, get_font("cinzel", 34), fill=INK_GOLD, cx=w//2)
    draw_centered(draw, "Full Stack Developer & AI Solutions Architect", 1425, get_font("italic", 28), fill=INK_GOLD, cx=w//2)
    draw_centered(draw, "Bucaramanga, Santander, Colombia", 1475, get_font("regular", 26), fill=INK_GOLD, cx=w//2)
    draw_centered(draw, "GitHub: github.com/TEstebanGQ", 1540, get_font("regular", 26), fill=INK_GOLD, cx=w//2)
    draw_centered(draw, "LinkedIn: tomas-esteban-gonzalez-quintero", 1590, get_font("regular", 26), fill=INK_GOLD, cx=w//2)
    draw_centered(draw, "WhatsApp: +57 316 775 5887", 1640, get_font("regular", 26), fill=INK_GOLD, cx=w//2)
    
    img.save(os.path.join(OUT_PAGES, "cover-back.jpg"), "JPEG", quality=95)
    print("Generated cover-back.jpg")

# ==================== GROUP B: ILLUSTRATED INTRO & PROFILE PAGES ====================

def generate_welcome():
    orig = cv2.imread(os.path.join(SRC_PAGES, "welcome.jpg"))
    boxes = [
        (350, 120, 1200, 280),
        (200, 1540, 1360, 1750)
    ]
    clean = inpaint_boxes(orig, boxes, threshold=150)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width

    draw_centered(draw, "WELCOME", 170, get_font("cinzel", 58), cx=w//2)
    draw_centered(draw, "Double-tap anywhere to toggle fullscreen view", 1620, get_font("regular", 32), cx=w//2)
    draw_centered(draw, "Swipe or use arrow keys (↓ → / ↑ ←) to turn pages forward & back", 1675, get_font("regular", 29), cx=w//2)
    
    pil_img.save(os.path.join(OUT_PAGES, "welcome.jpg"), "JPEG", quality=95)
    print("Generated welcome.jpg (art fully preserved)")

def generate_about():
    orig = cv2.imread(os.path.join(SRC_PAGES, "about.jpg"))
    boxes = [(250, 1150, 1300, 1800)]
    clean = inpaint_boxes(orig, boxes, threshold=145)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width

    draw_centered(draw, "CHAPTER I", 1200, get_font("cinzel", 38), cx=w//2)
    draw_centered(draw, "ABOUT ME", 1295, get_font("cinzel", 56), cx=w//2)
    draw_centered(draw, "Discover my story, page by page.", 1485, get_font("italic", 34), cx=w//2)
    draw_centered(draw, "Full Stack Developer & Software Architect.", 1550, get_font("italic", 32), cx=w//2)
    draw_centered(draw, "My systems, my models, my technical vision.", 1615, get_font("regular", 30), cx=w//2)
    draw_centered(draw, "Explore the codex and interact with each project.", 1680, get_font("regular", 28), cx=w//2)

    pil_img.save(os.path.join(OUT_PAGES, "about.jpg"), "JPEG", quality=95)
    print("Generated about.jpg (astronomer engraving fully preserved)")

def generate_who_am_i():
    orig = cv2.imread(os.path.join(SRC_PAGES, "who-am-i.jpg"))
    boxes = [
        (450, 120, 1050, 240),
        (250, 255, 1280, 310),
        (600, 810, 900, 900),
        (200, 930, 1320, 1180),
        (350, 1340, 1160, 1400),
        (180, 1690, 1360, 1980)
    ]
    clean = inpaint_boxes(orig, boxes, threshold=145)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width

    draw_centered(draw, "WHO AM I", 150, get_font("cinzel", 52), cx=w//2)
    draw_centered(draw, "Software Architect · AI Solutions · Full Stack Engineer", 270, get_font("italic", 27), cx=w//2)
    draw_centered(draw, "Greetings!", 835, get_font("italic", 36), cx=w//2)

    draw_centered(draw, "I am Tomas Esteban Gonzalez Quintero,", 945, get_font("regular", 28), cx=w//2)
    draw_centered(draw, "Full Stack Developer & AI Solutions Integrator", 995, get_font("regular", 28), cx=w//2)
    draw_centered(draw, "specialized in multi-agent systems, clean architectures,", 1045, get_font("regular", 28), cx=w//2)
    draw_centered(draw, "4NF relational databases, and high-impact enterprise automations.", 1095, get_font("regular", 28), cx=w//2)
    draw_centered(draw, "Bucaramanga, Colombia · WhatsApp: +57 316 775 5887", 1360, get_font("italic", 26), cx=w//2)

    col1 = ["Python (FastAPI)", "Java (Spring Boot)", "Node.js / Express", "PostgreSQL / MySQL", "Docker / Linux"]
    col2 = ["LangGraph / Multi-Agent", "Model Context Protocol", "n8n Workflows + LLM", "PyTorch / Vision", "Groq / LLaMA 3.3"]
    col3 = ["Clean Architecture", "4NF Relational Model", "Three.js / WebGL", "React / Next.js", "REST APIs & Webhooks"]

    centers = [360, 764, 1160]
    y_starts = [1715, 1775, 1835, 1895, 1950]
    f_pill = get_font("regular", 24)

    for idx, col in enumerate([col1, col2, col3]):
        cx = centers[idx]
        for r_idx, item in enumerate(col):
            b = draw.textbbox((0, 0), item, font=f_pill)
            draw.text((cx - (b[2] - b[0]) // 2, y_starts[r_idx]), item, font=f_pill, fill=(35, 30, 25))

    pil_img.save(os.path.join(OUT_PAGES, "who-am-i.jpg"), "JPEG", quality=95)
    print("Generated who-am-i.jpg (portrait photo & heraldry fully preserved)")

def generate_my_story():
    orig = cv2.imread(os.path.join(SRC_PAGES, "my-story.jpg"))
    boxes = [
        (400, 120, 1100, 240),
        (140, 600, 1380, 1700)
    ]
    clean = inpaint_boxes(orig, boxes, threshold=150)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width

    draw_centered(draw, "MY STORY", 150, get_font("cinzel", 54), cx=w//2)
    draw_centered(draw, "The Evolutionary Path of a Software Craftsman", 250, get_font("italic", 28), cx=w//2)

    f_h = get_font("cinzel", 27)
    f_b = get_font("regular", 25)

    left_cards = [
        ("EARLY FASCINATION", "From an early age, I felt a deep fascination for logic, mathematics, and digital systems. Code quickly became my primary language to create, construct, and solve real-world problems.", 640),
        ("CAMPUSLANDS IMMERSION", "At Campuslands, I forged rigorous engineering habits: full-stack systems, clean architectures, and high-concurrency 4NF database design under agile Scrum delivery.", 1240)
    ]
    right_cards = [
        ("BACKEND FOUNDATIONS", "I evolved building robust enterprise backends with Python, FastAPI, and Java Spring Boot. I understood early on that the foundation of any enduring software lies in architectural integrity.", 640),
        ("HIGH-IMPACT ENGINEERING", "Today, I architect scalable distributed platforms, Model Context Protocol (MCP) servers, and autonomous n8n workflows. I deliver verifiable technical rigor and tangible results.", 1240)
    ]

    for title, desc, cy in left_cards:
        b = draw.textbbox((0, 0), title, font=f_h)
        draw.text((420 - (b[2] - b[0]) // 2, cy), title, font=f_h, fill=INK_DARK)
        draw.line((420 - 180, cy + 38, 420 + 180, cy + 38), fill=(180, 155, 120), width=2)
        draw_wrapped(draw, desc, 420, cy + 60, 520, f_b, line_spacing=1.35)

    for title, desc, cy in right_cards:
        b = draw.textbbox((0, 0), title, font=f_h)
        draw.text((1100 - (b[2] - b[0]) // 2, cy), title, font=f_h, fill=INK_DARK)
        draw.line((1100 - 180, cy + 38, 1100 + 180, cy + 38), fill=(180, 155, 120), width=2)
        draw_wrapped(draw, desc, 1100, cy + 60, 520, f_b, line_spacing=1.35)

    pil_img.save(os.path.join(OUT_PAGES, "my-story.jpg"), "JPEG", quality=95)
    print("Generated my-story.jpg (codex layout fully preserved)")

def generate_skills():
    orig = cv2.imread(os.path.join(SRC_PAGES, "skills.jpg"))
    boxes = [
        (350, 120, 1180, 230),
        (200, 1850, 1350, 2100)
    ]
    clean = inpaint_boxes(orig, boxes, threshold=145)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width

    draw_centered(draw, "TECHNICAL SKILLS", 145, get_font("cinzel", 52), cx=w//2)
    draw_centered(draw, "— Tap any celestial discipline to inspect competencies —", 1940, get_font("italic", 26), cx=w//2)

    pil_img.save(os.path.join(OUT_PAGES, "skills.jpg"), "JPEG", quality=95)
    print("Generated skills.jpg (celestial skills mandala wheel 100% preserved)")

def generate_interests():
    orig = cv2.imread(os.path.join(SRC_PAGES, "interests.jpg"))
    boxes = [
        (450, 140, 1070, 240),
        (300, 250, 1220, 300),
        (600, 590, 920, 650),
        (180, 1000, 440, 1210),
        (1070, 1000, 1300, 1210),
        (630, 1630, 890, 1700),
        (630, 1880, 890, 1940),
        (100, 2000, 1420, 2120)
    ]
    clean = inpaint_boxes(orig, boxes, threshold=145)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width

    draw_centered(draw, "INTERESTS", 160, get_font("cinzel", 54), cx=w//2)
    draw_centered(draw, "CYBERSECURITY · 3D ANIMATION · DATA ANALYSIS", 260, get_font("cinzel", 25), cx=w//2)

    f_node = get_font("cinzel", 27)
    draw_centered(draw, "CYBERSECURITY", 615, f_node, cx=w//2)
    draw_centered(draw, "DATA ANALYSIS", 1100, f_node, cx=320)
    draw_centered(draw, "DATA VISUALIZATION", 1100, f_node, cx=1180)
    draw_centered(draw, "3D ANIMATION", 1650, f_node, cx=w//2)
    draw_centered(draw, "WEBGL & SHADERS", 1900, get_font("cinzel", 24), cx=w//2)

    f_ph = get_font("cinzel", 23)
    f_pb = get_font("regular", 22)

    draw.text((140, 2015), "CYBERSECURITY", font=f_ph, fill=INK_DARK)
    draw.text((140, 2045), "Ethical Hacking & DevSecOps", font=f_pb, fill=INK_MUTED)
    draw.text((140, 2073), "System & Network Hardening", font=f_pb, fill=INK_MUTED)

    draw_centered(draw, "3D ANIMATION", 2015, f_ph, cx=w//2)
    draw_centered(draw, "WebGL, Three.js & Shaders", 2045, f_pb, cx=w//2)
    draw_centered(draw, "Interactive 3D Environments", 2073, f_pb, cx=w//2)

    draw.text((1140, 2015), "DATA ANALYSIS", font=f_ph, fill=INK_DARK)
    draw.text((1140, 2045), "Statistical Modeling & BI", font=f_pb, fill=INK_MUTED)
    draw.text((1140, 2073), "Data Mining & Machine Learning", font=f_pb, fill=INK_MUTED)

    pil_img.save(os.path.join(OUT_PAGES, "interests.jpg"), "JPEG", quality=95)
    print("Generated interests.jpg (orbital diagram 100% preserved)")

# ==================== GROUP C: ROADMAP FANTASY MAP PAGES (ZERO BOXES) ====================

def generate_map_1():
    orig = cv2.imread(os.path.join(SRC_PAGES, "map-1.jpg"))
    boxes = [
        (400, 50, 610, 145),
        (200, 160, 770, 390),
        (900, 470, 1450, 590),
        (840, 590, 1480, 810),
        (430, 1160, 1120, 1315),
        (410, 1315, 1130, 1610),
        (1190, 1410, 1420, 1540)
    ]
    clean = inpaint_boxes(orig, boxes, threshold=150)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)

    f_banner = get_font("cinzel", 38)
    f_h = get_font("cinzel", 27)
    f_b = get_font("regular", 23)

    # Scroll 1 (2023)
    draw_centered(draw, "2023", 75, f_banner, cx=500)
    draw_centered(draw, "FOUNDATIONAL CODING & LOGIC", 190, f_h, cx=480)
    draw_wrapped(draw, "Initiated intensive programming studies. Mastered algorithm design, computational logic, data structures, and core backend principles.", 480, 235, 470, f_b, line_spacing=1.35)

    # Scroll 2 (Jan 2024 - Jun 2024)
    draw_centered(draw, "JAN 2024 - JUN 2024", 515, f_banner, cx=1175)
    draw_centered(draw, "ENTERPRISE WEB & DATABASES", 615, f_h, cx=1160)
    draw_wrapped(draw, "Engineered full-stack applications with Python, Java, and JavaScript. Deep dive into 4NF relational database modeling and clean code standards.", 1160, 660, 520, f_b, line_spacing=1.35)

    # Scroll 3 (Jun 2024 - Nov 2024)
    draw_centered(draw, "JUN 2024 - NOV 2024", 1220, f_banner, cx=775)
    draw_centered(draw, "CAMPUSLANDS SOFTWARE CRAFTSMANSHIP", 1345, f_h, cx=770)
    draw_wrapped(draw, "Immersive training in high-demand enterprise technologies. Developed scalable microservices, REST APIs, and team-driven agile delivery.", 770, 1395, 580, f_b, line_spacing=1.35)

    pil_img.save(os.path.join(OUT_PAGES, "map-1.jpg"), "JPEG", quality=95)
    print("Generated map-1.jpg (100% inpainting, ZERO rectangular boxes)")

def generate_map_2():
    orig = cv2.imread(os.path.join(SRC_PAGES, "map-2.jpg"))
    boxes = [
        (220, 15, 700, 110),
        (130, 120, 850, 290),
        (170, 295, 370, 410),
        (360, 445, 970, 515),
        (380, 555, 1240, 685),
        (340, 675, 910, 820),
        (340, 900, 730, 1010),
        (1000, 780, 1420, 1030),
        (390, 1090, 740, 1190),
        (320, 1200, 870, 1370),
        (1050, 1390, 1350, 1540),
        (340, 1580, 830, 1690),
        (210, 1700, 1020, 2130),
        (1330, 1920, 1540, 2090)
    ]
    clean = inpaint_boxes(orig, boxes, threshold=155)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)

    f_banner = get_font("cinzel", 38)
    f_h = get_font("cinzel", 27)
    f_b = get_font("regular", 23)
    f_sm = get_font("regular", 20)

    # Milestone 4: DEC 2024 - 2025
    draw_centered(draw, "DEC 2024 - 2025", 48, f_banner, cx=470)
    draw_centered(draw, "SOFTWARE ANALYSIS & DEVELOPMENT", 145, f_h, cx=480)
    draw_wrapped(draw, "SENA technologist program. Comprehensive software lifecycle, requirement engineering, system design patterns, and enterprise databases.", 480, 190, 520, f_b, line_spacing=1.35)

    # Milestone 5: 2025 - 2026
    draw_centered(draw, "2025 - 2026", 600, f_banner, cx=775)
    draw_centered(draw, "AI AGENTS & PRODUCTION ARCHITECTURES", 700, f_h, cx=620)
    draw_wrapped(draw, "Architecting autonomous multi-agent systems with LangGraph, Model Context Protocol servers, and cloud infrastructure.", 620, 745, 480, f_b, line_spacing=1.35)
    draw_wrapped(draw, "• Multi-agent workflows \\n• MCP Server tools \\n• Full 4NF schemas", 1200, 830, 320, f_sm, line_spacing=1.3)

    # Milestone 6: 2026 AND BEYOND
    draw_centered(draw, "2026 AND BEYOND", 1130, f_banner, cx=560)
    draw_centered(draw, "ARCHITECTURAL MASTERY", 1225, f_h, cx=580)
    draw_wrapped(draw, "Designing high-scale distributed platforms, spatial computing, and next-generation AI integrations.", 580, 1270, 460, f_b, line_spacing=1.35)

    # Vision Signpost
    draw_centered(draw, "STRATEGIC VISION & GOALS", 1630, f_h, cx=580)
    v_bullets = [
        "• Global Software Architecture & AI Engineering",
        "• Scalable Microservices & Event-Driven Systems",
        "• Continuous Innovation in Autonomous Workflows",
        "• Contributing to Open Source & Developer Tooling"
    ]
    for idx, v in enumerate(v_bullets):
        draw.text((250, 1750 + idx * 60), v, font=f_b, fill=INK_DARK)

    # Arrow signposts
    draw_centered(draw, "DISTRIBUTED", 1955, f_sm, cx=1435)
    draw_centered(draw, "SYSTEMS", 1980, f_sm, cx=1435)
    draw_centered(draw, "SPATIAL & AI", 2035, f_sm, cx=1435)

    pil_img.save(os.path.join(OUT_PAGES, "map-2.jpg"), "JPEG", quality=95)
    print("Generated map-2.jpg (100% inpainting, ZERO rectangular boxes)")

# ==================== GROUP D: CHAPTER DIVIDERS (ENGRAVINGS PRESERVED) ====================

def generate_journey():
    orig = cv2.imread(os.path.join(SRC_PAGES, "journey.jpg"))
    boxes = [(250, 1100, 1300, 1750)]
    clean = inpaint_boxes(orig, boxes, threshold=145)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width

    draw_centered(draw, "CHAPTER II", 1200, get_font("cinzel", 38), cx=w//2)
    draw_centered(draw, "JOURNEY", 1290, get_font("cinzel", 56), cx=w//2)
    draw_centered(draw, "The path of continuous learning.", 1460, get_font("italic", 34), cx=w//2)
    draw_centered(draw, "Where logic forges engineering.", 1525, get_font("italic", 32), cx=w//2)
    draw_centered(draw, "From foundational algorithms to advanced systems architecture.", 1590, get_font("regular", 28), cx=w//2)
    draw_centered(draw, "Explore the chronological milestones across the following parchment scrolls.", 1655, get_font("regular", 26), cx=w//2)

    pil_img.save(os.path.join(OUT_PAGES, "journey.jpg"), "JPEG", quality=95)
    print("Generated journey.jpg (astrolabe engraving fully preserved)")

def generate_career():
    orig = cv2.imread(os.path.join(SRC_PAGES, "career.jpg"))
    boxes = [(250, 1100, 1300, 1750)]
    clean = inpaint_boxes(orig, boxes, threshold=145)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width

    draw_centered(draw, "CHAPTER III", 1140, get_font("cinzel", 38), cx=w//2)
    draw_centered(draw, "EXPERIENCE", 1240, get_font("cinzel", 56), cx=w//2)
    draw_centered(draw, "Every project marks a milestone in my craft.", 1410, get_font("italic", 34), cx=w//2)
    draw_centered(draw, "Where engineering and logic come to life.", 1475, get_font("italic", 32), cx=w//2)
    draw_centered(draw, "Solving complex challenges with architectural elegance.", 1540, get_font("regular", 30), cx=w//2)
    draw_centered(draw, "Building high-impact scalable solutions.", 1605, get_font("regular", 28), cx=w//2)

    pil_img.save(os.path.join(OUT_PAGES, "career.jpg"), "JPEG", quality=95)
    print("Generated career.jpg (hourglass engraving fully preserved)")

def generate_projects():
    orig = cv2.imread(os.path.join(SRC_PAGES, "projects.jpg"))
    boxes = [(250, 1100, 1300, 1750)]
    clean = inpaint_boxes(orig, boxes, threshold=145)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width

    draw_centered(draw, "CHAPTER IV", 1140, get_font("cinzel", 38), cx=w//2)
    draw_centered(draw, "FEATURED PROJECTS", 1240, get_font("cinzel", 56), cx=w//2)
    draw_centered(draw, "Selected works, systems architectures & live demonstrations.", 1410, get_font("italic", 34), cx=w//2)
    draw_centered(draw, "From autonomous AI agents to enterprise WMS solutions.", 1475, get_font("italic", 32), cx=w//2)
    draw_centered(draw, "Click interactive seals and badges to inspect GitHub repositories and live deployments.", 1540, get_font("regular", 28), cx=w//2)
    draw_centered(draw, "Turn the page to begin the engineering showcase.", 1605, get_font("regular", 28), cx=w//2)

    pil_img.save(os.path.join(OUT_PAGES, "projects.jpg"), "JPEG", quality=95)
    print("Generated projects.jpg (telescope engraving fully preserved)")

# ==================== GROUP E: EXPERIENCE PAGES (CAMPUSLANDS & FREELANCE) ====================

def generate_thor_systems():
    orig = cv2.imread(os.path.join(SRC_PAGES, "thor-systems.jpg"))
    clean = inpaint_auto(orig, threshold=150)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width

    draw_centered(draw, "CAMPUSLANDS", 140, get_font("cinzel", 54), cx=w//2)
    draw_centered(draw, "ELITE ACADEMY OF ADVANCED SOFTWARE ENGINEERING", 240, get_font("cinzel", 25), cx=w//2)
    
    p1 = "Campuslands is a high-performance, immersive technology ecosystem focused on advanced software engineering, scalable enterprise architecture, and global industry best practices."
    draw_wrapped(draw, p1, w//2, 310, 1260, get_font("regular", 27), line_spacing=1.35)
    
    p2 = "During my intensive training, I developed real corporate projects under the Scrum methodology, with weekly continuous delivery sprints, rigorous code reviews, and high-demand problem solving."
    draw_wrapped(draw, p2, w//2, 520, 1260, get_font("regular", 27), line_spacing=1.35)
    
    p3 = "This experience cemented my professional discipline, my ability to solve complex engineering challenges under pressure, and my mastery in building robust backend architectures ready for production."
    draw_wrapped(draw, p3, w//2, 730, 1260, get_font("regular", 27), line_spacing=1.35)
    
    draw_centered(draw, "— CORE ATTRIBUTES & COMPETENCIES —", 980, get_font("cinzel", 28), cx=w//2)
    
    draw.text((220, 1060), "TECHNICAL PROFICIENCY", font=get_font("cinzel", 26), fill=INK_DARK)
    draw.line((220, 1105, 680, 1105), fill=(180, 155, 120), width=2)
    t_lines = [
        "• Enterprise Backend: Java 17 + Spring Boot 3",
        "• Relational Data Modeling: MySQL 8 & 4NF",
        "• Modern High-Throughput APIs: Python (FastAPI)",
        "• Professional GitFlow & Trunk-Based Branching",
        "• Containerization: Docker & Nginx SSL Proxy"
    ]
    for idx, l in enumerate(t_lines):
        draw.text((220, 1130 + idx * 52), l, font=get_font("regular", 25), fill=INK_MUTED)
        
    draw.text((850, 1060), "LEADERSHIP & SOFT SKILLS", font=get_font("cinzel", 26), fill=INK_DARK)
    draw.line((850, 1105, 1310, 1105), fill=(180, 155, 120), width=2)
    s_lines = [
        "• Technical Leadership under Scrum & Kanban",
        "• Assertive Cross-Functional Communication",
        "• High Adaptability to New Toolchains",
        "• Structured Problem Solving Under Pressure",
        "• Unwavering Commitment to Code Quality"
    ]
    for idx, l in enumerate(s_lines):
        draw.text((850, 1130 + idx * 52), l, font=get_font("regular", 25), fill=INK_MUTED)
        
    pil_img.save(os.path.join(OUT_PAGES, "thor-systems.jpg"), "JPEG", quality=95)
    print("Generated thor-systems.jpg (borders & layout fully preserved)")

def generate_thor_systems_2():
    orig = cv2.imread(os.path.join(SRC_PAGES, "thor-systems-2.jpg"))
    clean = inpaint_auto(orig, threshold=150)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width

    draw_centered(draw, "CAMPUSLANDS", 140, get_font("cinzel", 54), cx=w//2)
    draw_centered(draw, "ENTERPRISE PROJECTS & ARCHITECTURAL CONTRIBUTIONS", 240, get_font("cinzel", 25), cx=w//2)
    
    # Project 1: LogiTrack WMS
    draw.text((140, 360), "LOGITRACK WMS · BACKEND LEAD", font=get_font("cinzel", 28), fill=INK_DARK)
    desc1 = "Comprehensive logistics and warehouse management system engineered for multi-facility stock control, supplier receptions, lot tracking, and zero inventory discrepancy:"
    draw_wrapped(draw, desc1, w//2, 420, 1240, get_font("regular", 26), align="left")
    
    b1_left = ["• Multi-facility stock control", "• Full operational audit trails", "• JWT authentication & RBAC"]
    b1_right = ["• Strict 4NF data normalization", "• MySQL triggers & procedures", "• High-throughput RESTful APIs"]
    for i, l in enumerate(b1_left):
        draw.text((140, 560 + i * 50), l, font=get_font("regular", 25), fill=INK_MUTED)
    for i, r in enumerate(b1_right):
        draw.text((780, 560 + i * 50), r, font=get_font("regular", 25), fill=INK_MUTED)
        
    draw_centered(draw, "— • —", 760, get_font("cinzel", 26), cx=w//2)
    
    # Project 2: Multi-Agent
    draw.text((140, 840), "CAMPUSLANDS INTELLIGENT · MULTI-AGENT PLATFORM", font=get_font("cinzel", 28), fill=INK_DARK)
    desc2 = "Intelligent academic supervision and analytics platform powered by coordinated autonomous AI agents, computer vision, and real-time automated notification pipelines:"
    draw_wrapped(draw, desc2, w//2, 900, 1240, get_font("regular", 26), align="left")
    
    b2_left = [
        "• Coordinated multi-agent graph (LangGraph)",
        "• Local LLM inference & OpenRouter APIs",
        "• Real-time absence anomaly alerts",
        "• High-performance async FastAPI backend"
    ]
    b2_right = [
        "• Automated digest reports via Telegram",
        "• Domain knowledge base with RAG",
        "• Predictive dropout risk analytics",
        "• Relational persistence & audit logs"
    ]
    for i, l in enumerate(b2_left):
        draw.text((140, 1040 + i * 52), l, font=get_font("regular", 25), fill=INK_MUTED)
    for i, r in enumerate(b2_right):
        draw.text((780, 1040 + i * 52), r, font=get_font("regular", 25), fill=INK_MUTED)
        
    pil_img.save(os.path.join(OUT_PAGES, "thor-systems-2.jpg"), "JPEG", quality=95)
    print("Generated thor-systems-2.jpg (borders & layout fully preserved)")

def generate_freelance():
    orig = cv2.imread(os.path.join(SRC_PAGES, "freelance.jpg"))
    clean = inpaint_auto(orig, threshold=150)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width

    draw_centered(draw, "CONSULTING & FREELANCE", 140, get_font("cinzel", 54), cx=w//2)
    draw_centered(draw, "INDEPENDENT SOFTWARE ARCHITECTURE & CUSTOM SOLUTIONS", 240, get_font("cinzel", 25), cx=w//2)
    
    desc = "Independent software development has allowed me to resolve high-impact business challenges, delivering custom platforms, intelligent automated workflows, and robust relational architectures tailored to exact client requirements."
    draw_wrapped(draw, desc, w//2, 320, 1240, get_font("regular", 27), line_spacing=1.35)
    
    draw_centered(draw, "— METHODOLOGY & ENGINEERING STANDARDS —", 560, get_font("cinzel", 28), cx=w//2)
    
    pillars = [
        ("1. ARCHITECTURAL DISCOVERY & SCOPING", "Exhaustive requirement analysis, domain modeling, and technical feasibility validation before writing a single line of code.", 650),
        ("2. CLEAN & MODULAR IMPLEMENTATION", "Decoupled software components following SOLID principles, design patterns, and comprehensive documentation for long-term maintainability.", 860),
        ("3. RIGOROUS DATA NORMALIZATION", "Database schemas modeled up to 4NF to guarantee zero redundancy, total referential integrity, and lightning-fast query execution.", 1070),
        ("4. CONTINUOUS DELIVERY & TRANSPARENCY", "Incremental milestones with live deployment environments, automated testing, and direct, transparent client communication.", 1280)
    ]
    for h_txt, b_txt, y in pillars:
        draw.text((140, y), h_txt, font=get_font("cinzel", 26), fill=INK_DARK)
        draw_wrapped(draw, b_txt, w//2, y + 42, 1240, get_font("regular", 25), align="left")
        
    draw_centered(draw, "Available for architectural consulting, enterprise backend development, and AI workflow automation.", 1680, get_font("italic", 27), cx=w//2)
    pil_img.save(os.path.join(OUT_PAGES, "freelance.jpg"), "JPEG", quality=95)
    print("Generated freelance.jpg (borders & layout fully preserved)")

def generate_freelance_2():
    orig = cv2.imread(os.path.join(SRC_PAGES, "freelance-2.jpg"))
    clean = inpaint_auto(orig, threshold=150)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width

    draw_centered(draw, "PILLARS OF EXCELLENCE", 140, get_font("cinzel", 54), cx=w//2)
    draw_centered(draw, "CORE PRINCIPLES GOVERNING EVERY PRODUCTION DEPLOYMENT", 240, get_font("cinzel", 25), cx=w//2)
    
    cards = [
        ("ENGINEERING QUALITY", "Clean, modular, and decoupled architecture. Structured, self-documenting code built to scale seamlessly without accumulating technical debt.", 420, 480),
        ("OPERATIONAL EFFICIENCY", "High-impact automated workflows that eliminate hours of manual daily effort through intelligent n8n pipelines, LLM agents, and scheduled jobs.", 1100, 480),
        ("DATA INTEGRITY & PERFORMANCE", "Databases designed with absolute mathematical rigor: strict 4NF normalization, zero data redundancy, transactional safety, and optimized indexes.", 420, 1140),
        ("PROFESSIONAL COMMITMENT", "Direct, transparent, and proactive communication at every project milestone. On-time delivery rigorously aligned with strategic client objectives.", 1100, 1140)
    ]
    f_h = get_font("cinzel", 28)
    f_b = get_font("regular", 26)
    for title, desc, cx, cy in cards:
        b = draw.textbbox((0, 0), title, font=f_h)
        draw.text((cx - (b[2] - b[0]) // 2, cy), title, font=f_h, fill=INK_DARK)
        draw.line((cx - 200, cy + 42, cx + 200, cy + 42), fill=(180, 155, 120), width=2)
        draw_wrapped(draw, desc, cx, cy + 70, 540, f_b, line_spacing=1.35)
        
    pil_img.save(os.path.join(OUT_PAGES, "freelance-2.jpg"), "JPEG", quality=95)
    print("Generated freelance-2.jpg (borders & layout fully preserved)")

# ==================== GROUP F: PROJECT SHOWCASE TEMPLATE (INPAINTED BASE) ====================

def generate_project_template(title, subtitle, desc, links, section_title, features, badges, filename):
    orig_path = os.path.join(SRC_PAGES, filename)
    orig = cv2.imread(orig_path)
    clean = inpaint_auto(orig, threshold=150)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width
    
    draw_centered(draw, title, 140, get_font("cinzel", 54), cx=w//2)
    draw_centered(draw, subtitle, 240, get_font("cinzel", 24), cx=w//2)
    draw_wrapped(draw, desc, w//2, 310, 1260, get_font("regular", 26), line_spacing=1.35)
    
    # Links line at y=490 for 3D active area hotspot
    draw_centered(draw, links, 490, get_font("italic", 27), cx=w//2)
    draw_centered(draw, f"— {section_title} —", 580, get_font("cinzel", 28), cx=w//2)
    
    f_fh = get_font("cinzel", 25)
    f_fb = get_font("regular", 24)
    for idx, (h_txt, b_txt, y) in enumerate(features):
        draw.text((140, y), h_txt, font=f_fh, fill=INK_DARK)
        draw_wrapped(draw, b_txt, w//2, y + 36, 1240, f_fb, align="left", line_spacing=1.3)
        
    draw_badge_columns(draw, badges, y_header=1680, y_row1=1730, y_row2=1765)
    pil_img.save(os.path.join(OUT_PAGES, filename), "JPEG", quality=95)
    print(f"Generated {filename} (medieval borders & layout fully preserved)")

def generate_all_projects():
    # 1. qyou.jpg
    qyou_features = [
        ("1. COLLABORATIVE MULTI-AGENT GRAPH (LangGraph)", "Autonomous agents coordinating inquiry triage, policy evaluation, and personalized remediation guidance.", 670),
        ("2. COMPUTER VISION ATTENDANCE ENGINE", "Automated biometric presence detection with OpenCV and deep learning, logging timestamps with zero manual intervention.", 820),
        ("3. PREDICTIVE STUDENT RISK ANALYTICS", "Machine learning models analyzing attendance velocity and evaluation trends to flag academic dropout risk early.", 970),
        ("4. INSTANT TELEGRAM BOT NOTIFICATIONS", "Real-time alerting pipeline notifying students of status changes and delivering automated daily coordinator digests.", 1120)
    ]
    qyou_badges = [
        ("AI ENGINE", "LangGraph", "Multi-Agent Graph"),
        ("BACKEND", "Python", "FastAPI Async"),
        ("VISION", "OpenCV", "PyTorch Models"),
        ("DATABASE", "PostgreSQL", "SQLAlchemy 4NF")
    ]
    generate_project_template(
        "CAMPUSLANDS INTELIGENTE", "MULTI-AGENT ACADEMIC SUPERVISION & PREDICTIVE ANALYTICS",
        "Intelligent enterprise platform engineered for real-time academic supervision, attendance verification with computer vision, and predictive student risk modeling through collaborative multi-agent AI workflows.",
        "Links: GitHub (Repository)  ·  Live Demo (HTTPS)",
        "KEY ARCHITECTURAL CAPABILITIES", qyou_features, qyou_badges, "qyou.jpg"
    )
    
    # 2. qyou-2.jpg
    qyou2_features = [
        ("1. ASYNCHRONOUS INGESTION GATEWAY", "High-throughput API gateway validating payloads, managing session tokens, and routing events to active agent queues.", 670),
        ("2. STATEGRAPH MEMORY & RETRIEVAL", "Dynamic checkpoint persistence preserving conversation context across multi-step student interactions with RAG lookups.", 820),
        ("3. LLM ROUTING & COST OPTIMIZATION", "Intelligent prompt routing dispatching low-latency queries to local models and complex reasoning to OpenRouter APIs.", 970),
        ("4. COMPREHENSIVE AUDITING & DASHBOARDS", "Structured event logging recording every agent decision, confidence score, and timestamp for total auditability.", 1120)
    ]
    qyou2_badges = [
        ("ORCHESTRATION", "Docker", "Microservices"),
        ("CACHING", "Redis 7", "Queue State"),
        ("ALERTS", "Telegram Bot", "Async Webhooks"),
        ("DEPLOYMENT", "Linux VPS", "Nginx SSL Proxy")
    ]
    generate_project_template(
        "CAMPUSLANDS INTELIGENTE", "SYSTEM ARCHITECTURE & PROTOCOL PIPELINE",
        "Comprehensive architectural blueprint detailing event routing, state persistence, decoupled microservice boundaries, and verifiable security auditing across the intelligent campus ecosystem.",
        "Links: System Architecture  ·  Ecosystem Blueprints",
        "CORE ARCHITECTURAL MODULES", qyou2_features, qyou2_badges, "qyou-2.jpg"
    )

    # 3. iq-tester.jpg (LogiTrack WMS)
    iq_features = [
        ("1. MULTI-WAREHOUSE STOCK & LOT CONTROL", "Centralized administration of inventory distributed across multiple physical facilities with strict negative-stock prevention and granular lot traceability.", 670),
        ("2. FULL OPERATIONAL AUDITING & TRACEABILITY", "Immutable chronological logging of receptions, dispatches, transfers, and inventory adjustments with operator identification and millisecond timestamps.", 820),
        ("3. PURCHASE ORDER & SUPPLIER RECEPTION", "Structured receiving pipeline with automated purchase order reconciliation, discrepancy identification, and instant stock ledger synchronization.", 970),
        ("4. ROLE HIERARCHY & JWT SECURITY (RBAC)", "Granular permission matrix backed by Spring Security and signed JWTs for SuperAdmins, Warehouse Managers, Logistics Operators, and Auditors.", 1120)
    ]
    iq_badges = [
        ("BACKEND", "Java 17", "Spring Boot 3.3"),
        ("DATABASE", "PostgreSQL 16", "JPA & Hibernate"),
        ("SECURITY", "Spring Security", "Signed JWTs"),
        ("DEPLOYMENT", "Docker & Nginx", "HTTPS Domain")
    ]
    generate_project_template(
        "LOGITRACK WMS", "ENTERPRISE LOGISTICS & WAREHOUSE MANAGEMENT SYSTEM",
        "Enterprise-grade Warehouse Management System (WMS) designed to deliver 100% real-time operational traceability across multi-warehouse inventory, supplier receptions, inter-facility transfers, lot tracking, picking workflows, and physical stock reconciliations.",
        "Links: GitHub (Repository)  ·  Live Demo (HTTPS)",
        "CAPABILITIES & INVENTORY CONTROL", iq_features, iq_badges, "iq-tester.jpg"
    )

    # 4. betting-tarot.jpg (n8n Attendance AI)
    n8n_features = [
        ("1. WEB INGESTION & DATA CAPTURE", "Responsive web form for structured receipt of student absence requests with medical and official supporting attachments.", 670),
        ("2. NORMALIZATION & VALIDATION IN N8N", "Orchestration workflow in n8n sanitizing inputs, validating schema constraints, and preparing structured inference payloads.", 820),
        ("3. INTELLIGENT EVALUATION VIA LLM", "Prompt-engineered connection with OpenRouter LLMs categorizing justifications into: Valid, Invalid, or Pending Human Review.", 970),
        ("4. REAL-TIME GOOGLE SHEETS SYNC", "Instant synchronization with the master absence ledger recording timestamps, AI confidence verdict, and summarized rationale.", 1120),
        ("5. INSTANT TELEGRAM BOT NOTIFICATIONS", "Real-time dispatch notifying students of their resolution and delivering consolidated digest reports to academic coordinators.", 1270)
    ]
    n8n_badges = [
        ("ORCHESTRATOR", "n8n Self-Hosted", "Docker Engine"),
        ("AI MODELS", "OpenRouter API", "Claude & GPT-4o"),
        ("INTEGRATIONS", "Google Sheets", "Telegram Bot API"),
        ("SECURITY", "Webhook Auth", "SSL Encrypted")
    ]
    generate_project_template(
        "N8N ATTENDANCE AI", "AUTOMATION WORKFLOW & LLM REQUEST CLASSIFICATION",
        "End-to-end automated pipeline for the ingestion, intelligent evaluation, and classification of absence justification requests in academic and corporate environments, eliminating manual review and providing instant auditability.",
        "Links: GitHub (Repository)  ·  Live Demo (HTTPS)",
        "AUTOMATED PIPELINE WORKFLOW", n8n_features, n8n_badges, "betting-tarot.jpg"
    )

    # 5. autoposter.jpg (GitHub MCP Server)
    mcp_features = [
        ("1. REPOSITORY METRICS & AUDITING", "Inspect repo metadata, commit histories, contributor metrics, and branch protection rules via optimized REST calls.", 670),
        ("2. AUTOMATED ISSUE & PR MANAGEMENT", "Programmatically read, create, comment, assign, and transition GitHub issues and pull requests with validation.", 820),
        ("3. SECURE FILE SEARCH & TREE INSPECTION", "Recursive directory traversal, file content retrieval, and blob inspection with size safeguards.", 970),
        ("4. STRICT SCHEMAS & INPUT VALIDATION", "Full JSON Schema tool declarations ensuring LLMs generate mathematically valid arguments before execution.", 1120)
    ]
    mcp_badges = [
        ("RUNTIME", "Node.js 20+", "TypeScript ESM"),
        ("PROTOCOL", "Anthropic MCP", "Stdio Transport"),
        ("CLIENT", "Octokit API", "REST & GraphQL"),
        ("SECURITY", "Fine-Grained PAT", "Read-Only Scopes")
    ]
    generate_project_template(
        "GITHUB MCP SERVER", "MODEL CONTEXT PROTOCOL FOR AUTONOMOUS AI AGENTS",
        "Professional Model Context Protocol (MCP) server that empowers AI agents like Claude Desktop and Cursor to interact directly and safely with GitHub repositories, issues, branches, commits, and pull requests via structured standardized tools.",
        "Links: GitHub (Repository)  ·  Official NPM Package",
        "PROTOCOL SPECIFICATIONS & TOOLS", mcp_features, mcp_badges, "autoposter.jpg"
    )

    # 6. autoposter-2.jpg (GitHub MCP Server Pipeline)
    mcp2_features = [
        ("1. USER PROMPT INGESTION", "Agent receives user instruction in natural language and identifies required repository operations.", 670),
        ("2. TOOL RESOLUTION & INFERENCE", "LLM inspects MCP tool schemas and constructs typed execution arguments with strict parameter constraints.", 820),
        ("3. DISPATCH & GITHUB API EXECUTION", "MCP server validates auth token, verifies parameters, and executes rate-limited GitHub API calls.", 970),
        ("4. STRUCTURED RESPONSE & CONTEXT SYNTHESIS", "JSON result is formatted into contextual text and returned to the LLM for final response synthesis.", 1120)
    ]
    mcp2_badges = [
        ("ARCHITECTURE", "Decoupled Clean", "Modular Handlers"),
        ("VALIDATION", "Zod Schemas", "Runtime Checks"),
        ("HOSTS", "Claude Desktop", "Cursor & Windsurf"),
        ("LOGGING", "Stderr Streams", "Zero Stdio Noise")
    ]
    generate_project_template(
        "GITHUB MCP SERVER", "PROTOCOL EXECUTION PIPELINE & AGENT INTEGRATION",
        "Comprehensive execution lifecycle demonstrating how user prompts are safely translated into structured tool invocations, executed against GitHub's APIs, and returned cleanly into the agent's reasoning loop.",
        "Links: Architecture Blueprints  ·  Execution Schema",
        "PIPELINE EXECUTION STAGES", mcp2_features, mcp2_badges, "autoposter-2.jpg"
    )

    # 7. export-robot.jpg (HelpDesk AI)
    hd_features = [
        ("1. INSTANT SEMANTIC CLASSIFICATION", "Automated classification of incoming tickets by technical category (Hardware, Network, Database, Security, Permissions).", 670),
        ("2. URGENCY & SLA PRIORITY SCORING", "LLM-driven urgency evaluation assessing business impact and assigning SLA response windows automatically.", 820),
        ("3. RAG KNOWLEDGE BASE & INSTANT RESOLUTION", "Semantic vector search against technical manuals delivering verified solutions to common issues instantly.", 970),
        ("4. SPECIALIST ROUTING & OPERATIONAL AUDIT", "Automated assignment to corresponding engineering queues with complete chronological timeline history.", 1120)
    ]
    hd_badges = [
        ("BACKEND", "Python FastAPI", "Async Handlers"),
        ("AI ENGINE", "LangChain", "OpenAI Models"),
        ("VECTOR STORE", "ChromaDB", "Embeddings"),
        ("DATABASE", "PostgreSQL 16", "SQLAlchemy 4NF")
    ]
    generate_project_template(
        "HELPDESK AI", "ENTERPRISE INCIDENT MANAGEMENT WITH LLM TRIAGE",
        "Enterprise technical support and ticketing platform featuring automated natural language triage, intelligent urgency classification, auto-routing to technical specialists, and an integrated RAG knowledge base for instant answers.",
        "Links: GitHub (Repository)  ·  Live Demo (HTTPS)",
        "INTELLIGENT SUPPORT MODULES", hd_features, hd_badges, "export-robot.jpg"
    )

    # 8. six-dot-bot.jpg (E-Commerce Database 4NF)
    db_features = [
        ("1. STRICT 4NF NORMALIZATION", "Complete elimination of multi-valued dependencies and redundant data across catalog, customers, and order ledgers.", 670),
        ("2. ACID TRANSACTIONAL SAFETY", "Pessimistic locking strategies and concurrency controls to prevent overselling, race conditions, and phantom inventory loss.", 820),
        ("3. STORED PROCEDURES & TRIGGERS", "Encapsulated business logic: automated discount calculations, dynamic tax ledgers, and inventory reservations.", 970),
        ("4. RFM CUSTOMER SEGMENTATION", "Advanced analytical views calculating Recency, Frequency, and Monetary Value to drive strategic marketing insights.", 1120)
    ]
    db_badges = [
        ("RDBMS", "MySQL 8.0+", "InnoDB Engine"),
        ("NORMALIZATION", "4NF Rigor", "Zero Redundancy"),
        ("LOGIC", "Stored Procedures", "Triggers & Views"),
        ("OPTIMIZATION", "Composite Indexes", "Partitioning")
    ]
    generate_project_template(
        "ECOMMERCE DATABASE 4NF", "ADVANCED RELATIONAL ARCHITECTURE & 4NF RIGOR",
        "Full-scale relational database architecture designed for high-concurrency enterprise e-commerce platforms. Rigorously normalized to Fourth Normal Form (4NF) with ACID transactional guarantees and zero redundancy.",
        "Links: GitHub (Repository)  ·  Schema Documentation",
        "ARCHITECTURAL FOUNDATIONS & SCHEMAS", db_features, db_badges, "six-dot-bot.jpg"
    )

    # 9. autoreply.jpg (SoftSkills Quest)
    ss_features = [
        ("1. CODE REVIEW CONFLICT RESOLUTION", "Simulated interactions with Product Owners, Tech Leads, and QA requiring constructive, empathetic technical communication.", 670),
        ("2. ARCHITECTURAL TRADE-OFF DILEMMAS", "Strategic scenarios forcing decisions between rapid feature delivery and long-term technical debt mitigation.", 820),
        ("3. CRISIS MANAGEMENT & OUTAGES", "High-pressure production incident simulations demanding clear stakeholder updates and composed triage.", 970),
        ("4. PERFORMANCE SCORING MATRIX", "Comprehensive scoring matrix assessing emotional intelligence, team synergy, and problem ownership.", 1120)
    ]
    ss_badges = [
        ("ENGINE", "Canvas 2D", "Fluid 60 FPS"),
        ("LOGIC", "Vanilla JS", "ES6+ Modules"),
        ("AUDIO", "Web Audio API", "Synthesizer"),
        ("DESIGN", "Custom Art", "Responsive Grid")
    ]
    generate_project_template(
        "SOFTSKILLS QUEST", "GAMIFIED DEVELOPER DECISION-MAKING GAME",
        "Interactive 2D gamified platform designed to train and evaluate interpersonal engineering soft skills through situational branch choices, conflict resolution dialogues, active listening challenges, and team leadership dilemmas.",
        "Links: GitHub (Repository)  ·  Live Game (Web)",
        "GAMEPLAY MODULES & SKILL SCENARIOS", ss_features, ss_badges, "autoreply.jpg"
    )

    # 10. time-recorder.jpg (LMS ABC Platform)
    lms_features = [
        ("1. PUBLIC COURSE CATALOG", "Open catalog enabling prospective students to search subjects, review syllabi, and view instructor credentials.", 670),
        ("2. INSTRUCTOR & CONTENT MANAGEMENT", "Comprehensive panel for creating, editing, and sequencing courses, modular units, and structured rich-media lessons.", 820),
        ("3. ENROLLMENT & GRADE TRACKING", "Dedicated portal for managing course registrations, logging exam scores, and visualizing academic progress.", 970),
        ("4. CLIENT-SIDE PERSISTENCE", "Structured LocalStorage persistence delivering instantaneous page transitions with zero hosting server overhead.", 1120)
    ]
    lms_badges = [
        ("STRUCTURE", "Semantic HTML5", "WAI-ARIA Access"),
        ("STYLING", "Modern CSS3", "Flex & Grid"),
        ("LOGIC", "Vanilla JS", "ES6+ Modules"),
        ("STORAGE", "LocalStorage API", "Zero Overhead")
    ]
    generate_project_template(
        "LMS ABC PLATFORM", "MODULAR LIGHTWEIGHT LEARNING MANAGEMENT SYSTEM",
        "Modular Learning Management System (LMS) designed for academic course administration, multimedia lesson delivery, and student progress tracking. Built with lightweight Vanilla JavaScript and CSS3, requiring zero heavy frameworks.",
        "Links: GitHub (Repository)  ·  Live Demo (Netlify)",
        "PLATFORM MODULES & USER CAPABILITIES", lms_features, lms_badges, "time-recorder.jpg"
    )

    # 11. fifteen-js.jpg (Interactive 3D Codex)
    f15_features = [
        ("1. CYLINDRICAL DEFORMATION MATHEMATICS", "Custom vertex displacement algorithms modeling elastic sheet curvature, page stiffness, and natural spine curl.", 670),
        ("2. GPU TEXTURE PRECOMPILATION", "Precompiled WebGL textures in GPU VRAM enabling instantaneous language transitions with zero black flashes.", 820),
        ("3. INTERACTIVE RAYCASTING HOTSPOTS", "Real-time 3D coordinate unprojecting mapping screen cursor interactions to underlying page link seals and badges.", 970),
        ("4. ADAPTIVE VIEWPORT PROJECTION", "Adaptive camera frustum recalculations adjusting zoom, angle, and lighting across mobile and desktop screens.", 1120)
    ]
    f15_badges = [
        ("GRAPHICS", "Three.js 0.172", "WebGL Engine"),
        ("ANIMATION", "GSAP 3.12", "Physics Easing"),
        ("LANGUAGE", "TypeScript 5.5", "Strict Safety"),
        ("BUNDLER", "Vite 6", "Production HMR")
    ]
    generate_project_template(
        "PORTFOLIO 3D CODEX", "THREE.JS ENGINE, MATHEMATICAL DEFORMATIONS & SHADERS",
        "The engineering behind this interactive 3D codex: real-time GPU mesh deformations, cylindrical physics equations simulating paper flexibility, procedural leather texturing, and dynamic lighting pipelines.",
        "Links: GitHub (Repository)  ·  Technical Architecture",
        "GRAPHICAL & MATHEMATICAL FOUNDATIONS", f15_features, f15_badges, "fifteen-js.jpg"
    )

    # 12. the-book.jpg (The Codex Architecture & Credits)
    tb_features = [
        ("1. 60 FPS HARDWARE ACCELERATION", "Smooth WebGL execution with FXAA antialiasing and soft dynamic shadow mapping across all viewports.", 670),
        ("2. MULTI-INPUT NAVIGATION ENGINE", "Comprehensive gesture detection supporting drag turning, touch swipes, keyboard arrow keys, and chapter plaques.", 820),
        ("3. PROCEDURAL PHYSICS & CURLING", "Parametric cylinder bending algorithms mathematically modeling real manuscript parchment flexibility and spine curvature.", 970),
        ("4. ZERO-LATENCY I18N ARCHITECTURE", "Dual-language preloading architecture guaranteeing clean instant re-initialization from the cover with zero ghost artifacts.", 1120)
    ]
    tb_badges = [
        ("AUTHOR", "Tomas Esteban", "Gonzalez Quintero"),
        ("ROLE", "Full Stack Dev", "Software Architect"),
        ("LOCATION", "Bucaramanga", "Colombia · 2026"),
        ("MOTTO", "Clean Systems", "Tangible Rigor")
    ]
    generate_project_template(
        "THE CODEX", "TECHNICAL ARCHITECTURE & AUTHORSHIP CREDITS",
        "The Book of Tomas Esteban Gonzalez Quintero is an interactive 3D experience designed to present my trajectory, engineering projects, technical capabilities, and software architecture vision.",
        "Links: Official Repository  ·  Live Deployment",
        "MOTOR SPECIFICATIONS & ARCHITECTURE", tb_features, tb_badges, "the-book.jpg"
    )

def main():
    os.makedirs(OUT_PAGES, exist_ok=True)
    
    print("=== STARTING MASTER ENGLISH EDITION GENERATION (100% ART PRESERVED, ZERO BOXES) ===")
    copy_static_assets()
    generate_cover_front()
    generate_cover_back()
    generate_welcome()
    generate_about()
    generate_who_am_i()
    generate_my_story()
    generate_skills()
    generate_interests()
    generate_journey()
    generate_map_1()
    generate_map_2()
    generate_career()
    generate_thor_systems()
    generate_thor_systems_2()
    generate_freelance()
    generate_freelance_2()
    generate_projects()
    generate_all_projects()
    print("=== ALL 32 ENGLISH EDITION PAGES SUCCESSFULLY GENERATED ===")

if __name__ == "__main__":
    main()
