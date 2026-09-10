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
		docTitle: "El Libro de Tomás Esteban // Full Stack Developer & Arquitecto de Software",
		toastSwitched: "Idioma cambiado a Español 🇪🇸",
		pageSummaryTitle: "Resumen del Capítulo",
		viewTranslationBtn: "📜 Ver traducción en inglés",
		closeBtn: "Cerrar",
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
		docTitle: "The Book of Tomás Esteban // Full Stack Developer & Software Architect",
		toastSwitched: "Language switched to English 🇬🇧",
		pageSummaryTitle: "Chapter Summary in English",
		viewTranslationBtn: "📜 English translation available",
		closeBtn: "Close",
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
			es: "Desarrollador Full Stack, Integrador de Soluciones IA y Arquitecto de Software de Bucaramanga, Colombia. Especializado en Python (FastAPI, LangGraph), Java 17+ (Spring Boot), Node.js, bases de datos 4NF y flujos automatizados con n8n.",
			en: "Full Stack Developer, AI Solutions Integrator & Software Architect based in Bucaramanga, Colombia. Specialized in Python (FastAPI, LangGraph), Java 17+ (Spring Boot), Node.js, 4NF relational databases, and automated n8n workflows.",
		},
	},
	4: {
		title: {
			es: "Capítulo II: Trayectoria Profesional",
			en: "Chapter II: Professional Roadmap & Journey",
		},
		content: {
			es: "Mapa de ruta cronológico y evolución de aprendizaje en Campuslands: desarrollo de software de alto rendimiento, microservicios, seguridad con JWT y diseño de arquitecturas escalables.",
			en: "Chronological roadmap and engineering journey at Campuslands: high-performance software engineering, decoupled microservices, JWT security, and scalable distributed architectures.",
		},
	},
	6: {
		title: {
			es: "Capítulo III: Experiencia & Consultoría",
			en: "Chapter III: Enterprise Experience & Consulting",
		},
		content: {
			es: "Experiencia en Campuslands liderando arquitectura de software para WMS empresarial, automatizaciones con modelos de lenguaje (LLM) y consultoría independiente en ingeniería de software.",
			en: "Professional track record at Campuslands leading software architecture for enterprise WMS, LLM workflow automations, and independent consulting in full stack engineering.",
		},
	},
	9: {
		title: {
			es: "Capítulo IV: Proyectos de Ingeniería",
			en: "Chapter IV: Featured Engineering Projects",
		},
		content: {
			es: "• LogiTrack WMS: Sistema de gestión de inventarios y bodegas (Spring Boot 3, PostgreSQL, Docker).\n• n8n Attendance AI: Pipeline de clasificación de solicitudes con LLMs y Telegram.\n• Campuslands Inteligente: Plataforma multi-agente con LangGraph y FastAPI.\n• GitHub MCP Server: Servidor MCP en Node.js que conecta LLMs con GitHub API.",
			en: "• LogiTrack WMS: Enterprise warehouse & inventory management system (Spring Boot 3, PostgreSQL, Docker).\n• n8n Attendance AI: Automated classification pipeline using LLMs and Telegram.\n• Campuslands Intelligent: Multi-agent platform with LangGraph and FastAPI.\n• GitHub MCP Server: Node.js MCP server connecting LLMs to the GitHub API.",
		},
	},
};
