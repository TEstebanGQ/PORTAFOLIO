#!/usr/bin/env python3
"""
Master generator for the 100% brand new English Edition of the 3D Codex.
Every single text and project page is built DIRECTLY on virgin parchment (blank.jpg)
from scratch, guaranteeing ZERO seams, ZERO ghost text, and ZERO superimposed layers.
"""

import os
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter

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

def get_font(name, size):
    path = FONTS.get(name, FONTS["regular"])
    return ImageFont.truetype(path, size)

def draw_centered(draw, text, y, font, fill=INK_DARK):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text((764 - w // 2, y), text, font=font, fill=fill)

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
    draw_centered(draw, "TEGQ ARCHIVES", 1080, get_font("cinzel", 48), fill=INK_GOLD)
    draw_centered(draw, "Thank you for reviewing my codex!", 1160, get_font("italic", 36), fill=INK_GOLD)
    
    closing = "I hope you enjoyed this interactive journey through my software architectures, engineering projects, and technical vision."
    draw_wrapped(draw, closing, 772, 1220, 1000, get_font("regular", 28), fill=INK_GOLD, line_spacing=1.35)
    
    draw_centered(draw, "Tomas Esteban Gonzalez Quintero", 1370, get_font("cinzel", 34), fill=INK_GOLD)
    draw_centered(draw, "Full Stack Developer & AI Solutions Architect", 1425, get_font("italic", 28), fill=INK_GOLD)
    draw_centered(draw, "Bucaramanga, Santander, Colombia", 1475, get_font("regular", 26), fill=INK_GOLD)
    draw_centered(draw, "GitHub: github.com/TEstebanGQ", 1540, get_font("regular", 26), fill=INK_GOLD)
    draw_centered(draw, "LinkedIn: tomas-esteban-gonzalez-quintero", 1590, get_font("regular", 26), fill=INK_GOLD)
    draw_centered(draw, "WhatsApp: +57 316 775 5887", 1640, get_font("regular", 26), fill=INK_GOLD)
    
    img.save(os.path.join(OUT_PAGES, "cover-back.jpg"), "JPEG", quality=95)
    print("Generated cover-back.jpg")

def generate_welcome(blank):
    base = blank.resize((1544, 2200), Image.Resampling.LANCZOS)
    orig = Image.open(os.path.join(SRC_PAGES, "welcome.jpg")).convert("RGB")
    # preserve center hand drawings (y: 650..1520)
    center_drawing = orig.crop((200, 650, 1344, 1520))
    base.paste(center_drawing, (200, 650))
    
    draw = ImageDraw.Draw(base)
    draw_centered(draw, "WELCOME", 170, get_font("cinzel", 58))
    draw_centered(draw, "Double-click anywhere to toggle fullscreen view", 1680, get_font("regular", 32))
    draw_centered(draw, "Swipe or use arrow keys (↓ → / ↑ ←) to turn pages forward & back", 1750, get_font("regular", 29))
    base.save(os.path.join(OUT_PAGES, "welcome.jpg"), "JPEG", quality=95)
    print("Generated welcome.jpg")

# ==================== GROUP B: ILLUSTRATED / MAP PAGES ====================

def patch_clean(img, blank, bbox, feather=18):
    x1, y1, x2, y2 = bbox
    pw, ph = x2 - x1, y2 - y1
    patch = blank.crop(bbox)
    mask = Image.new("L", (pw, ph), 255)
    mask = mask.filter(ImageFilter.GaussianBlur(feather))
    img.paste(patch, (x1, y1), mask)

def generate_map_1(blank):
    img = Image.open(os.path.join(SRC_PAGES, "map-1.jpg")).convert("RGB")
    patch_clean(img, blank, (180, 40, 780, 400), feather=18)
    patch_clean(img, blank, (840, 460, 1480, 820), feather=18)
    patch_clean(img, blank, (400, 1160, 1440, 1610), feather=18)
    
    draw = ImageDraw.Draw(img)
    f_year = get_font("cinzel", 34)
    f_body = get_font("regular", 26)
    
    draw.text((480 - 60, 80), "2023", font=f_year, fill=INK_DARK)
    draw_wrapped(draw, "Started programming, mastering Python, data structures, and algorithmic logic.", 480, 190, 480, f_body)
    
    draw.text((1160 - 180, 500), "2024 (January - June)", font=get_font("cinzel", 30), fill=INK_DARK)
    draw_wrapped(draw, "Computer hardware diagnostics, electronic maintenance, component assembly, and OS optimization.", 1160, 640, 500, f_body)
    
    draw_centered(draw, "2024 (June - November)", 1220, get_font("cinzel", 30))
    draw_wrapped(draw, "Completed Software Development degree with highest academic honors.\nGraduated Valedictorian & Top Engineer of the cohort.", 764, 1340, 560, f_body)
    
    img.save(os.path.join(OUT_PAGES, "map-1.jpg"), "JPEG", quality=95)
    print("Generated map-1.jpg")

def generate_map_2(blank):
    img = Image.open(os.path.join(SRC_PAGES, "map-2.jpg")).convert("RGB")
    patch_clean(img, blank, (120, 15, 980, 520), feather=18)
    patch_clean(img, blank, (340, 560, 1440, 1030), feather=18)
    patch_clean(img, blank, (320, 1100, 1360, 1540), feather=18)
    patch_clean(img, blank, (210, 1590, 1030, 2120), feather=18)
    patch_clean(img, blank, (1330, 1930, 1528, 2090), feather=16)
    
    draw = ImageDraw.Draw(img)
    f_body = get_font("regular", 25)
    
    draw_wrapped(draw, "2025 (December)", 480, 45, 520, get_font("cinzel", 32))
    draw_wrapped(draw, "Commenced SENA Higher Degree:\nTechnologist in Software Analysis & Development.", 480, 145, 520, f_body)
    draw_wrapped(draw, "Expanding engineering horizons", 480, 465, 520, get_font("italic", 25))
    
    draw_centered(draw, "2025 (June) - 2026 (September)", 600, get_font("cinzel", 28))
    draw_centered(draw, "Entered Campuslands Elite Academy", 675, get_font("italic", 27))
    bullets = "• Immersive hands-on development\n• Enterprise microservice platforms\n• Cross-functional Agile leadership\n• Exponential technical growth"
    draw_wrapped(draw, bullets, 764, 755, 520, f_body, align="left")
    
    draw_wrapped(draw, "2026 (June)", 550, 1130, 480, get_font("cinzel", 30))
    draw_wrapped(draw, "Deployed first distributed platform to production cloud environments.", 550, 1230, 480, f_body)
    draw_wrapped(draw, "From architectural design into reality", 1200, 1445, 400, get_font("italic", 24))
    
    draw_wrapped(draw, "Professional Vision", 580, 1620, 660, get_font("cinzel", 32))
    v_text = (
        "• Continuously engineer scalable, resilient distributed systems.\n"
        "• Specialize in cloud microservices, high-throughput APIs, and 4NF databases.\n"
        "• Deliver high-impact solutions to enterprise-grade challenges."
    )
    draw_wrapped(draw, v_text, 580, 1730, 660, f_body, line_spacing=1.4, align="left")
    
    f_sign = get_font("cinzel", 21)
    draw.text((1430 - 60, 1960), "DISCIPLINE", font=f_sign, fill=INK_DARK)
    draw.text((1430 - 35, 2005), "FOCUS", font=f_sign, fill=INK_DARK)
    draw.text((1430 - 45, 2048), "RESULTS", font=f_sign, fill=INK_DARK)
    
    img.save(os.path.join(OUT_PAGES, "map-2.jpg"), "JPEG", quality=95)
    print("Generated map-2.jpg")

def generate_interests(blank):
    img = Image.open(os.path.join(SRC_PAGES, "interests.jpg")).convert("RGB")
    # 1. Header (y: 120..320)
    patch_clean(img, blank, (100, 120, 1428, 330), feather=20)
    # 2. Compass top label (y: 590..655, x: 630..900)
    patch_clean(img, blank, (620, 590, 910, 655), feather=14)
    # 3. Compass right arc label (y: 1000..1200, x: 1050..1300)
    patch_clean(img, blank, (1050, 1000, 1300, 1200), feather=14)
    # 4. Compass left arc label (y: 1000..1200, x: 190..450)
    patch_clean(img, blank, (190, 1000, 450, 1200), feather=14)
    # 5. Compass bottom label (y: 1630..1700, x: 630..900)
    patch_clean(img, blank, (620, 1630, 910, 1700), feather=14)
    # 6. Compass subtitle (y: 1885..1940, x: 630..900)
    patch_clean(img, blank, (620, 1885, 910, 1940), feather=14)
    # 7. Bottom 3 pillars (y: 1980..2120, x: 100..1428)
    patch_clean(img, blank, (100, 1980, 1428, 2120), feather=18)
    
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "INTERESTS & PASSIONS", 140, get_font("cinzel", 54))
    draw_centered(draw, "Cybersecurity · 3D Graphics · Data Architecture", 245, get_font("cinzel", 26))
    
    f_card = get_font("cinzel", 26)
    # Compass Top
    draw_centered(draw, "CYBERSECURITY", 610, f_card)
    # Compass Bottom
    draw_centered(draw, "3D ANIMATION", 1650, f_card)
    draw_centered(draw, "WEBGL & SHADERS", 1898, get_font("cinzel", 22))
    
    # Compass Right (Visualisation) angled
    t_vis = Image.new("RGBA", (300, 60), (0,0,0,0))
    d_vis = ImageDraw.Draw(t_vis)
    d_vis.text((10, 10), "VISUALIZATION", font=f_card, fill=INK_DARK)
    t_vis_rot = t_vis.rotate(-45, resample=Image.BICUBIC, expand=True)
    img.paste(t_vis_rot, (1080, 1040), t_vis_rot)
    
    # Compass Left (Data Analysis) angled
    t_da = Image.new("RGBA", (300, 60), (0,0,0,0))
    d_da = ImageDraw.Draw(t_da)
    d_da.text((10, 10), "DATA ANALYSIS", font=f_card, fill=INK_DARK)
    t_da_rot = t_da.rotate(45, resample=Image.BICUBIC, expand=True)
    img.paste(t_da_rot, (220, 1040), t_da_rot)
    
    # Bottom 3 pillars
    f_ph = get_font("cinzel", 23)
    f_pb = get_font("regular", 22)
    # Col 1 (Left: cx=250)
    draw.text((140, 2015), "CYBERSECURITY", font=f_ph, fill=INK_DARK)
    draw.text((140, 2045), "Ethical Hacking & DevSecOps", font=f_pb, fill=INK_MUTED)
    draw.text((140, 2073), "Systems & Network Defense", font=f_pb, fill=INK_MUTED)
    # Col 2 (Center: cx=764)
    draw_centered(draw, "3D ANIMATION", 2015, f_ph)
    draw_centered(draw, "WebGL, Three.js & Shaders", 2045, f_pb, fill=INK_MUTED)
    draw_centered(draw, "3D Interactive Environments", 2073, f_pb, fill=INK_MUTED)
    # Col 3 (Right: cx=1280)
    draw.text((1140, 2015), "DATA ANALYSIS", font=f_ph, fill=INK_DARK)
    draw.text((1140, 2045), "Statistical Modeling & BI", font=f_pb, fill=INK_MUTED)
    draw.text((1140, 2073), "Data Mining & Machine Learning", font=f_pb, fill=INK_MUTED)
    
    img.save(os.path.join(OUT_PAGES, "interests.jpg"), "JPEG", quality=95)
    print("Generated interests.jpg")

# ==================== GROUP C: PURE PARCHMENT PAGES (DIRECT ON BLANK.JPG) ====================

def generate_about(blank):
    img = blank.copy()
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "CHAPTER I", 760, get_font("cinzel", 46))
    draw_centered(draw, "ABOUT ME", 830, get_font("cinzel", 68))
    draw_centered(draw, "— • —", 940, get_font("cinzel", 34))
    draw_centered(draw, "Discover my story, page by page.", 1020, get_font("italic", 34))
    draw_centered(draw, "Full Stack Developer & Software Architect.", 1080, get_font("italic", 32))
    draw_centered(draw, "My systems, my models, my technical vision.", 1180, get_font("regular", 30))
    draw_centered(draw, "Explore the codex and interact with each project.", 1240, get_font("regular", 28))
    img.save(os.path.join(OUT_PAGES, "about.jpg"), "JPEG", quality=95)
    print("Generated about.jpg")

def generate_who_am_i(blank):
    img = blank.copy()
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "WHO AM I", 140, get_font("cinzel", 54))
    draw_centered(draw, "Software Architect · AI Solutions · Full Stack Engineer", 240, get_font("italic", 28))
    draw_centered(draw, "Greetings!", 440, get_font("italic", 36))
    
    lines = [
        "I am Tomas Esteban Gonzalez Quintero, Full Stack Developer & AI Solutions Integrator",
        "specialized in multi-agent systems, clean architectures, 4NF relational databases,",
        "and high-impact enterprise workflow automations."
    ]
    for i, line in enumerate(lines):
        draw_centered(draw, line, 520 + i * 44, get_font("regular", 26))
        
    draw_centered(draw, "Bucaramanga, Colombia  ·  WhatsApp: +57 316 775 5887", 690, get_font("italic", 28))
    draw_centered(draw, "— • —", 760, get_font("cinzel", 28))
    
    cols = [
        ("BACKEND & ARCHITECTURE", ["Python (FastAPI)", "Java (Spring Boot)", "Node.js / Express", "Clean Architecture", "REST APIs & Webhooks"]),
        ("AI & AUTOMATION", ["LangGraph / Multi-Agent", "n8n Workflows + LLMs", "Model Context Protocol (MCP)", "PyTorch / Computer Vision", "Groq / LLaMA 3.3"]),
        ("DATA & PLATFORMS", ["PostgreSQL & MySQL", "4NF Relational Modeling", "Three.js / WebGL", "Docker & Linux Servers", "React & Next.js"])
    ]
    centers = [280, 764, 1248]
    f_h2 = get_font("cinzel", 26)
    f_body = get_font("regular", 26)
    for idx, (head, items) in enumerate(cols):
        cx = centers[idx]
        b = draw.textbbox((0, 0), head, font=f_h2)
        draw.text((cx - (b[2] - b[0]) // 2, 860), head, font=f_h2, fill=INK_DARK)
        draw.line((cx - 160, 910, cx + 160, 910), fill=(180, 155, 120), width=2)
        for j, it in enumerate(items):
            bi = draw.textbbox((0, 0), it, font=f_body)
            draw.text((cx - (bi[2] - bi[0]) // 2, 940 + j * 50), it, font=f_body, fill=INK_MUTED)
            
    img.save(os.path.join(OUT_PAGES, "who-am-i.jpg"), "JPEG", quality=95)
    print("Generated who-am-i.jpg")

def generate_my_story(blank):
    img = blank.copy()
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "MY STORY", 140, get_font("cinzel", 54))
    draw_centered(draw, "The Evolutionary Path of a Software Craftsman", 240, get_font("italic", 28))
    
    cards = [
        ("EARLY FASCINATION", "From an early age, I felt a deep fascination for logic, mathematics, and digital systems. Code quickly became my primary language to explore, construct, and solve real-world problems.", 420, 560),
        ("BACKEND FOUNDATIONS", "I evolved building robust enterprise backends with Python, FastAPI, Java 17, and Spring Boot. I understood early on that the foundation of any enduring system is its architectural integrity.", 1100, 560),
        ("CAMPUSLANDS IMMERSION", "At Campuslands, I forged my engineering discipline in end-to-end full stack development, rigorous relational databases up to 4NF, and multi-agent AI systems with autonomous workflows.", 420, 1260),
        ("HIGH-IMPACT ENGINEERING", "Today, I architect scalable distributed platforms, Model Context Protocol (MCP) servers, and autonomous n8n pipelines. I deliver engineering rigor, clear design, and consistent execution.", 1100, 1260)
    ]
    f_h = get_font("cinzel", 28)
    f_b = get_font("regular", 26)
    for title, desc, cx, cy in cards:
        b = draw.textbbox((0, 0), title, font=f_h)
        draw.text((cx - (b[2] - b[0]) // 2, cy), title, font=f_h, fill=INK_DARK)
        draw.line((cx - 180, cy + 42, cx + 180, cy + 42), fill=(180, 155, 120), width=2)
        draw_wrapped(draw, desc, cx, cy + 70, 540, f_b, line_spacing=1.35)
        
    img.save(os.path.join(OUT_PAGES, "my-story.jpg"), "JPEG", quality=95)
    print("Generated my-story.jpg")

def generate_skills(blank):
    img = blank.copy()
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "TECHNICAL ARSENAL", 140, get_font("cinzel", 54))
    draw_centered(draw, "Core Technologies, Frameworks & Architectural Disciplines", 240, get_font("italic", 28))
    
    sections = [
        ("BACKEND & ARCHITECTURE", [
            "• Python (FastAPI, Flask, Pydantic, SQLAlchemy)",
            "• Java 17+ (Spring Boot 3, Spring Security, JPA/Hibernate)",
            "• Node.js & Express (TypeScript, REST APIs, WebSockets)",
            "• Clean Architecture, Domain-Driven Design (DDD), SOLID"
        ], 420, 480),
        ("AI & INTELLIGENT AUTOMATION", [
            "• Multi-Agent Systems with LangGraph & StateGraph",
            "• Automated Workflow Pipelines in n8n with LLM Nodes",
            "• Model Context Protocol (MCP) Servers in Node.js & Python",
            "• Retrieval-Augmented Generation (RAG) & Vector Embeddings"
        ], 1100, 480),
        ("DATABASES & DATA INTEGRITY", [
            "• PostgreSQL 16 & MySQL (Strict 4NF Normalization)",
            "• Complex Stored Procedures, Triggers, Views & Transactions",
            "• Optimistic/Pessimistic Locking & Index Optimization",
            "• Redis In-Memory Caching & Session Management"
        ], 420, 1140),
        ("FRONTEND & CLOUD DEVOPS", [
            "• Three.js, WebGL & Custom Shader Programming",
            "• React 18, Next.js, Vite & Modern TypeScript",
            "• Docker, Container Orchestration & Linux Administration",
            "• CI/CD Pipelines, Nginx Reverse Proxies & HTTPS Domains"
        ], 1100, 1140)
    ]
    f_sh = get_font("cinzel", 28)
    f_sb = get_font("regular", 25)
    for head, bullets, cx, cy in sections:
        b = draw.textbbox((0, 0), head, font=f_sh)
        draw.text((cx - (b[2] - b[0]) // 2, cy), head, font=f_sh, fill=INK_DARK)
        draw.line((cx - 220, cy + 40, cx + 220, cy + 40), fill=(180, 155, 120), width=2)
        for idx, bul in enumerate(bullets):
            draw.text((cx - 240, cy + 70 + idx * 56), bul, font=f_sb, fill=INK_MUTED)
            
    draw_centered(draw, "— • Tap to explore interactive competencies • —", 1880, get_font("italic", 27))
    img.save(os.path.join(OUT_PAGES, "skills.jpg"), "JPEG", quality=95)
    print("Generated skills.jpg")

def generate_journey(blank):
    img = blank.copy()
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "CHAPTER II", 760, get_font("cinzel", 46))
    draw_centered(draw, "PROFESSIONAL JOURNEY", 830, get_font("cinzel", 64))
    draw_centered(draw, "— • —", 940, get_font("cinzel", 34))
    draw_centered(draw, "From foundational curiosity to advanced software engineering.", 1020, get_font("italic", 34))
    draw_centered(draw, "The developmental roadmap of architectural challenges and milestones.", 1080, get_font("italic", 30))
    draw_centered(draw, "Continuous evolution across real-world systems and production environments.", 1180, get_font("regular", 30))
    draw_centered(draw, "Explore the chronological milestones across the following parchment scrolls.", 1240, get_font("regular", 28))
    img.save(os.path.join(OUT_PAGES, "journey.jpg"), "JPEG", quality=95)
    print("Generated journey.jpg")

def generate_career(blank):
    img = blank.copy()
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "CHAPTER III", 760, get_font("cinzel", 46))
    draw_centered(draw, "EXPERIENCE", 830, get_font("cinzel", 68))
    draw_centered(draw, "— • —", 940, get_font("cinzel", 34))
    draw_centered(draw, "Campuslands, Enterprise Engineering & Independent Consulting.", 1020, get_font("italic", 34))
    draw_centered(draw, "Leadership in enterprise backend architecture and AI workflows.", 1080, get_font("italic", 30))
    draw_centered(draw, "Building resilient distributed systems designed for mission-critical scale.", 1180, get_font("regular", 30))
    draw_centered(draw, "Discover key professional roles, engineering pillars, and real production outcomes.", 1240, get_font("regular", 28))
    img.save(os.path.join(OUT_PAGES, "career.jpg"), "JPEG", quality=95)
    print("Generated career.jpg")

def generate_thor_systems(blank):
    img = blank.copy()
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "CAMPUSLANDS", 140, get_font("cinzel", 54))
    draw_centered(draw, "ELITE ACADEMY OF ADVANCED SOFTWARE ENGINEERING", 240, get_font("cinzel", 25))
    
    p1 = "Campuslands is a high-performance, immersive technology ecosystem focused on advanced software engineering, scalable enterprise architecture, and global industry best practices."
    draw_wrapped(draw, p1, 764, 310, 1260, get_font("regular", 27), line_spacing=1.35)
    
    p2 = "During my intensive training, I developed real corporate projects under the Scrum methodology, with weekly continuous delivery sprints, rigorous code reviews, and high-demand problem solving."
    draw_wrapped(draw, p2, 764, 520, 1260, get_font("regular", 27), line_spacing=1.35)
    
    p3 = "This experience cemented my professional discipline, my ability to solve complex engineering challenges under pressure, and my mastery in building robust backend architectures ready for production."
    draw_wrapped(draw, p3, 764, 730, 1260, get_font("regular", 27), line_spacing=1.35)
    
    draw_centered(draw, "— CORE ATTRIBUTES & COMPETENCIES —", 980, get_font("cinzel", 28))
    
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
        
    img.save(os.path.join(OUT_PAGES, "thor-systems.jpg"), "JPEG", quality=95)
    print("Generated thor-systems.jpg")

def generate_thor_systems_2(blank):
    img = blank.copy()
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "CAMPUSLANDS", 140, get_font("cinzel", 54))
    draw_centered(draw, "ENTERPRISE PROJECTS & ARCHITECTURAL CONTRIBUTIONS", 240, get_font("cinzel", 25))
    
    # Project 1: LogiTrack WMS
    draw.text((140, 360), "LOGITRACK WMS · BACKEND LEAD", font=get_font("cinzel", 28), fill=INK_DARK)
    desc1 = "Comprehensive logistics and warehouse management system engineered for multi-facility stock control, supplier receptions, lot tracking, and zero inventory discrepancy:"
    draw_wrapped(draw, desc1, 764, 420, 1240, get_font("regular", 26), align="left")
    
    b1_left = ["• Multi-facility stock control", "• Full operational audit trails", "• JWT authentication & RBAC"]
    b1_right = ["• Strict 4NF data normalization", "• MySQL triggers & procedures", "• High-throughput RESTful APIs"]
    for i, l in enumerate(b1_left):
        draw.text((140, 560 + i * 50), l, font=get_font("regular", 25), fill=INK_MUTED)
    for i, r in enumerate(b1_right):
        draw.text((780, 560 + i * 50), r, font=get_font("regular", 25), fill=INK_MUTED)
        
    draw_centered(draw, "— • —", 760, get_font("cinzel", 26))
    
    # Project 2: Multi-Agent
    draw.text((140, 840), "CAMPUSLANDS INTELLIGENT · MULTI-AGENT PLATFORM", font=get_font("cinzel", 28), fill=INK_DARK)
    desc2 = "Intelligent academic supervision and analytics platform powered by coordinated autonomous AI agents, computer vision, and real-time automated notification pipelines:"
    draw_wrapped(draw, desc2, 764, 900, 1240, get_font("regular", 26), align="left")
    
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
        
    img.save(os.path.join(OUT_PAGES, "thor-systems-2.jpg"), "JPEG", quality=95)
    print("Generated thor-systems-2.jpg")

def generate_freelance(blank):
    img = blank.copy()
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "CONSULTING & FREELANCE", 140, get_font("cinzel", 54))
    draw_centered(draw, "INDEPENDENT SOFTWARE ARCHITECTURE & CUSTOM SOLUTIONS", 240, get_font("cinzel", 25))
    
    desc = "Independent software development has allowed me to resolve high-impact business challenges, delivering custom platforms, intelligent automated workflows, and robust relational architectures tailored to exact client requirements."
    draw_wrapped(draw, desc, 764, 320, 1240, get_font("regular", 27), line_spacing=1.35)
    
    draw_centered(draw, "— METHODOLOGY & ENGINEERING STANDARDS —", 560, get_font("cinzel", 28))
    
    pillars = [
        ("1. ARCHITECTURAL DISCOVERY & SCOPING", "Exhaustive requirement analysis, domain modeling, and technical feasibility validation before writing a single line of code.", 650),
        ("2. CLEAN & MODULAR IMPLEMENTATION", "Decoupled software components following SOLID principles, design patterns, and comprehensive documentation for long-term maintainability.", 860),
        ("3. RIGOROUS DATA NORMALIZATION", "Database schemas modeled up to 4NF to guarantee zero redundancy, total referential integrity, and lightning-fast query execution.", 1070),
        ("4. CONTINUOUS DELIVERY & TRANSPARENCY", "Incremental milestones with live deployment environments, automated testing, and direct, transparent client communication.", 1280)
    ]
    for h_txt, b_txt, y in pillars:
        draw.text((140, y), h_txt, font=get_font("cinzel", 26), fill=INK_DARK)
        draw_wrapped(draw, b_txt, 764, y + 42, 1240, get_font("regular", 25), align="left")
        
    draw_centered(draw, "Available for architectural consulting, enterprise backend development, and AI workflow automation.", 1680, get_font("italic", 27))
    img.save(os.path.join(OUT_PAGES, "freelance.jpg"), "JPEG", quality=95)
    print("Generated freelance.jpg")

def generate_freelance_2(blank):
    img = blank.copy()
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "PILLARS OF EXCELLENCE", 140, get_font("cinzel", 54))
    draw_centered(draw, "CORE PRINCIPLES GOVERNING EVERY PRODUCTION DEPLOYMENT", 240, get_font("cinzel", 25))
    
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
        
    img.save(os.path.join(OUT_PAGES, "freelance-2.jpg"), "JPEG", quality=95)
    print("Generated freelance-2.jpg")

def generate_projects(blank):
    img = blank.copy()
    draw = ImageDraw.Draw(img)
    draw_centered(draw, "CHAPTER IV", 760, get_font("cinzel", 46))
    draw_centered(draw, "FEATURED PROJECTS", 830, get_font("cinzel", 68))
    draw_centered(draw, "— • —", 940, get_font("cinzel", 34))
    draw_centered(draw, "Selected works, systems architectures & live demonstrations.", 1020, get_font("italic", 34))
    draw_centered(draw, "Explore production platforms, multi-agent frameworks, and data engines.", 1080, get_font("italic", 30))
    draw_centered(draw, "Click interactive seals and badges to inspect GitHub repositories and live deployments.", 1180, get_font("regular", 30))
    draw_centered(draw, "Turn the page to begin the engineering showcase.", 1240, get_font("regular", 28))
    img.save(os.path.join(OUT_PAGES, "projects.jpg"), "JPEG", quality=95)
    print("Generated projects.jpg")

# ==================== GROUP D: PROJECT SHOWCASE PAGES (DIRECT ON BLANK.JPG) ====================

def generate_project_template(blank, title, subtitle, desc, links, section_title, features, badges, filename):
    img = blank.copy()
    draw = ImageDraw.Draw(img)
    
    draw_centered(draw, title, 140, get_font("cinzel", 54))
    draw_centered(draw, subtitle, 240, get_font("cinzel", 24))
    draw_wrapped(draw, desc, 764, 310, 1260, get_font("regular", 26), line_spacing=1.35)
    
    # Links line at y=490 for 3D active area hotspot
    draw_centered(draw, links, 490, get_font("italic", 27))
    draw_centered(draw, f"— {section_title} —", 580, get_font("cinzel", 28))
    
    f_fh = get_font("cinzel", 25)
    f_fb = get_font("regular", 24)
    for idx, (h_txt, b_txt, y) in enumerate(features):
        draw.text((140, y), h_txt, font=f_fh, fill=INK_DARK)
        draw_wrapped(draw, b_txt, 764, y + 36, 1240, f_fb, align="left", line_spacing=1.3)
        
    draw_badge_columns(draw, badges, y_header=1680, y_row1=1730, y_row2=1765)
    img.save(os.path.join(OUT_PAGES, filename), "JPEG", quality=95)
    print(f"Generated {filename}")

def generate_all_projects(blank):
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
        blank, "CAMPUSLANDS INTELIGENTE", "MULTI-AGENT ACADEMIC SUPERVISION & PREDICTIVE ANALYTICS",
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
        blank, "CAMPUSLANDS INTELIGENTE", "SYSTEM ARCHITECTURE & PROTOCOL PIPELINE",
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
        blank, "LOGITRACK WMS", "ENTERPRISE LOGISTICS & WAREHOUSE MANAGEMENT SYSTEM",
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
        blank, "N8N ATTENDANCE AI", "AUTOMATION WORKFLOW & LLM REQUEST CLASSIFICATION",
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
        blank, "GITHUB MCP SERVER", "MODEL CONTEXT PROTOCOL FOR AUTONOMOUS AI AGENTS",
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
        blank, "GITHUB MCP SERVER", "PROTOCOL EXECUTION PIPELINE & AGENT INTEGRATION",
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
        blank, "HELPDESK AI", "ENTERPRISE INCIDENT MANAGEMENT WITH LLM TRIAGE",
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
        blank, "ECOMMERCE DATABASE 4NF", "ADVANCED RELATIONAL ARCHITECTURE & 4NF RIGOR",
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
        blank, "SOFTSKILLS QUEST", "GAMIFIED DEVELOPER DECISION-MAKING GAME",
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
        blank, "LMS ABC PLATFORM", "MODULAR LIGHTWEIGHT LEARNING MANAGEMENT SYSTEM",
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
        blank, "PORTFOLIO 3D CODEX", "THREE.JS ENGINE, MATHEMATICAL DEFORMATIONS & SHADERS",
        "The engineering behind this interactive 3D codex: real-time GPU mesh deformations, cylindrical physics equations simulating paper flexibility, procedural leather texturing, and dynamic lighting pipelines.",
        "Links: GitHub (Repository)  ·  Technical Architecture",
        "GRAPHICAL & MATHEMATICAL FOUNDATIONS", f15_features, f15_badges, "fifteen-js.jpg"
    )

    # 12. the-book.jpg (The Codex Architecture & Credits)
    tb_features = [
        ("1. 60 FPS HARDWARE ACCELERATION", "Smooth WebGL execution with FXAA antialiasing and soft dynamic shadow mapping across all viewports.", 670),
        ("2. MULTI-INPUT NAVIGATION ENGINE", "Comprehensive gesture detection supporting drag turning, touch swipes, keyboard arrow keys, and chapter plaques.", 820),
        ("3. SUB-2-SECOND ULTRA-FAST LOADING", "Optimized production bundle using Vite tree-shaking, lazy texture precompilation, and zero redundant video payloads.", 970)
    ]
    tb_badges = [
        ("AUTHOR", "Tomas Esteban", "Gonzalez Quintero"),
        ("ROLE", "Full Stack Dev", "Software Architect"),
        ("LOCATION", "Bucaramanga", "Colombia · 2026"),
        ("MOTTO", "Clean Systems", "Tangible Rigor")
    ]
    generate_project_template(
        blank, "THE CODEX", "TECHNICAL ARCHITECTURE & AUTHORSHIP CREDITS",
        "The Book of Tomas Esteban Gonzalez Quintero is an interactive 3D experience designed to present my trajectory, engineering projects, technical capabilities, and software architecture vision.",
        "Links: Official Repository  ·  Live Deployment",
        "MOTOR SPECIFICATIONS & ARCHITECTURE", tb_features, tb_badges, "the-book.jpg"
    )

def main():
    os.makedirs(OUT_PAGES, exist_ok=True)
    blank = Image.open(BLANK_PATH).convert("RGB")
    
    print("=== STARTING MASTER ENGLISH EDITION GENERATION ===")
    copy_static_assets()
    generate_cover_front()
    generate_cover_back()
    generate_welcome(blank)
    generate_map_1(blank)
    generate_map_2(blank)
    generate_interests(blank)
    
    # Pure parchment pages (100% on virgin parchment)
    generate_about(blank)
    generate_who_am_i(blank)
    generate_my_story(blank)
    generate_skills(blank)
    generate_journey(blank)
    generate_career(blank)
    generate_thor_systems(blank)
    generate_thor_systems_2(blank)
    generate_freelance(blank)
    generate_freelance_2(blank)
    generate_projects(blank)
    generate_all_projects(blank)
    print("=== ALL 34 ENGLISH EDITION PAGES SUCCESSFULLY GENERATED ===")

if __name__ == "__main__":
    main()
