<div align="center">

# 📖 El Libro de Tomás Esteban

**Portafolio interactivo 3D de [Tomás Esteban González Quintero](https://github.com/TEstebanGQ)**  
Full Stack Developer · AI Solutions Integrator · Arquitecto de Software  
📍 Bucaramanga, Santander, Colombia

[![Three.js](https://img.shields.io/badge/Three.js-000000?style=flat&logo=three.js&logoColor=white)](https://threejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat&logo=vite&logoColor=white)](https://vitejs.dev/)
[![GSAP](https://img.shields.io/badge/GSAP-88CE02?style=flat&logo=greensock&logoColor=black)](https://greensock.com/gsap/)

[![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=flat&logo=whatsapp&logoColor=white)](https://wa.me/573167755887)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/tomas-esteban-gonzalez-quintero/)
[![Email](https://img.shields.io/badge/Email-EA4335?style=flat&logo=gmail&logoColor=white)](mailto:tomasestebangonzalezquintero@gmail.com)

</div>

---

## 🌟 ¿Qué es este portafolio?

Una **bitácora técnica en 3D interactiva** que adapta el motor de físicas de páginas de [the-book-of-qbject](https://github.com/Qbject/the-book-of-qbject) con mi información, proyectos, habilidades y contacto. Las páginas se doblan orgánicamente con shaders GLSL procedimentales, exactamente como papel real.

> **Tecnología:** Three.js · TypeScript · Vite · GLSL Shaders · GSAP · Web Audio API

---

## 🗂 Estructura del proyecto

```
.
├── public/
│   ├── img/
│   │   ├── pages/          # Texturas de alta resolución de cada página (JPG, ~1528×2160)
│   │   │   ├── cover-front.jpg   # Portada personalizada con logo TG dorado
│   │   │   ├── who-am-i.jpg      # Perfil, bio, iconos de contacto (GitHub, WhatsApp, LinkedIn)
│   │   │   ├── my-story.jpg      # Historia de formación en Campuslands
│   │   │   ├── skills.jpg        # Mandala de tecnologías (Three.js + zoomable)
│   │   │   └── ...               # Proyectos, trayectoria, intereses, contraportada
│   │   ├── desk.jpg              # Textura del escritorio (escena WebGL)
│   │   └── logo.png              # Logo TG para pantalla de carga
│   └── video/                    # Videos de demo de proyectos
├── src/
│   ├── main.ts           # Punto de entrada: URLs de texturas y áreas interactivas
│   ├── flipbook.ts       # Motor principal del libro 3D (Three.js + GLSL)
│   ├── page.ts           # Geometría y curvatura procedimental de páginas
│   ├── page-curve-helper.ts  # Cálculo de curvas de doblado
│   ├── swipe-handler.ts  # Gestos táctiles y de ratón
│   └── style.css         # Estilos de pantalla de carga y overlay
├── assets/
│   ├── logo_gold.png     # Monograma TG en dorado (portada 3D)
│   ├── logo_clean.png    # Monograma TG en negro (páginas interiores)
│   └── logo_white.png    # Monograma TG en blanco (preloader)
├── index.html            # HTML base con metadata SEO personalizada
├── vite.config.js        # Configuración de Vite
└── tsconfig.json         # Configuración TypeScript
```

---

## 🚀 Instalación y uso local

```bash
# Clonar el repositorio
git clone https://github.com/TEstebanGQ/PORTAFOLIO.git
cd PORTAFOLIO

# Instalar dependencias
npm install

# Servidor de desarrollo con hot-reload
npm run dev

# Build de producción
npm run build

# Previsualizar el build de producción
npm run preview
```

> **Requisito:** Node.js 18+

---

## 📚 Páginas del libro

| # | Página | Contenido |
|---|--------|-----------|
| 0 | Portada | Monograma TG dorado · "El Libro de Tomás Esteban" |
| 1 | Bienvenido | Instrucciones de interacción (deslizar, pantalla completa) |
| 2–3 | Sobre Mí / Quién Soy | Bio, matriz de habilidades, contactos interactivos |
| 4–5 | Mi Historia / Habilidades | Trayectoria en Campuslands · Mandala de tecnologías |
| 6–7 | Intereses / Trayectoria | Áreas de interés · Capítulo de carrera |
| 8–17 | Proyectos | Fichas de cada proyecto con videos demostrativos |
| 30 | El Libro | Descripción del portafolio en sí mismo |
| 31 | Contraportada | Datos de contacto y cierre |

---

## 🔗 Proyectos destacados

| Proyecto | Descripción | Stack |
|----------|-------------|-------|
| 🧠 [campuslands-inteligente](https://github.com/TEstebanGQ/campuslands-inteligente) | Plataforma multi-agente con LangGraph, PyTorch y FastAPI | `Python` `LangGraph` `PyTorch` |
| 📦 [logitrack-wms-springboot](https://github.com/TEstebanGQ/logitrack-wms-springboot) | Sistema WMS empresarial con Spring Boot y JPA | `Java 17` `Spring Boot` `MySQL` |
| ⚙️ [n8n-attendance-ai-workflow](https://github.com/TEstebanGQ/n8n-attendance-ai-workflow) | Automatización de inasistencias con n8n + LLM | `n8n` `OpenRouter` `Telegram` |
| 🔌 [github-mcp-server](https://github.com/TEstebanGQ/github-mcp-server) | Servidor MCP en Node.js para conectar LLMs con GitHub | `Node.js` `MCP Protocol` `Groq` |
| 🎫 [HelpDeskAI](https://github.com/TEstebanGQ/HelpDeskAI) | Sistema de tickets asistido por IA y base de conocimientos | `JavaScript` `OpenRouter` `RAG` |
| 🗄️ [ecommerce-database-4nf](https://github.com/TEstebanGQ/ecommerce-database-4nf) | Base de datos relacional en 4NF con triggers y análisis RFM | `MySQL` `4NF` `Stored Procedures` |
| 🕹️ [softskills-quest](https://github.com/TEstebanGQ/softskills-quest) | Videojuego 2D gamificado con Canvas y Web Audio API | `JavaScript` `Canvas 2D` |

---

## 📬 Contacto directo

| Canal | Enlace |
|-------|--------|
| 💬 WhatsApp | [+57 316 775 5887](https://wa.me/573167755887?text=Hola%20Tom%C3%A1s,%20te%20contacto%20desde%20tu%20portafolio) |
| ✉️ Email | [tomasestebangonzalezquintero@gmail.com](mailto:tomasestebangonzalezquintero@gmail.com) |
| 💼 LinkedIn | [tomas-esteban-gonzalez-quintero](https://www.linkedin.com/in/tomas-esteban-gonzalez-quintero/) |
| 🐙 GitHub | [@TEstebanGQ](https://github.com/TEstebanGQ) |

---

<div align="center">
  <br/>
  <a href="https://github.com/TEstebanGQ">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/TEstebanGQ/TEstebanGQ/main/assets/logo_white.png">
      <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/TEstebanGQ/TEstebanGQ/main/assets/logo_clean.png">
      <img src="https://raw.githubusercontent.com/TEstebanGQ/TEstebanGQ/main/assets/logo_white.png" width="100" alt="TEGQ Brand Logo" />
    </picture>
  </a>
  <br/>
  <sub><b>© Tomas Esteban González Quintero — TEGQ</b></sub>
  <br/><br/>
  <em>Construido con pasión por la ingeniería y el detalle técnico.</em><br/>
  <strong>Tomás Esteban González Quintero · TEGQ · 2025–2026</strong>
</div>


