#!/usr/bin/env python3
"""
Generator for Page 29 (Enterprise Security API) and Page 30 (Campuslands Access Hub)
in both Spanish (public/img/pages/) and English (public/img/pages-en/).
Rendered on top of pristine blank parchment (public/img/pages/blank.webp).
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
BORDER_COLOR = (70, 56, 42)
DIVIDER_LINE = (180, 155, 120)

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
        draw.text((cx - (b_h[2] - b_h[0]) // 2, y_header), head, font=f_h, fill=INK_DARK)
        draw.line((cx - 130, y_header + 40, cx + 130, y_header + 40), fill=DIVIDER_LINE, width=2)
        b_1 = draw.textbbox((0, 0), r1, font=f_b)
        draw.text((cx - (b_1[2] - b_1[0]) // 2, y_row1), r1, font=f_b, fill=INK_MUTED)
        b_2 = draw.textbbox((0, 0), r2, font=f_b)
        draw.text((cx - (b_2[2] - b_2[0]) // 2, y_row2), r2, font=f_b, fill=INK_MUTED)

def render_page(data, out_path_jpg):
    img = Image.open(BLANK_PATH).convert("RGB")
    draw = ImageDraw.Draw(img)
    w, h = img.size
    cx = w // 2

    # 1. Title
    f_title = get_font("cinzel_bold", 58)
    tx, tw = draw_centered(draw, data["title"], 135, f_title, cx=cx)
    # Underline bar
    draw.line((cx - tw // 2 - 20, 208, cx + tw // 2 + 20, 208), fill=INK_DARK, width=2)

    # 2. Subtitle
    f_sub = get_font("cinzel_reg", 28)
    draw_centered(draw, data["subtitle"], 230, f_sub, cx=cx)

    # 3. Description
    f_desc = get_font("garamond_reg", 31)
    draw_wrapped(draw, data["desc"], cx, 300, 1280, f_desc, line_h=42, align="center")

    # 4. Links line (aligned to match 3D clickable hotspot at normalized x=115/764, y=240/1080)
    # In 1528x2160, x ~ 230, y ~ 480
    f_label = get_font("garamond_reg", 32)
    f_link = get_font("garamond_it", 32)
    
    label_txt = data["links_label"]
    link_txt = data["links_text"]
    
    draw.text((110, 475), label_txt, font=f_label, fill=INK_DARK)
    b_label = draw.textbbox((0, 0), label_txt, font=f_label)
    link_x = 110 + (b_label[2] - b_label[0]) + 20
    
    draw.text((link_x, 475), link_txt, font=f_link, fill=INK_DARK)
    b_link = draw.textbbox((0, 0), link_txt, font=f_link)
    link_w = b_link[2] - b_link[0]
    draw.line((link_x, 514, link_x + link_w, 514), fill=INK_DARK, width=2)

    # 4b. CV Download link in links row
    if "cv_text" in data:
        sep_x = link_x + link_w + 30
        draw.text((sep_x, 475), "·", font=f_label, fill=DIVIDER_LINE)
        cv_x = sep_x + 30
        cv_txt = data["cv_text"]
        draw.text((cv_x, 475), cv_txt, font=f_link, fill=INK_DARK)
        b_cv = draw.textbbox((0, 0), cv_txt, font=f_link)
        cv_w = b_cv[2] - b_cv[0]
        draw.line((cv_x, 514, cv_x + cv_w, 514), fill=BORDER_COLOR, width=2)

    # 5. Box frame (Double Renaissance border)
    box_left = 110
    box_top = 580
    box_right = w - 110
    box_bottom = 1580

    # Outer border
    draw.rectangle([box_left, box_top, box_right, box_bottom], outline=BORDER_COLOR, width=2)
    # Inner thin border
    draw.rectangle([box_left + 6, box_top + 6, box_right - 6, box_bottom - 6], outline=BORDER_COLOR, width=1)

    # Box Section Title
    f_sec = get_font("cinzel_reg", 30)
    draw_centered(draw, f"— {data['section_title']} —", box_top + 45, f_sec, cx=cx)

    # Features list inside box
    f_fh = get_font("cinzel_bold", 27)
    f_fb = get_font("garamond_reg", 28)
    
    curr_y = box_top + 130
    for idx, (head_text, body_text) in enumerate(data["features"]):
        draw.text((box_left + 40, curr_y), head_text, font=f_fh, fill=INK_DARK)
        curr_y += 38
        curr_y = draw_wrapped(draw, body_text, box_left + 40, curr_y, (box_right - box_left - 80), f_fb, line_h=38, align="left")
        curr_y += 32

    # 6. Badges
    draw_badge_columns(draw, data["badges"], y_header=1680, y_row1=1735, y_row2=1780)

    # 7. Bottom Quote & Optional Contact Plaque
    f_quote = get_font("garamond_it", 28)
    if data.get("contact_banner"):
        draw_centered(draw, data["quote"], 1865, f_quote, fill=INK_MUTED, cx=cx)
        
        box_b_top = 1925
        box_b_bottom = 2075
        draw.rectangle([box_left, box_b_top, box_right, box_b_bottom], outline=BORDER_COLOR, width=2)
        draw.rectangle([box_left + 4, box_b_top + 4, box_right - 4, box_b_bottom - 4], outline=DIVIDER_LINE, width=1)
        
        f_chead = get_font("cinzel_bold", 23)
        f_clinks = get_font("garamond_reg", 28)
        f_cbtn = get_font("cinzel_bold", 25)
        
        draw_centered(draw, data["contact_head"], box_b_top + 16, f_chead, fill=INK_DARK, cx=cx)
        draw_centered(draw, data["contact_links"], box_b_top + 54, f_clinks, fill=INK_MUTED, cx=cx)
        draw_centered(draw, data["contact_btn"], box_b_top + 98, f_cbtn, fill=(140, 105, 30), cx=cx)
    else:
        draw_centered(draw, data["quote"], 1930, f_quote, fill=INK_MUTED, cx=cx)

    # Save JPG and WEBP
    os.makedirs(os.path.dirname(out_path_jpg), exist_ok=True)
    img.save(out_path_jpg, "JPEG", quality=95)
    out_path_webp = out_path_jpg.replace(".jpg", ".webp")
    img.save(out_path_webp, "WEBP", quality=88)
    print(f"Generated: {out_path_jpg} & {out_path_webp}")

# ==================== PAGE DEFINITIONS ====================

PAGE_29_ES = {
    "title": "ENTERPRISE SECURITY API",
    "subtitle": "ARQUITECTURA HEXAGONAL & DEFENSIVA OWASP EN .NET 9",
    "desc": "API REST empresarial de alta seguridad diseñada bajo Arquitectura Hexagonal en .NET 9, integrando autenticación JWT blindada, cifrado BCrypt, análisis de vulnerabilidades OWASP, rate limiting y CRM seguro de clientes.",
    "links_label": "Enlaces:",
    "links_text": "GitHub (Repositorio Oficial)",
    "cv_text": "Descargar Hoja de Vida (PDF)",
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
    "cv_text": "Download Resume (PDF)",
    "section_title": "CYBERSECURITY MODULES & ACCESS CONTROL",
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
    "quote": "A defensive architecture engineered to secure critical identities and enterprise endpoints with banking-grade standards."
}

PAGE_30_ES = {
    "title": "CAMPUSLANDS ACCESS HUB",
    "subtitle": "GESTIÓN DE ACCESOS, ASISTENCIA Y CERTIFICADOS EN PRODUCCIÓN",
    "desc": "Sistema empresarial desplegado en producción y utilizado por cientos de participantes, con control de asistencia en tiempo real, gestión integral de grupos, emisión automatizada de certificados digitales y seguridad RBAC.",
    "links_label": "Enlaces:",
    "links_text": "GitHub (Repositorio de Producción)",
    "cv_text": "Descargar Hoja de Vida (PDF)",
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
    "quote": "Solución tecnológica de alto impacto en producción que resuelve la gestión académica y operativa.",
    "contact_banner": True,
    "contact_head": "✦ CONTACTO DIRECTO & HOJA DE VIDA ✦",
    "contact_links": "WhatsApp: +57 316 775 5887   ·   LinkedIn   ·   Email",
    "contact_btn": "✦ CLICK PARA DESCARGAR HOJA DE VIDA (PDF) ✦"
}

PAGE_30_EN = {
    "title": "CAMPUSLANDS ACCESS HUB",
    "subtitle": "PRODUCTION ACCESS CONTROL, ATTENDANCE & DIGITAL CERTIFICATES",
    "desc": "Enterprise system deployed to production and actively used by hundreds of participants, featuring real-time attendance tracking, group management, automated digital certificate issuance, and role-based access control (RBAC).",
    "links_label": "Links:",
    "links_text": "GitHub (Production Repository)",
    "cv_text": "Download Resume (PDF)",
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
    "quote": "High-impact production technology solving large-scale academic governance and automated attendance tracking.",
    "contact_banner": True,
    "contact_head": "✦ DIRECT CONTACT & OFFICIAL RESUME ✦",
    "contact_links": "WhatsApp: +57 316 775 5887   ·   LinkedIn   ·   Email",
    "contact_btn": "✦ CLICK TO DOWNLOAD OFFICIAL RESUME (PDF) ✦"
}

if __name__ == "__main__":
    print("=== Generating Clean Project Pages (Pages 29 & 30) ===")
    render_page(PAGE_29_ES, "public/img/pages/fifteen-js.jpg")
    render_page(PAGE_29_EN, "public/img/pages-en/fifteen-js.jpg")
    render_page(PAGE_30_ES, "public/img/pages/the-book.jpg")
    render_page(PAGE_30_EN, "public/img/pages-en/the-book.jpg")
    
    # Also save backups in backup-pages/
    render_page(PAGE_29_ES, "backup-pages/fifteen-js.jpg")
    render_page(PAGE_30_ES, "backup-pages/the-book.jpg")
    print("=== All 4 project pages generated successfully! ===")
