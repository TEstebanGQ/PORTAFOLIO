import { Language, I18N_TEXTS } from "./i18n";
import "./mobile-view.css";

export interface MobileFeature {
	heading: { es: string; en: string };
	text: { es: string; en: string };
}

export interface MobileBadgeGroup {
	label: { es: string; en: string };
	v1: string;
	v2: string;
}

export interface MobileProject {
	id: string;
	title: string;
	subtitle: { es: string; en: string };
	description: { es: string; en: string };
	features: MobileFeature[];
	badges: MobileBadgeGroup[];
	tags: string[];
	github?: string;
	demo?: string;
}

export const DETAILED_PROJECTS: MobileProject[] = [
	{
		id: "campus-hub",
		title: "Campuslands Access Hub",
		subtitle: {
			es: "Control de Acceso, Asistencia y Certificados en Producción Real",
			en: "Production Access Control, Attendance & Digital Certificates",
		},
		description: {
			es: "Sistema empresarial desplegado en producción y utilizado activamente por cientos de participantes. Cuenta con asistencia en tiempo real, administración de grupos, emisión de certificados digitales con QR criptográfico y control de acceso basado en roles (RBAC).",
			en: "Enterprise system deployed to production and actively used by hundreds of participants, featuring real-time attendance tracking, group management, automated digital certificate issuance, and role-based access control (RBAC).",
		},
		features: [
			{
				heading: {
					es: "1. Asistencia Multi-Tenant en Tiempo Real",
					en: "1. Real-Time Multi-Tenant Attendance",
				},
				text: {
					es: "Registro y verificación instantánea de presencia procesando cientos de registros diarios con tiempos de respuesta de sub-segundo.",
					en: "Instant attendance verification and logging processing hundreds of daily check-ins with sub-second response times.",
				},
			},
			{
				heading: {
					es: "2. Control de Acceso Basado en Roles (RBAC)",
					en: "2. Role-Based Access Control (RBAC)",
				},
				text: {
					es: "Jerarquía granular de permisos que asegura límites estrictos entre SuperAdmins, Coordinadores, Trainers y Campers.",
					en: "Granular permission hierarchy enforcing strict security boundaries across SuperAdmins, Coordinators, Trainers, and Campers.",
				},
			},
			{
				heading: {
					es: "3. Certificados Digitales Automáticos",
					en: "3. Automated Digital Certificates",
				},
				text: {
					es: "Generación automática y verificación criptográfica de diplomas de aprobación con código QR único a prueba de alteraciones.",
					en: "Automated generation and cryptographic verification of completion certificates featuring unique tamper-proof QR codes.",
				},
			},
			{
				heading: {
					es: "4. Dashboard Analítico de Métricas",
					en: "4. Analytic Metrics & Reporting Dashboard",
				},
				text: {
					es: "Panel interactivo para coordinadores con seguimiento de tasas de retención, anomalías de asistencia y exportación de reportes.",
					en: "Interactive coordinator dashboard tracking retention rates, attendance anomalies, and structured data exports.",
				},
			},
		],
		badges: [
			{ label: { es: "ENTORNO", en: "ENVIRONMENT" }, v1: "Live Production", v2: "Cientos de Usuarios" },
			{ label: { es: "STACK", en: "STACK" }, v1: "TypeScript / Node", v2: "PostgreSQL & Supabase" },
			{ label: { es: "SEGURIDAD", en: "SECURITY" }, v1: "Granular RBAC", v2: "Signed JWT" },
			{ label: { es: "OPERACIÓN", en: "OPERATION" }, v1: "Real-Time Sync", v2: "Digital QR Certs" },
		],
		tags: ["TypeScript", "Node.js", "PostgreSQL", "Supabase", "RBAC", "Producción"],
		github: "https://github.com/TEstebanGQ/Campus-Hub-zero",
	},
	{
		id: "enterprise-security-api",
		title: "Enterprise Security API",
		subtitle: {
			es: "Arquitectura Hexagonal & Seguridad Defensiva OWASP en .NET 9",
			en: "Hexagonal Architecture & OWASP Defensive Security in .NET 9",
		},
		description: {
			es: "API REST empresarial de alta seguridad diseñada bajo Arquitectura Hexagonal en .NET 9, integrando autenticación JWT blindada, cifrado BCrypt, análisis heurístico de vulnerabilidades OWASP, rate limiting y CRM seguro.",
			en: "High-security enterprise REST API designed under Hexagonal Architecture in .NET 9, featuring hardened JWT authentication, BCrypt password hashing, OWASP compliance analyzer, rate limiting, and client CRM.",
		},
		features: [
			{
				heading: {
					es: "1. Análisis de Contraseñas OWASP",
					en: "1. OWASP Password Vulnerability Analysis",
				},
				text: {
					es: "Evaluación heurística de entropía y cumplimiento estricto de directrices OWASP para erradicar ataques de diccionario y fuerza bruta.",
					en: "Heuristic entropy evaluation and strict OWASP compliance validation to eliminate dictionary and brute-force attack vectors.",
				},
			},
			{
				heading: {
					es: "2. JWT Blindado & Hash BCrypt",
					en: "2. Hardened JWT Auth & BCrypt Hashing",
				},
				text: {
					es: "Gestión segura de identidad con tokens JWT firmados criptográficamente, rotación de secretos y salting adaptativo con BCrypt.",
					en: "Secure identity management with cryptographically signed JWT tokens, secret rotation, and adaptive BCrypt salting.",
				},
			},
			{
				heading: {
					es: "3. Rate Limiting Distribuido & Defensa DoS",
					en: "3. Distributed Rate Limiting & DoS Defense",
				},
				text: {
					es: "Políticas granulares de limitación por IP y cliente que protegen endpoints críticos de autenticación frente a saturación.",
					en: "Granular per-IP and per-client throttling policies protecting critical authentication endpoints from flood attacks.",
				},
			},
			{
				heading: {
					es: "4. Auditoría Forense Inmutable",
					en: "4. Immutable Audit Logging & Traceability",
				},
				text: {
					es: "Registro estructurado del ciclo de vida de autenticación, intentos fallidos y elevaciones de privilegios para trazabilidad forense.",
					en: "Structured logging of authentication lifecycles, failed access attempts, and privilege elevations for forensics.",
				},
			},
		],
		badges: [
			{ label: { es: "FRAMEWORK", en: "FRAMEWORK" }, v1: "C# / .NET 9", v2: "ASP.NET Core" },
			{ label: { es: "ARQUITECTURA", en: "ARCHITECTURE" }, v1: "Hexagonal (Ports)", v2: "Clean Architecture" },
			{ label: { es: "SEGURIDAD", en: "SECURITY" }, v1: "OWASP Compliant", v2: "JWT & BCrypt" },
			{ label: { es: "PROTECCIÓN", en: "PROTECTION" }, v1: "Rate Limiting", v2: "Data Sanitization" },
		],
		tags: [".NET 9", "C#", "Arquitectura Hexagonal", "OWASP", "JWT", "Ciberseguridad"],
		github: "https://github.com/TEstebanGQ/dotnet-hexagonal-enterprise-security-api",
	},
	{
		id: "logitrack-wms",
		title: "LogiTrack WMS",
		subtitle: {
			es: "Sistema Empresarial de Logística & Gestión de Almacenes",
			en: "Enterprise Logistics & Warehouse Management System",
		},
		description: {
			es: "Sistema integral de gestión de almacenes (WMS) de alta concurrencia. Proporciona trazabilidad 100% en tiempo real sobre existencias multi-bodega, recepciones de proveedores, transferencias entre sedes, control de lotes y despachos.",
			en: "Enterprise-grade Warehouse Management System (WMS) designed to deliver 100% real-time operational traceability across multi-warehouse inventory, supplier receptions, inter-facility transfers, lot tracking, picking workflows, and reconciliations.",
		},
		features: [
			{
				heading: {
					es: "1. Control Multi-Bodega & Trazabilidad de Lotes",
					en: "1. Multi-Warehouse Stock & Lot Control",
				},
				text: {
					es: "Administración centralizada de inventario distribuido con prevención estricta de stock negativo y rastreo detallado de lotes.",
					en: "Centralized administration of inventory distributed across multiple physical facilities with strict negative-stock prevention and lot traceability.",
				},
			},
			{
				heading: {
					es: "2. Auditoría Operacional Inmutable",
					en: "2. Full Operational Auditing & Traceability",
				},
				text: {
					es: "Registro cronológico inalterable de recepciones, despachos y ajustes de stock con identificación de operador y milisegundos.",
					en: "Immutable chronological logging of receptions, dispatches, transfers, and inventory adjustments with operator identification.",
				},
			},
			{
				heading: {
					es: "3. Órdenes de Compra & Recepción de Proveedores",
					en: "3. Purchase Order & Supplier Reception",
				},
				text: {
					es: "Flujo estructurado con conciliación de pedidos, detección de discrepancias y sincronización automática del libro contable de existencias.",
					en: "Structured receiving pipeline with automated purchase order reconciliation, discrepancy identification, and stock ledger synchronization.",
				},
			},
			{
				heading: {
					es: "4. Jerarquía de Roles & Seguridad JWT (RBAC)",
					en: "4. Role Hierarchy & JWT Security (RBAC)",
				},
				text: {
					es: "Matriz de permisos blindada con Spring Security para SuperAdmins, Jefes de Bodega, Operadores y Auditores.",
					en: "Granular permission matrix backed by Spring Security and signed JWTs for SuperAdmins, Warehouse Managers, Operators, and Auditors.",
				},
			},
		],
		badges: [
			{ label: { es: "BACKEND", en: "BACKEND" }, v1: "Java 17", v2: "Spring Boot 3.3" },
			{ label: { es: "DATABASE", en: "DATABASE" }, v1: "PostgreSQL 16", v2: "JPA & Hibernate" },
			{ label: { es: "SEGURIDAD", en: "SECURITY" }, v1: "Spring Security", v2: "Signed JWTs" },
			{ label: { es: "DEPLOYMENT", en: "DEPLOYMENT" }, v1: "Docker & Nginx", v2: "GCP Domain" },
		],
		tags: ["Java 17", "Spring Boot 3", "PostgreSQL", "Docker", "GCP", "Spring Security"],
		github: "https://github.com/TEstebanGQ/logitrack-wms-springboot",
		demo: "https://logitrack.34.70.8.165.sslip.io",
	},
	{
		id: "n8n-attendance-ai",
		title: "n8n Attendance AI Workflow",
		subtitle: {
			es: "Flujo de Automatización & Clasificación Inteligente con LLMs",
			en: "Automation Workflow & LLM Request Classification",
		},
		description: {
			es: "Pipeline automatizado de extremo a extremo para la ingesta, evaluación inteligente y clasificación de peticiones de justificación de inasistencias en entornos académicos y corporativos, eliminando la revisión manual.",
			en: "End-to-end automated pipeline for the ingestion, intelligent evaluation, and classification of absence justification requests in academic and corporate environments, eliminating manual review and providing instant auditability.",
		},
		features: [
			{
				heading: {
					es: "1. Ingesta Web & Captura Estructurada",
					en: "1. Web Ingestion & Data Capture",
				},
				text: {
					es: "Formulario web responsivo para radicación ordenada con adjuntos médicos y soportes oficiales.",
					en: "Responsive web form for structured receipt of student absence requests with medical and official supporting attachments.",
				},
			},
			{
				heading: {
					es: "2. Normalización & Validación en n8n",
					en: "2. Normalization & Validation in n8n",
				},
				text: {
					es: "Flujo de orquestación que desinfecta entradas, valida restricciones de esquema y prepara cargas de inferencia.",
					en: "Orchestration workflow in n8n sanitizing inputs, validating schema constraints, and preparing structured inference payloads.",
				},
			},
			{
				heading: {
					es: "3. Evaluación Asistida por LLMs",
					en: "3. Intelligent Evaluation via LLM",
				},
				text: {
					es: "Conexión con modelos avanzados (Claude & GPT-4o vía OpenRouter) categorizando en: Válido, Inválido o Requiere Revisión Humana.",
					en: "Prompt-engineered connection with OpenRouter LLMs categorizing justifications into: Valid, Invalid, or Pending Human Review.",
				},
			},
			{
				heading: {
					es: "4. Notificaciones Inmediatas por Telegram & Sheets",
					en: "4. Real-Time Google Sheets Sync & Telegram",
				},
				text: {
					es: "Sincronización instantánea con el libro maestro y alertas automáticas personalizadas vía bot de Telegram a coordinadores y solicitantes.",
					en: "Instant synchronization with the master absence ledger and real-time dispatch notifying students and coordinators via Telegram bot.",
				},
			},
		],
		badges: [
			{ label: { es: "ORQUESTADOR", en: "ORCHESTRATOR" }, v1: "n8n Self-Hosted", v2: "Docker Engine" },
			{ label: { es: "MODELOS IA", en: "AI MODELS" }, v1: "OpenRouter API", v2: "Claude & GPT-4o" },
			{ label: { es: "INTEGRACIONES", en: "INTEGRATIONS" }, v1: "Google Sheets", v2: "Telegram Bot API" },
			{ label: { es: "SEGURIDAD", en: "SECURITY" }, v1: "Webhook Auth", v2: "SSL Encrypted" },
		],
		tags: ["n8n", "LLM", "OpenRouter", "Telegram Bot API", "Google Sheets", "Docker"],
		github: "https://github.com/TEstebanGQ/n8n-attendance-ai-workflow",
	},
	{
		id: "campuslands-inteligente",
		title: "Campuslands Inteligente",
		subtitle: {
			es: "Supervisión Académica Multi-Agente & Analítica Predictiva",
			en: "Multi-Agent Academic Supervision & Predictive Analytics",
		},
		description: {
			es: "Plataforma empresarial diseñada para supervisión académica en tiempo real, verificación de presencia con visión artificial y modelado predictivo del riesgo de deserción mediante flujos colaborativos de agentes de IA.",
			en: "Intelligent enterprise platform engineered for real-time academic supervision, attendance verification with computer vision, and predictive student risk modeling through collaborative multi-agent AI workflows.",
		},
		features: [
			{
				heading: {
					es: "1. Grafo Multi-Agente Colaborativo (LangGraph)",
					en: "1. Collaborative Multi-Agent Graph (LangGraph)",
				},
				text: {
					es: "Agentes autónomos coordinados para triaje de consultas, evaluación de políticas y orientación personalizada.",
					en: "Autonomous agents coordinating inquiry triage, policy evaluation, and personalized remediation guidance.",
				},
			},
			{
				heading: {
					es: "2. Motor de Asistencia por Visión Artificial",
					en: "2. Computer Vision Attendance Engine",
				},
				text: {
					es: "Detección biométrica automatizada con OpenCV y modelos de deep learning en PyTorch, registrando presencia sin fricción manual.",
					en: "Automated biometric presence detection with OpenCV and deep learning, logging timestamps with zero manual intervention.",
				},
			},
			{
				heading: {
					es: "3. Analítica Predictiva de Riesgo Académico",
					en: "3. Predictive Student Risk Analytics",
				},
				text: {
					es: "Modelos analíticos que evalúan la velocidad de inasistencias y tendencias de rendimiento para anticipar deserciones.",
					en: "Machine learning models analyzing attendance velocity and evaluation trends to flag academic dropout risk early.",
				},
			},
			{
				heading: {
					es: "4. Alertas Instantáneas & Reportes Consolidados",
					en: "4. Instant Telegram Bot Notifications",
				},
				text: {
					es: "Canal automatizado para notificar cambios de estado a estudiantes y remitir resúmenes diarios a los coordinadores.",
					en: "Real-time alerting pipeline notifying students of status changes and delivering automated daily coordinator digests.",
				},
			},
		],
		badges: [
			{ label: { es: "MOTOR IA", en: "AI ENGINE" }, v1: "LangGraph", v2: "Multi-Agent Graph" },
			{ label: { es: "BACKEND", en: "BACKEND" }, v1: "Python", v2: "FastAPI Async" },
			{ label: { es: "VISIÓN", en: "VISION" }, v1: "OpenCV", v2: "PyTorch Models" },
			{ label: { es: "DATABASE", en: "DATABASE" }, v1: "PostgreSQL", v2: "SQLAlchemy 4NF" },
		],
		tags: ["Python", "FastAPI", "LangGraph", "PyTorch", "OpenCV", "PostgreSQL"],
		github: "https://github.com/TEstebanGQ/campuslands-inteligente",
	},
	{
		id: "github-mcp-server",
		title: "GitHub MCP Server",
		subtitle: {
			es: "Model Context Protocol para Agentes Autónomos de IA",
			en: "Model Context Protocol for Autonomous AI Agents",
		},
		description: {
			es: "Servidor profesional Model Context Protocol (MCP) que permite a agentes de IA como Claude Desktop, Cursor y Windsurf interactuar directamente y de manera segura con repositorios, issues, ramas y pull requests de GitHub mediante herramientas estandarizadas.",
			en: "Professional Model Context Protocol (MCP) server that empowers AI agents like Claude Desktop and Cursor to interact directly and safely with GitHub repositories, issues, branches, commits, and pull requests via structured standardized tools.",
		},
		features: [
			{
				heading: {
					es: "1. Métricas de Repositorio & Auditoría",
					en: "1. Repository Metrics & Auditing",
				},
				text: {
					es: "Inspección de metadatos, historial de commits, métricas de contribuidores y reglas de protección de ramas vía llamadas REST.",
					en: "Inspect repo metadata, commit histories, contributor metrics, and branch protection rules via optimized REST calls.",
				},
			},
			{
				heading: {
					es: "2. Gestión Programática de Issues & PRs",
					en: "2. Automated Issue & PR Management",
				},
				text: {
					es: "Creación, lectura, asignación y comentarios en pull requests e incidentes con validación previa de argumentos.",
					en: "Programmatically read, create, comment, assign, and transition GitHub issues and pull requests with validation.",
				},
			},
			{
				heading: {
					es: "3. Búsqueda Segura & Exploración de Árboles",
					en: "3. Secure File Search & Tree Inspection",
				},
				text: {
					es: "Recorrido recursivo de directorios y lectura de blobs con límites estrictos de tamaño para salvaguardar el contexto.",
					en: "Recursive directory traversal, file content retrieval, and blob inspection with size safeguards.",
				},
			},
			{
				heading: {
					es: "4. Esquemas Estrictos con Zod",
					en: "4. Strict Schemas & Input Validation",
				},
				text: {
					es: "Declaraciones JSON Schema rigurosas que garantizan que el LLM genere argumentos matemáticamente válidos antes de su ejecución.",
					en: "Full JSON Schema tool declarations ensuring LLMs generate mathematically valid arguments before execution.",
				},
			},
		],
		badges: [
			{ label: { es: "RUNTIME", en: "RUNTIME" }, v1: "Node.js 20+", v2: "TypeScript ESM" },
			{ label: { es: "PROTOCOLO", en: "PROTOCOL" }, v1: "Anthropic MCP", v2: "Stdio Transport" },
			{ label: { es: "CLIENTE", en: "CLIENT" }, v1: "Octokit API", v2: "REST & GraphQL" },
			{ label: { es: "SEGURIDAD", en: "SECURITY" }, v1: "Fine-Grained PAT", v2: "Read-Only Scopes" },
		],
		tags: ["Model Context Protocol", "TypeScript", "Node.js", "Octokit API", "Zod"],
		github: "https://github.com/TEstebanGQ/github-mcp-server",
	},
	{
		id: "helpdesk-ai",
		title: "HelpDesk AI",
		subtitle: {
			es: "Gestión Inteligente de Incidentes Empresariales con RAG & LLMs",
			en: "Enterprise Incident Management with LLM Triage",
		},
		description: {
			es: "Plataforma de mesa de ayuda y soporte técnico asistida por IA con triaje automático por lenguaje natural, cálculo de severidad y SLA, enrutamiento a especialistas y base de conocimiento RAG integrada para respuestas verificadas.",
			en: "Enterprise technical support and ticketing platform featuring automated natural language triage, intelligent urgency classification, auto-routing to technical specialists, and an integrated RAG knowledge base for instant answers.",
		},
		features: [
			{
				heading: {
					es: "1. Clasificación Semántica Inmediata",
					en: "1. Instant Semantic Classification",
				},
				text: {
					es: "Categorización automática de tickets por naturaleza técnica (Hardware, Redes, Base de Datos, Ciberseguridad, Permisos).",
					en: "Automated classification of incoming tickets by technical category (Hardware, Network, Database, Security, Permissions).",
				},
			},
			{
				heading: {
					es: "2. Puntuación de Urgencia & Ventanas SLA",
					en: "2. Urgency & SLA Priority Scoring",
				},
				text: {
					es: "Evaluación del impacto en el negocio que asigna automáticamente prioridades y plazos máximos de resolución.",
					en: "LLM-driven urgency evaluation assessing business impact and assigning SLA response windows automatically.",
				},
			},
			{
				heading: {
					es: "3. Base de Conocimiento RAG & Respuestas Inmediatas",
					en: "3. RAG Knowledge Base & Instant Resolution",
				},
				text: {
					es: "Búsqueda vectorial semántica sobre manuales técnicos que entrega soluciones comprobadas a incidentes comunes al instante.",
					en: "Semantic vector search against technical manuals delivering verified solutions to common issues instantly.",
				},
			},
			{
				heading: {
					es: "4. Enrutamiento a Especialistas & Auditoría",
					en: "4. Specialist Routing & Operational Audit",
				},
				text: {
					es: "Asignación automática a la cola del equipo correspondiente con línea temporal completa e inmutable del caso.",
					en: "Automated assignment to corresponding engineering queues with complete chronological timeline history.",
				},
			},
		],
		badges: [
			{ label: { es: "BACKEND", en: "BACKEND" }, v1: "Python FastAPI", v2: "Async Handlers" },
			{ label: { es: "MOTOR IA", en: "AI ENGINE" }, v1: "LangChain", v2: "OpenAI Models" },
			{ label: { es: "VECTOR STORE", en: "VECTOR STORE" }, v1: "ChromaDB", v2: "Embeddings" },
			{ label: { es: "DATABASE", en: "DATABASE" }, v1: "PostgreSQL 16", v2: "SQLAlchemy 4NF" },
		],
		tags: ["Python FastAPI", "LangChain", "ChromaDB", "PostgreSQL", "RAG Embeddings"],
		github: "https://github.com/TEstebanGQ/HelpDeskAI",
	},
	{
		id: "ecommerce-database-4nf",
		title: "Ecommerce Database 4NF",
		subtitle: {
			es: "Arquitectura Relacional Avanzada & Normalización Estricta 4NF",
			en: "Advanced Relational Architecture & 4NF Rigor",
		},
		description: {
			es: "Arquitectura de base de datos relacional de gran escala diseñada para plataformas de comercio electrónico de alta concurrencia. Rigurosamente normalizada en Cuarta Forma Normal (4NF) con garantías ACID y cero redundancia.",
			en: "Full-scale relational database architecture designed for high-concurrency enterprise e-commerce platforms. Rigorously normalized to Fourth Normal Form (4NF) with ACID transactional guarantees and zero redundancy.",
		},
		features: [
			{
				heading: {
					es: "1. Normalización Rigurosa en 4NF",
					en: "1. Strict 4NF Normalization",
				},
				text: {
					es: "Eliminación total de dependencias multivaluadas y datos redundantes en catálogos, clientes y libros de pedidos.",
					en: "Complete elimination of multi-valued dependencies and redundant data across catalog, customers, and order ledgers.",
				},
			},
			{
				heading: {
					es: "2. Seguridad Transaccional ACID",
					en: "2. ACID Transactional Safety",
				},
				text: {
					es: "Estrategias de bloqueo pesimista y control de concurrencia para evitar sobreventa, carreras y pérdida de inventario.",
					en: "Pessimistic locking strategies and concurrency controls to prevent overselling, race conditions, and phantom inventory loss.",
				},
			},
			{
				heading: {
					es: "3. Procedimientos Almacenados & Triggers",
					en: "3. Stored Procedures & Triggers",
				},
				text: {
					es: "Lógica de negocio encapsulada en motor: descuentos automáticos, libros de impuestos dinámicos y reservas de stock.",
					en: "Encapsulated business logic: automated discount calculations, dynamic tax ledgers, and inventory reservations.",
				},
			},
			{
				heading: {
					es: "4. Segmentación Analítica RFM",
					en: "4. RFM Customer Segmentation",
				},
				text: {
					es: "Vistas analíticas avanzadas que computan Recencia, Frecuencia y Valor Monetario para segmentación estratégica.",
					en: "Advanced analytical views calculating Recency, Frequency, and Monetary Value to drive strategic marketing insights.",
				},
			},
		],
		badges: [
			{ label: { es: "RDBMS", en: "RDBMS" }, v1: "MySQL 8.0+", v2: "InnoDB Engine" },
			{ label: { es: "NORMALIZACIÓN", en: "NORMALIZATION" }, v1: "4NF Rigor", v2: "Zero Redundancy" },
			{ label: { es: "LÓGICA", en: "LOGIC" }, v1: "Stored Procedures", v2: "Triggers & Views" },
			{ label: { es: "OPTIMIZACIÓN", en: "OPTIMIZATION" }, v1: "Composite Indexes", v2: "Partitioning" },
		],
		tags: ["MySQL 8", "InnoDB", "Rigor 4NF", "Procedimientos Almacenados", "Analítica RFM"],
		github: "https://github.com/TEstebanGQ/ecommerce-database-4nf",
	},
	{
		id: "softskills-quest",
		title: "SoftSkills Quest",
		subtitle: {
			es: "Simulador de Toma de Decisiones y Liderazgo para Desarrolladores",
			en: "Gamified Developer Decision-Making Game",
		},
		description: {
			es: "Plataforma gamificada interactiva en 2D diseñada para entrenar y evaluar habilidades blandas en ingeniería mediante bifurcaciones situacionales, resolución de conflictos en code reviews y dilemas de liderazgo técnico.",
			en: "Interactive 2D gamified platform designed to train and evaluate interpersonal engineering soft skills through situational branch choices, conflict resolution dialogues, active listening challenges, and team leadership dilemmas.",
		},
		features: [
			{
				heading: {
					es: "1. Resolución de Conflictos en Code Reviews",
					en: "1. Code Review Conflict Resolution",
				},
				text: {
					es: "Interacciones simuladas con Product Owners, Tech Leads y QA que exigen comunicación técnica constructiva y empática.",
					en: "Simulated interactions with Product Owners, Tech Leads, and QA requiring constructive, empathetic technical communication.",
				},
			},
			{
				heading: {
					es: "2. Dilemas de Deuda Técnica vs Velocidad",
					en: "2. Architectural Trade-Off Dilemmas",
				},
				text: {
					es: "Escenarios estratégicos que obligan a ponderar entre entregas rápidas de características y sostenibilidad a largo plazo.",
					en: "Strategic scenarios forcing decisions between rapid feature delivery and long-term technical debt mitigation.",
				},
			},
			{
				heading: {
					es: "3. Gestión de Incidentes Críticos en Producción",
					en: "3. Crisis Management & Outages",
				},
				text: {
					es: "Simulaciones de caídas en entornos productivos que exigen temple, comunicación clara con stakeholders y triaje ordenado.",
					en: "High-pressure production incident simulations demanding clear stakeholder updates and composed triage.",
				},
			},
			{
				heading: {
					es: "4. Matriz de Puntuación de Inteligencia Emocional",
					en: "4. Performance Scoring Matrix",
				},
				text: {
					es: "Métricas estructuradas que evalúan la inteligencia emocional, la sinergia de equipo y la apropiación de problemas.",
					en: "Comprehensive scoring matrix assessing emotional intelligence, team synergy, and problem ownership.",
				},
			},
		],
		badges: [
			{ label: { es: "MOTOR", en: "ENGINE" }, v1: "Canvas 2D", v2: "Fluid 60 FPS" },
			{ label: { es: "LÓGICA", en: "LOGIC" }, v1: "Vanilla JS", v2: "ES6+ Modules" },
			{ label: { es: "AUDIO", en: "AUDIO" }, v1: "Web Audio API", v2: "Synthesizer" },
			{ label: { es: "DISEÑO", en: "DESIGN" }, v1: "Custom Art", v2: "Responsive Grid" },
		],
		tags: ["Canvas 2D", "Vanilla JS", "Web Audio API", "Game Loop", "Educación"],
		github: "https://github.com/TEstebanGQ",
		demo: "https://github.com/TEstebanGQ",
	},
	{
		id: "lms-abc",
		title: "LMS ABC Learning Platform",
		subtitle: {
			es: "Sistema Modular Ligero de Gestión de Aprendizaje",
			en: "Modular Lightweight Learning Management System",
		},
		description: {
			es: "Sistema de gestión de aprendizaje (LMS) modular diseñado para la administración de cursos académicos, entrega de lecciones multimedia y seguimiento del progreso de estudiantes. Construido con Vanilla JavaScript y CSS3 moderno sin sobrecarga de frameworks.",
			en: "Modular Learning Management System (LMS) designed for academic course administration, multimedia lesson delivery, and student progress tracking. Built with lightweight Vanilla JavaScript and CSS3, requiring zero heavy frameworks.",
		},
		features: [
			{
				heading: {
					es: "1. Catálogo Público de Cursos",
					en: "1. Public Course Catalog",
				},
				text: {
					es: "Catálogo abierto que permite a los estudiantes explorar asignaturas, revisar temarios detallados y consultar instructores.",
					en: "Open catalog enabling prospective students to search subjects, review syllabi, and view instructor credentials.",
				},
			},
			{
				heading: {
					es: "2. Gestión de Instructores & Lecciones",
					en: "2. Instructor & Content Management",
				},
				text: {
					es: "Panel integral para crear, ordenar y estructurar unidades modulares y lecciones enriquecidas con contenido multimedia.",
					en: "Comprehensive panel for creating, editing, and sequencing courses, modular units, and structured rich-media lessons.",
				},
			},
			{
				heading: {
					es: "3. Matrículas & Seguimiento de Calificaciones",
					en: "3. Enrollment & Grade Tracking",
				},
				text: {
					es: "Portal dedicado para la inscripción a cursos, registro de evaluaciones y visualización del avance académico del alumno.",
					en: "Dedicated portal for managing course registrations, logging exam scores, and visualizing academic progress.",
				},
			},
			{
				heading: {
					es: "4. Persistencia Local Ultrarrápida",
					en: "4. Client-Side Persistence",
				},
				text: {
					es: "Almacenamiento estructurado con LocalStorage API que entrega transiciones instantáneas con cero sobrecosto de hosting.",
					en: "Structured LocalStorage persistence delivering instantaneous page transitions with zero hosting server overhead.",
				},
			},
		],
		badges: [
			{ label: { es: "ESTRUCTURA", en: "STRUCTURE" }, v1: "Semantic HTML5", v2: "WAI-ARIA Access" },
			{ label: { es: "ESTILOS", en: "STYLING" }, v1: "Modern CSS3", v2: "Flex & Grid" },
			{ label: { es: "LÓGICA", en: "LOGIC" }, v1: "Vanilla JS", v2: "ES6+ Modules" },
			{ label: { es: "STORAGE", en: "STORAGE" }, v1: "LocalStorage API", v2: "Zero Overhead" },
		],
		tags: ["HTML5", "CSS3", "Vanilla JS", "LocalStorage API", "Modular"],
		github: "https://github.com/TEstebanGQ",
		demo: "https://github.com/TEstebanGQ",
	},
	{
		id: "the-book",
		title: "El Libro de Tomás Esteban",
		subtitle: {
			es: "Portafolio Interactivo 3D con Físicas Realistas & WebGL",
			en: "Interactive 3D Codex with Realistic Physics & WebGL",
		},
		description: {
			es: "Experiencia tridimensional interactiva inspirada en los códices del Renacimiento. Desarrollada con Three.js, shaders GLSL y físicas de deformación de páginas para navegación inmersiva de 32 páginas en alta resolución.",
			en: "Interactive three-dimensional experience inspired by Renaissance codices. Built with Three.js, custom GLSL shaders, and page-curl physics for immersive navigation through 32 high-resolution parchment pages.",
		},
		features: [
			{
				heading: {
					es: "1. Físicas de Paginación 3D en Tiempo Real",
					en: "1. Real-Time 3D Page Curl Physics",
				},
				text: {
					es: "Modelado geométrico con mallas segmentadas que responden al arrastre táctil y del cursor con cinemática realista.",
					en: "Segmented mesh geometry dynamically deforming in response to touch drag and mouse coordinates with realistic kinematics.",
				},
			},
			{
				heading: {
					es: "2. Arquitectura Híbrida Responsiva",
					en: "2. Hybrid Responsive Architecture",
				},
				text: {
					es: "Detección inteligente de viewport que adapta la vista de códice tridimensional a vista móvil optimizada sin perder contenido.",
					en: "Intelligent viewport detection adapting between immersive 3D codex and responsive mobile view without compromising content depth.",
				},
			},
			{
				heading: {
					es: "3. Hotspots Interactivos & Multilingüe (ES/EN)",
					en: "3. Interactive Hotspots & Full Bilingual Support",
				},
				text: {
					es: "Áreas activas para interacción directa, cambio de textura de páginas en tiempo real y soporte fluido en español e inglés.",
					en: "Raycasted interactive hotspots, live texture swapping, and seamless language synchronization between Spanish and English.",
				},
			},
			{
				heading: {
					es: "4. Alto Rendimiento a 60 FPS",
					en: "4. High-Performance 60 FPS Rendering",
				},
				text: {
					es: "Gestión eficiente de recursos WebGL, mipmapping optimizado y liberación de texturas para ejecución fluida en todo dispositivo.",
					en: "Optimized WebGL resource management, tailored mipmapping, and active texture disposal ensuring smooth performance on all devices.",
				},
			},
		],
		badges: [
			{ label: { es: "RENDER", en: "RENDER" }, v1: "Three.js", v2: "WebGL & Shaders" },
			{ label: { es: "LENGUAJE", en: "LANGUAGE" }, v1: "TypeScript", v2: "Vite Bundler" },
			{ label: { es: "DISEÑO", en: "DESIGN" }, v1: "Renaissance Codex", v2: "High-Res Pergamino" },
			{ label: { es: "SOPORTE", en: "SUPPORT" }, v1: "Bilingüe ES / EN", v2: "60 FPS Fluid" },
		],
		tags: ["Three.js", "WebGL", "TypeScript", "Vite", "Shaders", "Responsive"],
		github: "https://github.com/TEstebanGQ/PORTAFOLIO",
	},
];

export class MobileView {
	private viewEl!: HTMLElement;
	private switchBtnToMobile!: HTMLElement;
	private currentLang: Language;
	private isVisible = false;
	private onSwitchTo3DCallback: () => void;
	private onSwitchToMobileCallback: () => void;
	private onLangChangeCallback: (lang: Language) => void;

	constructor(
		initialLang: Language,
		onSwitchTo3D: () => void,
		onSwitchToMobile: () => void,
		onLangChange: (lang: Language) => void,
	) {
		this.currentLang = initialLang;
		this.onSwitchTo3DCallback = onSwitchTo3D;
		this.onSwitchToMobileCallback = onSwitchToMobile;
		this.onLangChangeCallback = onLangChange;

		this.createViewElement();
		this.create3DSwitchButton();
		this.render();
	}

	public getIsVisible(): boolean {
		return this.isVisible;
	}

	public show() {
		this.isVisible = true;
		this.viewEl.classList.add("active");
		this.updateSwitchBtnVisibility();
		document.body.style.overflow = "auto";
	}

	public hide() {
		this.isVisible = false;
		this.viewEl.classList.remove("active");
		this.updateSwitchBtnVisibility();
		document.body.style.overflow = "hidden";
	}

	public updateSwitchBtnVisibility() {
		const isMobile = window.innerWidth <= 820;
		if (this.isVisible) {
			this.switchBtnToMobile.classList.add("is-hidden");
		} else if (isMobile) {
			this.switchBtnToMobile.classList.remove("is-hidden");
		} else {
			this.switchBtnToMobile.classList.add("is-hidden");
		}
	}

	public setLanguage(lang: Language) {
		this.currentLang = lang;
		this.render();
	}

	private create3DSwitchButton() {
		this.switchBtnToMobile = document.createElement("button");
		this.switchBtnToMobile.type = "button";
		this.switchBtnToMobile.className = "floating-3d-switch is-hidden";
		this.switchBtnToMobile.setAttribute("aria-label", "Abrir vista resumen");
		this.switchBtnToMobile.innerHTML = `
			<span class="switch-glyph">✦</span>
			<span class="switch-text">${this.currentLang === "en" ? "Mobile View" : "Vista Resumen"}</span>
		`;
		this.switchBtnToMobile.addEventListener("click", () => {
			this.onSwitchToMobileCallback();
		});
		document.body.appendChild(this.switchBtnToMobile);

		window.addEventListener("resize", () => {
			this.updateSwitchBtnVisibility();
		});
		this.updateSwitchBtnVisibility();
	}

	private createViewElement() {
		this.viewEl = document.createElement("section");
		this.viewEl.id = "mobile-portfolio-view";
		this.viewEl.setAttribute("aria-label", "Portafolio Adaptado");
		document.body.appendChild(this.viewEl);
	}

	private render() {
		const isEn = this.currentLang === "en";
		const texts = I18N_TEXTS[this.currentLang];

		const whatsAppUrl = isEn
			? "https://wa.me/573167755887?text=Hello%20Tom%C3%A1s,%20I'm%20contacting%20you%20from%20your%20portfolio%20website"
			: "https://wa.me/573167755887?text=Hola%20Tom%C3%A1s,%20te%20contacto%20desde%20tu%20portafolio%20web";

		const emailAddress = "tomasestebangonzalezquintero@gmail.com";

		this.viewEl.innerHTML = `
			<div class="mobile-container">
				<!-- Top Bar -->
				<header class="mobile-topbar">
					<span class="mobile-badge">${texts.mobileBadge}</span>
					<button type="button" class="mobile-lang-btn" aria-label="Cambiar idioma">
						${isEn ? "ESPAÑOL" : "ENGLISH"}
					</button>
				</header>

				<!-- Hero Profile -->
				<div class="mobile-hero">
					<div class="mobile-avatar-wrapper">
						<div class="mobile-avatar-frame"></div>
						<img src="/img/photo.jpg" alt="Tomás Esteban González Quintero" class="mobile-avatar" width="112" height="112" />
					</div>
					<h1 class="mobile-name">Tomás Esteban</h1>
					<div class="mobile-role">${texts.heroRole}</div>
					<div class="mobile-location">${texts.heroLocation}</div>
					<p class="mobile-bio">${texts.heroBio}</p>

					<!-- Quick Contact Actions -->
					<div class="mobile-actions">
						<a href="${whatsAppUrl}" target="_blank" rel="noopener noreferrer" class="mobile-action-btn primary">
							<span class="btn-glyph">✦</span> ${texts.contactWhatsApp}
						</a>
						<a href="https://www.linkedin.com/in/tomas-esteban-gonzalez-quintero/" target="_blank" rel="noopener noreferrer" class="mobile-action-btn">
							<span class="btn-glyph">✦</span> ${texts.contactLinkedIn}
						</a>
						<a href="https://github.com/TEstebanGQ" target="_blank" rel="noopener noreferrer" class="mobile-action-btn">
							<span class="btn-glyph">✦</span> ${texts.contactGitHub}
						</a>
						<a href="mailto:${emailAddress}" class="mobile-action-btn">
							<span class="btn-glyph">✦</span> ${texts.contactEmail}
						</a>
					</div>
				</div>

				<!-- ================= CAPÍTULO I ================= -->
				<div class="mobile-section">
					<div class="mobile-corner top-left"></div>
					<div class="mobile-corner top-right"></div>
					<div class="mobile-corner bottom-left"></div>
					<div class="mobile-corner bottom-right"></div>

					<div class="mobile-section-header">
						<span class="mobile-fleuron">❧</span>
						<span class="mobile-chapter-tag">${isEn ? "CHAPTER I" : "CAPÍTULO I"}</span>
						<h2 class="mobile-section-title">${texts.sectionAbout}</h2>
						<div class="mobile-section-subtitle">
							${isEn ? "The Evolutionary Path of a Software Craftsman" : "El Camino Evolutivo de un Artesano del Software"}
						</div>
					</div>

					<!-- Story Paragraphs -->
					<div class="mobile-narrative-box">
						<p class="narrative-p">
							${isEn
								? "From an early age, I felt a deep fascination for logic, mathematics, and digital systems. Code quickly became my primary language to create, construct, and solve real-world challenges."
								: "Desde temprana edad, sentí una profunda fascinación por la lógica, las matemáticas y los sistemas digitales. El código se convirtió en mi lenguaje predilecto para construir y resolver desafíos del mundo real."}
						</p>
						<p class="narrative-p">
							${isEn
								? "I evolved building robust enterprise backends with Python, FastAPI, and Java Spring Boot. I understood early on that the foundation of any enduring software lies in strict architectural integrity."
								: "Evolucioné desarrollando backends empresariales con Python (FastAPI), C# (.NET 9) y Java (Spring Boot), comprendiendo que los cimientos de un software duradero radican en su integridad arquitectónica."}
						</p>
						<p class="narrative-p">
							${isEn
								? "At Campuslands, I forged rigorous engineering habits: full-stack systems, clean architectures, and high-concurrency database design up to 4NF under agile Scrum delivery."
								: "En Campuslands forjé hábitos de alta exigencia: sistemas full-stack, arquitecturas limpias y diseño de bases de datos de alta concurrencia hasta 4NF bajo entregas ágiles Scrum."}
						</p>
						<p class="narrative-p">
							${isEn
								? "Today, I architect scalable distributed platforms, Model Context Protocol (MCP) servers, and autonomous n8n workflows with AI. I deliver verifiable technical rigor and tangible results."
								: "Hoy diseño plataformas distribuidas, servidores Model Context Protocol (MCP) y flujos autónomos en n8n con IA, aportando rigor técnico comprobable y resultados tangibles."}
						</p>
					</div>

					<!-- Strategic Projections / Interests -->
					<div class="skills-category">
						<div class="skills-category-title">${isEn ? "Strategic Future Focus: AI Engineering" : "Enfoque Futuro: Ingeniería de IA & Agentes"}</div>
						<div class="skills-tags-wrap">
							<span class="skill-tag highlight">LangGraph (Multi-Agentes)</span>
							<span class="skill-tag highlight">Model Context Protocol (MCP)</span>
							<span class="skill-tag">n8n Workflows + LLM</span>
							<span class="skill-tag">PyTorch & OpenCV (Visión)</span>
							<span class="skill-tag">RAG & Embeddings</span>
						</div>
					</div>

					<div class="skills-category">
						<div class="skills-category-title">${isEn ? "Strategic Future Focus: Data Analysis" : "Enfoque Futuro: Análisis de Datos & Rendimiento"}</div>
						<div class="skills-tags-wrap">
							<span class="skill-tag highlight">Normalización Estricta 4NF</span>
							<span class="skill-tag highlight">Análisis RFM</span>
							<span class="skill-tag">PostgreSQL 16 & MySQL 8</span>
							<span class="skill-tag">Triggers & Stored Procedures</span>
							<span class="skill-tag">Modelado Estadístico & BI</span>
						</div>
					</div>

					<div class="skills-category">
						<div class="skills-category-title">${isEn ? "Strategic Future Focus: Cybersecurity" : "Enfoque Futuro: Ciberseguridad & DevSecOps"}</div>
						<div class="skills-tags-wrap">
							<span class="skill-tag highlight">Seguridad Defensiva OWASP</span>
							<span class="skill-tag highlight">JWT Reforzado & BCrypt</span>
							<span class="skill-tag">Rate Limiting Distribuido</span>
							<span class="skill-tag">Control de Acceso RBAC</span>
							<span class="skill-tag">Hardening de Endpoints</span>
						</div>
					</div>

					<div class="skills-category">
						<div class="skills-category-title">${isEn ? "Core Full Stack Stack & Architecture" : "Stack Principal & Arquitectura"}</div>
						<div class="skills-tags-wrap">
							<span class="skill-tag highlight">Node.js (TypeScript)</span>
							<span class="skill-tag highlight">C# (.NET 9 Hexagonal)</span>
							<span class="skill-tag highlight">Java 17 (Spring Boot 3)</span>
							<span class="skill-tag highlight">Python (FastAPI)</span>
							<span class="skill-tag">React Native</span>
							<span class="skill-tag">Supabase</span>
							<span class="skill-tag">Docker</span>
							<span class="skill-tag">Three.js & WebGL</span>
							<span class="skill-tag">Scrum & Kanban</span>
						</div>
					</div>
				</div>

				<!-- ================= CAPÍTULO II ================= -->
				<div class="mobile-section">
					<div class="mobile-corner top-left"></div>
					<div class="mobile-corner top-right"></div>
					<div class="mobile-corner bottom-left"></div>
					<div class="mobile-corner bottom-right"></div>

					<div class="mobile-section-header">
						<span class="mobile-fleuron">❧</span>
						<span class="mobile-chapter-tag">${isEn ? "CHAPTER II" : "CAPÍTULO II"}</span>
						<h2 class="mobile-section-title">${texts.sectionJourney}</h2>
						<div class="mobile-section-subtitle">
							${isEn ? "The Path of Continuous Learning & Milestones" : "El Sendero del Aprendizaje Continuo y la Evolución Técnica"}
						</div>
					</div>

					<div class="mobile-timeline">
						<div class="timeline-item">
							<div class="timeline-marker">✦</div>
							<div class="timeline-content">
								<div class="timeline-date">2023</div>
								<h3 class="timeline-title">${isEn ? "Programming Foundations" : "Inicios en Programación & Fundamentos"}</h3>
								<p class="timeline-desc">
									${isEn
										? "Started programming with Python, mastering core backend logic, algorithms & data structures."
										: "Comienzo en el desarrollo con Python, dominando lógica backend, estructuras de datos y algoritmia fundamental."}
								</p>
							</div>
						</div>

						<div class="timeline-item">
							<div class="timeline-marker">✦</div>
							<div class="timeline-content">
								<div class="timeline-date">${isEn ? "JAN 2024 - JUN 2024" : "ENE 2024 - JUN 2024"}</div>
								<h3 class="timeline-title">${isEn ? "Hardware & IT Infrastructure" : "Infraestructura & Diagnóstico IT"}</h3>
								<p class="timeline-desc">
									${isEn
										? "Enterprise hardware diagnostics, system architecture, maintenance, and IT infrastructure support."
										: "Diagnóstico de hardware empresarial, arquitectura de sistemas, mantenimiento preventivo/correctivo y soporte de infraestructura TI."}
								</p>
							</div>
						</div>

						<div class="timeline-item">
							<div class="timeline-marker">✦</div>
							<div class="timeline-content">
								<div class="timeline-date">${isEn ? "JUN 2024 - NOV 2024" : "JUN 2024 - NOV 2024"}</div>
								<h3 class="timeline-title">${isEn ? "Software Technologist (Honors)" : "Técnico en Desarrollo de Software (Con Honores)"}</h3>
								<p class="timeline-desc">
									${isEn
										? "Software Development Technologist at Promoción Social. Graduated Top of the Class with Academic Honors."
										: "Técnico en Desarrollo de Software en Promoción Social. Graduado como Mejor de la Promoción con Honores Académicos."}
								</p>
							</div>
						</div>

						<div class="timeline-item">
							<div class="timeline-marker">✦</div>
							<div class="timeline-content">
								<div class="timeline-date">${isEn ? "DEC 2024 - 2025" : "DIC 2024 - 2025"}</div>
								<h3 class="timeline-title">${isEn ? "SENA Software Analysis & Development" : "Tecnólogo SENA en Análisis & Desarrollo (ADSO)"}</h3>
								<p class="timeline-desc">
									${isEn
										? "SENA Technologist in Software Analysis & Development. Advanced systems modeling, requirements, and relational databases."
										: "Tecnólogo en Análisis y Desarrollo de Software (ADSO) en el SENA. Modelado formal de requerimientos, diseño de sistemas distribuidos y bases de datos relacionales avanzadas."}
								</p>
							</div>
						</div>

						<div class="timeline-item">
							<div class="timeline-marker">✦</div>
							<div class="timeline-content">
								<div class="timeline-date">${isEn ? "2025 - 2026" : "2025 - 2026"}</div>
								<h3 class="timeline-title">${isEn ? "Campuslands Elite Academy" : "Campuslands Academia de Élite de Software"}</h3>
								<p class="timeline-desc">
									${isEn
										? "Campuslands Elite Software Academy. Developing production multi-agent AI platforms, LangGraph workflows, Spring Boot backends, and strict 4NF databases under Scrum."
										: "Academia de Élite Campuslands. Desarrollo de sistemas en producción, microservicios en Spring Boot 3, grafos multi-agente con LangGraph, servidores MCP y bases de datos en 4NF bajo Scrum."}
								</p>
							</div>
						</div>

						<div class="timeline-item">
							<div class="timeline-marker">✦</div>
							<div class="timeline-content">
								<div class="timeline-date">${isEn ? "2026 AND BEYOND" : "2026 EN ADELANTE"}</div>
								<h3 class="timeline-title">${isEn ? "Strategic Engineering Vision" : "Visión Profesional Estratégica"}</h3>
								<p class="timeline-desc">
									${isEn
										? "Next-generation distributed architectures, event-driven systems, spatial web & 3D visualization, and global technical leadership."
										: "Arquitecturas de microservicios distribuidos, sistemas orientados a eventos, liderazgo técnico, web inmersiva en 3D e innovación continua en agentes autónomos de IA."}
								</p>
							</div>
						</div>
					</div>
				</div>

				<!-- ================= CAPÍTULO III ================= -->
				<div class="mobile-section">
					<div class="mobile-corner top-left"></div>
					<div class="mobile-corner top-right"></div>
					<div class="mobile-corner bottom-left"></div>
					<div class="mobile-corner bottom-right"></div>

					<div class="mobile-section-header">
						<span class="mobile-fleuron">❧</span>
						<span class="mobile-chapter-tag">${isEn ? "CHAPTER III" : "CAPÍTULO III"}</span>
						<h2 class="mobile-section-title">${texts.sectionExperience}</h2>
						<div class="mobile-section-subtitle">
							${isEn ? "Production Systems & Engineering Track Record" : "Experiencia en Producción Real y Consultoría Técnica"}
						</div>
					</div>

					<div class="mobile-experience-blocks">
						<!-- Block 1: Campuslands -->
						<div class="experience-card">
							<div class="exp-card-header">
								<div>
									<h3 class="exp-card-title">Campuslands / Thor Systems</h3>
									<div class="exp-card-role">${isEn ? "Software Engineer & Backend Architect" : "Ingeniero de Software & Arquitectura Backend"}</div>
								</div>
								<span class="exp-card-badge">Campuslands</span>
							</div>
							<p class="exp-card-desc">
								${isEn
									? "Participated actively in corporate engineering teams under agile Scrum, with weekly continuous delivery sprints, rigorous peer code reviews, and high-demand technical challenges. Led backend architectures for LogiTrack WMS and Campuslands Inteligente multi-agent systems."
									: "Participación activa en equipos corporativos bajo metodología Scrum con sprints de entrega continua semanal, revisión rigurosa de código y resolución de desafíos de alta exigencia. Lideré la arquitectura backend de LogiTrack WMS y la plataforma multi-agente Campuslands Inteligente."}
							</p>
							<div class="exp-highlights">
								<div class="exp-highlight-item">
									<strong class="highlight-title">${isEn ? "Soft Skills & Leadership:" : "Habilidades Blandas & Liderazgo:"}</strong>
									<span>${isEn ? "Technical leadership under Scrum & Kanban, assertive communication, disciplined execution under pressure." : "Liderazgo técnico bajo Scrum y Kanban, comunicación asertiva, alta adaptabilidad y resolución disciplinada bajo presión."}</span>
								</div>
								<div class="exp-highlight-item">
									<strong class="highlight-title">${isEn ? "Technical Proficiency:" : "Dominio Tecnológico:"}</strong>
									<span>${isEn ? "Spring Boot 3, Java 17, strict 4NF relational schemas in MySQL/PostgreSQL, FastAPI async APIs, Docker and CI/CD." : "Spring Boot 3, Java 17, esquemas relacionales estrictos en 4NF en MySQL/PostgreSQL, APIs asíncronas en FastAPI, Docker y CI/CD."}</span>
								</div>
							</div>
						</div>

						<!-- Block 2: Freelance & Consulting -->
						<div class="experience-card">
							<div class="exp-card-header">
								<div>
									<h3 class="exp-card-title">${isEn ? "Independent Consulting & Freelance" : "Consultoría Independiente & Soluciones a Medida"}</h3>
									<div class="exp-card-role">${isEn ? "Full Stack & Automation Architect" : "Ingeniero Full Stack & Automatización de Procesos"}</div>
								</div>
								<span class="exp-card-badge">Consulting</span>
							</div>
							<p class="exp-card-desc">
								${isEn
									? "Independent software engineering delivering custom enterprise platforms, automated n8n workflows, and robust relational architectures solving tangible operational bottlenecks for organizations."
									: "Desarrollo de software independiente enfocado en resolver cuellos de botella empresariales mediante plataformas a medida, flujos automatizados en n8n y arquitecturas relacionales blindadas."}
							</p>
							<div class="exp-highlights">
								<div class="exp-highlight-item">
									<strong class="highlight-title">${isEn ? "Full Stack & APIs:" : "Full Stack & APIs:"}</strong>
									<span>${isEn ? "Modern web interfaces with React/TypeScript and secure high-throughput backends with FastAPI and Spring Boot." : "Interfaces web modernas con React/TypeScript y backends seguros de alto rendimiento en FastAPI y Spring Boot."}</span>
								</div>
								<div class="exp-highlight-item">
									<strong class="highlight-title">${isEn ? "Intelligent Automation:" : "Automatización Inteligente:"}</strong>
									<span>${isEn ? "Autonomous workflows in n8n integrating payment gateways, Telegram/WhatsApp bots, and live CRMs." : "Flujos autónomos en n8n integrando pasarelas de pago, bots de Telegram/WhatsApp y CRMs en tiempo real."}</span>
								</div>
								<div class="exp-highlight-item">
									<strong class="highlight-title">${isEn ? "AI & MCP Integration:" : "Integración de IA & MCP:"}</strong>
									<span>${isEn ? "Model Context Protocol servers and RAG pipelines connecting LLMs directly to enterprise tooling." : "Servidores Model Context Protocol y pipelines RAG para conectar LLMs directamente a bases de datos y herramientas empresariales."}</span>
								</div>
							</div>
						</div>
					</div>
				</div>

				<!-- ================= CAPÍTULO IV ================= -->
				<div class="mobile-section">
					<div class="mobile-corner top-left"></div>
					<div class="mobile-corner top-right"></div>
					<div class="mobile-corner bottom-left"></div>
					<div class="mobile-corner bottom-right"></div>

					<div class="mobile-section-header">
						<span class="mobile-fleuron">❧</span>
						<span class="mobile-chapter-tag">${isEn ? "CHAPTER IV" : "CAPÍTULO IV"}</span>
						<h2 class="mobile-section-title">${texts.sectionProjects}</h2>
						<div class="mobile-section-subtitle">
							${isEn ? "Selected Works, Systems Architectures & Live Demonstrations" : "Selección de Sistemas, Arquitecturas y Demostraciones en Vivo"}
						</div>
					</div>

					<div class="mobile-projects-list">
						${DETAILED_PROJECTS.map(proj => `
							<article class="mobile-project-card" id="card-${proj.id}">
								<div class="project-card-header">
									<h3 class="project-card-title">${proj.title}</h3>
								</div>
								<div class="project-card-subtitle">${isEn ? proj.subtitle.en : proj.subtitle.es}</div>
								<p class="project-card-desc">${isEn ? proj.description.en : proj.description.es}</p>

								<!-- Capabilities Accordion / List -->
								<div class="project-capabilities-box">
									<div class="capabilities-header">
										${isEn ? "KEY CAPABILITIES & ARCHITECTURE" : "CAPACIDADES & ARQUITECTURA CLAVE"}
									</div>
									<div class="capabilities-list">
										${proj.features.map(f => `
											<div class="capability-item">
												<div class="capability-title">${isEn ? f.heading.en : f.heading.es}</div>
												<div class="capability-desc">${isEn ? f.text.en : f.text.es}</div>
											</div>
										`).join("")}
									</div>
								</div>

								<!-- 4 Column Badges Matrix -->
								<div class="project-badges-matrix">
									${proj.badges.map(b => `
										<div class="badge-col">
											<div class="badge-col-header">${isEn ? b.label.en : b.label.es}</div>
											<div class="badge-col-v1">${b.v1}</div>
											<div class="badge-col-v2">${b.v2}</div>
										</div>
									`).join("")}
								</div>

								<!-- Tag pills -->
								<div class="project-card-tags">
									${proj.tags.map(t => `<span class="project-tag">${t}</span>`).join("")}
								</div>

								<!-- Direct Action Links (NO EMOJIS) -->
								<div class="project-card-buttons">
									${proj.github ? `
										<a href="${proj.github}" target="_blank" rel="noopener noreferrer" class="project-btn" aria-label="${texts.viewCodeBtn}">
											<span class="btn-glyph">✦</span> ${texts.viewCodeBtn}
										</a>
									` : ""}
									${proj.demo ? `
										<a href="${proj.demo}" target="_blank" rel="noopener noreferrer" class="project-btn demo" aria-label="${texts.liveDemoBtn}">
											<span class="btn-glyph">✦</span> ${texts.liveDemoBtn}
										</a>
									` : ""}
								</div>
							</article>
						`).join("")}
					</div>

					<!-- ================= CIERRE: HOJA DE VIDA & CONTACTO DIRECTO ================= -->
					<div class="mobile-cv-section" id="section-contact-cv">
						<div class="mobile-corner top-left"></div>
						<div class="mobile-corner top-right"></div>
						<div class="mobile-corner bottom-left"></div>
						<div class="mobile-corner bottom-right"></div>

						<div class="mobile-section-header">
							<span class="mobile-fleuron">❧ ✦ ❧</span>
							<span class="mobile-chapter-tag">${texts.cvSectionTag}</span>
							<h3 class="mobile-section-title">${texts.cvSectionTitle}</h3>
							<div class="mobile-section-subtitle">${texts.cvSectionSubtitle}</div>
						</div>

						<!-- CV Download Card -->
						<div class="mobile-cv-card">
							<div class="cv-card-top">
								<div class="cv-badge-row">
									<span class="cv-official-pill">✦ ${texts.cvOfficialBadge}</span>
									<span class="cv-format-pill">PDF · A4</span>
								</div>
								<h4 class="cv-person-name">Tomás Esteban González Quintero</h4>
								<div class="cv-person-role">${texts.heroRole}</div>
								<div class="cv-person-sub">ID: 1.097.101.275 · Bucaramanga / Floridablanca, Colombia</div>
							</div>

							<div class="cv-highlights-box">
								<div class="cv-highlight-row">
									<span class="cv-hl-dot">✦</span>
									<span class="cv-hl-text"><strong>${isEn ? "Specialized Focus:" : "Enfoque Especializado:"}</strong> ${isEn ? "Full Stack, AI Agents (MCP / LangGraph), Hexagonal .NET & Spring Boot 3" : "Full Stack, Agentes de IA (MCP / LangGraph), Arquitectura Hexagonal .NET y Spring Boot 3"}</span>
								</div>
								<div class="cv-highlight-row">
									<span class="cv-hl-dot">✦</span>
									<span class="cv-hl-text"><strong>${texts.cvEducationLabel}:</strong> ${texts.cvEducationValue}</span>
								</div>
							</div>

							<!-- Action Buttons -->
							<div class="cv-card-actions">
								<a
									href="/Tomas_Esteban_Gonzalez_Quintero_CV.pdf"
									download="Tomas_Esteban_Gonzalez_Quintero_CV.pdf"
									class="cv-action-btn primary"
									aria-label="${texts.downloadCV}"
								>
									<span class="cv-btn-glyph">✦</span>
									<span class="cv-btn-title">${texts.downloadCV}</span>
									<span class="cv-btn-meta">327 KB · PDF</span>
								</a>
								<a
									href="/Tomas_Esteban_Gonzalez_Quintero_CV.pdf"
									target="_blank"
									rel="noopener noreferrer"
									class="cv-action-btn secondary"
									aria-label="${texts.viewCV}"
								>
									<span class="cv-btn-glyph">↗</span>
									<span class="cv-btn-title">${texts.viewCV}</span>
								</a>
							</div>
						</div>

						<!-- Contact Channels (Repeated at the end of projects) -->
						<div class="mobile-cv-contact-box">
							<div class="contact-box-header">
								<span class="contact-box-title">✦ ${texts.cvContactHeader} ✦</span>
							</div>

							<div class="mobile-actions cv-contact-actions">
								<a href="${whatsAppUrl}" target="_blank" rel="noopener noreferrer" class="mobile-action-btn primary">
									<span class="btn-glyph">✦</span> ${texts.contactWhatsApp}
								</a>
								<a href="https://www.linkedin.com/in/tomas-esteban-gonzalez-quintero/" target="_blank" rel="noopener noreferrer" class="mobile-action-btn">
									<span class="btn-glyph">✦</span> ${texts.contactLinkedIn}
								</a>
								<a href="https://github.com/TEstebanGQ" target="_blank" rel="noopener noreferrer" class="mobile-action-btn">
									<span class="btn-glyph">✦</span> ${texts.contactGitHub}
								</a>
								<a href="mailto:${emailAddress}" class="mobile-action-btn">
									<span class="btn-glyph">✦</span> ${texts.contactEmail}
								</a>
							</div>

							<!-- Detailed Contact Information Grid -->
							<div class="cv-details-grid">
								<div class="cv-detail-cell">
									<span class="cell-label">${texts.cvPhoneLabel}</span>
									<a href="https://wa.me/573167755887" target="_blank" rel="noopener noreferrer" class="cell-value link">+57 316 775 5887</a>
								</div>
								<div class="cv-detail-cell">
									<span class="cell-label">${texts.cvEmailLabel}</span>
									<a href="mailto:${emailAddress}" class="cell-value link">${emailAddress}</a>
								</div>
								<div class="cv-detail-cell">
									<span class="cell-label">${texts.cvLocationLabel}</span>
									<span class="cell-value">Floridablanca / Bucaramanga, Santander</span>
								</div>
								<div class="cv-detail-cell">
									<span class="cell-label">${texts.cvIdLabel}</span>
									<span class="cell-value">1.097.101.275</span>
								</div>
							</div>
						</div>
					</div>

					<!-- Tip Banner -->
					<div class="mobile-tip-banner">
						<span class="tip-banner-glyph">✦</span>
						<p class="tip-banner-text">${texts.rotateHint}</p>
					</div>
				</div>

				<!-- Footer -->
				<footer class="mobile-footer">
					<div class="footer-fleuron">❧ ✦ ❧</div>
					<div class="footer-copy">Tomás Esteban González Quintero · Bucaramanga, Colombia</div>
					<div class="footer-tech">Architected with Three.js, TypeScript & Semantic Modern Web</div>
				</footer>
			</div>

			<!-- Floating Switcher: Switch to 3D Book -->
			<button type="button" class="floating-view-switch" id="btn-switch-3d" aria-label="${texts.mobileSwitchTo3D}">
				<span class="switch-glyph">✦</span>
				<span class="switch-label">${texts.mobileSwitchTo3D}</span>
			</button>
		`;

		// Attach events
		const langBtn = this.viewEl.querySelector<HTMLButtonElement>(".mobile-lang-btn");
		langBtn?.addEventListener("click", () => {
			const nextLang: Language = this.currentLang === "es" ? "en" : "es";
			this.onLangChangeCallback(nextLang);
		});

		const switch3DBtn = this.viewEl.querySelector<HTMLButtonElement>("#btn-switch-3d");
		switch3DBtn?.addEventListener("click", () => {
			this.onSwitchTo3DCallback();
		});

		// Update 3D switch button text (when viewing 3D)
		if (this.switchBtnToMobile) {
			const switchText = this.switchBtnToMobile.querySelector(".switch-text");
			if (switchText) {
				switchText.textContent = texts.mobileSwitchToWeb;
			}
		}
	}
}
