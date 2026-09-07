/**
 * ====================================================================
 * TEGQ // 3D INTERACTIVE BOOK ENGINE
 * High-Contrast Editorial Aesthetic, Deep Ink Black Typography,
 * Flush Golden Ribbon, and Subtle Mouse Tilt Parallax.
 * ====================================================================
 */

class Book3DApp {
  constructor(containerId, options = {}) {
    this.container = document.getElementById(containerId);
    if (!this.container) {
      console.error("Book3DApp: Container not found:", containerId);
      return;
    }

    this.options = Object.assign({
      onPageChange: () => {},
      onInteractiveClick: () => {},
      onLoadComplete: () => {},
      soundEnabled: true
    }, options);

    // Book Dimensions
    this.pageWidth = 2.45;
    this.pageHeight = 3.45;
    this.bookThickness = 0.08;

    // Spreads:
    // 0: Portada cerrada
    // 1: Cap. 01 - Portada & Stack Principal (Image 2 style)
    // 2: Cap. 02 - Proyectos I (n8n & MCP)
    // 3: Cap. 03 - Proyectos II (Banco & Campus)
    // 4: Cap. 04 - Stack & Contacto
    // 5: Contraportada
    this.totalSpreads = 6;
    this.currentSpread = 1;
    this.isAnimating = false;

    // Parallax mouse tilt
    this.targetRotationX = 0;
    this.targetRotationY = 0;
    this.currentRotationX = 0;
    this.currentRotationY = 0;

    // Assets
    this.logoTexture = null;
    this.pageTextures = [];

    this.initScene();
    this.initLights();
    this.loadAssetsAndBuild();
    this.bindEvents();

    this.animate = this.animate.bind(this);
    requestAnimationFrame(this.animate);
  }

  /* ------------------------------------------------------------------
     1. THREE.JS SCENE SETUP
  ------------------------------------------------------------------ */
  initScene() {
    const w = this.container.clientWidth;
    const h = this.container.clientHeight;

    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x080d16);

    // Direct frontal camera with perspective
    this.camera = new THREE.PerspectiveCamera(40, w / h, 0.1, 100);
    this.updateCameraPosition();

    this.renderer = new THREE.WebGLRenderer({
      antialias: true,
      powerPreference: "high-performance"
    });
    this.renderer.setSize(w, h);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    // Balanced exposure for high contrast ink
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.0;

    this.container.appendChild(this.renderer.domElement);

    this.raycaster = new THREE.Raycaster();
    this.mouse = new THREE.Vector2();

    this.bookGroup = new THREE.Group();
    this.scene.add(this.bookGroup);
  }

  updateCameraPosition() {
    const isMobile = window.innerWidth <= 768;
    if (isMobile) {
      this.camera.position.set(0, 0, 7.0);
    } else {
      this.camera.position.set(0, 0, 5.15);
    }
    this.camera.lookAt(0, 0, 0);
  }

  /* ------------------------------------------------------------------
     2. BALANCED LIGHTS (NO BLOWN OUT / WASHED OUT TEXT)
  ------------------------------------------------------------------ */
  initLights() {
    // Soft warm ambient
    const ambient = new THREE.AmbientLight(0xfff8ee, 0.55);
    this.scene.add(ambient);

    // Key light for crisp paper definition
    this.keyLight = new THREE.DirectionalLight(0xffffff, 0.65);
    this.keyLight.position.set(3, 5, 5);
    this.keyLight.castShadow = true;
    this.keyLight.shadow.mapSize.width = 2048;
    this.keyLight.shadow.mapSize.height = 2048;
    this.keyLight.shadow.bias = -0.0001;
    this.scene.add(this.keyLight);

    // Soft fill from opposite side
    const fillLight = new THREE.DirectionalLight(0xdbe4ee, 0.35);
    fillLight.position.set(-3, 2, 4);
    this.scene.add(fillLight);

    // Shadow catcher plane behind book
    const shadowGeo = new THREE.PlaneGeometry(12, 10);
    const shadowMat = new THREE.ShadowMaterial({ opacity: 0.45 });
    const shadowMesh = new THREE.Mesh(shadowGeo, shadowMat);
    shadowMesh.position.set(0, 0, -0.15);
    shadowMesh.receiveShadow = true;
    this.scene.add(shadowMesh);
  }

  /* ------------------------------------------------------------------
     3. ASSETS & CANVAS TEXTURES
  ------------------------------------------------------------------ */
  loadAssetsAndBuild() {
    const loader = new THREE.TextureLoader();
    loader.load(
      "assets/logo_clean.png",
      (tex) => {
        this.logoTexture = tex;
        this.buildAll();
      },
      undefined,
      () => {
        this.buildAll();
      }
    );
  }

  buildAll() {
    this.generatePageTextures();
    this.buildBookMeshes();
    this.updateSpreadVisuals();
    this.options.onLoadComplete();
  }

  /* ------------------------------------------------------------------
     4. HIGH-CONTRAST EDITORIAL PAGES GENERATION
  ------------------------------------------------------------------ */
  generatePageTextures() {
    this.texW = 1400;
    this.texH = 1960;
    this.pageTextures = [];

    for (let i = 0; i < 12; i++) {
      const canvas = document.createElement("canvas");
      canvas.width = this.texW;
      canvas.height = this.texH;
      const ctx = canvas.getContext("2d");

      this.renderEditorialPage(ctx, i);

      const tex = new THREE.CanvasTexture(canvas);
      tex.anisotropy = 16;
      tex.minFilter = THREE.LinearMipmapLinearFilter;
      this.pageTextures.push(tex);
    }
  }

  renderEditorialPage(ctx, idx) {
    const W = this.texW;
    const H = this.texH;

    // Warm natural book paper background
    const fillPaper = () => {
      ctx.fillStyle = "#F5EEDC";
      ctx.fillRect(0, 0, W, H);

      // Subtle paper fibers
      ctx.fillStyle = "rgba(0, 0, 0, 0.015)";
      for (let i = 0; i < 40; i++) {
        const y = Math.random() * H;
        ctx.fillRect(0, y, W, 1);
      }
    };

    // Badge helper with deep ink black text and crisp borders
    const drawBadge = (text, x, y) => {
      ctx.font = "700 26px 'Space Mono', monospace";
      const metrics = ctx.measureText(text);
      const padX = 24;
      const padY = 16;
      const bW = metrics.width + padX * 2;
      const bH = 56;

      ctx.fillStyle = "#ffffff";
      ctx.fillRect(x, y - padY - 14, bW, bH);
      ctx.strokeStyle = "#1e293b";
      ctx.lineWidth = 2.5;
      ctx.strokeRect(x, y - padY - 14, bW, bH);

      ctx.fillStyle = "#000000";
      ctx.fillText(text, x + padX, y + 16);
      return bW + 18;
    };

    switch (idx) {
      // -------------------------------------------------------------
      // 0: PORTADA CERRADA
      // -------------------------------------------------------------
      case 0:
        ctx.fillStyle = "#121722";
        ctx.fillRect(0, 0, W, H);

        ctx.strokeStyle = "#cda34f";
        ctx.lineWidth = 6;
        ctx.strokeRect(70, 70, W - 140, H - 140);
        ctx.strokeRect(86, 86, W - 172, H - 172);

        if (this.logoTexture && this.logoTexture.image) {
          const sz = 400;
          ctx.drawImage(this.logoTexture.image, W / 2 - sz / 2, H / 2 - sz / 2 - 110, sz, sz);
        }

        ctx.fillStyle = "#cda34f";
        ctx.font = "700 28px 'Space Mono', monospace";
        ctx.textAlign = "center";
        ctx.fillText("BITÁCORA TÉCNICA // VOL. 01", W / 2, 220);

        ctx.font = "italic 700 78px 'Fraunces', Georgia, serif";
        ctx.fillStyle = "#ffffff";
        ctx.fillText("Tomas Esteban", W / 2, H / 2 + 190);
        ctx.fillText("González Quintero", W / 2, H / 2 + 280);

        ctx.fillStyle = "#cda34f";
        ctx.font = "700 26px 'Space Mono', monospace";
        ctx.fillText("FULL STACK JUNIOR DEVELOPER", W / 2, H / 2 + 360);

        ctx.fillStyle = "#ffffff";
        ctx.font = "700 24px 'Space Mono', monospace";
        ctx.fillText("CLIC O 'SIGUIENTE' PARA ABRIR ▶", W / 2, H - 140);
        break;

      // -------------------------------------------------------------
      // 1: INTERIOR PORTADA
      // -------------------------------------------------------------
      case 1:
        ctx.fillStyle = "#151a24";
        ctx.fillRect(0, 0, W, H);
        ctx.fillStyle = "#64748b";
        ctx.font = "700 24px 'Space Mono', monospace";
        ctx.textAlign = "center";
        ctx.fillText("TEGQ ARCHIVE  •  EDICIÓN 2025", W / 2, H / 2);
        break;

      // -------------------------------------------------------------
      // 2: CAP. 01 — PORTADA IZQUIERDA (HIGH CONTRAST BOLD)
      // -------------------------------------------------------------
      case 2:
        fillPaper();

        // Top chapter tag (bold dark slate)
        ctx.fillStyle = "#0f172a";
        ctx.font = "700 26px 'Space Mono', monospace";
        ctx.textAlign = "left";
        ctx.fillText("CAP. 01 — PORTADA", 130, 180);

        // Big elegant title (Pure Rich Black)
        ctx.fillStyle = "#000000";
        ctx.font = "italic 700 84px 'Fraunces', Georgia, serif";
        ctx.fillText("Tomas Esteban", 130, 310);
        ctx.fillText("González Quintero", 130, 405);

        // Subtitle (Bold Deep Ink)
        ctx.fillStyle = "#1e293b";
        ctx.font = "700 32px 'Space Mono', monospace";
        ctx.fillText("Full Stack Junior Developer", 130, 490);

        // Bio text (Crisp Black and legible)
        ctx.fillStyle = "#0a0a0a";
        ctx.font = "700 30px/1.5 'Space Mono', monospace";
        const linesBio = [
          "Construyo productos de punta a punta:",
          "automatizaciones con n8n, backends en Node y",
          "Python, integraciones de IA y bots que hacen el",
          "trabajo repetitivo por vos."
        ];
        linesBio.forEach((line, lIdx) => {
          ctx.fillText(line, 130, 600 + lIdx * 56);
        });

        // Link button (Dark amber with thick underline)
        ctx.fillStyle = "#92400e";
        ctx.font = "700 30px 'Space Mono', monospace";
        ctx.fillText("→ VER PROYECTOS", 130, 920);

        ctx.strokeStyle = "#92400e";
        ctx.lineWidth = 3.5;
        ctx.beginPath();
        ctx.moveTo(130, 938);
        ctx.lineTo(440, 938);
        ctx.stroke();

        // Page number bottom-left
        ctx.fillStyle = "#334155";
        ctx.font = "700 28px 'Space Mono', monospace";
        ctx.fillText("01", 130, H - 120);
        break;

      // -------------------------------------------------------------
      // 3: CAP. 01 — DERECHA: STACK PRINCIPAL (HIGH CONTRAST)
      // -------------------------------------------------------------
      case 3:
        fillPaper();

        // Header
        ctx.fillStyle = "#0f172a";
        ctx.font = "700 26px 'Space Mono', monospace";
        ctx.textAlign = "left";
        ctx.fillText("STACK PRINCIPAL", 130, 180);

        // Badges Row 1
        let bx = 130;
        let by = 265;
        bx += drawBadge("Node.js", bx, by);
        bx += drawBadge("Python", bx, by);
        bx += drawBadge("n8n", bx, by);
        bx += drawBadge("Supabase", bx, by);
        drawBadge("PostgreSQL", bx, by);

        // Badges Row 2
        bx = 130;
        by = 350;
        bx += drawBadge("Docker", bx, by);
        bx += drawBadge("LangChain", bx, by);
        bx += drawBadge("GSAP", bx, by);
        drawBadge(".NET 8", bx, by);

        // Divider
        ctx.strokeStyle = "#94a3b8";
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.moveTo(130, 450);
        ctx.lineTo(W - 130, 450);
        ctx.stroke();

        // 3 Stats columns
        const stats = [
          { val: "6+", label: "PROYECTOS SHIP.", x: 130 },
          { val: "2025", label: "TEC. DESARROLLO SW", x: 480 },
          { val: "IA", label: "INTEGRACIONES", x: 860 }
        ];

        stats.forEach((st) => {
          ctx.fillStyle = "#000000";
          ctx.font = "900 62px 'Fraunces', serif";
          ctx.fillText(st.val, st.x, 545);

          ctx.fillStyle = "#1e293b";
          ctx.font = "700 20px 'Space Mono', monospace";
          ctx.fillText(st.label, st.x, 595);
        });

        // Detail Box
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(130, 700, W - 260, 440);
        ctx.strokeStyle = "#1e293b";
        ctx.lineWidth = 2.5;
        ctx.strokeRect(130, 700, W - 260, 440);

        ctx.fillStyle = "#000000";
        ctx.font = "700 28px 'Space Mono', monospace";
        ctx.fillText("CAMPUSLANDS // FORMACIÓN INTENSA", 170, 770);

        ctx.fillStyle = "#0f172a";
        ctx.font = "700 26px/1.5 'Space Mono', monospace";
        const bioDetail = [
          "Enfoque riguroso en arquitectura limpia,",
          "bases de datos relacionales normalizadas",
          "hasta 4NF, y código listo para producción",
          "sin dependencias frágiles.",
          "Disponible para nuevos desafíos y contratación."
        ];
        bioDetail.forEach((bd, idx) => {
          ctx.fillText(bd, 170, 840 + idx * 50);
        });

        // Page number bottom-right
        ctx.fillStyle = "#334155";
        ctx.font = "700 28px 'Space Mono', monospace";
        ctx.textAlign = "right";
        ctx.fillText("02", W - 130, H - 120);
        break;

      // -------------------------------------------------------------
      // 4: CAP. 02 — PROYECTO 01 (n8n WORKFLOW)
      // -------------------------------------------------------------
      case 4:
        fillPaper();
        ctx.fillStyle = "#0f172a";
        ctx.font = "700 26px 'Space Mono', monospace";
        ctx.textAlign = "left";
        ctx.fillText("CAP. 02 — PROYECTO SELECCIONADO", 130, 180);

        ctx.fillStyle = "#000000";
        ctx.font = "italic 700 68px 'Fraunces', serif";
        ctx.fillText("Sistema de Justificación", 130, 280);
        ctx.fillText("Escolar Automatizado", 130, 360);

        ctx.fillStyle = "#1e293b";
        ctx.font = "700 24px 'Space Mono', monospace";
        ctx.fillText("n8n  •  OpenRouter AI  •  Telegram Bot  •  Sheets DB", 130, 430);

        // Diagram Frame
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(130, 480, W - 260, 360);
        ctx.strokeStyle = "#000000";
        ctx.lineWidth = 2.5;
        ctx.strokeRect(130, 480, W - 260, 360);

        const flowNodes = [
          { name: "FORM WEB", sub: "Ingest público", x: 180, y: 540, c: "#fef08a" },
          { name: "AI PARSER", sub: "OpenRouter GPT", x: 450, y: 540, c: "#bae6fd" },
          { name: "SHEETS DB", sub: "Persistencia 4NF", x: 730, y: 540, c: "#fbcfe8" },
          { name: "BOT TELEGRAM", sub: "Alerta Docentes", x: 730, y: 690, c: "#bbf7d0" }
        ];

        flowNodes.forEach(fn => {
          ctx.fillStyle = fn.c;
          ctx.fillRect(fn.x, fn.y, 220, 95);
          ctx.strokeStyle = "#000000";
          ctx.lineWidth = 2.5;
          ctx.strokeRect(fn.x, fn.y, 220, 95);

          ctx.fillStyle = "#000000";
          ctx.font = "700 20px 'Space Mono', monospace";
          ctx.fillText(fn.name, fn.x + 18, fn.y + 42);
          ctx.font = "700 15px 'Space Mono', monospace";
          ctx.fillText(fn.sub, fn.x + 18, fn.y + 72);
        });

        // Description
        ctx.fillStyle = "#0a0a0a";
        ctx.font = "700 28px/1.5 'Space Mono', monospace";
        const n8nDesc = [
          "Workflow de automatización en n8n que orquesta un",
          "formulario público, clasificación AI vía OpenRouter,",
          "archivos en Drive, Sheets como base de datos y un",
          "bot de Telegram para coordinadores docentes.",
          "Solucioné deadlocks en merge nodes y loops infinitos."
        ];
        n8nDesc.forEach((d, i) => ctx.fillText(d, 130, 910 + i * 50));

        ctx.fillStyle = "#92400e";
        ctx.font = "700 28px 'Space Mono', monospace";
        ctx.fillText("→ VER REPOSITORIO EN GITHUB", 130, 1220);

        ctx.fillStyle = "#334155";
        ctx.font = "700 28px 'Space Mono', monospace";
        ctx.fillText("03", 130, H - 120);
        break;

      // -------------------------------------------------------------
      // 5: CAP. 02 — PROYECTO 02 (GITHUB MCP SERVER)
      // -------------------------------------------------------------
      case 5:
        fillPaper();
        ctx.fillStyle = "#0f172a";
        ctx.font = "700 26px 'Space Mono', monospace";
        ctx.textAlign = "left";
        ctx.fillText("CAP. 02 — PROYECTO SELECCIONADO", 130, 180);

        ctx.fillStyle = "#000000";
        ctx.font = "italic 700 68px 'Fraunces', serif";
        ctx.fillText("GitHub MCP Server", 130, 280);
        ctx.fillText("CLI Conversacional", 130, 360);

        ctx.fillStyle = "#1e293b";
        ctx.font = "700 24px 'Space Mono', monospace";
        ctx.fillText("Node.js  •  Model Context Protocol  •  Groq  •  LLaMA 3.3", 130, 430);

        // Terminal mockup
        ctx.fillStyle = "#0b0f19";
        ctx.fillRect(130, 480, W - 260, 360);
        ctx.strokeStyle = "#1e293b";
        ctx.lineWidth = 2.5;
        ctx.strokeRect(130, 480, W - 260, 360);

        const cliLines = [
          { c: "#cbd5e1", t: "$ mcp connect github-cli" },
          { c: "#38bdf8", t: "→ Model Context Protocol (v2024-11) ready" },
          { c: "#ffffff", t: '$ "Crea un repositorio para backend .NET"' },
          { c: "#fbbf24", t: "→ Parsing intent & calling github.createRepo()" },
          { c: "#4ade80", t: "✓ Status: 201 Created — https://github.com/TEstebanGQ" }
        ];
        cliLines.forEach((cl, i) => {
          ctx.fillStyle = cl.c;
          ctx.font = "700 22px 'Space Mono', monospace";
          ctx.fillText(cl.t, 160, 550 + i * 50);
        });

        ctx.fillStyle = "#0a0a0a";
        ctx.font = "700 28px/1.5 'Space Mono', monospace";
        const mcpDesc = [
          "Servidor MCP en Node que expone la API de GitHub",
          "a un LLM (LLaMA via Groq) para gestión por lenguaje",
          "natural desde CLI. Crear repos, abrir issues y",
          "listar PRs de forma conversacional sin wrappers opacos."
        ];
        mcpDesc.forEach((d, i) => ctx.fillText(d, 130, 910 + i * 50));

        ctx.fillStyle = "#92400e";
        ctx.font = "700 28px 'Space Mono', monospace";
        ctx.fillText("→ VER CÓDIGO EN GITHUB", 130, 1220);

        ctx.fillStyle = "#334155";
        ctx.font = "700 28px 'Space Mono', monospace";
        ctx.textAlign = "right";
        ctx.fillText("04", W - 130, H - 120);
        break;

      // -------------------------------------------------------------
      // 6: CAP. 03 — PROYECTO 03 (BANCO ACME)
      // -------------------------------------------------------------
      case 6:
        fillPaper();
        ctx.fillStyle = "#0f172a";
        ctx.font = "700 26px 'Space Mono', monospace";
        ctx.textAlign = "left";
        ctx.fillText("CAP. 03 — CASO DE ESTUDIO", 130, 180);

        ctx.fillStyle = "#000000";
        ctx.font = "italic 700 68px 'Fraunces', serif";
        ctx.fillText("Banco ACME", 130, 280);
        ctx.fillText("Vanilla JS SPA", 130, 360);

        ctx.fillStyle = "#1e293b";
        ctx.font = "700 24px 'Space Mono', monospace";
        ctx.fillText("JavaScript Puro  •  localStorage  •  CSS3 Tokens", 130, 430);

        // Card Graphic
        ctx.fillStyle = "#111827";
        ctx.fillRect(130, 480, 420, 240);
        ctx.fillStyle = "#FFE600";
        ctx.font = "900 32px 'Fraunces', serif";
        ctx.fillText("ACME BANK", 160, 545);
        ctx.font = "700 22px 'Space Mono', monospace";
        ctx.fillText("**** **** 7445", 160, 620);
        ctx.fillText("T. GONZALEZ", 160, 675);

        ctx.fillStyle = "#ffffff";
        ctx.fillRect(590, 480, W - 720, 240);
        ctx.strokeStyle = "#000000";
        ctx.lineWidth = 2.5;
        ctx.strokeRect(590, 480, W - 720, 240);

        ctx.fillStyle = "#475569";
        ctx.font = "700 20px 'Space Mono', monospace";
        ctx.fillText("SALDO CUENTA", 630, 545);
        ctx.fillStyle = "#000000";
        ctx.font = "900 52px 'Fraunces', serif";
        ctx.fillText("$ 12,450.00", 630, 615);
        ctx.fillStyle = "#15803d";
        ctx.font = "700 20px 'Space Mono', monospace";
        ctx.fillText("✓ Transferencias SPA", 630, 675);

        ctx.fillStyle = "#0a0a0a";
        ctx.font = "700 28px/1.5 'Space Mono', monospace";
        const bankDesc = [
          "Aplicación bancaria interactiva construida en JavaScript",
          "puro sin frameworks. Flujo multi-pantalla, validación",
          "estricta de saldos y persistencia con Web Storage.",
          "Proyecto base para dominar fundamentos nativos."
        ];
        bankDesc.forEach((d, i) => ctx.fillText(d, 130, 800 + i * 50));

        ctx.fillStyle = "#92400e";
        ctx.font = "700 28px 'Space Mono', monospace";
        ctx.fillText("→ VER DEMO / CÓDIGO", 130, 1120);

        ctx.fillStyle = "#334155";
        ctx.font = "700 28px 'Space Mono', monospace";
        ctx.fillText("05", 130, H - 120);
        break;

      // -------------------------------------------------------------
      // 7: CAP. 03 — PROYECTO 04 (CAMPUS BUILD)
      // -------------------------------------------------------------
      case 7:
        fillPaper();
        ctx.fillStyle = "#0f172a";
        ctx.font = "700 26px 'Space Mono', monospace";
        ctx.textAlign = "left";
        ctx.fillText("CAP. 03 — CASO DE ESTUDIO", 130, 180);

        ctx.fillStyle = "#000000";
        ctx.font = "italic 700 68px 'Fraunces', serif";
        ctx.fillText("Campus Build", 130, 280);
        ctx.fillText("Gestión Modular Gantt", 130, 360);

        ctx.fillStyle = "#1e293b";
        ctx.font = "700 24px 'Space Mono', monospace";
        ctx.fillText("JS Modular  •  Gantt  •  Event Delegation  •  JSON Sync", 130, 430);

        ctx.fillStyle = "#ffffff";
        ctx.fillRect(130, 480, W - 260, 260);
        ctx.strokeStyle = "#000000";
        ctx.lineWidth = 2.5;
        ctx.strokeRect(130, 480, W - 260, 260);

        const kCols = ["TODO", "IN PROGRESS", "DONE"];
        kCols.forEach((kc, i) => {
          const kx = 160 + i * 350;
          ctx.fillStyle = "#f1f5f9";
          ctx.fillRect(kx, 510, 320, 200);
          ctx.strokeStyle = "#0f172a";
          ctx.lineWidth = 2;
          ctx.strokeRect(kx, 510, 320, 200);

          ctx.fillStyle = "#000000";
          ctx.font = "700 20px 'Space Mono', monospace";
          ctx.fillText(kc, kx + 20, 555);
        });

        ctx.fillStyle = "#0a0a0a";
        ctx.font = "700 28px/1.5 'Space Mono', monospace";
        const campusDesc = [
          "Web app de gestión de proyectos y actividades estilo",
          "Gantt construida con arquitectura modular por capas.",
          "Event delegation eficiente, utilidades de fechas",
          "y exportación de backups en formato JSON."
        ];
        campusDesc.forEach((d, i) => ctx.fillText(d, 130, 800 + i * 50));

        ctx.fillStyle = "#92400e";
        ctx.font = "700 28px 'Space Mono', monospace";
        ctx.fillText("→ VER DEMO / CÓDIGO", 130, 1120);

        ctx.fillStyle = "#334155";
        ctx.font = "700 28px 'Space Mono', monospace";
        ctx.textAlign = "right";
        ctx.fillText("06", W - 130, H - 120);
        break;

      // -------------------------------------------------------------
      // 8: CAP. 04 — STACK COMPLETO
      // -------------------------------------------------------------
      case 8:
        fillPaper();
        ctx.fillStyle = "#0f172a";
        ctx.font = "700 26px 'Space Mono', monospace";
        ctx.textAlign = "left";
        ctx.fillText("CAP. 04 — COMPETENCIAS TÉCNICAS", 130, 180);

        ctx.fillStyle = "#000000";
        ctx.font = "italic 700 68px 'Fraunces', serif";
        ctx.fillText("Stack & Arquitectura", 130, 280);

        const categories = [
          { cat: "BACKEND & ARQUITECTURA", items: [".NET 8", "C#", "Node.js", "Arquitectura Hexagonal", "Supabase"] },
          { cat: "FRONTEND & MOBILE", items: ["React Native", "Expo", "JavaScript Vanilla", "HTML5/CSS3"] },
          { cat: "BASES DE DATOS & DATA", items: ["PostgreSQL", "MySQL", "Diseño 4NF", "Stored Procedures"] },
          { cat: "AUTOMATIZACIÓN & AI", items: ["n8n Self-Hosted", "OpenRouter AI", "Telegram Bots", "Webhooks"] },
          { cat: "DEVOPS & HERRAMIENTAS", items: ["Git & GitHub", "Docker", "Arch Linux", "Scrum"] }
        ];

        let ty = 370;
        categories.forEach((cat) => {
          ctx.fillStyle = "#000000";
          ctx.font = "700 24px 'Space Mono', monospace";
          ctx.fillText(`// ${cat.cat}`, 130, ty);

          let itemX = 130;
          let itemY = ty + 50;
          cat.items.forEach((it) => {
            itemX += drawBadge(it, itemX, itemY);
          });

          ty += 145;
        });

        ctx.fillStyle = "#334155";
        ctx.font = "700 28px 'Space Mono', monospace";
        ctx.fillText("07", 130, H - 120);
        break;

      // -------------------------------------------------------------
      // 9: CAP. 05 — CONTACTO & WHATSAPP
      // -------------------------------------------------------------
      case 9:
        fillPaper();
        ctx.fillStyle = "#0f172a";
        ctx.font = "700 26px 'Space Mono', monospace";
        ctx.textAlign = "left";
        ctx.fillText("CAP. 05 — TRANSMISIÓN DIRECTA", 130, 180);

        ctx.fillStyle = "#000000";
        ctx.font = "italic 700 68px 'Fraunces', serif";
        ctx.fillText("¿Hablamos de tu Proyecto?", 130, 280);

        ctx.fillStyle = "#0f172a";
        ctx.font = "700 28px/1.5 'Space Mono', monospace";
        const contactIntro = [
          "Disponible para vacantes de desarrollador full stack,",
          "contratos freelance y desarrollo de automatizaciones.",
          "Conectemos de inmediato a través de estos canales:"
        ];
        contactIntro.forEach((ci, i) => ctx.fillText(ci, 130, 360 + i * 50));

        // WhatsApp card
        ctx.fillStyle = "#dcfce7";
        ctx.fillRect(130, 550, W - 260, 160);
        ctx.strokeStyle = "#15803d";
        ctx.lineWidth = 2.5;
        ctx.strokeRect(130, 550, W - 260, 160);

        ctx.fillStyle = "#14532d";
        ctx.font = "900 28px 'Space Mono', monospace";
        ctx.fillText("💬 WHATSAPP DIRECTO", 170, 615);
        ctx.font = "700 24px 'Space Mono', monospace";
        ctx.fillText("+57 316 775 5887  (CLIC PARA CHATEAR)", 170, 668);

        // Form card
        ctx.fillStyle = "#fef9c3";
        ctx.fillRect(130, 750, W - 260, 160);
        ctx.strokeStyle = "#a16207";
        ctx.lineWidth = 2.5;
        ctx.strokeRect(130, 750, W - 260, 160);

        ctx.fillStyle = "#713f12";
        ctx.font = "900 28px 'Space Mono', monospace";
        ctx.fillText("✉ FORMULARIO OFICIAL DE CONTACTO", 170, 815);
        ctx.font = "700 24px 'Space Mono', monospace";
        ctx.fillText("Motivo, requerimientos y cotización en 1 clic", 170, 868);

        // Direct info
        ctx.fillStyle = "#000000";
        ctx.font = "700 24px 'Space Mono', monospace";
        ctx.fillText("📧 tomasestebangonzalezquintero@gmail.com", 130, 980);
        ctx.fillText("🐙 GitHub: @TEstebanGQ", 130, 1030);
        ctx.fillText("💼 LinkedIn: Tomas E. González Q.", 130, 1080);

        ctx.fillStyle = "#334155";
        ctx.font = "700 28px 'Space Mono', monospace";
        ctx.textAlign = "right";
        ctx.fillText("08", W - 130, H - 120);
        break;

      // -------------------------------------------------------------
      // 10 & 11: CONTRAPORTADA
      // -------------------------------------------------------------
      case 10:
        ctx.fillStyle = "#151a24";
        ctx.fillRect(0, 0, W, H);
        break;

      case 11:
        ctx.fillStyle = "#121722";
        ctx.fillRect(0, 0, W, H);
        ctx.strokeStyle = "#cda34f";
        ctx.lineWidth = 4;
        ctx.strokeRect(80, 80, W - 160, H - 160);

        if (this.logoTexture && this.logoTexture.image) {
          const sz = 280;
          ctx.drawImage(this.logoTexture.image, W / 2 - sz / 2, H / 2 - sz / 2 - 40, sz, sz);
        }

        ctx.fillStyle = "#ffffff";
        ctx.font = "700 24px 'Space Mono', monospace";
        ctx.textAlign = "center";
        ctx.fillText("TEGQ // ARCHIVE", W / 2, H / 2 + 160);
        ctx.fillStyle = "#cda34f";
        ctx.fillText("BUCARAMANGA, COLOMBIA ✺", W / 2, H / 2 + 205);
        break;
    }
  }

  /* ------------------------------------------------------------------
     5. BUILD BOOK MESHES (FLUSH GOLDEN RIBBON)
  ------------------------------------------------------------------ */
  buildBookMeshes() {
    this.coverGroup = new THREE.Group();
    this.bookGroup.add(this.coverGroup);

    this.spineWidth = 0.12;

    // Left Page Mesh
    const pageGeoLeft = new THREE.PlaneGeometry(this.pageWidth, this.pageHeight, 16, 2);
    pageGeoLeft.translate(-this.pageWidth / 2 - this.spineWidth / 2, 0, 0.02);

    this.leftPageMat = new THREE.MeshStandardMaterial({
      roughness: 0.9,
      metalness: 0.05,
      side: THREE.FrontSide
    });
    this.leftPageMesh = new THREE.Mesh(pageGeoLeft, this.leftPageMat);
    this.leftPageMesh.receiveShadow = true;
    this.coverGroup.add(this.leftPageMesh);

    // Right Page Mesh
    const pageGeoRight = new THREE.PlaneGeometry(this.pageWidth, this.pageHeight, 16, 2);
    pageGeoRight.translate(this.pageWidth / 2 + this.spineWidth / 2, 0, 0.02);

    this.rightPageMat = new THREE.MeshStandardMaterial({
      roughness: 0.9,
      metalness: 0.05,
      side: THREE.FrontSide
    });
    this.rightPageMesh = new THREE.Mesh(pageGeoRight, this.rightPageMat);
    this.rightPageMesh.receiveShadow = true;
    this.coverGroup.add(this.rightPageMesh);

    // Center Gold Ribbon (Flush with page edges, no protrusion)
    const ribbonGeo = new THREE.PlaneGeometry(0.065, this.pageHeight);
    const ribbonMat = new THREE.MeshStandardMaterial({
      color: 0xcda34f,
      roughness: 0.35,
      metalness: 0.75
    });
    this.ribbonMesh = new THREE.Mesh(ribbonGeo, ribbonMat);
    this.ribbonMesh.position.set(0, 0, 0.028);
    this.ribbonMesh.castShadow = true;
    this.coverGroup.add(this.ribbonMesh);

    // Back Cover (depth border)
    const coverGeo = new THREE.BoxGeometry(
      (this.pageWidth + 0.08) * 2 + this.spineWidth,
      this.pageHeight + 0.12,
      this.bookThickness
    );
    const coverMat = new THREE.MeshStandardMaterial({
      color: 0x141824,
      roughness: 0.6,
      metalness: 0.2
    });
    this.backCoverMesh = new THREE.Mesh(coverGeo, coverMat);
    this.backCoverMesh.position.set(0, 0, -this.bookThickness / 2);
    this.backCoverMesh.castShadow = true;
    this.backCoverMesh.receiveShadow = true;
    this.coverGroup.add(this.backCoverMesh);

    // Flipping Page Pivot & Mesh
    this.flippingPivot = new THREE.Group();
    this.flippingPivot.position.set(0, 0, 0.025);
    this.coverGroup.add(this.flippingPivot);

    this.flipSegments = 32;
    this.flipGeo = new THREE.PlaneGeometry(this.pageWidth, this.pageHeight, this.flipSegments, 2);
    this.flipGeo.translate(this.pageWidth / 2 + this.spineWidth / 2, 0, 0);
    this.flipOriginalPositions = this.flipGeo.attributes.position.array.slice();

    this.flipFrontMat = new THREE.MeshStandardMaterial({
      roughness: 0.9,
      metalness: 0.05,
      side: THREE.FrontSide
    });
    this.flipBackMat = new THREE.MeshStandardMaterial({
      roughness: 0.9,
      metalness: 0.05,
      side: THREE.BackSide
    });

    this.flipFrontMesh = new THREE.Mesh(this.flipGeo, this.flipFrontMat);
    this.flipFrontMesh.castShadow = true;
    this.flippingPivot.add(this.flipFrontMesh);

    const flipBackGeo = this.flipGeo.clone();
    this.flipBackMesh = new THREE.Mesh(flipBackGeo, this.flipBackMat);
    this.flipBackMesh.castShadow = true;
    this.flippingPivot.add(this.flipBackMesh);

    this.flippingPivot.visible = false;
  }

  /* ------------------------------------------------------------------
     6. SPREAD UPDATES
  ------------------------------------------------------------------ */
  updateSpreadVisuals() {
    if (this.currentSpread === 0) {
      this.leftPageMesh.visible = false;
      this.rightPageMesh.visible = true;
      this.rightPageMat.map = this.pageTextures[0];
      this.rightPageMat.needsUpdate = true;
      this.ribbonMesh.visible = false;
    } else if (this.currentSpread === 5) {
      this.leftPageMesh.visible = true;
      this.rightPageMesh.visible = false;
      this.leftPageMat.map = this.pageTextures[11];
      this.leftPageMat.needsUpdate = true;
      this.ribbonMesh.visible = false;
    } else {
      this.leftPageMesh.visible = true;
      this.rightPageMesh.visible = true;
      this.ribbonMesh.visible = true;

      const leftIdx = this.currentSpread * 2;
      const rightIdx = this.currentSpread * 2 + 1;

      this.leftPageMat.map = this.pageTextures[leftIdx];
      this.leftPageMat.needsUpdate = true;

      this.rightPageMat.map = this.pageTextures[rightIdx];
      this.rightPageMat.needsUpdate = true;
    }

    this.options.onPageChange(this.currentSpread, this.totalSpreads);
  }

  /* ------------------------------------------------------------------
     7. ANIMATED PAGE FLIP WITH PROCEDURAL BENDING
  ------------------------------------------------------------------ */
  turnPage(dir) {
    if (this.isAnimating) return;
    const targetSpread = this.currentSpread + dir;
    if (targetSpread < 0 || targetSpread >= this.totalSpreads) return;

    this.isAnimating = true;
    this.playPaperSound();

    if (typeof gsap === "undefined") {
      this.currentSpread = targetSpread;
      this.updateSpreadVisuals();
      this.isAnimating = false;
      return;
    }

    if (dir > 0) {
      const currentRightIdx = this.currentSpread * 2 + 1;
      const nextLeftIdx = targetSpread * 2;
      const nextRightIdx = targetSpread * 2 + 1;

      this.flipFrontMat.map = this.pageTextures[currentRightIdx];
      this.flipFrontMat.needsUpdate = true;
      this.flipBackMat.map = this.pageTextures[nextLeftIdx];
      this.flipBackMat.needsUpdate = true;

      if (targetSpread <= 4) {
        this.rightPageMat.map = this.pageTextures[nextRightIdx];
        this.rightPageMat.needsUpdate = true;
      }

      this.flippingPivot.visible = true;
      this.flippingPivot.rotation.y = 0;

      const animObj = { angle: 0 };
      gsap.to(animObj, {
        angle: -Math.PI,
        duration: 0.75,
        ease: "power2.inOut",
        onUpdate: () => {
          this.flippingPivot.rotation.y = animObj.angle;
          const prog = Math.abs(animObj.angle) / Math.PI;
          const bend = Math.sin(prog * Math.PI) * 0.4;
          this.applyPageBend(bend);
        },
        onComplete: () => {
          this.flippingPivot.visible = false;
          this.resetPageBend();
          this.currentSpread = targetSpread;
          this.updateSpreadVisuals();
          this.isAnimating = false;
        }
      });
    } else {
      const currentLeftIdx = this.currentSpread * 2;
      const prevRightIdx = targetSpread * 2 + 1;
      const prevLeftIdx = targetSpread * 2;

      this.flipFrontMat.map = this.pageTextures[prevRightIdx];
      this.flipFrontMat.needsUpdate = true;
      this.flipBackMat.map = this.pageTextures[currentLeftIdx];
      this.flipBackMat.needsUpdate = true;

      if (targetSpread >= 1) {
        this.leftPageMat.map = this.pageTextures[prevLeftIdx];
        this.leftPageMat.needsUpdate = true;
      }

      this.flippingPivot.visible = true;
      this.flippingPivot.rotation.y = -Math.PI;

      const animObj = { angle: -Math.PI };
      gsap.to(animObj, {
        angle: 0,
        duration: 0.75,
        ease: "power2.inOut",
        onUpdate: () => {
          this.flippingPivot.rotation.y = animObj.angle;
          const prog = 1.0 - Math.abs(animObj.angle) / Math.PI;
          const bend = -Math.sin(prog * Math.PI) * 0.4;
          this.applyPageBend(bend);
        },
        onComplete: () => {
          this.flippingPivot.visible = false;
          this.resetPageBend();
          this.currentSpread = targetSpread;
          this.updateSpreadVisuals();
          this.isAnimating = false;
        }
      });
    }
  }

  applyPageBend(amount) {
    const pos = this.flipGeo.attributes.position.array;
    const orig = this.flipOriginalPositions;
    for (let i = 0; i < pos.length; i += 3) {
      const x = orig[i];
      const normX = (x - this.spineWidth / 2) / this.pageWidth;
      const zOffset = Math.sin(normX * Math.PI) * amount;
      pos[i + 2] = orig[i + 2] + zOffset;
    }
    this.flipGeo.attributes.position.needsUpdate = true;
    this.flipGeo.computeVertexNormals();
  }

  resetPageBend() {
    const pos = this.flipGeo.attributes.position.array;
    const orig = this.flipOriginalPositions;
    for (let i = 0; i < pos.length; i++) {
      pos[i] = orig[i];
    }
    this.flipGeo.attributes.position.needsUpdate = true;
    this.flipGeo.computeVertexNormals();
  }

  /* ------------------------------------------------------------------
     8. WEB AUDIO PROCEDURAL FLIP SOUND
  ------------------------------------------------------------------ */
  playPaperSound() {
    if (!this.options.soundEnabled) return;
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (!AudioContext) return;
      if (!this.audioCtx) this.audioCtx = new AudioContext();
      if (this.audioCtx.state === "suspended") this.audioCtx.resume();

      const dur = 0.25;
      const bufSize = Math.floor(this.audioCtx.sampleRate * dur);
      const buf = this.audioCtx.createBuffer(1, bufSize, this.audioCtx.sampleRate);
      const d = buf.getChannelData(0);
      for (let i = 0; i < bufSize; i++) {
        d[i] = (Math.random() * 2 - 1) * Math.exp(-i / (this.audioCtx.sampleRate * 0.08));
      }

      const noise = this.audioCtx.createBufferSource();
      noise.buffer = buf;
      const filter = this.audioCtx.createBiquadFilter();
      filter.type = "bandpass";
      const now = this.audioCtx.currentTime;
      filter.frequency.setValueAtTime(600, now);
      filter.frequency.exponentialRampToValueAtTime(2800, now + 0.1);
      filter.frequency.exponentialRampToValueAtTime(450, now + dur);
      filter.Q.setValueAtTime(2.5, now);

      const gain = this.audioCtx.createGain();
      gain.gain.setValueAtTime(0.2, now);
      gain.gain.exponentialRampToValueAtTime(0.01, now + dur);

      noise.connect(filter);
      filter.connect(gain);
      gain.connect(this.audioCtx.destination);
      noise.start();
    } catch (e) {}
  }

  /* ------------------------------------------------------------------
     9. EVENT HANDLING & MOUSE TILT PARALLAX
  ------------------------------------------------------------------ */
  bindEvents() {
    window.addEventListener("resize", () => {
      const w = this.container.clientWidth;
      const h = this.container.clientHeight;
      this.camera.aspect = w / h;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(w, h);
      this.updateCameraPosition();
    });

    window.addEventListener("mousemove", (e) => {
      const normX = (e.clientX / window.innerWidth) * 2 - 1;
      const normY = (e.clientY / window.innerHeight) * 2 - 1;
      this.targetRotationY = normX * 0.12;
      this.targetRotationX = -normY * 0.10;
    });

    this.container.addEventListener("click", (e) => {
      const rect = this.renderer.domElement.getBoundingClientRect();
      this.mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      this.mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

      this.raycaster.setFromCamera(this.mouse, this.camera);
      const hits = this.raycaster.intersectObjects([
        this.rightPageMesh,
        this.leftPageMesh
      ]);

      if (hits.length > 0) {
        const hit = hits[0];
        if (hit.object === this.rightPageMesh) {
          if (hit.uv && hit.uv.y < 0.28 && this.currentSpread === 4) {
            this.options.onInteractiveClick(this.currentSpread, "right");
          } else {
            this.turnPage(1);
          }
        } else if (hit.object === this.leftPageMesh) {
          if (hit.uv && hit.uv.y < 0.28 && this.currentSpread === 1) {
            this.turnPage(1);
          } else {
            this.turnPage(-1);
          }
        }
      }
    });

    window.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight" || e.key === "PageDown" || e.key === " ") {
        this.turnPage(1);
      } else if (e.key === "ArrowLeft" || e.key === "PageUp") {
        this.turnPage(-1);
      }
    });
  }

  jumpToSpread(idx) {
    if (idx === this.currentSpread || this.isAnimating) return;
    this.currentSpread = idx;
    this.updateSpreadVisuals();
    this.playPaperSound();
  }

  /* ------------------------------------------------------------------
     10. RENDER LOOP
  ------------------------------------------------------------------ */
  animate() {
    requestAnimationFrame(this.animate);

    this.currentRotationX += (this.targetRotationX - this.currentRotationX) * 0.06;
    this.currentRotationY += (this.targetRotationY - this.currentRotationY) * 0.06;

    this.bookGroup.rotation.x = this.currentRotationX;
    this.bookGroup.rotation.y = this.currentRotationY;

    this.renderer.render(this.scene, this.camera);
  }
}

window.Book3DApp = Book3DApp;
