import Flipbook from "./flipbook";

export interface Chapter {
	id: number;
	roman: string;
	title: string;
	page: number;
	minProgress: number;
	maxProgress: number;
}

export const CHAPTERS: Chapter[] = [
	{
		id: 1,
		roman: "I",
		title: "Sobre Mí",
		page: 1,
		minProgress: 0.5,
		maxProgress: 3.5,
	},
	{
		id: 2,
		roman: "II",
		title: "Trayectoria",
		page: 4,
		minProgress: 3.5,
		maxProgress: 5.5,
	},
	{
		id: 3,
		roman: "III",
		title: "Experiencia",
		page: 6,
		minProgress: 5.5,
		maxProgress: 8.5,
	},
	{
		id: 4,
		roman: "IV",
		title: "Proyectos",
		page: 9,
		minProgress: 8.5,
		maxProgress: 99,
	},
];

export class ChaptersNav {
	private flipbook: Flipbook;
	private containerEl!: HTMLElement;
	private navEl!: HTMLElement;
	private toggleBtn!: HTMLElement;
	private chapterButtons: Map<number, HTMLButtonElement> = new Map();
	private activeChapterId: number | null = null;
	private isMobileOpen = false;

	constructor(flipbook: Flipbook) {
		this.flipbook = flipbook;
		this.createElements();
		this.attachEventListeners();
	}

	private createElements() {
		// Main Widget container
		this.containerEl = document.createElement("div");
		this.containerEl.id = "chapters-widget";
		this.containerEl.className = "chapters-widget";
		this.containerEl.setAttribute("aria-label", "Navegación de Capítulos");

		// Mobile floating toggle button
		this.toggleBtn = document.createElement("button");
		this.toggleBtn.id = "chapters-toggle-btn";
		this.toggleBtn.className = "chapters-toggle-btn";
		this.toggleBtn.setAttribute("aria-label", "Abrir índice de capítulos");
		this.toggleBtn.innerHTML = `
			<span class="toggle-icon">📜</span>
			<span class="toggle-text">Capítulos</span>
		`;

		// Nav plaque
		this.navEl = document.createElement("nav");
		this.navEl.id = "chapters-nav";
		this.navEl.className = "chapters-nav";

		// Corner decorations for antique book plaque
		const cornerTL = document.createElement("div");
		cornerTL.className = "chapters-corner top-left";
		const cornerTR = document.createElement("div");
		cornerTR.className = "chapters-corner top-right";
		const cornerBL = document.createElement("div");
		cornerBL.className = "chapters-corner bottom-left";
		const cornerBR = document.createElement("div");
		cornerBR.className = "chapters-corner bottom-right";

		// Header
		const header = document.createElement("div");
		header.className = "chapters-header";
		header.innerHTML = `
			<div class="header-banner">
				<span class="fleuron">❧</span>
				<span class="header-title">ÍNDICE</span>
				<span class="fleuron">❧</span>
			</div>
			<div class="header-subtitle">CAPÍTULOS</div>
		`;

		// Divider
		const divider1 = document.createElement("div");
		divider1.className = "chapters-divider";

		// List of chapters
		const list = document.createElement("div");
		list.className = "chapters-list";

		CHAPTERS.forEach(ch => {
			const btn = document.createElement("button");
			btn.type = "button";
			btn.className = "chapter-btn";
			btn.dataset.chapterId = String(ch.id);
			btn.dataset.page = String(ch.page);
			btn.innerHTML = `
				<div class="chapter-seal">${ch.roman}</div>
				<div class="chapter-text-group">
					<span class="chapter-number">Capítulo ${ch.roman}</span>
					<span class="chapter-name">${ch.title}</span>
				</div>
				<div class="chapter-active-indicator"></div>
			`;
			btn.addEventListener("click", () => {
				this.onChapterClick(ch.page);
			});
			this.chapterButtons.set(ch.id, btn);
			list.appendChild(btn);
		});

		// Divider 2
		const divider2 = document.createElement("div");
		divider2.className = "chapters-divider";

		// Footer with Portada / Inicio option
		const footer = document.createElement("div");
		footer.className = "chapters-footer";
		const coverBtn = document.createElement("button");
		coverBtn.type = "button";
		coverBtn.className = "chapter-cover-btn";
		coverBtn.title = "Volver a la portada";
		coverBtn.innerHTML = `
			<span class="cover-seal">✦</span>
			<span class="cover-text">Portada Inicial</span>
		`;
		coverBtn.addEventListener("click", () => {
			this.onChapterClick(0);
		});
		footer.appendChild(coverBtn);

		// Assemble
		this.navEl.appendChild(cornerTL);
		this.navEl.appendChild(cornerTR);
		this.navEl.appendChild(cornerBL);
		this.navEl.appendChild(cornerBR);
		this.navEl.appendChild(header);
		this.navEl.appendChild(divider1);
		this.navEl.appendChild(list);
		this.navEl.appendChild(divider2);
		this.navEl.appendChild(footer);

		this.containerEl.appendChild(this.toggleBtn);
		this.containerEl.appendChild(this.navEl);

		// Prevent double-clicks inside the chapters widget from triggering fullscreen toggle
		this.containerEl.addEventListener("dblclick", e => {
			e.stopPropagation();
		});

		const mountTarget =
			this.flipbook.getContainerEl() ||
			document.getElementById("flipbook-container") ||
			document.body;
		mountTarget.appendChild(this.containerEl);
	}

	private showNav() {
		if (this.containerEl.classList.contains("visible")) return;
		this.containerEl.classList.add("visible");
		this.updateActiveChapter(this.flipbook.getProgress());
	}

	private attachEventListeners() {
		// Listen for intro completion to show the navigation widget
		this.flipbook.onIntroCompleted(() => {
			this.showNav();
		});

		// Listen for progress changes to update the active chapter and show nav
		this.flipbook.onProgressChange(progress => {
			if (progress >= 0.45) {
				this.showNav();
			}
			this.updateActiveChapter(progress);
		});

		// Mobile toggle button
		this.toggleBtn.addEventListener("click", () => {
			this.isMobileOpen = !this.isMobileOpen;
			this.containerEl.classList.toggle("mobile-open", this.isMobileOpen);
		});

		// Close mobile menu if clicked outside
		document.addEventListener("click", e => {
			if (
				this.isMobileOpen &&
				!this.containerEl.contains(e.target as Node)
			) {
				this.isMobileOpen = false;
				this.containerEl.classList.remove("mobile-open");
			}
		});
	}

	private onChapterClick(page: number) {
		// On mobile, close drawer on selection
		if (this.isMobileOpen) {
			this.isMobileOpen = false;
			this.containerEl.classList.remove("mobile-open");
		}
		this.flipbook.goToPage(page);
	}

	private updateActiveChapter(progress: number) {
		let currentId: number | null = null;
		for (const ch of CHAPTERS) {
			if (progress >= ch.minProgress && progress < ch.maxProgress) {
				currentId = ch.id;
				break;
			}
		}

		if (currentId === this.activeChapterId) return;
		this.activeChapterId = currentId;

		this.chapterButtons.forEach((btn, id) => {
			if (id === currentId) {
				btn.classList.add("active");
			} else {
				btn.classList.remove("active");
			}
		});
	}
}

export default function initChaptersNav(flipbook: Flipbook): ChaptersNav {
	return new ChaptersNav(flipbook);
}
