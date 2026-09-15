#!/usr/bin/env python3
"""
apply_purple_theme.py
1. Renders Page 29 (Enterprise Security API) & Page 30 (Campuslands Access Hub)
   with royal purple decorative frames, section titles, and badge accents.
2. Enhances the 3D book leather textures to a vibrant, authentic royal purple.
3. Composites the inside covers (welcome.webp on Sheet 0 and the-book.webp on Sheet 15)
   with full 1544x2200 dimensions and prominent purple leather margins.
"""

import os
from PIL import Image, ImageDraw, ImageFont

FONTS_DIR = "scripts/fonts"
BLANK_PATH = "public/img/pages/blank.webp"

FONTS = {
    "cinzel_bold": os.path.join(FONTS_DIR, "Cinzel-Bold.ttf"),
    "cinzel_reg": os.path.join(FONTS_DIR, "Cinzel-Regular.ttf"),
    "garamond_reg": os.path.join(FONTS_DIR, "EBGaramond-Regular.ttf"),
    "garamond_it": os.path.join(FONTS_DIR, "EBGaramond-Italic.ttf"),
}

INK_DARK = (24, 20, 17)
INK_MUTED = (55, 45, 36)

# Royal Purple Palette for Frames and Highlights
PURPLE_PRIMARY = (112, 42, 142)       # Rich royal purple for outer frame
PURPLE_SECONDARY = (150, 68, 182)     # Lighter vibrant purple for inner double border
PURPLE_TITLE = (92, 28, 122)          # Deep imperial violet for section title
PURPLE_ACCENT = (135, 55, 165)        # Badge divider accent
DIVIDER_LINE = (165, 85, 195)

def get_font(name, size):
    return ImageFont.truetype(FONTS[name], size)

def draw_centered(draw, text, y, font, fill=INK_DARK, cx=764):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text((cx - w // 2, y), text, font=font, fill=fill)
    return cx - w // 2, w

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
            draw.text((cx, curr_y), line, font=font, fill=fill)
        curr_y += line_h
    return curr_y

def draw_badge_columns(draw, badges, y_header=1680, y_row1=1735, y_row2=1780):
    f_h = get_font("cinzel_bold", 26)
    f_b = get_font("garamond_it", 27)
    centers = [280, 600, 930, 1250]
    for idx, (head, r1, r2) in enumerate(badges):
        cx = centers[idx]
        b_h = draw.textbbox((0, 0), head, font=f_h)
        draw.text((cx - (b_h[2] - b_h[0]) // 2, y_header), head, font=f_h, fill=PURPLE_TITLE)
        draw.line((cx - 130, y_header + 40, cx + 130, y_header + 40), fill=DIVIDER_LINE, width=2)
        b_1 = draw.textbbox((0, 0), r1, font=f_b)
        draw.text((cx - (b_1[2] - b_1[0]) // 2, y_row1), r1, font=f_b, fill=INK_MUTED)
        b_2 = draw.textbbox((0, 0), r2, font=f_b)
        draw.text((cx - (b_2[2] - b_2[0]) // 2, y_row2), r2, font=f_b, fill=INK_MUTED)

def render_parchment_content(data):
    img = Image.open(BLANK_PATH).convert("RGB")
    draw = ImageDraw.Draw(img)
    w, h = img.size
    cx = w // 2

    # 1. Title
    f_title = get_font("cinzel_bold", 58)
    tx, tw = draw_centered(draw, data["title"], 135, f_title, cx=cx)
    # Underline bar in deep purple
    draw.line((cx - tw // 2 - 20, 208, cx + tw // 2 + 20, 208), fill=PURPLE_PRIMARY, width=3)

    # 2. Subtitle
    f_sub = get_font("cinzel_reg", 28)
    draw_centered(draw, data["subtitle"], 230, f_sub, fill=PURPLE_TITLE, cx=cx)

    # 3. Description
    f_desc = get_font("garamond_reg", 31)
    draw_wrapped(draw, data["desc"], cx, 300, 1280, f_desc, line_h=42, align="center")

    # 4. Links line
    f_label = get_font("garamond_reg", 32)
    f_link = get_font("garamond_it", 32)
    
    label_txt = data["links_label"]
    link_txt = data["links_text"]
    
    draw.text((110, 475), label_txt, font=f_label, fill=INK_DARK)
    b_label = draw.textbbox((0, 0), label_txt, font=f_label)
    link_x = 110 + (b_label[2] - b_label[0]) + 20
    
    draw.text((link_x, 475), link_txt, font=f_link, fill=PURPLE_TITLE)
    b_link = draw.textbbox((0, 0), link_txt, font=f_link)
    link_w = b_link[2] - b_link[0]
    draw.line((link_x, 514, link_x + link_w, 514), fill=PURPLE_PRIMARY, width=2)

    # 5. Box frame (Royal Purple Double Renaissance Border)
    box_left = 110
    box_top = 580
    box_right = w - 110
    box_bottom = 1580

    # Outer border: Royal Purple, width 3
    draw.rectangle([box_left, box_top, box_right, box_bottom], outline=PURPLE_PRIMARY, width=3)
    # Inner decorative border: Vibrant purple, width 2
    draw.rectangle([box_left + 6, box_top + 6, box_right - 6, box_bottom - 6], outline=PURPLE_SECONDARY, width=2)

    # Box Section Title in Imperial Violet
    f_sec = get_font("cinzel_reg", 30)
    draw_centered(draw, f"— {data['section_title']} —", box_top + 45, f_sec, fill=PURPLE_TITLE, cx=cx)

    # Features list inside box
    f_fh = get_font("cinzel_bold", 27)
    f_fb = get_font("garamond_reg", 28)
    
    curr_y = box_top + 130
    for idx, (head_text, body_text) in enumerate(data["features"]):
        draw.text((box_left + 40, curr_y), head_text, font=f_fh, fill=PURPLE_TITLE)
        curr_y += 38
        curr_y = draw_wrapped(draw, body_text, box_left + 40, curr_y, (box_right - box_left - 80), f_fb, line_h=38, align="left")
        curr_y += 32

    # 6. Badges
    draw_badge_columns(draw, data["badges"], y_header=1680, y_row1=1735, y_row2=1780)

    # 7. Bottom Quote
    f_quote = get_font("garamond_it", 29)
    draw_centered(draw, data["quote"], 1930, f_quote, fill=INK_MUTED, cx=cx)

    return img

def enhance_leather(img):
    """Enhance leather texture to rich royal purple while preserving grain and lighting."""
    img = img.convert("RGB")
    r, g, b = img.split()
    r = r.point(lambda p: min(255, int(p * 1.35)))
    g = g.point(lambda p: int(p * 0.70))
    b = b.point(lambda p: min(255, int(p * 1.35)))
    return Image.merge("RGB", (r, g, b))

def composite_inside_cover(parchment_img, leather_bg, side="right"):
    """
    Composites a 1528x2160 parchment page onto a 1544x2200 leather cover.
    - side='right': Sheet 15 (the-book.webp, inside back cover). Leather border on Top, Bottom, Right.
    - side='left': Sheet 0 (welcome.webp, inside front cover). Leather border on Top, Bottom, Left.
    """
    canvas = leather_bg.copy().resize((1544, 2200), Image.LANCZOS)
    
    # Scale parchment slightly to fit inside the leather margin
    # Leather margin: top=22px, bottom=22px. Total parchment height = 2200 - 44 = 2156
    # Width: 1544 - 32px margin = 1512
    parchment_w = 1512
    parchment_h = 2156
    scaled_parchment = parchment_img.resize((parchment_w, parchment_h), Image.LANCZOS)
    
    paste_y = 22
    if side == "right":
        # Leather on right (x = 1512..1544), spine on left (x = 0)
        paste_x = 0
    else:
        # Leather on left (x = 0..32), spine on right (x = 1544)
        paste_x = 32
        
    canvas.paste(scaled_parchment, (paste_x, paste_y))
    
    # Draw soft crease/shadow along the seam where parchment meets leather
    draw = ImageDraw.Draw(canvas)
    if side == "right":
        for i in range(4):
            draw.line([(paste_x + parchment_w - 1 - i, paste_y), (paste_x + parchment_w - 1 - i, paste_y + parchment_h)], fill=(40, 20, 50), width=1)
        draw.line([(paste_x, paste_y), (paste_x + parchment_w, paste_y)], fill=(50, 25, 60), width=2)
        draw.line([(paste_x, paste_y + parchment_h), (paste_x + parchment_w, paste_y + parchment_h)], fill=(50, 25, 60), width=2)
    else:
        for i in range(4):
            draw.line([(paste_x + i, paste_y), (paste_x + i, paste_y + parchment_h)], fill=(40, 20, 50), width=1)
        draw.line([(paste_x, paste_y), (paste_x + parchment_w, paste_y)], fill=(50, 25, 60), width=2)
        draw.line([(paste_x, paste_y + parchment_h), (paste_x + parchment_w, paste_y + parchment_h)], fill=(50, 25, 60), width=2)
        
    return canvas

PAGE_29_ES = {
    "title": "ENTERPRISE SECURITY API",
    "subtitle": "ARQUITECTURA HEXAGONAL & DEFENSIVA OWASP EN .NET 9",
    "desc": "API REST empresarial de alta seguridad diseñada bajo Arquitectura Hexagonal en .NET 9, integrando autenticación JWT blindada, cifrado BCrypt, análisis de vulnerabilidades OWASP, rate limiting y CRM seguro de clientes.",
    "links_label": "Enlaces:",
    "links_text": "GitHub (Repositorio Oficial)",
    "section_title": "MÓDULOS DE CIBERSEGURIDAD Y CONTROL",
    "features": [
        ("1. ANÁLISIS DE CONTRASEÑAS OWASP",
         "Evaluación heurística de entropía y cumplimiento estricto de estándares OWASP para mitigar ataques de diccionario y fuerza bruta."),
        ("2. AUTENTICACIÓN JWT Y HASHING BCRYPT",
         "Gestión segura de identidades con tokens criptográficos firmados, rotación de claves secretas y hashing adaptativo de credenciales."),
        ("3. RATE LIMITING Y PROTECCIÓN CONTRA ABUSO",
         "Políticas estrictas de limitación de tasa por IP y por cliente para defender los endpoints críticos frente a ráfagas y denegación de servicio."),
        ("4. AUDITORÍA Y TRAZABILIDAD INMUTABLE",
         "Registro estructurado de eventos de autenticación, intentos fallidos y cambios de privilegios para cumplimiento normativo y forense digital.")
    ],
    "badges": [
        ("FRAMEWORK", "C# / .NET 9", "ASP.NET Core"),
        ("ARQUITECTURA", "Hexagonal (Ports)", "Clean Architecture"),
        ("SEGURIDAD", "OWASP Compliant", "JWT & BCrypt"),
        ("PROTECCIÓN", "Rate Limiting", "Data Sanitization")
    ],
    "quote": "Una arquitectura defensiva diseñada para proteger identidades y endpoints críticos con estándares bancarios."
}

PAGE_29_EN = {
    "title": "ENTERPRISE SECURITY API",
    "subtitle": "HEXAGONAL ARCHITECTURE & OWASP DEFENSIVE SECURITY IN .NET 9",
    "desc": "High-security enterprise REST API designed under Hexagonal Architecture in .NET 9, featuring hardened JWT authentication, BCrypt password hashing, OWASP compliance analyzer, rate limiting, and client CRM.",
    "links_label": "Links:",
    "links_text": "GitHub (Official Repository)",
    "section_title": "CYBERSECURITY & DEFENSIVE MODULES",
    "features": [
        ("1. OWASP PASSWORD VULNERABILITY ANALYSIS",
         "Heuristic entropy evaluation and strict OWASP compliance validation to eliminate dictionary and brute-force attack vectors."),
        ("2. HARDENED JWT AUTH & BCRYPT HASHING",
         "Secure identity management with cryptographically signed JWT tokens, secret rotation, and adaptive BCrypt salting."),
        ("3. DISTRIBUTED RATE LIMITING & DOS DEFENSE",
         "Granular per-IP and per-client throttling policies protecting critical authentication endpoints from flood attacks."),
        ("4. IMMUTABLE AUDIT LOGGING & TRACEABILITY",
         "Structured logging of authentication lifecycles, failed access attempts, and privilege elevations for forensics.")
    ],
    "badges": [
        ("FRAMEWORK", "C# / .NET 9", "ASP.NET Core"),
        ("ARCHITECTURE", "Hexagonal (Ports)", "Clean Architecture"),
        ("SECURITY", "OWASP Compliant", "JWT & BCrypt"),
        ("PROTECTION", "Rate Limiting", "Data Sanitization")
    ],
    "quote": "A robust defensive architecture safeguarding mission-critical identities and modern enterprise endpoints."
}

PAGE_30_ES = {
    "title": "CAMPUSLANDS ACCESS HUB",
    "subtitle": "GESTIÓN DE ACCESOS, ASISTENCIA Y CERTIFICADOS EN PRODUCCIÓN",
    "desc": "Sistema empresarial desplegado en producción y utilizado por cientos de participantes, con control de asistencia en tiempo real, gestión integral de grupos, emisión automatizada de certificados digitales y seguridad RBAC.",
    "links_label": "Enlaces:",
    "links_text": "GitHub (Repositorio de Producción)",
    "section_title": "CAPACIDADES OPERATIVAS EN PRODUCCIÓN",
    "features": [
        ("1. ASISTENCIA BIOMÉTRICA EN TIEMPO REAL",
         "Registro instantáneo de ingresos y salidas con verificación multi-factor, procesando cientos de registros diarios sin latencia."),
        ("2. CONTROL DE ACCESO BASADO EN ROLES (RBAC)",
         "Matriz jerárquica de permisos granulares para SuperAdmins, Coordinadores, Trainers y Campers con políticas estrictas."),
        ("3. CERTIFICADOS DIGITALES AUTOMATIZADOS",
         "Generación y validación criptográfica de certificados de asistencia y aprobación con código único de verificación QR."),
        ("4. DASHBOARD ANALÍTICO Y REPORTES",
         "Panel de control interactivo con métricas de permanencia, tasas de inasistencia y exportación estructurada de datos auditables.")
    ],
    "badges": [
        ("ENTORNO", "Producción Real", "Cientos de Usuarios"),
        ("STACK", "TypeScript / Node", "PostgreSQL & Supabase"),
        ("SEGURIDAD", "RBAC Granular", "JWT Tokens"),
        ("OPERACIÓN", "Tiempo Real", "Certificados QR")
    ],
    "quote": "Solución tecnológica de alto impacto en producción que resuelve la gestión académica y operativa a gran escala."
}

PAGE_30_EN = {
    "title": "CAMPUSLANDS ACCESS HUB",
    "subtitle": "PRODUCTION ACCESS CONTROL, ATTENDANCE & DIGITAL CERTIFICATES",
    "desc": "Enterprise system deployed to production and actively used by hundreds of participants, featuring real-time attendance tracking, group management, automated digital certificate issuance, and role-based access control (RBAC).",
    "links_label": "Links:",
    "links_text": "GitHub (Production Repository)",
    "section_title": "PRODUCTION OPERATIONAL CAPABILITIES",
    "features": [
        ("1. REAL-TIME MULTI-TENANT ATTENDANCE",
         "Instant attendance verification and logging processing hundreds of daily check-ins with sub-second response times."),
        ("2. ROLE-BASED ACCESS CONTROL (RBAC)",
         "Granular permission hierarchy enforcing strict security boundaries across SuperAdmins, Coordinators, Trainers, and Campers."),
        ("3. AUTOMATED DIGITAL CERTIFICATES",
         "Automated generation and cryptographic verification of completion certificates featuring unique tamper-proof QR codes."),
        ("4. ANALYTIC METRICS & REPORTING DASHBOARD",
         "Interactive coordinator dashboard tracking retention rates, attendance anomalies, and structured data exports.")
    ],
    "badges": [
        ("ENVIRONMENT", "Live Production", "Hundreds of Users"),
        ("STACK", "TypeScript / Node", "PostgreSQL & Supabase"),
        ("SECURITY", "Granular RBAC", "Signed JWT"),
        ("OPERATION", "Real-Time Sync", "Digital QR Certs")
    ],
    "quote": "High-impact production technology solving large-scale academic governance and automated attendance tracking."
}

def main():
    print("=== 1. Enhancing Leather Textures to Royal Purple ===")
    cb_raw = Image.open("backup-pages/covers/cover-back.webp")
    cf_raw = Image.open("backup-pages/covers/cover-front.webp")
    lr_raw = Image.open("backup-pages/covers/cover-edge-lr.webp")
    tb_raw = Image.open("backup-pages/covers/cover-edge-tb.webp")
    sp_raw = Image.open("backup-pages/covers/spine.webp")
    wel_raw = Image.open("backup-pages/covers/welcome.webp")

    cb_purple = enhance_leather(cb_raw)
    cf_purple = enhance_leather(cf_raw)
    lr_purple = enhance_leather(lr_raw)
    tb_purple = enhance_leather(tb_raw)
    sp_purple = enhance_leather(sp_raw)

    # Save enhanced cover textures in both ES and EN
    for folder in ["public/img/pages/", "public/img/pages-en/"]:
        cb_purple.save(f"{folder}cover-back.webp", "WEBP", quality=85)
        cf_purple.save(f"{folder}cover-front.webp", "WEBP", quality=85)
        lr_purple.save(f"{folder}cover-edge-lr.webp", "WEBP", quality=85)
        tb_purple.save(f"{folder}cover-edge-tb.webp", "WEBP", quality=85)
        sp_purple.save(f"{folder}spine.webp", "WEBP", quality=85)

    print("=== 2. Rendering Page 29 (Enterprise Security API with Purple Boxes) ===")
    p29_es = render_parchment_content(PAGE_29_ES)
    p29_en = render_parchment_content(PAGE_29_EN)

    p29_es.save("public/img/pages/fifteen-js.webp", "WEBP", quality=85)
    p29_en.save("public/img/pages-en/fifteen-js.webp", "WEBP", quality=85)
    p29_es.save("backup-pages/fifteen-js.jpg", "JPEG", quality=95)

    print("=== 3. Rendering Page 30 (Campuslands Access Hub with Purple Boxes) ===")
    p30_es = render_parchment_content(PAGE_30_ES)
    p30_en = render_parchment_content(PAGE_30_EN)

    # Composite Page 30 onto the Royal Purple Leather Back Cover (Sheet 15 inside)
    # This creates the authentic 1544x2200 texture with the purple leather border on Top, Bottom, and Right!
    book_cover_es = composite_inside_cover(p30_es, cb_purple, side="right")
    book_cover_en = composite_inside_cover(p30_en, cb_purple, side="right")

    book_cover_es.save("public/img/pages/the-book.webp", "WEBP", quality=85)
    book_cover_en.save("public/img/pages-en/the-book.webp", "WEBP", quality=85)
    book_cover_es.save("backup-pages/the-book.jpg", "JPEG", quality=95)

    print("=== 4. Updating welcome.webp (Sheet 0 inside) with Matching Purple Leather Border ===")
    # Extract parchment from welcome.webp and composite onto purple leather
    wel_parchment = wel_raw.crop((16, 20, 1544, 2180))
    welcome_es = composite_inside_cover(wel_parchment, cf_purple, side="left")
    
    welcome_es.save("public/img/pages/welcome.webp", "WEBP", quality=85)
    welcome_es.save("public/img/pages-en/welcome.webp", "WEBP", quality=85)

    print("=== All Purple Theme Textures Generated Successfully! ===")

if __name__ == "__main__":
    main()
