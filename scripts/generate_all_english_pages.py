#!/usr/bin/env python3
"""
Master generator for the 100% brand new English Edition of the 3D Codex.
Carefully calibrated with large, legible typography (30pt-74pt),
perfect alignment with all Renaissance drawings (astrolabes, hourglasses,
crystals, quills, cauldrons, Sun, Moon, and celestial mandala),
and zero white cloudy halos or rectangular patches on map scrolls.
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
INK_MUTED = (45, 38, 30)
INK_GOLD = (230, 215, 175)
GOLD_ACCENT = (195, 155, 75)

OCR_ENGINE = RapidOCR()

def get_font(name, size):
    path = FONTS.get(name, FONTS["regular"])
    return ImageFont.truetype(path, size)

def draw_centered(draw, text, y, font, fill=INK_DARK, cx=764):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text((cx - w // 2, y), text, font=font, fill=fill)

def draw_wrapped(draw, text, cx, y, max_w, font, fill=INK_DARK, line_h=42, align="center"):
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

def draw_badge_columns(draw, badges, y_header=1675, y_row1=1725, y_row2=1765):
    f_h = get_font("cinzel", 26)
    f_b = get_font("regular", 26)
    centers = [280, 600, 930, 1250]
    for idx, (head, r1, r2) in enumerate(badges):
        cx = centers[idx]
        b_h = draw.textbbox((0, 0), head, font=f_h)
        draw.text((cx - (b_h[2] - b_h[0]) // 2, y_header), head, font=f_h, fill=INK_DARK)
        draw.line((cx - 130, y_header + 36, cx + 130, y_header + 36), fill=(180, 155, 120), width=2)
        b_1 = draw.textbbox((0, 0), r1, font=f_b)
        draw.text((cx - (b_1[2] - b_1[0]) // 2, y_row1), r1, font=f_b, fill=INK_MUTED)
        b_2 = draw.textbbox((0, 0), r2, font=f_b)
        draw.text((cx - (b_2[2] - b_2[0]) // 2, y_row2), r2, font=f_b, fill=INK_MUTED)

# ==================== INPAINTING UTILITIES ====================

def inpaint_boxes(orig_bgr, boxes, threshold=135, dilate_iter=1, radius=3):
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

def inpaint_auto(orig_bgr, exclude_regions=None, threshold=140, dilate_iter=1, radius=4):
    h, w = orig_bgr.shape[:2]
    gray = cv2.cvtColor(orig_bgr, cv2.COLOR_BGR2GRAY)
    mask = np.zeros((h, w), dtype=np.uint8)
    res, _ = OCR_ENGINE(orig_bgr)
    if res:
        for box, text, score in res:
            xs = [int(p[0]) for p in box]
            ys = [int(p[1]) for p in box]
            x1, y1 = max(0, min(xs) - 5), max(0, min(ys) - 5)
            x2, y2 = min(w, max(xs) + 5), min(h, max(ys) + 5)
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
            m = cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=dilate_iter)
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
    f = get_font("regular", 62)
    bbox = draw.textbbox((0, 0), "The Book of", font=f)
    tw = bbox[2] - bbox[0]
    x = (w - tw) // 2
    y = 290

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
    draw_centered(draw, "TEGQ ARCHIVES", 1070, get_font("cinzel", 54), fill=INK_GOLD, cx=w//2)
    draw_centered(draw, "Thank you for reviewing my codex!", 1150, get_font("italic", 38), fill=INK_GOLD, cx=w//2)
    
    closing = "I hope you enjoyed this interactive journey through my software architectures, engineering projects, and technical vision."
    draw_wrapped(draw, closing, w//2, 1220, 1040, get_font("regular", 32), fill=INK_GOLD, line_h=46)
    
    draw_centered(draw, "Tomas Esteban Gonzalez Quintero", 1380, get_font("cinzel", 38), fill=INK_GOLD, cx=w//2)
    draw_centered(draw, "Full Stack Developer & AI Solutions Architect", 1440, get_font("italic", 32), fill=INK_GOLD, cx=w//2)
    draw_centered(draw, "Bucaramanga, Santander, Colombia", 1495, get_font("regular", 30), fill=INK_GOLD, cx=w//2)
    draw_centered(draw, "GitHub: github.com/TEstebanGQ", 1565, get_font("regular", 30), fill=INK_GOLD, cx=w//2)
    draw_centered(draw, "LinkedIn: tomas-esteban-gonzalez-quintero", 1620, get_font("regular", 30), fill=INK_GOLD, cx=w//2)
    draw_centered(draw, "WhatsApp: +57 316 775 5887", 1675, get_font("regular", 30), fill=INK_GOLD, cx=w//2)
    
    img.save(os.path.join(OUT_PAGES, "cover-back.jpg"), "JPEG", quality=95)
    print("Generated cover-back.jpg")

# ==================== GROUP B: WELCOME, ABOUT & PROFILES ====================

def generate_welcome():
    orig = cv2.imread(os.path.join(SRC_PAGES, "welcome.jpg"))
    boxes = [
        (350, 120, 1200, 280),
        (200, 1540, 1360, 1750)
    ]
    clean = inpaint_boxes(orig, boxes, threshold=140, radius=4)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width

    draw_centered(draw, "WELCOME", 170, get_font("cinzel", 68), cx=w//2)
    draw_centered(draw, "Double-tap anywhere to toggle fullscreen view", 1610, get_font("regular", 36), cx=w//2)
    draw_centered(draw, "Swipe or use arrow keys (↓ → / ↑ ←) to turn pages forward & back", 1675, get_font("regular", 32), cx=w//2)
    
    pil_img.save(os.path.join(OUT_PAGES, "welcome.jpg"), "JPEG", quality=95)
    print("Generated welcome.jpg (large typography)")

def generate_about():
    orig = cv2.imread(os.path.join(SRC_PAGES, "about.jpg"))
    boxes = [(250, 1150, 1300, 1800)]
    clean = inpaint_boxes(orig, boxes, threshold=140, radius=4)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width

    draw_centered(draw, "CHAPTER I", 1180, get_font("cinzel", 48), cx=w//2)
    draw_centered(draw, "ABOUT ME", 1275, get_font("cinzel", 68), cx=w//2)
    draw_centered(draw, "Discover my story, page by page.", 1470, get_font("italic", 38), cx=w//2)
    draw_centered(draw, "Full Stack Developer & Software Architect.", 1540, get_font("italic", 36), cx=w//2)
    draw_centered(draw, "My systems, my models, my technical vision.", 1615, get_font("regular", 34), cx=w//2)
    draw_centered(draw, "Explore the codex and interact with each project.", 1685, get_font("regular", 32), cx=w//2)

    pil_img.save(os.path.join(OUT_PAGES, "about.jpg"), "JPEG", quality=95)
    print("Generated about.jpg (large typography)")

def generate_who_am_i():
    orig = cv2.imread(os.path.join(SRC_PAGES, "who-am-i.jpg"))
    boxes = [
        (450, 120, 1050, 240),
        (250, 255, 1280, 315),
        (600, 810, 900, 900),
        (200, 930, 1320, 1190),
        (350, 1340, 1160, 1400),
        (180, 1690, 1360, 1980)
    ]
    clean = inpaint_boxes(orig, boxes, threshold=140, radius=4)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width

    draw_centered(draw, "WHO AM I", 145, get_font("cinzel", 74), cx=w//2)
    draw_centered(draw, "Software Architect · AI Solutions · Full Stack Engineer", 265, get_font("italic", 34), cx=w//2)
    draw_centered(draw, "Greetings!", 830, get_font("italic", 52), cx=w//2)

    draw_centered(draw, "I am Tomas Esteban Gonzalez Quintero,", 940, get_font("regular", 36), cx=w//2)
    draw_centered(draw, "Full Stack Developer & AI Solutions Integrator", 995, get_font("regular", 36), cx=w//2)
    draw_centered(draw, "specialized in multi-agent systems, clean architectures,", 1050, get_font("regular", 36), cx=w//2)
    draw_centered(draw, "4NF relational databases, and high-impact enterprise automations.", 1105, get_font("regular", 36), cx=w//2)
    draw_centered(draw, "Bucaramanga, Colombia · WhatsApp: +57 316 775 5887", 1360, get_font("italic", 32), cx=w//2)

    # 3 columns under Quill, Scroll, Books
    col1 = ["Python (FastAPI)", "Java (Spring Boot)", "Node.js / Express", "PostgreSQL / MySQL", "Docker / Linux"]
    col2 = ["LangGraph / Multi-Agent", "Model Context Protocol", "n8n Workflows + LLM", "PyTorch / Vision", "Groq / LLaMA 3.3"]
    col3 = ["Clean Architecture", "4NF Relational Model", "Three.js / WebGL", "React / Next.js", "REST APIs & Webhooks"]

    centers = [365, 764, 1160]
    y_starts = [1705, 1762, 1820, 1878, 1935]
    f_pill = get_font("regular", 30)

    for idx, col in enumerate([col1, col2, col3]):
        cx = centers[idx]
        for r_idx, item in enumerate(col):
            b = draw.textbbox((0, 0), item, font=f_pill)
            draw.text((cx - (b[2] - b[0]) // 2, y_starts[r_idx]), item, font=f_pill, fill=(35, 30, 25))

    pil_img.save(os.path.join(OUT_PAGES, "who-am-i.jpg"), "JPEG", quality=95)
    print("Generated who-am-i.jpg (large, balanced typography)")

def generate_my_story():
    orig = cv2.imread(os.path.join(SRC_PAGES, "my-story.jpg"))
    boxes = [
        (400, 120, 1100, 240),
        (140, 620, 1380, 920),
        (140, 1400, 1380, 1700)
    ]
    clean = inpaint_boxes(orig, boxes, threshold=140, radius=4)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width

    draw_centered(draw, "MY STORY", 145, get_font("cinzel", 68), cx=w//2)
    draw_centered(draw, "The Evolutionary Path of a Software Craftsman", 250, get_font("italic", 34), cx=w//2)

    f_b = get_font("regular", 32)

    # 4 narrative blocks sitting between crystal drawings
    draw_wrapped(draw, "From an early age, I felt a deep fascination for logic, mathematics, and digital systems. Code quickly became my primary language to create, construct, and solve real-world challenges.", 400, 640, 480, f_b, line_h=44)
    draw_wrapped(draw, "I evolved building robust enterprise backends with Python, FastAPI, and Java Spring Boot. I understood early on that the foundation of any enduring software lies in strict architectural integrity.", 1120, 640, 480, f_b, line_h=44)
    
    draw_wrapped(draw, "At Campuslands, I forged rigorous engineering habits: full-stack systems, clean architectures, and high-concurrency database design up to 4NF under agile Scrum delivery.", 400, 1420, 480, f_b, line_h=44)
    draw_wrapped(draw, "Today, I architect scalable distributed platforms, Model Context Protocol (MCP) servers, and autonomous n8n workflows. I deliver verifiable technical rigor and tangible results.", 1120, 1420, 480, f_b, line_h=44)

    pil_img.save(os.path.join(OUT_PAGES, "my-story.jpg"), "JPEG", quality=95)
    print("Generated my-story.jpg (flowing 32pt narrative)")

def generate_skills():
    orig = cv2.imread(os.path.join(SRC_PAGES, "skills.jpg"))
    boxes = [
        (350, 120, 1180, 230),
        (550, 1620, 980, 1710),
        (200, 1850, 1350, 2100)
    ]
    clean = inpaint_boxes(orig, boxes, threshold=145, radius=4)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width

    draw_centered(draw, "TECHNICAL SKILLS", 145, get_font("cinzel", 64), cx=w//2)
    draw_centered(draw, "Tap to explore", 1650, get_font("italic", 28), cx=w//2)
    draw_centered(draw, "— Celestial Matrix of Technical Competencies —", 1950, get_font("cinzel", 30), cx=w//2)

    pil_img.save(os.path.join(OUT_PAGES, "skills.jpg"), "JPEG", quality=95)
    print("Generated skills.jpg (mandala preserved, 64pt title, translated hint)")

def generate_interests():
    orig = cv2.imread(os.path.join(SRC_PAGES, "interests.jpg"))
    boxes = [
        (450, 140, 1070, 240),
        (300, 250, 1220, 310),
        (600, 590, 920, 650),
        (180, 1000, 440, 1210),
        (1070, 1000, 1300, 1210),
        (630, 1630, 890, 1700),
        (630, 1880, 890, 1940),
        (100, 2000, 1420, 2120)
    ]
    clean = inpaint_boxes(orig, boxes, threshold=140, radius=4)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width

    draw_centered(draw, "INTERESTS", 160, get_font("cinzel", 66), cx=w//2)
    draw_centered(draw, "CYBERSECURITY · 3D ANIMATION · DATA ANALYSIS", 265, get_font("cinzel", 30), cx=w//2)

    f_node = get_font("cinzel", 32)
    draw_centered(draw, "CYBERSECURITY", 615, f_node, cx=w//2)
    draw_centered(draw, "DATA ANALYSIS", 1100, f_node, cx=320)
    draw_centered(draw, "DATA VISUALIZATION", 1100, f_node, cx=1180)
    draw_centered(draw, "3D ANIMATION", 1650, f_node, cx=w//2)
    draw_centered(draw, "WEBGL & SHADERS", 1900, get_font("cinzel", 28), cx=w//2)

    f_ph = get_font("cinzel", 27)
    f_pb = get_font("regular", 25)

    draw.text((140, 2010), "CYBERSECURITY", font=f_ph, fill=INK_DARK)
    draw.text((140, 2045), "Ethical Hacking & DevSecOps", font=f_pb, fill=INK_MUTED)
    draw.text((140, 2075), "System & Network Hardening", font=f_pb, fill=INK_MUTED)

    draw_centered(draw, "3D ANIMATION", 2010, f_ph, cx=w//2)
    draw_centered(draw, "WebGL, Three.js & Shaders", 2045, f_pb, cx=w//2)
    draw_centered(draw, "Interactive 3D Environments", 2075, f_pb, cx=w//2)

    draw.text((1140, 2010), "DATA ANALYSIS", font=f_ph, fill=INK_DARK)
    draw.text((1140, 2045), "Statistical Modeling & BI", font=f_pb, fill=INK_MUTED)
    draw.text((1140, 2075), "Data Mining & Machine Learning", font=f_pb, fill=INK_MUTED)

    pil_img.save(os.path.join(OUT_PAGES, "interests.jpg"), "JPEG", quality=95)
    print("Generated interests.jpg (constellation preserved, 66pt title)")

# ==================== GROUP D: MAP / JOURNEY PAGES ====================

def generate_map_1():
    orig = cv2.imread(os.path.join(SRC_PAGES, "map-1.jpg"))
    boxes = [
        (400, 50, 610, 145),
        (210, 170, 760, 385),
        (910, 480, 1440, 580),
        (850, 600, 1470, 800),
        (440, 1170, 1110, 1310),
        (400, 1310, 1150, 1610),
        (1190, 1410, 1420, 1540)
    ]
    clean = inpaint_boxes(orig, boxes, threshold=165, dilate_iter=1, radius=4)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)

    f_banner = get_font("cinzel", 52)
    f_h = get_font("cinzel", 34)
    f_b = get_font("regular", 34)

    # Scroll 1 (2023)
    draw_centered(draw, "2023", 75, f_banner, cx=500)
    draw_wrapped(draw, "Started programming with Python, mastering core backend logic, algorithms & data structures.", 485, 205, 520, f_b, line_h=44)

    # Scroll 2 (Jan 2024 - Jun 2024)
    draw_centered(draw, "JAN 2024 - JUN 2024", 515, get_font("cinzel", 44), cx=1175)
    draw_wrapped(draw, "Enterprise hardware diagnostics, system architecture, maintenance, and IT infrastructure support.", 1160, 625, 540, f_b, line_h=44)

    # Scroll 3 (Jun 2024 - Nov 2024)
    draw_centered(draw, "JUN 2024 - NOV 2024", 1220, get_font("cinzel", 44), cx=775)
    draw_wrapped(draw, "Software Development Technologist at Promoción Social. Graduated Top of the Class with Academic Honors.", 770, 1350, 600, f_b, line_h=46)

    pil_img.save(os.path.join(OUT_PAGES, "map-1.jpg"), "JPEG", quality=95)
    print("Generated map-1.jpg (clean, 34pt scroll typography, zero halo)")

def generate_map_2():
    orig = cv2.imread(os.path.join(SRC_PAGES, "map-2.jpg"))
    boxes = [
        (230, 20, 690, 110),
        (140, 120, 840, 280),
        (180, 300, 360, 400),
        (370, 450, 960, 510),
        (400, 565, 1200, 675),
        (350, 680, 900, 810),
        (370, 910, 720, 1000),
        (1000, 780, 1420, 1030),
        (400, 1100, 730, 1180),
        (330, 1210, 860, 1360),
        (1060, 1400, 1340, 1530),
        (350, 1590, 820, 1680),
        (220, 1710, 1010, 2120),
        (1340, 1930, 1530, 2080)
    ]
    clean = inpaint_boxes(orig, boxes, threshold=125, dilate_iter=1, radius=3)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)

    f_banner = get_font("cinzel", 48)
    f_h = get_font("cinzel", 34)
    f_b = get_font("regular", 33)
    f_sm = get_font("regular", 28)

    # Milestone 4: DEC 2024 - 2025
    draw_centered(draw, "DEC 2024 - 2025", 48, f_banner, cx=470)
    draw_wrapped(draw, "SENA Technologist in Software Analysis & Development. Advanced systems modeling, requirements, and databases.", 480, 150, 560, f_b, line_h=42)

    # Milestone 5: 2025 - 2026
    draw_centered(draw, "2025 - 2026", 595, f_banner, cx=775)
    draw_wrapped(draw, "Campuslands Elite Software Academy. Developing production multi-agent AI platforms and LangGraph workflows.", 620, 695, 520, f_b, line_h=42)
    draw_wrapped(draw, "• Multi-Agent LangGraph \\n• Model Context Protocol \\n• Strict 4NF MySQL/Postgres \\n• Production CI/CD & Docker", 1200, 800, 360, f_sm, line_h=38)

    # Milestone 6: 2026 AND BEYOND
    draw_centered(draw, "2026 AND BEYOND", 1130, f_banner, cx=560)
    draw_wrapped(draw, "Next-generation distributed architectures, spatial web & 3D visualization, and global technical leadership.", 580, 1230, 500, f_b, line_h=44)

    # Vision Signpost
    draw_centered(draw, "STRATEGIC PROFESSIONAL VISION", 1630, f_h, cx=580)
    v_bullets = [
        "• Enterprise Software Architecture & AI Engineering",
        "• Scalable Microservices & Event-Driven Systems",
        "• Continuous Innovation in Autonomous Agent Workflows",
        "• Open Source Tooling & Technical Mentorship"
    ]
    for idx, v in enumerate(v_bullets):
        draw.text((250, 1740 + idx * 64), v, font=get_font("regular", 32), fill=INK_DARK)

    # Arrow signposts
    draw_centered(draw, "DISTRIBUTED", 1955, get_font("cinzel", 25), cx=1435)
    draw_centered(draw, "SYSTEMS", 1985, get_font("cinzel", 25), cx=1435)
    draw_centered(draw, "SPATIAL & AI", 2040, get_font("cinzel", 25), cx=1435)

    pil_img.save(os.path.join(OUT_PAGES, "map-2.jpg"), "JPEG", quality=95)
    print("Generated map-2.jpg (clean, 33pt scroll typography, zero halo)")

# ==================== GROUP D: CHAPTER DIVIDERS (ENGRAVINGS PRESERVED) ====================

def generate_journey():
    orig = cv2.imread(os.path.join(SRC_PAGES, "journey.jpg"))
    boxes = [(250, 1100, 1300, 1750)]
    clean = inpaint_boxes(orig, boxes, threshold=140, radius=4)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width

    draw_centered(draw, "CHAPTER II", 1180, get_font("cinzel", 48), cx=w//2)
    draw_centered(draw, "JOURNEY", 1275, get_font("cinzel", 68), cx=w//2)
    draw_centered(draw, "The path of continuous learning.", 1460, get_font("italic", 38), cx=w//2)
    draw_centered(draw, "Where logic forges engineering.", 1530, get_font("italic", 36), cx=w//2)
    draw_centered(draw, "From foundational algorithms to advanced systems architecture.", 1605, get_font("regular", 34), cx=w//2)
    draw_centered(draw, "Explore the chronological milestones across the following parchment scrolls.", 1675, get_font("regular", 30), cx=w//2)

    pil_img.save(os.path.join(OUT_PAGES, "journey.jpg"), "JPEG", quality=95)
    print("Generated journey.jpg (astrolabe preserved, large typography)")

def generate_career():
    orig = cv2.imread(os.path.join(SRC_PAGES, "career.jpg"))
    boxes = [(250, 1100, 1300, 1750)]
    clean = inpaint_boxes(orig, boxes, threshold=140, radius=4)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width

    draw_centered(draw, "CHAPTER III", 1140, get_font("cinzel", 48), cx=w//2)
    draw_centered(draw, "EXPERIENCE", 1235, get_font("cinzel", 68), cx=w//2)
    draw_centered(draw, "Every project marks a milestone in my craft.", 1410, get_font("italic", 38), cx=w//2)
    draw_centered(draw, "Where engineering and logic come to life.", 1480, get_font("italic", 36), cx=w//2)
    draw_centered(draw, "Solving complex challenges with architectural elegance.", 1555, get_font("regular", 34), cx=w//2)
    draw_centered(draw, "Building high-impact scalable solutions.", 1625, get_font("regular", 32), cx=w//2)

    pil_img.save(os.path.join(OUT_PAGES, "career.jpg"), "JPEG", quality=95)
    print("Generated career.jpg (hourglass preserved, large typography)")

def generate_projects():
    orig = cv2.imread(os.path.join(SRC_PAGES, "projects.jpg"))
    boxes = [(250, 1100, 1300, 1750)]
    clean = inpaint_boxes(orig, boxes, threshold=140, radius=4)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width

    draw_centered(draw, "CHAPTER IV", 1140, get_font("cinzel", 52), cx=w//2)
    draw_centered(draw, "FEATURED PROJECTS", 1235, get_font("cinzel", 68), cx=w//2)
    draw_centered(draw, "Selected works, systems architectures & live demonstrations.", 1410, get_font("italic", 38), cx=w//2)
    draw_centered(draw, "From autonomous AI agents to enterprise WMS solutions.", 1480, get_font("italic", 36), cx=w//2)
    draw_centered(draw, "Click interactive seals and badges to inspect GitHub repositories and live deployments.", 1555, get_font("regular", 32), cx=w//2)
    draw_centered(draw, "Turn the page to begin the engineering showcase.", 1625, get_font("regular", 32), cx=w//2)

    pil_img.save(os.path.join(OUT_PAGES, "projects.jpg"), "JPEG", quality=95)
    print("Generated projects.jpg (stack of books preserved, large typography)")

# ==================== GROUP E: EXPERIENCE PAGES (PERFECT ALIGNMENT) ====================

def generate_thor_systems():
    orig = cv2.imread(os.path.join(SRC_PAGES, "thor-systems.jpg"))
    gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
    mask = np.zeros(orig.shape[:2], dtype=np.uint8)

    boxes = [
        (450, 150, 1100, 260),
        (90, 270, 1430, 440),
        (90, 480, 1430, 840),
        (90, 960, 1430, 1180),
        (90, 1320, 670, 1760),
        (810, 1320, 1440, 1760)
    ]
    for x1, y1, x2, y2 in boxes:
        roi = gray[y1:y2, x1:x2]
        m = np.zeros_like(roi)
        m[roi < 142] = 255
        m = cv2.dilate(m, np.ones((3,3), np.uint8), iterations=1)
        mask[y1:y2, x1:x2] = np.maximum(mask[y1:y2, x1:x2], m)

    # Protect Sun and Moon drawings
    mask[670:855, 100:305] = 0
    mask[1415:1735, 675:805] = 0

    clean = cv2.inpaint(orig, mask, 4, cv2.INPAINT_TELEA)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width

    draw_centered(draw, "CAMPUSLANDS", 175, get_font("cinzel", 64), cx=w//2)
    draw_centered(draw, "ELITE ACADEMY OF ADVANCED SOFTWARE ENGINEERING", 265, get_font("cinzel", 28), cx=w//2)
    
    # Paragraph 1
    draw_wrapped(draw, "Campuslands is an intensive elite technology ecosystem focused on advanced software engineering, scalable enterprise architecture, and global industry best practices.", w//2, 320, 1260, get_font("regular", 32), line_h=44)
    
    # Paragraph 2 (placed gracefully to the right of the Sun!)
    draw_wrapped(draw, "Participated actively in corporate engineering teams under agile Scrum, with weekly continuous delivery sprints, rigorous peer code reviews, and high-demand technical challenge solving.", 880, 680, 1000, get_font("regular", 31), line_h=42)
    
    # Paragraph 3
    draw_wrapped(draw, "This experience cemented my professional discipline, my structured problem-solving capabilities under pressure, and my mastery in building robust backend architectures ready for enterprise production.", w//2, 980, 1260, get_font("regular", 32), line_h=44)
    
    # Bottom Columns (flanking the Moon drawing!)
    draw.text((100, 1335), "— SOFT SKILLS & LEADERSHIP —", font=get_font("cinzel", 27), fill=INK_DARK)
    s_lines = [
        "• Technical leadership and team synergy under",
        "  agile Scrum & Kanban frameworks.",
        "• Assertive communication, high adaptability,",
        "  and structured problem-solving.",
        "• Disciplined execution, efficient time management,",
        "  and an unwavering commitment to quality."
    ]
    for idx, l in enumerate(s_lines):
        draw.text((100, 1400 + idx * 46), l, font=get_font("regular", 27), fill=INK_MUTED)

    draw.text((820, 1335), "— TECHNICAL PROFICIENCY —", font=get_font("cinzel", 27), fill=INK_DARK)
    t_lines = [
        "• Enterprise backend architecture with Java 17",
        "  and Spring Boot 3 (Security, JPA, microservices).",
        "• Advanced relational data modeling in MySQL",
        "  (strict 4NF, triggers, views & stored procedures).",
        "• High-performance REST APIs in Python (FastAPI)",
        "  and professional GitFlow & Docker CI/CD."
    ]
    for idx, l in enumerate(t_lines):
        draw.text((820, 1400 + idx * 46), l, font=get_font("regular", 27), fill=INK_MUTED)

    pil_img.save(os.path.join(OUT_PAGES, "thor-systems.jpg"), "JPEG", quality=95)
    print("Generated thor-systems.jpg (Sun & Moon protected, zero ghost text)")

def generate_thor_systems_2():
    orig = cv2.imread(os.path.join(SRC_PAGES, "thor-systems-2.jpg"))
    gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
    mask = np.zeros(orig.shape[:2], dtype=np.uint8)

    boxes = [
        (450, 150, 1100, 250),
        (100, 270, 1430, 380),
        (380, 480, 1150, 535),
        (100, 550, 1430, 660),
        (100, 830, 1430, 1030),
        (250, 1140, 1280, 1195),
        (100, 1210, 1430, 1325),
        (100, 1480, 1430, 1950)
    ]
    for x1, y1, x2, y2 in boxes:
        roi = gray[y1:y2, x1:x2]
        m = np.zeros_like(roi)
        m[roi < 142] = 255
        m = cv2.dilate(m, np.ones((3,3), np.uint8), iterations=1)
        mask[y1:y2, x1:x2] = np.maximum(mask[y1:y2, x1:x2], m)

    # Protect center Hourglass and Runic column
    mask[845:1015, 695:835] = 0
    mask[1480:1920, 725:805] = 0

    clean = cv2.inpaint(orig, mask, 4, cv2.INPAINT_TELEA)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width

    draw_centered(draw, "CAMPUSLANDS", 175, get_font("cinzel", 64), cx=w//2)
    draw_centered(draw, "ENTERPRISE PROJECTS & ARCHITECTURAL CONTRIBUTIONS", 265, get_font("cinzel", 28), cx=w//2)
    draw_wrapped(draw, "During my career at Campuslands, I led and collaborated in building complex software architectures and high-impact production platforms:", w//2, 310, 1280, get_font("regular", 32), line_h=42)

    # Project 1: LogiTrack WMS
    draw_centered(draw, "LOGITRACK WMS · BACKEND LEAD", 495, get_font("cinzel", 36), cx=w//2)
    draw_wrapped(draw, "Comprehensive enterprise logistics and warehouse management system engineered for multi-facility stock control, supplier receptions, lot tracking, and zero inventory discrepancy:", w//2, 565, 1280, get_font("regular", 31), line_h=42)

    b1_left = [
        "• Multi-warehouse stock control",
        "• Operational audit trails",
        "• JWT security & RBAC matrix"
    ]
    b1_right = [
        "• Strict 4NF normalization",
        "• MySQL triggers & procedures",
        "• High-throughput REST APIs"
    ]
    for i, l in enumerate(b1_left):
        draw.text((260, 850 + i * 54), l, font=get_font("regular", 30), fill=INK_MUTED)
    for i, r in enumerate(b1_right):
        draw.text((860, 850 + i * 54), r, font=get_font("regular", 30), fill=INK_MUTED)

    # Project 2: Multi-Agent
    draw_centered(draw, "CAMPUSLANDS INTELIGENTE · MULTI-AGENT PLATFORM", 1155, get_font("cinzel", 34), cx=w//2)
    draw_wrapped(draw, "Intelligent academic supervision and analytics platform powered by coordinated autonomous AI agents, computer vision, and real-time automated notification pipelines:", w//2, 1225, 1280, get_font("regular", 31), line_h=42)

    b2_left = [
        "• Coordinated agents (LangGraph)",
        "• Local LLMs & OpenRouter APIs",
        "• Real-time absence alerts",
        "• Predictive dropout risk analytics"
    ]
    b2_right = [
        "• Automated Telegram digests",
        "• Domain knowledge base with RAG",
        "• Academic performance metrics",
        "• Relational persistence & audit logs"
    ]
    for i, l in enumerate(b2_left):
        draw.text((210, 1500 + i * 110), l, font=get_font("regular", 29), fill=INK_MUTED)
    for i, r in enumerate(b2_right):
        draw.text((830, 1500 + i * 110), r, font=get_font("regular", 29), fill=INK_MUTED)

    pil_img.save(os.path.join(OUT_PAGES, "thor-systems-2.jpg"), "JPEG", quality=95)
    print("Generated thor-systems-2.jpg (hourglass & runes preserved)")

def generate_freelance():
    orig = cv2.imread(os.path.join(SRC_PAGES, "freelance.jpg"))
    gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
    mask = np.zeros(orig.shape[:2], dtype=np.uint8)

    boxes = [
        (80, 160, 1430, 430),
        (330, 600, 1420, 810),
        (330, 910, 1420, 1120),
        (330, 1210, 1420, 1420),
        (330, 1510, 1420, 1720),
        (80, 1820, 1440, 1960)
    ]
    for x1, y1, x2, y2 in boxes:
        roi = gray[y1:y2, x1:x2]
        m = np.zeros_like(roi)
        m[roi < 145] = 255
        m = cv2.dilate(m, np.ones((3,3), np.uint8), iterations=1)
        mask[y1:y2, x1:x2] = np.maximum(mask[y1:y2, x1:x2], m)

    clean = cv2.inpaint(orig, mask, 4, cv2.INPAINT_TELEA)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width

    draw_centered(draw, "CONSULTING & FREELANCE", 170, get_font("cinzel", 64), cx=w//2)
    draw_wrapped(draw, "Independent software engineering has allowed me to resolve concrete business challenges for clients and organizations, delivering custom platforms, automated workflows, and robust relational architectures.", w//2, 315, 1280, get_font("regular", 32), line_h=44)

    # 4 Services flanking the drawings on the left (x < 330)
    services = [
        ("FULL-STACK DEVELOPMENT & HIGH-PERFORMANCE APIS",
         "Design and construction of modern web applications with React/TypeScript and secure enterprise backends with Python (FastAPI) and Java (Spring Boot), engineered for high availability and seamless scalability.",
         610, 660),
        ("INTELLIGENT PROCESS AUTOMATION (N8N)",
         "Creation of autonomous workflows integrating payment gateways, instant messaging (Telegram / WhatsApp), databases, and CRMs, eliminating repetitive manual tasks and optimizing business operations.",
         920, 970),
        ("PRACTICAL AI INTEGRATION & AUTONOMOUS AGENTS",
         "Implementation of coordinated agents with LangGraph, intelligent support systems (HelpDesk AI), and MCP servers to connect large language models with proprietary enterprise tools and databases.",
         1220, 1270),
        ("END-TO-END SOFTWARE LIFECYCLE MANAGEMENT",
         "Comprehensive guidance from requirement gathering and normalized database architecture to cloud deployment, automated testing, and ongoing performance monitoring.",
         1520, 1570)
    ]

    f_sh = get_font("cinzel", 28)
    f_sb = get_font("regular", 29)
    for h_txt, b_txt, hy, by in services:
        draw.text((340, hy), h_txt, font=f_sh, fill=INK_DARK)
        draw_wrapped(draw, b_txt, 875, by, 1070, f_sb, line_h=42, align="left")

    draw_centered(draw, "Rigorous commitment to clean code, security, clear technical documentation,", 1845, get_font("italic", 32), cx=w//2)
    draw_centered(draw, "and on-time value delivery across every production engagement.", 1895, get_font("italic", 32), cx=w//2)

    pil_img.save(os.path.join(OUT_PAGES, "freelance.jpg"), "JPEG", quality=95)
    print("Generated freelance.jpg (drawings on left, clean 29pt text on right)")

def generate_freelance_2():
    orig = cv2.imread(os.path.join(SRC_PAGES, "freelance-2.jpg"))
    gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
    mask = np.zeros(orig.shape[:2], dtype=np.uint8)

    boxes = [
        (200, 160, 1350, 420),
        (130, 780, 680, 1050),
        (850, 780, 1410, 1050),
        (140, 1300, 1400, 1560),
        (130, 1780, 680, 2020),
        (850, 1780, 1410, 2020)
    ]
    for x1, y1, x2, y2 in boxes:
        roi = gray[y1:y2, x1:x2]
        m = np.zeros_like(roi)
        m[roi < 145] = 255
        m = cv2.dilate(m, np.ones((3,3), np.uint8), iterations=1)
        mask[y1:y2, x1:x2] = np.maximum(mask[y1:y2, x1:x2], m)

    clean = cv2.inpaint(orig, mask, 4, cv2.INPAINT_TELEA)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width

    draw_centered(draw, "PILLARS OF EXCELLENCE", 175, get_font("cinzel", 64), cx=w//2)
    draw_wrapped(draw, "Every engineering engagement and professional collaboration is built upon solid software principles, guaranteeing measurable quality, high performance, and enduring technical trust:", w//2, 315, 1260, get_font("regular", 32), line_h=44)

    f_box_h = get_font("cinzel", 26)
    f_box_b = get_font("regular", 29)

    # Box 1: Engineering Quality
    draw_wrapped(draw, "Clean, modular, and decoupled architecture. Structured, self-documenting code built to scale without technical debt.", 390, 810, 500, f_box_b, line_h=40)
    draw_centered(draw, "— ENGINEERING QUALITY —", 1010, f_box_h, cx=390)

    # Box 2: Operational Efficiency
    draw_wrapped(draw, "High-impact automated workflows that eliminate hours of manual daily effort through intelligent n8n pipelines and precise AI agents.", 1125, 810, 500, f_box_b, line_h=40)
    draw_centered(draw, "— OPERATIONAL EFFICIENCY —", 1010, f_box_h, cx=1125)

    # Middle: Data Integrity
    draw_wrapped(draw, "Databases designed with absolute mathematical rigor: strict 4NF normalization, total referential integrity, optimized queries, and zero data redundancy.", w//2, 1318, 1220, f_box_b, line_h=42)
    draw_centered(draw, "— DATA INTEGRITY & PERFORMANCE —", 1518, f_box_h, cx=w//2)

    # Box 3: Professional Commitment
    draw_wrapped(draw, "Direct, transparent, and proactive communication at every stage. On-time delivery rigorously aligned with strategic objectives.", 390, 1810, 500, f_box_b, line_h=40)
    draw_centered(draw, "— PROFESSIONAL COMMITMENT —", 1960, f_box_h, cx=390)

    # Box 4: AI Innovation
    draw_wrapped(draw, "Adoption of cutting-edge technologies: autonomous agents (LangGraph), MCP servers, RAG pipelines, and seamless enterprise LLM integration.", 1125, 1810, 500, f_box_b, line_h=40)
    draw_centered(draw, "— AI & INNOVATION —", 1960, f_box_h, cx=1125)

    pil_img.save(os.path.join(OUT_PAGES, "freelance-2.jpg"), "JPEG", quality=95)
    print("Generated freelance-2.jpg (boxes perfectly populated)")

# ==================== GROUP F: PROJECT SHOWCASE TEMPLATE (LARGE TYPOGRAPHY) ====================

def generate_project_template(title, subtitle, desc, links, section_title, features, badges, filename):
    orig_path = os.path.join(SRC_PAGES, filename)
    orig = cv2.imread(orig_path)
    clean = inpaint_auto(orig, threshold=142, radius=4)
    pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    w = pil_img.width
    
    draw_centered(draw, title, 140, get_font("cinzel", 60), cx=w//2)
    draw_centered(draw, subtitle, 235, get_font("cinzel", 28), cx=w//2)
    draw_wrapped(draw, desc, w//2, 305, 1280, get_font("regular", 31), line_h=42)
    
    # Links line at y=490 for 3D active area hotspot
    draw_centered(draw, links, 490, get_font("italic", 31), cx=w//2)
    draw_centered(draw, f"— {section_title} —", 580, get_font("cinzel", 30), cx=w//2)
    
    f_fh = get_font("cinzel", 28)
    f_fb = get_font("regular", 28)
    for idx, (h_txt, b_txt, y) in enumerate(features):
        draw.text((140, y), h_txt, font=f_fh, fill=INK_DARK)
        draw_wrapped(draw, b_txt, 764, y + 38, 1240, f_fb, align="left", line_h=38)
        
    draw_badge_columns(draw, badges, y_header=1675, y_row1=1725, y_row2=1765)
    pil_img.save(os.path.join(OUT_PAGES, filename), "JPEG", quality=95)
    print(f"Generated {filename} (large, readable 28-31pt typography)")

def generate_all_projects():
    # 1. qyou.jpg
    qyou_features = [
        ("1. COLLABORATIVE MULTI-AGENT GRAPH (LangGraph)", "Autonomous agents coordinating inquiry triage, policy evaluation, and personalized remediation guidance.", 665),
        ("2. COMPUTER VISION ATTENDANCE ENGINE", "Automated biometric presence detection with OpenCV and deep learning, logging timestamps with zero manual intervention.", 815),
        ("3. PREDICTIVE STUDENT RISK ANALYTICS", "Machine learning models analyzing attendance velocity and evaluation trends to flag academic dropout risk early.", 965),
        ("4. INSTANT TELEGRAM BOT NOTIFICATIONS", "Real-time alerting pipeline notifying students of status changes and delivering automated daily coordinator digests.", 1115)
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
        ("1. ASYNCHRONOUS INGESTION GATEWAY", "High-throughput API gateway validating payloads, managing session tokens, and routing events to active agent queues.", 665),
        ("2. STATEGRAPH MEMORY & RETRIEVAL", "Dynamic checkpoint persistence preserving conversation context across multi-step student interactions with RAG lookups.", 815),
        ("3. LLM ROUTING & COST OPTIMIZATION", "Intelligent prompt routing dispatching low-latency queries to local models and complex reasoning to OpenRouter APIs.", 965),
        ("4. COMPREHENSIVE AUDITING & DASHBOARDS", "Structured event logging recording every agent decision, confidence score, and timestamp for total auditability.", 1115)
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
        ("1. MULTI-WAREHOUSE STOCK & LOT CONTROL", "Centralized administration of inventory distributed across multiple physical facilities with strict negative-stock prevention and granular lot traceability.", 665),
        ("2. FULL OPERATIONAL AUDITING & TRACEABILITY", "Immutable chronological logging of receptions, dispatches, transfers, and inventory adjustments with operator identification and millisecond timestamps.", 815),
        ("3. PURCHASE ORDER & SUPPLIER RECEPTION", "Structured receiving pipeline with automated purchase order reconciliation, discrepancy identification, and instant stock ledger synchronization.", 965),
        ("4. ROLE HIERARCHY & JWT SECURITY (RBAC)", "Granular permission matrix backed by Spring Security and signed JWTs for SuperAdmins, Warehouse Managers, Logistics Operators, and Auditors.", 1115)
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
        ("1. WEB INGESTION & DATA CAPTURE", "Responsive web form for structured receipt of student absence requests with medical and official supporting attachments.", 665),
        ("2. NORMALIZATION & VALIDATION IN N8N", "Orchestration workflow in n8n sanitizing inputs, validating schema constraints, and preparing structured inference payloads.", 815),
        ("3. INTELLIGENT EVALUATION VIA LLM", "Prompt-engineered connection with OpenRouter LLMs categorizing justifications into: Valid, Invalid, or Pending Human Review.", 965),
        ("4. REAL-TIME GOOGLE SHEETS SYNC", "Instant synchronization with the master absence ledger recording timestamps, AI confidence verdict, and summarized rationale.", 1115),
        ("5. INSTANT TELEGRAM BOT NOTIFICATIONS", "Real-time dispatch notifying students of their resolution and delivering consolidated digest reports to academic coordinators.", 1265)
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
        ("1. REPOSITORY METRICS & AUDITING", "Inspect repo metadata, commit histories, contributor metrics, and branch protection rules via optimized REST calls.", 665),
        ("2. AUTOMATED ISSUE & PR MANAGEMENT", "Programmatically read, create, comment, assign, and transition GitHub issues and pull requests with validation.", 815),
        ("3. SECURE FILE SEARCH & TREE INSPECTION", "Recursive directory traversal, file content retrieval, and blob inspection with size safeguards.", 965),
        ("4. STRICT SCHEMAS & INPUT VALIDATION", "Full JSON Schema tool declarations ensuring LLMs generate mathematically valid arguments before execution.", 1115)
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
        ("1. USER PROMPT INGESTION", "Agent receives user instruction in natural language and identifies required repository operations.", 665),
        ("2. TOOL RESOLUTION & INFERENCE", "LLM inspects MCP tool schemas and constructs typed execution arguments with strict parameter constraints.", 815),
        ("3. DISPATCH & GITHUB API EXECUTION", "MCP server validates auth token, verifies parameters, and executes rate-limited GitHub API calls.", 965),
        ("4. STRUCTURED RESPONSE & CONTEXT SYNTHESIS", "JSON result is formatted into contextual text and returned to the LLM for final response synthesis.", 1115)
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
        ("1. INSTANT SEMANTIC CLASSIFICATION", "Automated classification of incoming tickets by technical category (Hardware, Network, Database, Security, Permissions).", 665),
        ("2. URGENCY & SLA PRIORITY SCORING", "LLM-driven urgency evaluation assessing business impact and assigning SLA response windows automatically.", 815),
        ("3. RAG KNOWLEDGE BASE & INSTANT RESOLUTION", "Semantic vector search against technical manuals delivering verified solutions to common issues instantly.", 965),
        ("4. SPECIALIST ROUTING & OPERATIONAL AUDIT", "Automated assignment to corresponding engineering queues with complete chronological timeline history.", 1115)
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
        ("1. STRICT 4NF NORMALIZATION", "Complete elimination of multi-valued dependencies and redundant data across catalog, customers, and order ledgers.", 665),
        ("2. ACID TRANSACTIONAL SAFETY", "Pessimistic locking strategies and concurrency controls to prevent overselling, race conditions, and phantom inventory loss.", 815),
        ("3. STORED PROCEDURES & TRIGGERS", "Encapsulated business logic: automated discount calculations, dynamic tax ledgers, and inventory reservations.", 965),
        ("4. RFM CUSTOMER SEGMENTATION", "Advanced analytical views calculating Recency, Frequency, and Monetary Value to drive strategic marketing insights.", 1115)
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
        ("1. CODE REVIEW CONFLICT RESOLUTION", "Simulated interactions with Product Owners, Tech Leads, and QA requiring constructive, empathetic technical communication.", 665),
        ("2. ARCHITECTURAL TRADE-OFF DILEMMAS", "Strategic scenarios forcing decisions between rapid feature delivery and long-term technical debt mitigation.", 815),
        ("3. CRISIS MANAGEMENT & OUTAGES", "High-pressure production incident simulations demanding clear stakeholder updates and composed triage.", 965),
        ("4. PERFORMANCE SCORING MATRIX", "Comprehensive scoring matrix assessing emotional intelligence, team synergy, and problem ownership.", 1115)
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
        ("1. PUBLIC COURSE CATALOG", "Open catalog enabling prospective students to search subjects, review syllabi, and view instructor credentials.", 665),
        ("2. INSTRUCTOR & CONTENT MANAGEMENT", "Comprehensive panel for creating, editing, and sequencing courses, modular units, and structured rich-media lessons.", 815),
        ("3. ENROLLMENT & GRADE TRACKING", "Dedicated portal for managing course registrations, logging exam scores, and visualizing academic progress.", 965),
        ("4. CLIENT-SIDE PERSISTENCE", "Structured LocalStorage persistence delivering instantaneous page transitions with zero hosting server overhead.", 1115)
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
        ("1. CYLINDRICAL DEFORMATION MATHEMATICS", "Custom vertex displacement algorithms modeling elastic sheet curvature, page stiffness, and natural spine curl.", 665),
        ("2. GPU TEXTURE PRECOMPILATION", "Precompiled WebGL textures in GPU VRAM enabling instantaneous language transitions with zero black flashes.", 815),
        ("3. INTERACTIVE RAYCASTING HOTSPOTS", "Real-time 3D coordinate unprojecting mapping screen cursor interactions to underlying page link seals and badges.", 965),
        ("4. ADAPTIVE VIEWPORT PROJECTION", "Adaptive camera frustum recalculations adjusting zoom, angle, and lighting across mobile and desktop screens.", 1115)
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
        ("1. 60 FPS HARDWARE ACCELERATION", "Smooth WebGL execution with FXAA antialiasing and soft dynamic shadow mapping across all viewports.", 665),
        ("2. MULTI-INPUT NAVIGATION ENGINE", "Comprehensive gesture detection supporting drag turning, touch swipes, keyboard arrow keys, and chapter plaques.", 815),
        ("3. PROCEDURAL PHYSICS & CURLING", "Parametric cylinder bending algorithms mathematically modeling real manuscript parchment flexibility and spine curvature.", 965),
        ("4. ZERO-LATENCY I18N ARCHITECTURE", "Dual-language preloading architecture guaranteeing clean instant re-initialization from the cover with zero ghost artifacts.", 1115)
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
    
    print("=== STARTING REFINED MASTER GENERATION (LARGE TYPOGRAPHY, PERFECT ALIGNMENT) ===")
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
    print("=== ALL 32 ENGLISH EDITION PAGES SUCCESSFULLY REGENERATED ===")

if __name__ == "__main__":
    main()
