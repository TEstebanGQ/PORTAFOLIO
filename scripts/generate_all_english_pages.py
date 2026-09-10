#!/usr/bin/env python3
"""
Complete English Page Texture Generator for 3D Codex Portfolio.
Uses feathered Gaussian alpha blending from blank.jpg to cleanly erase Spanish text,
and renders English text with authentic Renaissance typography (Cinzel & EB Garamond).
"""

import os
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PAGES = os.path.join(BASE_DIR, "public", "img", "pages")
OUT_PAGES = os.path.join(BASE_DIR, "public", "img", "pages-en")

BLANK_PATH = os.path.join(SRC_PAGES, "blank.jpg")
FONTS_DIR = os.path.join(BASE_DIR, "public", "fonts")

FONT_CINZEL_PATH = os.path.join(FONTS_DIR, "Cinzel.ttf")
FONT_REG_PATH = os.path.join(FONTS_DIR, "EBGaramond-Regular.ttf")
FONT_ITALIC_PATH = os.path.join(FONTS_DIR, "EBGaramond-Italic.ttf")

COLOR_INK = (32, 25, 18)
COLOR_INK_MUTED = (75, 62, 48)
COLOR_GOLD = (218, 185, 115)
COLOR_GOLD_BRIGHT = (240, 215, 155)

def get_font(font_type, size):
    if font_type == "cinzel":
        return ImageFont.truetype(FONT_CINZEL_PATH, size)
    elif font_type == "italic":
        return ImageFont.truetype(FONT_ITALIC_PATH, size)
    else:
        return ImageFont.truetype(FONT_REG_PATH, size)

def patch_clean(img, blank, bbox, feather=16):
    x1, y1, x2, y2 = bbox
    w, h = x2 - x1, y2 - y1
    crop = blank.crop((x1, y1, x2, y2))
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    pad = max(2, min(feather, w // 4, h // 4))
    d.rectangle([pad, pad, w - pad, h - pad], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(pad / 2))
    img.paste(crop, (x1, y1), mask)

def patch_polygon(img, blank, poly, feather=8):
    mask = Image.new("L", img.size, 0)
    d = ImageDraw.Draw(mask)
    d.polygon(poly, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(feather))
    img.paste(blank, (0, 0), mask)

def patch_clean_leather(img, target_box, source_box, feather=20):
    x1, y1, x2, y2 = target_box
    sx1, sy1, sx2, sy2 = source_box
    bw, bh = x2 - x1, y2 - y1
    source_crop = img.crop((sx1, sy1, sx2, sy2)).resize((bw, bh))
    mask = Image.new("L", (bw, bh), 0)
    d = ImageDraw.Draw(mask)
    pad = max(2, min(feather, bw // 4, bh // 4))
    d.rectangle([pad, pad, bw - pad, bh - pad], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(pad / 2))
    img.paste(source_crop, (x1, y1), mask)

def draw_centered(draw, text, cx, y, font, fill=COLOR_INK):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text((cx - tw / 2, y), text, font=font, fill=fill)
    return y + (bbox[3] - bbox[0])

def draw_wrapped(draw, text, cx, y, max_w, font, fill=COLOR_INK, line_spacing=1.3, align="center"):
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
    
    line_h = font.size * line_spacing
    for l in lines:
        bbox = draw.textbbox((0, 0), l, font=font)
        lw = bbox[2] - bbox[0]
        if align == "center":
            draw.text((cx - lw / 2, y), l, font=font, fill=fill)
        elif align == "left":
            draw.text((cx - max_w / 2, y), l, font=font, fill=fill)
        y += line_h
    return y

def draw_badge_columns(draw, col_data, y_header=1655, y_row1=1705, y_row2=1745):
    """Draw 4 standard tech badges with header and 2 rows."""
    f_h = get_font("cinzel", 24)
    f_b = get_font("regular", 23)
    centers = [300, 610, 920, 1230]
    for (cx, (h, r1, r2)) in zip(centers, col_data):
        draw_centered(draw, h, cx, y_header, f_h)
        draw_centered(draw, r1, cx, y_row1, f_b)
        draw_centered(draw, r2, cx, y_row2, f_b)

def generate_welcome(blank):
    img = Image.open(os.path.join(SRC_PAGES, "welcome.jpg")).convert("RGB")
    blank_scaled = blank.resize(img.size)
    patch_clean(img, blank_scaled, (300, 100, 1250, 260), feather=24)
    patch_clean(img, blank_scaled, (100, 1550, 1440, 1850), feather=24)
    
    draw = ImageDraw.Draw(img)
    font_title = get_font("cinzel", 56)
    font_body = get_font("regular", 28)
    draw_centered(draw, "WELCOME", 772, 160, font_title)
    draw_wrapped(draw, "Double-click to toggle\nfullscreen view", 470, 1660, 450, font_body)
    draw_wrapped(draw, "Swipe or use arrow keys (↓ →)\nto turn pages forward & back", 1080, 1660, 480, font_body)
    img.save(os.path.join(OUT_PAGES, "welcome.jpg"), "JPEG", quality=95)
    print("Generated welcome.jpg")

def generate_about(blank):
    img = Image.open(os.path.join(SRC_PAGES, "about.jpg")).convert("RGB")
    patch_clean(img, blank, (180, 1180, 1350, 1780), feather=24)
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "CHAPTER I", 764, 1205, get_font("cinzel", 44))
    draw_centered(draw, "ABOUT ME", 764, 1305, get_font("cinzel", 64))
    draw_centered(draw, "Discover my journey, page by page.", 764, 1490, get_font("italic", 32))
    draw_centered(draw, "Full Stack Developer & Software Architect.", 764, 1550, get_font("regular", 30))
    draw_centered(draw, "My systems, my models, my engineering craft.", 764, 1615, get_font("regular", 30))
    draw_centered(draw, "Explore the codex and interact with each project.", 764, 1680, get_font("italic", 30))
    img.save(os.path.join(OUT_PAGES, "about.jpg"), "JPEG", quality=95)
    print("Generated about.jpg")

def generate_who_am_i(blank):
    img = Image.open(os.path.join(SRC_PAGES, "who-am-i.jpg")).convert("RGB")
    patch_clean(img, blank, (240, 110, 1290, 320), feather=24)
    patch_clean(img, blank, (180, 800, 1350, 1200), feather=24)
    patch_clean(img, blank, (280, 1335, 1250, 1415), feather=20)
    patch_clean(img, blank, (560, 1690, 960, 1755), feather=12)
    patch_clean(img, blank, (600, 1865, 930, 1925), feather=12)
    patch_clean(img, blank, (960, 1690, 1360, 1755), feather=12)
    patch_clean(img, blank, (960, 1755, 1360, 1808), feather=12)
    
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "WHO AM I", 764, 135, get_font("cinzel", 58))
    draw_centered(draw, "Software Architect • AI Solutions • Full Stack Engineer", 764, 265, get_font("cinzel", 26))
    draw_centered(draw, "Welcome!", 764, 825, get_font("italic", 44))
    draw_centered(draw, "I am Tomás Esteban González Quintero,", 764, 940, get_font("regular", 32))
    draw_centered(draw, "Full Stack Developer & AI Solutions Integrator —", 764, 1005, get_font("italic", 28))
    draw_centered(draw, "specialized in multi-agent architectures, clean code,", 764, 1068, get_font("regular", 28))
    draw_centered(draw, "4NF relational databases, and high-impact enterprise automations.", 764, 1122, get_font("regular", 28))
    draw_centered(draw, "Bucaramanga, Colombia • WhatsApp: +57 316 775 5887", 764, 1355, get_font("italic", 26))
    
    f_t = get_font("regular", 28)
    draw_centered(draw, "LangGraph / Agents", 764, 1708, f_t)
    draw_centered(draw, "PyTorch / Vision", 764, 1882, f_t)
    draw_centered(draw, "Clean Architecture", 1160, 1708, f_t)
    draw_centered(draw, "4NF Relational Model", 1160, 1765, f_t)
    img.save(os.path.join(OUT_PAGES, "who-am-i.jpg"), "JPEG", quality=95)
    print("Generated who-am-i.jpg")

def generate_my_story(blank):
    img = Image.open(os.path.join(SRC_PAGES, "my-story.jpg")).convert("RGB")
    patch_clean(img, blank, (380, 130, 1150, 235), feather=24)
    patch_clean(img, blank, (180, 620, 750, 920), feather=20)
    patch_clean(img, blank, (780, 620, 1350, 920), feather=20)
    patch_clean(img, blank, (180, 1400, 750, 1700), feather=20)
    patch_clean(img, blank, (780, 1400, 1350, 1700), feather=20)
    
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "MY STORY", 764, 150, get_font("cinzel", 58))
    f_b = get_font("regular", 27)
    p1 = "From an early age, I felt a deep fascination for logic, mathematics, and digital systems. Code naturally became my native language to create, explore, and solve complex problems."
    p2 = "I evolved by engineering robust backend systems with Python, FastAPI, and Spring Boot, understanding that the enduring foundation of any great platform is its architecture."
    p3 = "At Campuslands, I forged my discipline in full stack engineering, designing 4NF relational databases, modular microservices, and autonomous multi-agent workflows with AI."
    p4 = "Today I build scalable platforms, MCP servers, and enterprise automation pipelines. I bring engineering rigor, modern architectural vision, and relentless delivery."
    draw_wrapped(draw, p1, 465, 645, 470, f_b, line_spacing=1.35)
    draw_wrapped(draw, p2, 1065, 645, 470, f_b, line_spacing=1.35)
    draw_wrapped(draw, p3, 465, 1425, 470, f_b, line_spacing=1.35)
    draw_wrapped(draw, p4, 1065, 1425, 470, f_b, line_spacing=1.35)
    img.save(os.path.join(OUT_PAGES, "my-story.jpg"), "JPEG", quality=95)
    print("Generated my-story.jpg")

def generate_skills(blank):
    img = Image.open(os.path.join(SRC_PAGES, "skills.jpg")).convert("RGB")
    patch_clean(img, blank, (320, 120, 1210, 235), feather=24)
    patch_clean(img, blank, (180, 1610, 1350, 2120), feather=24)
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "TECHNICAL SKILLS", 764, 150, get_font("cinzel", 58))
    draw_centered(draw, "Tap to zoom & inspect mandala", 764, 1750, get_font("italic", 34))
    img.save(os.path.join(OUT_PAGES, "skills.jpg"), "JPEG", quality=95)
    print("Generated skills.jpg")

def generate_interests(blank):
    img = Image.open(os.path.join(SRC_PAGES, "interests.jpg")).convert("RGB")
    patch_clean(img, blank, (300, 130, 1230, 240), feather=24)
    patch_clean(img, blank, (180, 250, 1350, 310), feather=20)
    patch_clean(img, blank, (520, 600, 1010, 650), feather=12)
    patch_clean(img, blank, (520, 1640, 1010, 1690), feather=12)
    patch_clean(img, blank, (50, 1980, 1480, 2135), feather=24)
    
    # Patch the 2 curved text arcs
    poly1 = [(208, 1175), (410, 1018), (426, 1055), (224, 1200)]
    poly2 = [(1100, 1018), (1273, 1152), (1239, 1175), (1086, 1055)]
    patch_polygon(img, blank, poly1, feather=6)
    patch_polygon(img, blank, poly2, feather=6)
    
    # Draw angled text
    f_arc = get_font("cinzel", 22)
    t_im1 = Image.new("RGBA", (300, 60), (0, 0, 0, 0))
    ImageDraw.Draw(t_im1).text((10, 10), "DATA ANALYSIS", font=f_arc, fill=(32, 25, 18, 255))
    rot1 = t_im1.rotate(37.5, expand=True, resample=Image.BICUBIC)
    img.paste(rot1, (215, 1030), rot1)
    
    t_im2 = Image.new("RGBA", (300, 60), (0, 0, 0, 0))
    ImageDraw.Draw(t_im2).text((10, 10), "VISUALIZATION", font=f_arc, fill=(32, 25, 18, 255))
    rot2 = t_im2.rotate(-37.5, expand=True, resample=Image.BICUBIC)
    img.paste(rot2, (1080, 1030), rot2)
    
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "INTERESTS & PASSIONS", 764, 155, get_font("cinzel", 56))
    draw_centered(draw, "CYBERSECURITY • 3D ANIMATION • DATA ENGINEERING", 764, 265, get_font("cinzel", 24))
    draw_centered(draw, "CYBERSECURITY", 764, 615, get_font("cinzel", 23))
    draw_centered(draw, "3D ANIMATION", 764, 1655, get_font("cinzel", 23))
    
    f_ch = get_font("cinzel", 24)
    f_cb = get_font("regular", 22)
    draw_centered(draw, "CYBERSECURITY", 290, 2012, f_ch)
    draw_centered(draw, "Ethical Hacking & DevSecOps", 290, 2045, f_cb)
    draw_centered(draw, "Systems & Network Defense", 290, 2073, f_cb)
    draw_centered(draw, "3D ANIMATION", 764, 2012, f_ch)
    draw_centered(draw, "WebGL, Three.js & Shaders", 764, 2045, f_cb)
    draw_centered(draw, "Real-time Interactive 3D", 764, 2073, f_cb)
    draw_centered(draw, "DATA ENGINEERING", 1240, 2012, f_ch)
    draw_centered(draw, "Statistical Modeling & BI", 1240, 2045, f_cb)
    draw_centered(draw, "ETL Pipelines & Machine Learning", 1240, 2073, f_cb)
    
    img.save(os.path.join(OUT_PAGES, "interests.jpg"), "JPEG", quality=95)
    print("Generated interests.jpg")

def generate_journey(blank):
    img = Image.open(os.path.join(SRC_PAGES, "journey.jpg")).convert("RGB")
    patch_clean(img, blank, (180, 1160, 1350, 1750), feather=24)
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "CHAPTER II", 764, 1190, get_font("cinzel", 44))
    draw_centered(draw, "ROADMAP & JOURNEY", 764, 1280, get_font("cinzel", 60))
    draw_centered(draw, "The path of continuous mastery.", 764, 1460, get_font("italic", 32))
    draw_centered(draw, "Where analytical logic forges engineering.", 764, 1520, get_font("regular", 30))
    draw_centered(draw, "From essential algorithms and clean code", 764, 1585, get_font("regular", 30))
    draw_centered(draw, "to applied artificial intelligence.", 764, 1650, get_font("italic", 30))
    img.save(os.path.join(OUT_PAGES, "journey.jpg"), "JPEG", quality=95)
    print("Generated journey.jpg")

def generate_map_1(blank):
    img = Image.open(os.path.join(SRC_PAGES, "map-1.jpg")).convert("RGB")
    # Patch scroll 1 (LEFT: x: 180..780, y: 40..400)
    patch_clean(img, blank, (180, 40, 780, 400), feather=18)
    # Patch scroll 2 (RIGHT: x: 840..1480, y: 460..820)
    patch_clean(img, blank, (840, 460, 1480, 820), feather=18)
    # Patch scroll 3 (CENTER: x: 400..1440, y: 1160..1610)
    patch_clean(img, blank, (400, 1160, 1440, 1610), feather=18)
    
    draw = ImageDraw.Draw(img)
    f_year = get_font("cinzel", 34)
    f_body = get_font("regular", 26)
    
    # Scroll 1
    draw_centered(draw, "2023", 480, 80, f_year)
    draw_wrapped(draw, "Started programming, mastering Python, data structures, and algorithmic logic.", 480, 190, 480, f_body)
    
    # Scroll 2
    draw_centered(draw, "2024 (January - June)", 1160, 500, get_font("cinzel", 30))
    draw_wrapped(draw, "Computer hardware diagnostics, electronic maintenance, component assembly, and OS optimization.", 1160, 640, 500, f_body)
    
    # Scroll 3
    draw_centered(draw, "2024 (June - November)", 764, 1220, get_font("cinzel", 30))
    draw_wrapped(draw, "Completed Software Development degree with highest academic honors.\nGraduated Valedictorian & Top Engineer of the cohort.", 764, 1340, 560, f_body)
    
    img.save(os.path.join(OUT_PAGES, "map-1.jpg"), "JPEG", quality=95)
    print("Generated map-1.jpg")

def generate_map_2(blank):
    img = Image.open(os.path.join(SRC_PAGES, "map-2.jpg")).convert("RGB")
    # Patch scroll 1 (LEFT: x: 120..980, y: 15..520)
    patch_clean(img, blank, (120, 15, 980, 520), feather=18)
    # Patch scroll 2 (Campuslands: x: 340..1440, y: 560..1030)
    patch_clean(img, blank, (340, 560, 1440, 1030), feather=18)
    # Patch scroll 3 (Deployment: x: 320..1360, y: 1100..1540)
    patch_clean(img, blank, (320, 1100, 1360, 1540), feather=18)
    # Patch vision on LEFT (x: 210..1030, y: 1590..2120)
    patch_clean(img, blank, (210, 1590, 1030, 2120), feather=18)
    # Patch signpost on RIGHT (x: 1330..1528, y: 1930..2090)
    patch_clean(img, blank, (1330, 1930, 1528, 2090), feather=16)
    
    draw = ImageDraw.Draw(img)
    f_body = get_font("regular", 25)
    
    # Scroll 1
    draw_centered(draw, "2025 (December)", 480, 45, get_font("cinzel", 32))
    draw_wrapped(draw, "Commenced SENA Higher Degree:\nTechnologist in Software Analysis & Development.", 480, 145, 520, f_body)
    draw_centered(draw, "Expanding engineering horizons", 480, 465, get_font("italic", 25))
    
    # Scroll 2: Campuslands
    draw_centered(draw, "2025 (June) - 2026 (September)", 764, 600, get_font("cinzel", 28))
    draw_centered(draw, "Entered Campuslands Elite Academy", 764, 675, get_font("italic", 27))
    bullets = "• Immersive hands-on development\n• Enterprise microservice platforms\n• Cross-functional Agile leadership\n• Exponential technical growth"
    draw_wrapped(draw, bullets, 764, 755, 520, f_body, align="left")
    
    # Scroll 3: Deployment
    draw_centered(draw, "2026 (June)", 550, 1130, get_font("cinzel", 30))
    draw_wrapped(draw, "Deployed first distributed platform to production cloud environments.", 550, 1230, 480, f_body)
    draw_centered(draw, "From architectural design into reality", 1200, 1445, get_font("italic", 24))
    
    # Vision (Left side)
    draw_centered(draw, "Professional Vision", 580, 1620, get_font("cinzel", 32))
    v_text = (
        "• Continuously engineer scalable, resilient distributed systems.\n"
        "• Specialize in cloud microservices, high-throughput APIs, and 4NF databases.\n"
        "• Deliver high-impact solutions to enterprise-grade challenges."
    )
    draw_wrapped(draw, v_text, 580, 1730, 660, f_body, line_spacing=1.4, align="left")
    
    # Signpost arrows (Right side)
    f_sign = get_font("cinzel", 21)
    draw_centered(draw, "DISCIPLINE", 1430, 1960, f_sign)
    draw_centered(draw, "FOCUS", 1430, 2005, f_sign)
    draw_centered(draw, "RESULTS", 1430, 2048, f_sign)
    
    img.save(os.path.join(OUT_PAGES, "map-2.jpg"), "JPEG", quality=95)
    print("Generated map-2.jpg")

def generate_career(blank):
    img = Image.open(os.path.join(SRC_PAGES, "career.jpg")).convert("RGB")
    patch_clean(img, blank, (180, 1100, 1350, 1700), feather=24)
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "CHAPTER III", 764, 1130, get_font("cinzel", 44))
    draw_centered(draw, "PROFESSIONAL CAREER", 764, 1220, get_font("cinzel", 58))
    draw_centered(draw, "Every milestone marks a leap in engineering.", 764, 1400, get_font("italic", 32))
    draw_centered(draw, "Where structured architecture meets execution.", 764, 1460, get_font("regular", 30))
    draw_centered(draw, "Solving complex enterprise problems with elegance.", 764, 1525, get_font("regular", 30))
    draw_centered(draw, "Building scalable, resilient, high-impact systems.", 764, 1590, get_font("italic", 30))
    img.save(os.path.join(OUT_PAGES, "career.jpg"), "JPEG", quality=95)
    print("Generated career.jpg")

def generate_thor_systems(blank):
    img = Image.open(os.path.join(SRC_PAGES, "thor-systems.jpg")).convert("RGB")
    patch_clean(img, blank, (140, 310, 1390, 470), feather=20)
    patch_clean(img, blank, (140, 690, 1390, 810), feather=20)
    patch_clean(img, blank, (140, 960, 1390, 1180), feather=20)
    patch_clean(img, blank, (130, 1320, 745, 1760), feather=18)
    patch_clean(img, blank, (775, 1320, 1395, 1760), feather=18)
    
    draw = ImageDraw.Draw(img)
    f_body = get_font("regular", 27)
    intro = "Campuslands is an elite high-performance technology ecosystem dedicated to advanced software engineering, scalable enterprise architecture, and global industry best practices."
    p1 = "Engineered production-grade corporate platforms under Scrum methodology, featuring weekly continuous delivery cycles, high-demand technical challenges, and rigorous peer code reviews."
    p2 = "This experience solidified my engineering discipline, structured problem-solving under pressure, and mastery in constructing robust backend architectures prepared for high-concurrency production environments."
    draw_wrapped(draw, intro, 764, 325, 1250, f_body, line_spacing=1.35)
    draw_wrapped(draw, p1, 764, 705, 1250, f_body, line_spacing=1.35)
    draw_wrapped(draw, p2, 764, 975, 1250, f_body, line_spacing=1.35)
    
    draw_centered(draw, "SOFT SKILLS", 437, 1345, get_font("cinzel", 26))
    s_skills = "Technical leadership and cross-functional team collaboration under agile Scrum and Kanban frameworks. Assertive technical communication, rapid adaptability, structured problem-solving under pressure, constant self-discipline, efficient time management, and a relentless focus on delivery quality."
    draw_wrapped(draw, s_skills, 437, 1410, 560, get_font("regular", 24), line_spacing=1.3)
    
    draw_centered(draw, "TECHNICAL SKILLS", 1085, 1345, get_font("cinzel", 26))
    t_skills = "Enterprise backend architecture with Java 17 and Spring Boot (Spring Security, JPA/Hibernate, microservices). Advanced relational modeling in MySQL and PostgreSQL (4NF normalization, triggers, views, and stored procedures). High-performance RESTful APIs in Python (FastAPI) and professional GitFlow."
    draw_wrapped(draw, t_skills, 1085, 1410, 560, get_font("regular", 24), line_spacing=1.3)
    img.save(os.path.join(OUT_PAGES, "thor-systems.jpg"), "JPEG", quality=95)
    print("Generated thor-systems.jpg")

def generate_thor_systems_2(blank):
    img = Image.open(os.path.join(SRC_PAGES, "thor-systems-2.jpg")).convert("RGB")
    patch_clean(img, blank, (140, 270, 1390, 380), feather=20)
    patch_clean(img, blank, (140, 550, 1390, 660), feather=20)
    patch_clean(img, blank, (140, 830, 1390, 1040), feather=20)
    patch_clean(img, blank, (140, 1130, 1390, 1195), feather=18)
    patch_clean(img, blank, (140, 1210, 1390, 1330), feather=20)
    patch_clean(img, blank, (140, 1480, 1390, 1960), feather=20)
    
    draw = ImageDraw.Draw(img)
    sub = "During my journey at Campuslands, I led and collaborated in engineering complex software architectures and high-impact production systems:"
    draw_wrapped(draw, sub, 764, 280, 1250, get_font("regular", 27), line_spacing=1.35)
    
    l_desc = "Comprehensive warehouse management system (WMS) for real-time inventory control, supplier dispatches, and absolute stock traceability without discrepancies:"
    draw_wrapped(draw, l_desc, 764, 560, 1250, get_font("regular", 26), line_spacing=1.35)
    
    f_p = get_font("regular", 25)
    draw_wrapped(draw, "• Multi-warehouse stock control", 440, 845, 540, f_p, align="left")
    draw_wrapped(draw, "• Strict 4NF relational design", 1040, 845, 540, f_p, align="left")
    draw_wrapped(draw, "• Full operational audit logging", 440, 915, 540, f_p, align="left")
    draw_wrapped(draw, "• MySQL triggers & stored procedures", 1040, 915, 540, f_p, align="left")
    draw_wrapped(draw, "• JWT authentication & RBAC security", 440, 985, 540, f_p, align="left")
    draw_wrapped(draw, "• High-throughput RESTful APIs", 1040, 985, 540, f_p, align="left")
    
    draw_centered(draw, "CAMPUSLANDS INTELLIGENT • MULTI-AGENT", 764, 1145, get_font("cinzel", 30))
    c_desc = "Intelligent supervision and academic analytics platform driven by autonomous AI agents and automated management workflows:"
    draw_wrapped(draw, c_desc, 764, 1220, 1250, get_font("regular", 26), line_spacing=1.35)
    
    draw_wrapped(draw, "• Coordinated multi-agent graphs (LangGraph)", 440, 1495, 560, f_p, align="left")
    draw_wrapped(draw, "• Automated reporting via Telegram Bot", 1040, 1495, 560, f_p, align="left")
    draw_wrapped(draw, "• Local LLM inference & Cloud AI APIs", 440, 1630, 560, f_p, align="left")
    draw_wrapped(draw, "• Knowledge base retrieval with RAG", 1040, 1630, 560, f_p, align="left")
    draw_wrapped(draw, "• Real-time attendance anomaly alerts", 440, 1765, 560, f_p, align="left")
    draw_wrapped(draw, "• Predictive academic dropout analytics", 1040, 1765, 560, f_p, align="left")
    draw_wrapped(draw, "• Early intervention student alerts", 440, 1900, 560, f_p, align="left")
    draw_wrapped(draw, "• Decoupled relational persistence", 1040, 1900, 560, f_p, align="left")
    
    img.save(os.path.join(OUT_PAGES, "thor-systems-2.jpg"), "JPEG", quality=95)
    print("Generated thor-systems-2.jpg")

def generate_freelance(blank):
    img = Image.open(os.path.join(SRC_PAGES, "freelance.jpg")).convert("RGB")
    patch_clean(img, blank, (240, 160, 1290, 255), feather=24)
    patch_clean(img, blank, (140, 310, 1390, 420), feather=20)
    patch_clean(img, blank, (130, 600, 1395, 810), feather=20)
    patch_clean(img, blank, (130, 910, 1395, 1120), feather=20)
    patch_clean(img, blank, (130, 1210, 1395, 1420), feather=20)
    patch_clean(img, blank, (130, 1510, 1395, 1720), feather=20)
    patch_clean(img, blank, (140, 1830, 1390, 1950), feather=20)
    
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "CONSULTING & FREELANCE", 764, 175, get_font("cinzel", 54))
    sub = "Independent consulting has empowered me to solve concrete business challenges for clients and organizations, transforming technical requirements into scalable, secure, and automated platforms."
    draw_wrapped(draw, sub, 764, 320, 1250, get_font("regular", 27), line_spacing=1.35)
    
    f_ch = get_font("cinzel", 28)
    f_cb = get_font("regular", 25)
    draw_centered(draw, "FULL STACK DEVELOPMENT & HIGH-PERFORMANCE APIS", 764, 615, f_ch)
    c1 = "Architecture and engineering of modern web applications with React/TypeScript and secure backends with Python (FastAPI) and Java (Spring Boot), built for high availability, low latency, and clean scalability."
    draw_wrapped(draw, c1, 764, 670, 1200, f_cb, line_spacing=1.35)
    
    draw_centered(draw, "INTELLIGENT PROCESS AUTOMATION (N8N)", 764, 925, f_ch)
    c2 = "Engineering autonomous workflows integrating payment gateways, instant messaging (Telegram/WhatsApp), databases, and CRMs, eliminating repetitive manual toil and streamlining operational efficiency."
    draw_wrapped(draw, c2, 764, 980, 1200, f_cb, line_spacing=1.35)
    
    draw_centered(draw, "PRACTICAL AI INTEGRATION & AUTONOMOUS AGENTS", 764, 1225, f_ch)
    c3 = "Implementation of multi-agent state graphs with LangGraph, AI-assisted customer support (HelpDeskAI), and Model Context Protocol (MCP) servers connecting frontier LLMs to enterprise databases and tools."
    draw_wrapped(draw, c3, 764, 1280, 1200, f_cb, line_spacing=1.35)
    
    draw_centered(draw, "END-TO-END SOFTWARE LIFECYCLE MANAGEMENT", 764, 1525, f_ch)
    c4 = "Full development lifecycle oversight from requirements elicitation and 4NF database architecture to cloud container deployments, automated unit testing, CI/CD pipelines, and continuous observability."
    draw_wrapped(draw, c4, 764, 1580, 1200, f_cb, line_spacing=1.35)
    
    foot = "Rigorous commitment to clean code, security, clear technical documentation, and punctual delivery of business value in every deployed solution."
    draw_wrapped(draw, foot, 764, 1850, 1250, get_font("italic", 26), line_spacing=1.35)
    img.save(os.path.join(OUT_PAGES, "freelance.jpg"), "JPEG", quality=95)
    print("Generated freelance.jpg")

def generate_freelance_2(blank):
    img = Image.open(os.path.join(SRC_PAGES, "freelance-2.jpg")).convert("RGB")
    patch_clean(img, blank, (240, 160, 1290, 255), feather=24)
    patch_clean(img, blank, (140, 305, 1390, 420), feather=20)
    patch_clean(img, blank, (130, 795, 745, 930), feather=16)
    patch_clean(img, blank, (775, 795, 1395, 930), feather=16)
    patch_clean(img, blank, (130, 1000, 745, 1050), feather=14)
    patch_clean(img, blank, (775, 1000, 1395, 1050), feather=14)
    patch_clean(img, blank, (130, 1310, 1395, 1415), feather=18)
    patch_clean(img, blank, (300, 1505, 1230, 1560), feather=16)
    patch_clean(img, blank, (130, 1800, 745, 1940), feather=16)
    patch_clean(img, blank, (775, 1800, 1395, 1940), feather=16)
    patch_clean(img, blank, (130, 1950, 745, 2000), feather=14)
    patch_clean(img, blank, (775, 1950, 1395, 2000), feather=14)
    
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "PILLARS OF EXCELLENCE", 764, 175, get_font("cinzel", 54))
    sub = "Every engineering project and professional engagement is grounded in proven software principles, guaranteeing measurable quality, operational efficiency, and long-term trust:"
    draw_wrapped(draw, sub, 764, 320, 1250, get_font("regular", 27), line_spacing=1.35)
    
    f_pb = get_font("regular", 24)
    f_ph = get_font("cinzel", 25)
    draw_wrapped(draw, "Clean, modular, and decoupled architecture. Well-structured and documented code engineered to scale gracefully without technical debt.", 437, 810, 560, f_pb, line_spacing=1.3)
    draw_centered(draw, "— ENGINEERING QUALITY —", 437, 1015, f_ph)
    
    draw_wrapped(draw, "High-impact automations eliminating hours of daily manual toil through resilient n8n pipelines and precise, robust AI agents.", 1085, 810, 560, f_pb, line_spacing=1.3)
    draw_centered(draw, "— OPERATIONAL EFFICIENCY —", 1085, 1015, f_ph)
    
    p3 = "Relational databases designed with mathematical rigor: 4NF normalization, absolute referential integrity, highly optimized indexed queries, and zero data redundancy."
    draw_wrapped(draw, p3, 764, 1325, 1200, f_pb, line_spacing=1.35)
    draw_centered(draw, "— DATA INTEGRITY & PERFORMANCE —", 764, 1520, f_ph)
    
    draw_wrapped(draw, "Direct, transparent, and continuous communication at every project stage. Punctual deliveries strictly aligned with strategic goals.", 437, 1815, 560, f_pb, line_spacing=1.3)
    draw_centered(draw, "— PROFESSIONAL INTEGRITY —", 437, 1965, f_ph)
    
    draw_wrapped(draw, "Adoption of frontier technologies: autonomous agent graphs (LangGraph), MCP protocol servers, RAG, and fine-tuned LLM workflows.", 1085, 1815, 560, f_pb, line_spacing=1.3)
    draw_centered(draw, "— APPLIED AI INNOVATION —", 1085, 1965, f_ph)
    img.save(os.path.join(OUT_PAGES, "freelance-2.jpg"), "JPEG", quality=95)
    print("Generated freelance-2.jpg")

def generate_projects(blank):
    img = Image.open(os.path.join(SRC_PAGES, "projects.jpg")).convert("RGB")
    patch_clean(img, blank, (180, 1100, 1350, 1720), feather=24)
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "CHAPTER IV", 764, 1130, get_font("cinzel", 44))
    draw_centered(draw, "FEATURED PROJECTS", 764, 1220, get_font("cinzel", 58))
    draw_centered(draw, "Engineered with technical rigor and craftsmanship.", 764, 1400, get_font("italic", 32))
    draw_centered(draw, "From autonomous AI agents to enterprise WMS.", 764, 1460, get_font("regular", 30))
    draw_centered(draw, "Explore the open source codebases on GitHub.", 764, 1525, get_font("regular", 30))
    draw_centered(draw, "Modern distributed architectures built to scale.", 764, 1590, get_font("italic", 30))
    img.save(os.path.join(OUT_PAGES, "projects.jpg"), "JPEG", quality=95)
    print("Generated projects.jpg")

def generate_qyou(blank):
    img = Image.open(os.path.join(SRC_PAGES, "qyou.jpg")).convert("RGB")
    patch_clean(img, blank, (200, 140, 1330, 290), feather=24)
    patch_clean(img, blank, (130, 310, 1400, 465), feather=20)
    patch_clean(img, blank, (130, 680, 1400, 1270), feather=22)
    patch_clean(img, blank, (130, 1545, 1400, 1750), feather=20)
    patch_clean(img, blank, (130, 1850, 1400, 1950), feather=20)
    
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "CAMPUSLANDS INTELLIGENT", 764, 150, get_font("cinzel", 52))
    draw_centered(draw, "MULTI-AGENT SYSTEM & COMPUTER VISION", 764, 255, get_font("cinzel", 25))
    desc = "Enterprise predictive analytics and academic monitoring platform engineered for Campuslands. Integrates intelligent agents orchestrated with LangGraph, computer vision with PyTorch for automated attendance, and real-time operational alerts via Telegram bots."
    draw_wrapped(draw, desc, 764, 320, 1260, get_font("regular", 26), line_spacing=1.35)
    
    f_sh = get_font("cinzel", 26)
    f_sb = get_font("regular", 24)
    draw_centered(draw, "1. MULTI-AGENT ORCHESTRATION (LANGGRAPH)", 764, 690, f_sh)
    s1 = "Cyclic state graphs where specialized agents analyze attendance patterns, detect dropout anomalies, and generate automated intervention workflows with full state persistence and observability."
    draw_wrapped(draw, s1, 764, 735, 1240, f_sb, line_spacing=1.3)
    
    draw_centered(draw, "2. COMPUTER VISION & EMBEDDING INFERENCE (PYTORCH)", 764, 890, f_sh)
    s2 = "Neural network inference models in PyTorch for precise biometric attendance recognition, ensuring low-latency processing, robust feature extraction, and verifiable audit records."
    draw_wrapped(draw, s2, 764, 935, 1240, f_sb, line_spacing=1.3)
    
    draw_centered(draw, "3. AUTOMATED ALERT DISPATCH (TELEGRAM BOT)", 764, 1100, f_sh)
    s3 = "Instant notification channel alerting instructors and academic directors of critical student absences and early risk indicators via asynchronous webhook triggers and rich Markdown reports."
    draw_wrapped(draw, s3, 764, 1145, 1240, f_sb, line_spacing=1.3)
    
    badges = [
        ("BACKEND", "Python 3.10+", "FastAPI & SQLAlchemy"),
        ("AI ENGINE", "LangGraph & PyTorch", "OpenAI & Ollama"),
        ("DATABASE", "PostgreSQL", "Docker Containers"),
        ("MESSAGING", "Telegram Bot API", "Async Webhooks")
    ]
    draw_badge_columns(draw, badges, y_header=1560, y_row1=1615, y_row2=1655)
    
    foot = "Engineered under horizontal scalability principles, continuous observability, and modular Docker containerization."
    draw_wrapped(draw, foot, 764, 1870, 1250, get_font("italic", 25), line_spacing=1.35)
    img.save(os.path.join(OUT_PAGES, "qyou.jpg"), "JPEG", quality=95)
    print("Generated qyou.jpg")

def generate_qyou_2(blank):
    img = Image.open(os.path.join(SRC_PAGES, "qyou-2.jpg")).convert("RGB")
    patch_clean(img, blank, (200, 140, 1330, 290), feather=24)
    patch_clean(img, blank, (130, 325, 1400, 1150), feather=22)
    patch_clean(img, blank, (300, 1250, 1230, 1310), feather=16)
    
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "CAMPUSLANDS INTELLIGENT", 764, 150, get_font("cinzel", 52))
    draw_centered(draw, "KEY CAPABILITIES & ECOSYSTEM", 764, 255, get_font("cinzel", 25))
    draw_centered(draw, "KEY CAPABILITIES", 437, 335, get_font("cinzel", 27))
    draw_centered(draw, "ACTIVE ARCHITECTURE", 1085, 335, get_font("cinzel", 27))
    
    rows = [
        ("• Cyclic state graphs with LangGraph", "• Instant alerts via Telegram Bot"),
        ("• Visual inference with neural networks", "• Real-time attendance & retention metrics"),
        ("• Predictive absenteeism anomaly detection", "• Decoupled Docker container microservices"),
        ("• Asynchronous event-driven pipeline", "• Documented RESTful OpenAPI endpoints"),
        ("• Secure JWT authentication & RBAC roles", "• Integrated RAG knowledge base pipeline")
    ]
    y_starts = [450, 590, 730, 870, 1010]
    f_r = get_font("regular", 25)
    for (left_t, right_t), y in zip(rows, y_starts):
        draw_wrapped(draw, left_t, 437, y, 560, f_r, align="left")
        draw_wrapped(draw, right_t, 1085, y, 560, f_r, align="left")
    draw_centered(draw, "ECOSYSTEM TECHNOLOGIES", 764, 1270, get_font("cinzel", 28))
    img.save(os.path.join(OUT_PAGES, "qyou-2.jpg"), "JPEG", quality=95)
    print("Generated qyou-2.jpg")

def generate_iq_tester(blank):
    img = Image.open(os.path.join(SRC_PAGES, "iq-tester.jpg")).convert("RGB")
    patch_clean(img, blank, (200, 140, 1330, 290), feather=24)
    patch_clean(img, blank, (130, 310, 1400, 490), feather=20)
    patch_clean(img, blank, (130, 620, 1400, 1310), feather=22)
    patch_clean(img, blank, (130, 1765, 1400, 1910), feather=20)
    
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "LOGITRACK WMS", 764, 150, get_font("cinzel", 54))
    draw_centered(draw, "ENTERPRISE LOGISTICS & WAREHOUSE MANAGEMENT", 764, 255, get_font("cinzel", 25))
    desc = "Enterprise-grade Warehouse Management System (WMS) designed to deliver 100% real-time operational traceability across multi-warehouse inventory, supplier receptions, inter-facility transfers, lot tracking, picking workflows, and physical stock reconciliations."
    draw_wrapped(draw, desc, 764, 320, 1260, get_font("regular", 26), line_spacing=1.35)
    draw_centered(draw, "— CAPABILITIES & INVENTORY CONTROL —", 764, 635, get_font("cinzel", 28))
    
    f_ch = get_font("cinzel", 25)
    f_cb = get_font("regular", 24)
    draw_centered(draw, "MULTI-WAREHOUSE STOCK & LOT CONTROL", 764, 715, f_ch)
    c1 = "Centralized administration of inventory distributed across multiple physical facilities with strict negative-stock prevention and granular lot traceability."
    draw_wrapped(draw, c1, 764, 760, 1240, f_cb, line_spacing=1.3)
    
    draw_centered(draw, "FULL OPERATIONAL AUDITING & TRACEABILITY", 764, 870, f_ch)
    c2 = "Immutable chronological logging of receptions, dispatches, transfers, and inventory adjustments with operator identification and millisecond timestamps."
    draw_wrapped(draw, c2, 764, 915, 1240, f_cb, line_spacing=1.3)
    
    draw_centered(draw, "PURCHASE ORDER & SUPPLIER RECEPTION WORKFLOW", 764, 1020, f_ch)
    c3 = "Structured receiving pipeline with automated purchase order reconciliation, discrepancy identification, and instant stock ledger synchronization."
    draw_wrapped(draw, c3, 764, 1065, 1240, f_cb, line_spacing=1.3)
    
    draw_centered(draw, "ROLE HIERARCHY & JWT SECURITY (RBAC)", 764, 1170, f_ch)
    c4 = "Granular permission matrix backed by Spring Security and signed JWTs for SuperAdmins, Warehouse Managers, Logistics Operators, and Auditors."
    draw_wrapped(draw, c4, 764, 1215, 1240, f_cb, line_spacing=1.3)
    
    badges = [
        ("BACKEND", "Java 17", "Spring Boot 3.3"),
        ("DATABASE", "PostgreSQL 16", "JPA & Hibernate"),
        ("SECURITY", "Spring Security", "JWT Signed Tokens"),
        ("DEPLOYMENT", "Docker & Nginx", "HTTPS Domain")
    ]
    draw_badge_columns(draw, badges, y_header=1780, y_row1=1830, y_row2=1865)
    img.save(os.path.join(OUT_PAGES, "iq-tester.jpg"), "JPEG", quality=95)
    print("Generated iq-tester.jpg")

def generate_betting_tarot(blank):
    img = Image.open(os.path.join(SRC_PAGES, "betting-tarot.jpg")).convert("RGB")
    patch_clean(img, blank, (200, 140, 1330, 290), feather=24)
    patch_clean(img, blank, (130, 310, 1400, 460), feather=20)
    patch_clean(img, blank, (130, 675, 1400, 1400), feather=22)
    patch_clean(img, blank, (130, 1665, 1400, 1765), feather=20)
    patch_clean(img, blank, (130, 1860, 1400, 2030), feather=20)
    
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "N8N ATTENDANCE AI", 764, 150, get_font("cinzel", 54))
    draw_centered(draw, "AUTOMATION & LLM CLASSIFICATION", 764, 255, get_font("cinzel", 25))
    desc = "End-to-end automated pipeline for the ingestion, intelligent evaluation, and classification of absence justification requests in academic and corporate environments, eliminating manual review and providing instant auditability."
    draw_wrapped(draw, desc, 764, 320, 1260, get_font("regular", 26), line_spacing=1.35)
    
    f_sh = get_font("cinzel", 25)
    f_sb = get_font("regular", 24)
    steps = [
        ("1. WEB INGESTION & DATA CAPTURE", "Responsive web form for structured receipt of student absence requests with medical and official supporting attachments.", 690),
        ("2. NORMALIZATION & VALIDATION IN N8N", "Orchestration workflow in n8n sanitizing inputs, validating schema constraints, and preparing structured inference payloads.", 835),
        ("3. INTELLIGENT EVALUATION VIA LLM", "Prompt-engineered connection with OpenRouter LLMs categorizing justifications into: Valid, Invalid, or Pending Human Review.", 985),
        ("4. REAL-TIME GOOGLE SHEETS SYNC", "Instant synchronization with the master absence ledger recording timestamps, AI confidence verdict, and summarized rationale.", 1130),
        ("5. INSTANT TELEGRAM BOT NOTIFICATIONS", "Real-time dispatch notifying students of their resolution and delivering consolidated digest reports to academic coordinators.", 1275)
    ]
    for h_txt, b_txt, y in steps:
        draw_centered(draw, h_txt, 764, y, f_sh)
        draw_wrapped(draw, b_txt, 764, y + 42, 1240, f_sb, line_spacing=1.3)
        
    high = "Reduces administrative operational toil by over 90%, delivering instant responses within seconds with full evidentiary audit backing."
    draw_wrapped(draw, high, 764, 1685, 1250, get_font("italic", 25), line_spacing=1.35)
    
    badges = [
        ("ORCHESTRATOR", "n8n Automation Engine", "Webhooks & Cron Triggers"),
        ("AI ENGINE", "OpenRouter API", "Specialized LLM Models"),
        ("STORAGE", "Google Sheets API", "Google Drive Storage"),
        ("MESSAGING", "Telegram Bot API", "Instant Push Alerts")
    ]
    draw_badge_columns(draw, badges, y_header=1875, y_row1=1920, y_row2=1960)
    img.save(os.path.join(OUT_PAGES, "betting-tarot.jpg"), "JPEG", quality=95)
    print("Generated betting-tarot.jpg")

def generate_autoposter(blank):
    img = Image.open(os.path.join(SRC_PAGES, "autoposter.jpg")).convert("RGB")
    patch_clean(img, blank, (200, 140, 1330, 290), feather=24)
    patch_clean(img, blank, (130, 310, 1400, 460), feather=20)
    patch_clean(img, blank, (130, 670, 1400, 860), feather=22)
    patch_clean(img, blank, (130, 1070, 1400, 1220), feather=22)
    patch_clean(img, blank, (300, 1445, 1230, 1495), feather=16)
    patch_clean(img, blank, (130, 1535, 1400, 1680), feather=20)
    patch_clean(img, blank, (130, 1820, 1400, 1920), feather=20)
    
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "GITHUB MCP SERVER", 764, 150, get_font("cinzel", 54))
    draw_centered(draw, "MODEL CONTEXT PROTOCOL FOR AI AGENTS", 764, 255, get_font("cinzel", 25))
    desc = "Production server implementing the open Model Context Protocol (MCP) standard in Node.js, enabling autonomous AI agents (Groq / LLaMA 3.3) to interact seamlessly and securely with the GitHub REST API."
    draw_wrapped(draw, desc, 764, 320, 1260, get_font("regular", 26), line_spacing=1.35)
    
    f_b = get_font("regular", 25)
    p1 = "Provides a standardized bidirectional bridge between frontier language models and source code repositories, allowing autonomous agents to inspect branches, commit code, open pull requests, and audit issues unattended."
    draw_wrapped(draw, p1, 764, 690, 1240, f_b, line_spacing=1.35)
    
    p2 = "Enforces strict validation via JSON Schema, robust error recovery, and granular authentication with GitHub Personal Access Tokens (PAT), securing mission-critical development operations throughout the lifecycle."
    draw_wrapped(draw, p2, 764, 1090, 1240, f_b, line_spacing=1.35)
    draw_centered(draw, "CAPABILITIES & PROTOCOL", 764, 1455, get_font("cinzel", 28))
    
    badges = [
        ("MCP STANDARD", "Model Context Protocol", "Anthropic Specification"),
        ("RUNTIME", "Node.js v18+", "ES Modules & TypeScript"),
        ("AI MODELS", "Groq Cloud API", "LLaMA 3.3 70B Versatile"),
        ("INTEGRATION", "GitHub REST API", "Octokit & Webhooks")
    ]
    draw_badge_columns(draw, badges, y_header=1545, y_row1=1595, y_row2=1635)
    
    foot = "Enables autonomous workflows where AI agents function as junior engineers, auditing codebases, identifying bugs, and submitting pull requests directly on GitHub."
    draw_wrapped(draw, foot, 764, 1835, 1250, get_font("italic", 25), line_spacing=1.35)
    img.save(os.path.join(OUT_PAGES, "autoposter.jpg"), "JPEG", quality=95)
    print("Generated autoposter.jpg")

def generate_autoposter_2(blank):
    img = Image.open(os.path.join(SRC_PAGES, "autoposter-2.jpg")).convert("RGB")
    patch_clean(img, blank, (200, 140, 1330, 290), feather=24)
    step_y_ranges = [
        (350, 400), (505, 555), (660, 715), (815, 870), (970, 1025),
        (1125, 1180), (1280, 1335), (1440, 1495), (1595, 1650), (1750, 1805)
    ]
    for sy1, sy2 in step_y_ranges:
        patch_clean(img, blank, (300, sy1, 1230, sy2), feather=12)
        
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "GITHUB MCP SERVER", 764, 150, get_font("cinzel", 54))
    draw_centered(draw, "PROTOCOL EXECUTION PIPELINE", 764, 255, get_font("cinzel", 25))
    
    f_step = get_font("regular", 25)
    steps = [
        ("Natural language user prompt ingestion", 365),
        ("MCP server tool discovery and resolution", 520),
        ("JSON Schema validation of call arguments", 675),
        ("Secure PAT authentication to GitHub API", 830),
        ("Git tree inspection and branch metadata lookup", 985),
        ("Source code extraction and PR diff parsing", 1140),
        ("Automated commit generation & issue commentary", 1295),
        ("HTTP response sanitization and formatting", 1455),
        ("Context injection back to LLaMA 3.3 model", 1610),
        ("Final operation telemetry & execution logging", 1765)
    ]
    for txt, y in steps:
        draw_centered(draw, txt, 764, y, f_step)
    img.save(os.path.join(OUT_PAGES, "autoposter-2.jpg"), "JPEG", quality=95)
    print("Generated autoposter-2.jpg")

def generate_export_robot(blank):
    img = Image.open(os.path.join(SRC_PAGES, "export-robot.jpg")).convert("RGB")
    patch_clean(img, blank, (200, 140, 1330, 290), feather=24)
    patch_clean(img, blank, (130, 310, 1400, 460), feather=20)
    patch_clean(img, blank, (130, 615, 1400, 1280), feather=22)
    patch_clean(img, blank, (130, 1640, 1400, 1800), feather=20)
    patch_clean(img, blank, (130, 1875, 1400, 1970), feather=20)
    
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "HELPDESK AI", 764, 150, get_font("cinzel", 54))
    draw_centered(draw, "AI-ASSISTED SUPPORT & RAG KNOWLEDGE BASE", 764, 255, get_font("cinzel", 25))
    desc = "Intelligent help desk and ticket resolution platform powered by Retrieval-Augmented Generation (RAG). Queries company knowledge bases to generate context-accurate technical answers, slashing first-response times."
    draw_wrapped(draw, desc, 764, 320, 1260, get_font("regular", 26), line_spacing=1.35)
    
    f_sh = get_font("cinzel", 25)
    f_sb = get_font("regular", 24)
    sections = [
        ("1. RAG PIPELINE & KNOWLEDGE BASE RETRIEVAL", "Vector indexing of technical documentation, FAQs, and prior ticket resolutions providing grounded context to language models.", 630),
        ("2. AUTOMATED TICKET TRIAGE & ROUTING", "Intelligent classification of incident severity, urgency, and technical domain for automated routing to specialized engineers.", 780),
        ("3. REAL-TIME COPILOT SUGGESTIONS", "Context-aware response drafts generated in real time for support engineers to inspect, refine, and dispatch in a single click.", 930),
        ("4. SLA MONITORING & SATISFACTION METRICS", "Continuous tracking of resolution latency, SLA compliance thresholds, and user satisfaction ratings across all departments.", 1080)
    ]
    for h_txt, b_txt, y in sections:
        draw_centered(draw, h_txt, 764, y, f_sh)
        draw_wrapped(draw, b_txt, 764, y + 42, 1240, f_sb, line_spacing=1.3)
        
    badges = [
        ("FRONTEND", "HTML5 & CSS3", "Vanilla JavaScript"),
        ("AI ENGINE", "OpenAI GPT-4", "OpenRouter RAG"),
        ("AUTOMATION", "n8n Workflows", "Webhook APIs"),
        ("DATABASE", "PostgreSQL", "Full Audit Logging")
    ]
    draw_badge_columns(draw, badges, y_header=1665, y_row1=1710, y_row2=1748)
    
    foot = "Enhances technical support by merging proprietary corporate knowledge with the velocity of modern generative AI."
    draw_wrapped(draw, foot, 764, 1890, 1250, get_font("italic", 25), line_spacing=1.35)
    img.save(os.path.join(OUT_PAGES, "export-robot.jpg"), "JPEG", quality=95)
    print("Generated export-robot.jpg")

def generate_six_dot_bot(blank):
    img = Image.open(os.path.join(SRC_PAGES, "six-dot-bot.jpg")).convert("RGB")
    patch_clean(img, blank, (200, 140, 1330, 290), feather=24)
    patch_clean(img, blank, (130, 310, 1400, 460), feather=20)
    patch_clean(img, blank, (130, 590, 1400, 1230), feather=22)
    patch_clean(img, blank, (130, 1620, 1400, 1770), feather=20)
    patch_clean(img, blank, (130, 1855, 1400, 1955), feather=20)
    
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "ECOMMERCE DATABASE 4NF", 764, 150, get_font("cinzel", 54))
    draw_centered(draw, "RIGOROUS RELATIONAL DESIGN & FOURTH NORMAL FORM", 764, 255, get_font("cinzel", 25))
    desc = "High-performance relational database architecture engineered under strict fourth normal form (4NF) normalization principles. Eliminates multivalued dependencies and data anomalies, guaranteeing absolute referential integrity for high-volume e-commerce platforms."
    draw_wrapped(draw, desc, 764, 320, 1260, get_font("regular", 26), line_spacing=1.35)
    draw_centered(draw, "— RELATIONAL RIGOR & ACID ARCHITECTURE —", 764, 600, get_font("cinzel", 28))
    
    f_ch = get_font("cinzel", 25)
    f_cb = get_font("regular", 24)
    sections = [
        ("STRICT FOURTH NORMAL FORM (4NF)", "Mathematical decomposition of complex relations to isolate independent multivalued dependencies, guaranteeing zero redundancy.", 680),
        ("DATABASE TRIGGERS & BUSINESS INTEGRITY", "Automated triggers for price audit histories, atomic stock ledger updates, and strict transactional constraint validation.", 825),
        ("STORED PROCEDURES & ACID TRANSACTIONS", "Critical checkout, inventory deduction, and billing logic encapsulated in stored procedures with strict ACID isolation.", 970),
        ("RFM CUSTOMER SEGMENTATION & ANALYTICS", "Advanced analytical queries for Recency, Frequency, Monetary (RFM) customer cohort segmentation driving data-informed decisions.", 1115)
    ]
    for h_txt, b_txt, y in sections:
        draw_centered(draw, h_txt, 764, y, f_ch)
        draw_wrapped(draw, b_txt, 764, y + 40, 1240, f_cb, line_spacing=1.3)
        
    badges = [
        ("DB ENGINE", "MySQL 8.0+", "InnoDB Engine"),
        ("DESIGN", "Fourth Normal Form", "Zero Redundancy (4NF)"),
        ("AUTOMATION", "Triggers & Views", "Stored Procedures"),
        ("ANALYTICS", "RFM Analytics", "Executive Reports")
    ]
    draw_badge_columns(draw, badges, y_header=1635, y_row1=1680, y_row2=1720)
    
    foot = "An enterprise-grade data architecture proving that rigorous normalization is the indispensable cornerstone of scalable commerce platforms."
    draw_wrapped(draw, foot, 764, 1870, 1250, get_font("italic", 25), line_spacing=1.35)
    img.save(os.path.join(OUT_PAGES, "six-dot-bot.jpg"), "JPEG", quality=95)
    print("Generated six-dot-bot.jpg")

def generate_autoreply(blank):
    img = Image.open(os.path.join(SRC_PAGES, "autoreply.jpg")).convert("RGB")
    patch_clean(img, blank, (200, 140, 1330, 290), feather=24)
    patch_clean(img, blank, (130, 310, 1400, 460), feather=20)
    patch_clean(img, blank, (130, 605, 1400, 1410), feather=22)
    patch_clean(img, blank, (130, 1680, 1400, 1835), feather=20)
    patch_clean(img, blank, (130, 1915, 1400, 2015), feather=20)
    
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "SOFTSKILLS QUEST", 764, 150, get_font("cinzel", 54))
    draw_centered(draw, "GAMIFIED DEVELOPER LEARNING PLATFORM", 764, 255, get_font("cinzel", 25))
    desc = "Interactive 2D gamified learning platform engineered in pure JavaScript with HTML5 Canvas and Web Audio API. Its objective is to reflect on and cultivate 5 essential soft skills for software engineers through playable metaphor levels and 30 structured engineering insights."
    draw_wrapped(draw, desc, 764, 320, 1260, get_font("regular", 26), line_spacing=1.35)
    draw_centered(draw, "— 5 ENGINEERING TRAINING LEVELS —", 764, 620, get_font("cinzel", 28))
    
    f_sh = get_font("cinzel", 24)
    f_sb = get_font("regular", 23)
    levels = [
        ("1. SELF-DISCIPLINE - CI/CD GATES & ROUTINES:", "Platformer mechanics where the player must clear strict linter checks, unit tests, and build gates before advancing.", 695),
        ("2. PERSEVERANCE - REFACTORING THE MONOLITH:", "Precision spatial puzzle with immediate respawn to foster grit, refactoring complex legacy monolith obstacles with patience.", 840),
        ("3. ASSERTIVENESS - THE CODE REVIEW TRIAL:", "Branching interactive dialogues with simulated teammates (Product Owner, Senior Dev, QA) navigating constructive, assertive code reviews.", 985),
        ("4. CREATIVITY - THINKING OUTSIDE THE SANDBOX:", "Overcoming physics puzzles through creative problem-solving, generating dynamic code bridges and algorithmic shortcuts in real time.", 1130),
        ("5. STRATEGIC PLANNING - BLUEPRINT ARCHITECTURE:", "Architectural blueprint mode allowing strategic level inspection and resource planning before initiating any movement.", 1275)
    ]
    for h_txt, b_txt, y in levels:
        draw_centered(draw, h_txt, 764, y, f_sh)
        draw_wrapped(draw, b_txt, 764, y + 38, 1240, f_sb, line_spacing=1.3)
        
    badges = [
        ("CANVAS 2D", "HTML5 Graphics Engine", "Fluid 60 FPS Render"),
        ("CORE LOGIC", "JavaScript ES Modules", "Zero Dependencies"),
        ("DYNAMIC AUDIO", "Web Audio API", "Procedural Synth"),
        ("PEDAGOGY", "Active Gamification", "Professional Growth")
    ]
    draw_badge_columns(draw, badges, y_header=1700, y_row1=1748, y_row2=1788)
    
    foot = "Demonstrates that technical prowess and human soft skills are twin pillars in forging well-rounded software engineers."
    draw_wrapped(draw, foot, 764, 1930, 1250, get_font("italic", 25), line_spacing=1.35)
    img.save(os.path.join(OUT_PAGES, "autoreply.jpg"), "JPEG", quality=95)
    print("Generated autoreply.jpg")

def generate_time_recorder(blank):
    img = Image.open(os.path.join(SRC_PAGES, "time-recorder.jpg")).convert("RGB")
    patch_clean(img, blank, (200, 140, 1330, 290), feather=24)
    patch_clean(img, blank, (130, 310, 1400, 460), feather=20)
    patch_clean(img, blank, (130, 605, 1400, 1285), feather=22)
    # Patch clean ENTIRE badge block including sub-labels
    patch_clean(img, blank, (130, 1640, 1400, 1800), feather=20)
    patch_clean(img, blank, (130, 1875, 1400, 1975), feather=20)
    
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "LMS ABC PLATFORM", 764, 150, get_font("cinzel", 54))
    draw_centered(draw, "MODULAR LEARNING MANAGEMENT SYSTEM", 764, 255, get_font("cinzel", 25))
    desc = "Modular Learning Management System (LMS) engineered for the efficient administration of educational curricula. Built with a lightweight decoupled architecture in Vanilla JavaScript and CSS3, free of heavy external dependencies or frameworks."
    draw_wrapped(draw, desc, 764, 320, 1260, get_font("regular", 26), line_spacing=1.35)
    draw_centered(draw, "— EDUCATIONAL PLATFORM MODULES —", 764, 620, get_font("cinzel", 28))
    
    f_ch = get_font("cinzel", 25)
    f_cb = get_font("regular", 24)
    modules = [
        ("PUBLIC COURSE EXPLORATION PORTAL:", "Open course catalog where visitors can search disciplines, inspect comprehensive syllabi, and view instructor profiles.", 695),
        ("FACULTY & CURRICULUM MANAGEMENT:", "Comprehensive instructor dashboard to create, update, and sequence courses, modular units, and rich multimedia lessons.", 845),
        ("STUDENT ENROLLMENT & GRADEBOOK:", "Administrative module handling course registrations, gradebook entries, and visual progress tracking for individual students.", 995),
        ("CLIENT-SIDE STATE & DATA PERSISTENCE:", "Robust state management backed by structured LocalStorage schemas, delivering instant response times at zero server overhead.", 1145)
    ]
    for h_txt, b_txt, y in modules:
        draw_centered(draw, h_txt, 764, y, f_ch)
        draw_wrapped(draw, b_txt, 764, y + 40, 1240, f_cb, line_spacing=1.3)
        
    badges = [
        ("STRUCTURE", "Semantic HTML5", "Web Accessibility"),
        ("STYLING", "Modern CSS3", "Responsive Design"),
        ("LOGIC", "JavaScript ES6+", "Decoupled Modules"),
        ("STORAGE", "LocalStorage API", "Data Persistence")
    ]
    draw_badge_columns(draw, badges, y_header=1665, y_row1=1710, y_row2=1748)
    
    foot = "Tangible proof of deep mastery over core web fundamentals (HTML, CSS, Vanilla JS), delivering a complete tool without tech bloat."
    draw_wrapped(draw, foot, 764, 1890, 1250, get_font("italic", 25), line_spacing=1.35)
    img.save(os.path.join(OUT_PAGES, "time-recorder.jpg"), "JPEG", quality=95)
    print("Generated time-recorder.jpg")

def generate_fifteen_js(blank):
    img = Image.open(os.path.join(SRC_PAGES, "fifteen-js.jpg")).convert("RGB")
    patch_clean(img, blank, (200, 140, 1330, 290), feather=24)
    patch_clean(img, blank, (130, 310, 1400, 460), feather=20)
    patch_clean(img, blank, (130, 605, 1400, 1285), feather=22)
    patch_clean(img, blank, (130, 1640, 1400, 1800), feather=20)
    patch_clean(img, blank, (130, 1875, 1400, 1945), feather=20)
    
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "INTERACTIVE 3D CODEX", 764, 150, get_font("cinzel", 54))
    draw_centered(draw, "THREE.JS ENGINE, SHADERS & MATHEMATICS", 764, 255, get_font("cinzel", 25))
    desc = "The engineering behind this very 3D interactive portfolio: a web experience built with Three.js, TypeScript, and procedural curvature algorithms that simulate with physical fidelity the bending of a classic bound manuscript."
    draw_wrapped(draw, desc, 764, 320, 1260, get_font("regular", 26), line_spacing=1.35)
    draw_centered(draw, "— GRAPHIC ENGINEERING PRINCIPLES —", 764, 620, get_font("cinzel", 28))
    
    f_ch = get_font("cinzel", 25)
    f_cb = get_font("regular", 24)
    pillars = [
        ("PROCEDURAL GEOMETRIC CURVATURE:", "Real-time parametric mesh deformation using mathematical splines, recreating the organic physical curvature of turning pages.", 695),
        ("PBR MATERIALS & PARCHMENT SHADERS:", "Physically Based Rendering (PBR) with diffuse lighting, roughness maps, and PCF Soft Shadows recreating authentic aged parchment.", 845),
        ("SPATIAL INTERACTION VIA RAYCASTING:", "Projection of pointer coordinates and touch gestures onto 3D page surfaces via raycasting, driving page flips and active hotspots.", 995),
        ("PROCEDURAL AUDIO & SOUND MODULATION:", "Real-time procedural audio synthesis modulating page-flip sound effects, synchronizing volume and pitch with flip velocity.", 1145)
    ]
    for h_txt, b_txt, y in pillars:
        draw_centered(draw, h_txt, 764, y, f_ch)
        draw_wrapped(draw, b_txt, 764, y + 40, 1240, f_cb, line_spacing=1.3)
        
    badges = [
        ("RENDERER", "Three.js & WebGL", "Custom Shaders"),
        ("LANGUAGE", "Strict TypeScript", "OOP Architecture"),
        ("ANIMATION", "GSAP & Tweens", "Organic Physics"),
        ("OPTIMIZATION", "Vite Bundler", "VRAM Caching")
    ]
    draw_badge_columns(draw, badges, y_header=1665, y_row1=1710, y_row2=1748)
    
    foot = "A seamless synthesis between Renaissance editorial artistry and the cutting-edge capabilities of browser graphics."
    draw_wrapped(draw, foot, 764, 1890, 1250, get_font("italic", 25), line_spacing=1.35)
    img.save(os.path.join(OUT_PAGES, "fifteen-js.jpg"), "JPEG", quality=95)
    print("Generated fifteen-js.jpg")

def generate_the_book(blank):
    img = Image.open(os.path.join(SRC_PAGES, "the-book.jpg")).convert("RGB")
    patch_clean(img, blank, (200, 140, 1330, 290), feather=24)
    patch_clean(img, blank, (130, 310, 1400, 420), feather=20)
    patch_clean(img, blank, (130, 580, 1400, 785), feather=22)
    patch_clean(img, blank, (130, 1470, 1400, 1760), feather=22)
    patch_clean(img, blank, (130, 1890, 1400, 1995), feather=20)
    
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "THE CODEX", 764, 150, get_font("cinzel", 54))
    draw_centered(draw, "ARCHITECTURE & COLOPHON", 764, 255, get_font("cinzel", 25))
    desc = "The Codex of Tomás Esteban González Quintero is an interactive 3D web experience designed to showcase my engineering career, featured systems, technical skills, and software architecture vision."
    draw_wrapped(draw, desc, 764, 320, 1260, get_font("regular", 26), line_spacing=1.35)
    
    draw_centered(draw, "— TECHNICAL SPECIFICATIONS —", 764, 595, get_font("cinzel", 28))
    f_b = get_font("regular", 25)
    specs = (
        "• High-fidelity Three.js rendering at 60 FPS with antialiasing and PCF soft shadow maps.\n"
        "• Responsive multi-device support with touch swipe gestures, keyboard arrows, and orientation adaptivity.\n"
        "• Sub-2-second load times via modern Vite bundling, WebP asset compression, and GPU VRAM precompilation."
    )
    draw_wrapped(draw, specs, 764, 650, 1240, f_b, line_spacing=1.45, align="left")
    
    draw_centered(draw, "— CREDITS & AUTHORSHIP —", 764, 1490, get_font("cinzel", 28))
    credits = (
        "Engineered and customized by Tomás Esteban González Quintero.\n"
        "Full Stack Developer • Software Architect.\n"
        "Bucaramanga, Santander, Colombia • 2026.\n"
        "Inspired by classical codex bookbinding and interactive graphics mathematics."
    )
    draw_wrapped(draw, credits, 764, 1555, 1240, f_b, line_spacing=1.45, align="center")
    
    foot = "Visit the GitHub repositories to inspect source codebases, architecture diagrams, and technical documentation for each system."
    draw_wrapped(draw, foot, 764, 1910, 1250, get_font("italic", 25), line_spacing=1.35)
    img.save(os.path.join(OUT_PAGES, "the-book.jpg"), "JPEG", quality=95)
    print("Generated the-book.jpg")

def generate_cover_back():
    img = Image.open(os.path.join(SRC_PAGES, "cover-back.jpg")).convert("RGB")
    patch_clean_leather(img, (500, 540, 1050, 660), (500, 720, 1050, 840), feather=25)
    patch_clean_leather(img, (220, 980, 1320, 1590), (250, 700, 1280, 950), feather=25)
    
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "TEGQ ARCHIVES", 772, 575, get_font("cinzel", 50), fill=COLOR_GOLD)
    draw_centered(draw, "Thank you for reviewing my codex!", 772, 1020, get_font("italic", 38), fill=COLOR_GOLD_BRIGHT)
    draw_centered(draw, "I hope you enjoyed exploring this experience as much as I enjoyed building it.", 772, 1140, get_font("italic", 27), fill=COLOR_GOLD_BRIGHT)
    draw_centered(draw, "TOMÁS ESTEBAN GONZÁLEZ QUINTERO", 772, 1315, get_font("cinzel", 34), fill=COLOR_GOLD)
    draw_centered(draw, "Full Stack Developer • AI Solutions • Software Architect", 772, 1375, get_font("regular", 26), fill=COLOR_GOLD_BRIGHT)
    draw_centered(draw, "WhatsApp: +57 316 775 5887", 772, 1435, get_font("regular", 25), fill=COLOR_GOLD_BRIGHT)
    draw_centered(draw, "tomasestebangonzalezquintero@gmail.com", 772, 1485, get_font("regular", 25), fill=COLOR_GOLD_BRIGHT)
    draw_centered(draw, "github.com/TEstebanGQ • Bucaramanga, Colombia", 772, 1535, get_font("regular", 25), fill=COLOR_GOLD_BRIGHT)
    img.save(os.path.join(OUT_PAGES, "cover-back.jpg"), "JPEG", quality=95)
    print("Generated cover-back.jpg")

def copy_static_assets():
    assets = [
        "blank.jpg", "cover-edge-lr.jpg", "cover-edge-tb.jpg",
        "spine.jpg", "spine-edge-tb.jpg"
    ]
    for a in assets:
        src = os.path.join(SRC_PAGES, a)
        dst = os.path.join(OUT_PAGES, a)
        shutil.copy2(src, dst)
        print(f"Copied static asset: {a}")
        
    cf_src = os.path.join(SRC_PAGES, "cover-front.jpg")
    cf_dst = os.path.join(OUT_PAGES, "cover-front.jpg")
    if not os.path.exists(cf_dst):
        shutil.copy2(cf_src, cf_dst)

def main():
    os.makedirs(OUT_PAGES, exist_ok=True)
    blank = Image.open(BLANK_PATH).convert("RGB")
    
    print("=== STARTING REFINED FULL ENGLISH PAGE GENERATION ===")
    copy_static_assets()
    generate_welcome(blank)
    generate_about(blank)
    generate_who_am_i(blank)
    generate_my_story(blank)
    generate_skills(blank)
    generate_interests(blank)
    generate_journey(blank)
    generate_map_1(blank)
    generate_map_2(blank)
    generate_career(blank)
    generate_thor_systems(blank)
    generate_thor_systems_2(blank)
    generate_freelance(blank)
    generate_freelance_2(blank)
    generate_projects(blank)
    generate_qyou(blank)
    generate_qyou_2(blank)
    generate_iq_tester(blank)
    generate_betting_tarot(blank)
    generate_autoposter(blank)
    generate_autoposter_2(blank)
    generate_export_robot(blank)
    generate_six_dot_bot(blank)
    generate_autoreply(blank)
    generate_time_recorder(blank)
    generate_fifteen_js(blank)
    generate_the_book(blank)
    generate_cover_back()
    print("=== ALL ENGLISH PAGES SUCCESSFULLY GENERATED ===")

if __name__ == "__main__":
    main()
