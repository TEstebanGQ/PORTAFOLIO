export type Language = "es" | "en";

export interface ActiveAreaTranslation {
	faceIndex: number;
	title: { es: string; en: string };
	link?: string | ((lang: Language) => string);
	top: number;
	left: number;
	width: number;
	height: number;
	zoom?: { top: number; left: number; width: number; height: number };
	preserveDefaultCursor?: boolean;
}

export const I18N_TEXTS = {
	es: {
		langButton: "Español",
		navIndex: "ÍNDICE",
		navChapters: "CAPÍTULOS",
		chapterPrefix: "Capítulo",
		coverButton: "Portada Inicial",
		coverTooltip: "Volver a la portada",
		mobileButton: "Capítulos",
		keyboardHint: "Navega con flechas (↓ → / ↑ ←)",
		docTitle: "El Libro de Tomás Esteban // Desarrollador Junior Full Stack",
		toastSwitched: "Idioma cambiado a Español",
		pageSummaryTitle: "Resumen del Capítulo",
		viewTranslationBtn: "Ver traducción en inglés",
		closeBtn: "Cerrar",
		mobileSwitchTo3D: "Ver Libro 3D",
		mobileSwitchToWeb: "Vista Resumen",
		mobileBadge: "Versión Móvil Optimizada",
		heroRole: "Desarrollador Junior Full Stack",
		heroLocation: "Bucaramanga, Colombia",
		heroBio: "Desarrollador Full Stack con experiencia en JavaScript, Node.js, C# .NET, Java, Spring Boot, React Native y Supabase. Proyección estratégica en Análisis de Datos, Ingeniería de IA y Ciberseguridad.",
		sectionAbout: "Sobre Mí & Especialidad",
		sectionSkills: "Tecnologías & Dominio",
		sectionJourney: "Trayectoria & Roadmap",
		sectionExperience: "Experiencia en Producción",
		sectionProjects: "Proyectos de Ingeniería",
		sectionContact: "Contacto Inmediato",
		viewCodeBtn: "GitHub",
		liveDemoBtn: "Demo en Vivo",
		contactWhatsApp: "WhatsApp",
		contactEmail: "Correo",
		contactLinkedIn: "LinkedIn",
		contactGitHub: "GitHub",
		rotateHint: "Sugerencia: Puedes explorar la versión interactiva 3D con el botón inferior.",
		downloadCV: "Descargar Hoja de Vida (PDF)",
		viewCV: "Ver Hoja de Vida",
		cvSectionTag: "CIERRE & HOJA DE VIDA",
		cvSectionTitle: "Contacto Directo & Hoja de Vida",
		cvSectionSubtitle: "Documento oficial consolidado con perfil técnico, experiencia en producción y formación.",
		cvOfficialBadge: "Curriculum Vitae Oficial",
		cvFileName: "Tomas_Esteban_Gonzalez_Quintero_CV.pdf",
		cvFileSize: "PDF Oficial · Formato A4 · 327 KB",
		cvContactHeader: "Canales de Contacto Directo",
		cvPhoneLabel: "Teléfono / WhatsApp",
		cvEmailLabel: "Correo Electrónico",
		cvLocationLabel: "Ubicación",
		cvIdLabel: "Identificación (C.C.)",
		cvRoleLabel: "Rol Profesional",
		cvEducationLabel: "Formación",
		cvEducationValue: "Campuslands · Técnico Laboral en Desarrollo de Software",
		cvNavDownloadBtn: "Descargar CV (PDF)",
		cvNavDownloadTooltip: "Descargar Hoja de Vida oficial en PDF",
	},
	en: {
		langButton: "English",
		navIndex: "INDEX",
		navChapters: "CHAPTERS",
		chapterPrefix: "Chapter",
		coverButton: "Cover Page",
		coverTooltip: "Back to initial cover",
		mobileButton: "Chapters",
		keyboardHint: "Navigate with arrows (↓ → / ↑ ←)",
		docTitle: "The Book of Tomás Esteban // Junior Full Stack Developer",
		toastSwitched: "Language switched to English",
		pageSummaryTitle: "Chapter Summary in English",
		viewTranslationBtn: "English translation available",
		closeBtn: "Close",
		mobileSwitchTo3D: "View 3D Book",
		mobileSwitchToWeb: "Mobile View",
		mobileBadge: "Optimized Mobile View",
		heroRole: "Junior Full Stack Developer",
		heroLocation: "Bucaramanga, Colombia",
		heroBio: "Full Stack Developer experienced in JavaScript, Node.js, C# .NET, Java, Spring Boot, React Native, and Supabase. Strategic focus on Data Analysis, AI Engineering, and Cybersecurity.",
		sectionAbout: "About Me & Focus",
		sectionSkills: "Technologies & Core Stack",
		sectionJourney: "Journey & Roadmap",
		sectionExperience: "Production Experience",
		sectionProjects: "Engineering Projects",
		sectionContact: "Direct Contact",
		viewCodeBtn: "GitHub",
		liveDemoBtn: "Live Demo",
		contactWhatsApp: "WhatsApp",
		contactEmail: "Email",
		contactLinkedIn: "LinkedIn",
		contactGitHub: "GitHub",
		rotateHint: "Tip: You can explore the interactive 3D version using the button below.",
		downloadCV: "Download Resume / CV (PDF)",
		viewCV: "View Resume",
		cvSectionTag: "CLOSING & RESUME",
		cvSectionTitle: "Direct Contact & Resume",
		cvSectionSubtitle: "Official consolidated document with technical profile, production experience, and education.",
		cvOfficialBadge: "Official Curriculum Vitae",
		cvFileName: "Tomas_Esteban_Gonzalez_Quintero_CV.pdf",
		cvFileSize: "Official PDF · A4 Format · 327 KB",
		cvContactHeader: "Direct Contact Channels",
		cvPhoneLabel: "Phone / WhatsApp",
		cvEmailLabel: "Email Address",
		cvLocationLabel: "Location",
		cvIdLabel: "National ID",
		cvRoleLabel: "Primary Role",
		cvEducationLabel: "Education",
		cvEducationValue: "Campuslands · Software Development Technologist",
		cvNavDownloadBtn: "Download CV (PDF)",
		cvNavDownloadTooltip: "Download official resume in PDF",
	},
};

export const PAGE_SUMMARIES: Record<number, { title: { es: string; en: string }; content: { es: string; en: string } }> = {
	1: {
		title: {
			es: "Bienvenido a la Bitácora",
			en: "Welcome to The Codex",
		},
		content: {
			es: "Portafolio interactivo 3D de Tomás Esteban González Quintero. Pasa las páginas arrastrando las esquinas o usando las flechas de tu teclado (↓ → / ↑ ←). Doble clic para activar pantalla completa.",
			en: "Interactive 3D portfolio of Tomás Esteban González Quintero. Turn pages by dragging the corners or using your arrow keys (↓ → / ↑ ←). Double-click to enter fullscreen mode.",
		},
	},
	2: {
		title: {
			es: "Capítulo I: Sobre Mí & Habilidades",
			en: "Chapter I: About Me & Technical Skills",
		},
		content: {
			es: "Desarrollador Junior Full Stack con experiencia práctica en JavaScript, Node.js, C# .NET, Java, Spring Boot, React Native y Supabase. Enfoque estratégico a futuro en Análisis de Datos, Ingeniería de IA y Ciberseguridad.",
			en: "Junior Full Stack Developer experienced in JavaScript, Node.js, C# .NET, Java, Spring Boot, React Native, and Supabase. Strategic future focus on Data Analysis, AI Engineering, and Cybersecurity.",
		},
	},
	4: {
		title: {
			es: "Capítulo II: Trayectoria Profesional",
			en: "Chapter II: Professional Roadmap & Journey",
		},
		content: {
			es: "Mapa de ruta cronológico y evolución formativa en Campuslands y Promoción Social: desarrollo de software moderno, microservicios, seguridad con JWT y diseño de arquitecturas escalables.",
			en: "Chronological roadmap and engineering journey at Campuslands and Promoción Social: modern software engineering, decoupled microservices, JWT security, and scalable distributed architectures.",
		},
	},
	6: {
		title: {
			es: "Capítulo III: Experiencia & Producción",
			en: "Chapter III: Production Experience & Engineering",
		},
		content: {
			es: "Experiencia comprobada en producción: Campuslands Access Hub (sistema en producción con RBAC y cientos de participantes), Automatización de Inasistencias con n8n e IA, y servidor GitHub MCP en Node.js.",
			en: "Proven production track record: Campuslands Access Hub (production system with RBAC for hundreds of users), Attendance AI Automation with n8n & LLMs, and Node.js GitHub MCP Server.",
		},
	},
	9: {
		title: {
			es: "Capítulo IV: Proyectos de Ingeniería",
			en: "Chapter IV: Featured Engineering Projects",
		},
		content: {
			es: "• Campuslands Access Hub: Sistema de gestión y RBAC en producción para cientos de usuarios.\n• Enterprise Security API: REST API defensiva en .NET 9 con OWASP, JWT y Rate Limiting.\n• Campuslands Inteligente: Plataforma multi-agente con LangGraph, PyTorch y FastAPI.\n• LogiTrack WMS: Sistema de inventarios y bodegas (Spring Boot 3, PostgreSQL, Docker).\n• n8n Attendance AI: Automatización de inasistencias con LLMs y Telegram.\n• GitHub MCP Server: Servidor MCP en Node.js que conecta LLMs con la API de GitHub.\n• eCommerce Database 4NF: Base de datos relacional avanzada con análisis RFM.",
			en: "• Campuslands Access Hub: Production governance & RBAC system for hundreds of participants.\n• Enterprise Security API: Defensive REST API in .NET 9 with OWASP, JWT, and Rate Limiting.\n• Campuslands Intelligent: Multi-agent platform with LangGraph, PyTorch, and FastAPI.\n• LogiTrack WMS: Enterprise warehouse management system (Spring Boot 3, PostgreSQL, Docker).\n• n8n Attendance AI: Automated absence classification pipeline using LLMs and Telegram.\n• GitHub MCP Server: Node.js MCP server connecting LLMs to the GitHub API.\n• eCommerce Database 4NF: Advanced relational database with RFM analytical modeling.",
		},
	},
};
