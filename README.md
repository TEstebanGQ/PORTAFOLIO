# TEGQ // Portfolio

Portafolio one-page de **Tomas Esteban Gonzalez Quintero** — Full Stack Developer.
Estética: neubrutalism híbrido editorial. Animaciones con **GSAP**.

## Stack
- HTML / CSS / JavaScript vanilla — sin build tools, sin bundlers.
- GSAP 3.12 + ScrollTrigger (cargado vía CDN).
- Fuentes: Archivo Black, Space Mono, Fraunces (Google Fonts).

## Estructura
```
.
├── index.html          # markup
├── styles.css          # estilos (mobile-first responsive)
├── script.js           # GSAP + interacciones
└── cv-tomas-gonzalez.pdf  # CV descargable (reemplazar)
```

## Antes de desplegar — checklist

1. **Reemplaza el CV**: pon tu PDF real con el nombre `cv-tomas-gonzalez.pdf` en la raíz.
2. **Actualiza enlaces de redes** en `index.html` (sección `#contact`):
   - GitHub: cambia `https://github.com/` por tu URL real.
   - LinkedIn: cambia `https://www.linkedin.com/` por tu URL real.
   - WhatsApp: cambia `https://wa.me/57` por tu número real (formato `https://wa.me/57XXXXXXXXXX`).
3. **(Opcional)** Cambia el título del navegador o los meta tags de SEO.

## Desplegar en GitHub Pages

```bash
# 1. Inicializa el repo
git init
git add .
git commit -m "feat: portfolio inicial"

# 2. Crea el repo en GitHub y conéctalo
git branch -M main
git remote add origin https://github.com/TU-USUARIO/TU-USUARIO.github.io.git
git push -u origin main
```

> 💡 Tip: si nombras el repo `TU-USUARIO.github.io`, el sitio queda en
> `https://TU-USUARIO.github.io` directamente. Si usas otro nombre,
> queda en `https://TU-USUARIO.github.io/nombre-del-repo`.

3. Activa Pages: **Settings → Pages → Source: `main` / root → Save**.
4. Espera ~1 min y abre la URL.

## Probar localmente

```bash
# Cualquier servidor estático sirve. Por ejemplo con Python:
python3 -m http.server 8080
# → http://localhost:8080
```

O simplemente abre `index.html` en el navegador (algunas features pueden
requerir servidor por CORS de fonts).

## Licencia
Código personal — siéntete libre de inspirarte, pero el contenido (textos,
proyectos) es propio.