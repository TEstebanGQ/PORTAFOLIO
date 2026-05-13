<div align="center">

# ⬛ TEGQ // PORTFOLIO

**Portafolio personal de [Tomas Esteban González Quintero](https://portafolio-tegq.netlify.app/)**  
Full Stack Developer · Bucaramanga, Colombia

[![Netlify Status](https://api.netlify.com/api/v1/badges/placeholder/deploy-status)](https://portafolio-tegq.netlify.app/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![GSAP](https://img.shields.io/badge/GSAP-88CE02?style=flat&logo=greensock&logoColor=black)](https://greensock.com/gsap/)

🌐 **[portafolio-tegq.netlify.app](https://portafolio-tegq.netlify.app/)**

</div>

---

## ✦ Vista previa

> Portafolio one-page de estética **neubrutalism híbrido editorial** — tipografía agresiva, paleta de alto contraste, animaciones GSAP orquestadas y cero dependencias de build.

---

## 🗂 Estructura del proyecto

```
.
├── index.html               # Markup semántico — toda la estructura del sitio
├── styles.css               # Diseño mobile-first, tokens CSS, componentes brutales
├── script.js                # Animaciones GSAP + ScrollTrigger + interacciones
└── cv-tomas-gonzalez.pdf    # CV descargable (reemplazar con tu PDF real)
```

---

## ⚙️ Stack técnico

| Capa | Tecnología |
|------|------------|
| Markup | HTML5 semántico |
| Estilos | CSS3 vanilla — mobile-first, custom properties, sin preprocessadores |
| Animaciones | [GSAP 3.12](https://gsap.com/) + ScrollTrigger (CDN) |
| Fuentes | Archivo Black · Space Mono · Fraunces — vía Google Fonts |
| Deploy | [Netlify](https://netlify.com/) |

> Sin bundlers. Sin frameworks. Sin dependencias de `node_modules` en producción.

---

## ✨ Features

- **Cursor personalizado** con efecto `mix-blend-mode: difference` y trailing ring animado
- **Elementos magnéticos** que reaccionan al mouse (desktop)
- **Timeline de entrada hero** con split de caracteres y animación por stagger
- **Efecto scramble** en el título al hacer hover (caracteres aleatorios → texto original)
- **ScrollTrigger** en secciones: headers, textos, tarjetas de stack, proyectos con parallax
- **Marquee ticker** superior y break de tecnologías animados en CSS puro
- **Navegación responsive** con menú hamburguesa
- **Graceful degradation** — fallback completo si GSAP no carga desde CDN
- **Soporte `prefers-reduced-motion`** — animaciones desactivadas para accesibilidad

---

## 🚀 Correr localmente

No requiere instalación. Cualquier servidor estático sirve:

```bash
# Python (sin instalar nada)
python3 -m http.server 8080
# → http://localhost:8080

# Node.js con npx
npx serve .
# → http://localhost:3000

# O simplemente abrir index.html en el navegador
# (algunas fuentes pueden fallar por CORS sin servidor)
```

---

## 📦 Deploy en Netlify

El sitio está desplegado en **[portafolio-tegq.netlify.app](https://portafolio-tegq.netlify.app/)** vía Netlify con deploy continuo desde el repositorio.

Para tu propio deploy:

1. Conecta tu repo en [netlify.com](https://netlify.com/)
2. Build command: *(vacío — no hay build)*
3. Publish directory: `.` (raíz)
4. ¡Listo!

---

## 📄 Deploy alternativo en GitHub Pages

```bash
# 1. Inicializar repo
git init
git add .
git commit -m "feat: portfolio inicial"

# 2. Conectar con GitHub
git branch -M main
git remote add origin https://github.com/TEstebanGQ/TEstebanGQ.github.io.git
git push -u origin main
```

3. Ir a **Settings → Pages → Source: `main` / root → Save**
4. El sitio queda en `https://TEstebanGQ.github.io`

---

## ✅ Checklist antes de publicar

- [ ] Reemplazar `cv-tomas-gonzalez.pdf` con tu CV real
- [ ] Verificar enlace de GitHub en la sección `#contact`
- [ ] Verificar enlace de LinkedIn (`/in/tomas-esteban-gonzalez-quintero/`)
- [ ] Actualizar enlace de WhatsApp con número real (`https://wa.me/57XXXXXXXXXX`)
- [ ] Revisar meta tags OG (`og:title`, `og:description`, `og:image`)

---

## 🧩 Secciones del sitio

| # | Sección | Contenido |
|---|---------|-----------|
| — | Hero | Nombre, rol, CTA, stickers animados |
| 01 | Sobre mí | Bio, stack filosófico, info-blocks |
| 02 | Proyectos | 4 proyectos seleccionados con SVG ilustrado |
| 03 | Stack técnico | 6 tarjetas por categoría |
| 04 | Contacto | Email · GitHub · LinkedIn |

---

## 📬 Contacto

| Canal | Link |
|-------|------|
| 🌐 Portfolio | [portafolio-tegq.netlify.app](https://portafolio-tegq.netlify.app/) |
| 📧 Email | tomasestebangonzalezquintero@gmail.com |
| 🐙 GitHub | [@TEstebanGQ](https://github.com/TEstebanGQ) |
| 💼 LinkedIn | [Tomas E. González Q.](https://www.linkedin.com/in/tomas-esteban-gonzalez-quintero/) |

---

<div align="center">

**Diseñado y codificado desde cero — Bucaramanga, Colombia ✺**

</div>