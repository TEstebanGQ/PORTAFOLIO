import "./style.css";
import Flipbook from "./flipbook";
import initChaptersNav from "./chapters-nav";
import { Language } from "./i18n";

declare global {
	interface Window {
		flipbook: Flipbook;
	}
}

function getActiveAreas(lang: Language, pageWidth: number, pageHeight: number) {
	const isEn = lang === "en";
	return [
		{
			faceIndex: 3,
			link: "https://github.com/TEstebanGQ",
			top: 211 / pageHeight,
			left: 68 / pageWidth,
			width: 100 / pageWidth,
			height: 100 / pageHeight,
			title: "GitHub",
		},
		{
			faceIndex: 3,
			// simple spam crawler protection
			link: () =>
				atob(
					"t92YuwWah12ZA9mclRnbpVXc6VGbhpnbvdmbhJWZ0NXZzFWbvRnOvRHbpFWb"
						.split("")
						.reverse()
						.join(""),
				),
			top: 420 / pageHeight,
			left: 68 / pageWidth,
			width: 100 / pageWidth,
			height: 100 / pageHeight,
			title: "E-Mail",
		},
		{
			faceIndex: 3,
			link: isEn
				? "https://wa.me/573167755887?text=Hello%20Tom%C3%A1s,%20I'm%20contacting%20you%20from%20your%20portfolio%20website"
				: "https://wa.me/573167755887?text=Hola%20Tom%C3%A1s,%20te%20contacto%20desde%20tu%20portafolio%20web",
			top: 211 / pageHeight,
			left: 591 / pageWidth,
			width: 100 / pageWidth,
			height: 100 / pageHeight,
			title: "WhatsApp",
		},
		{
			faceIndex: 3,
			link: "https://www.linkedin.com/in/tomas-esteban-gonzalez-quintero/",
			top: 420 / pageHeight,
			left: 591 / pageWidth,
			width: 100 / pageWidth,
			height: 100 / pageHeight,
			title: "LinkedIn",
		},
		{
			faceIndex: 13,
			link: "https://campuslands.com/",
			top: 152 / pageHeight,
			left: 50 / pageWidth,
			width: 180 / pageWidth,
			height: 50 / pageHeight,
			title: "Campuslands",
		},
		{
			faceIndex: 16,
			link: isEn
				? "https://wa.me/573167755887?text=Hello%20Tom%C3%A1s,%20I'm%20contacting%20you%20from%20your%20portfolio"
				: "https://wa.me/573167755887?text=Hola%20Tom%C3%A1s,%20te%20contacto%20desde%20tu%20portafolio",
			top: 152 / pageHeight,
			left: 50 / pageWidth,
			width: 260 / pageWidth,
			height: 50 / pageHeight,
			title: isEn ? "WhatsApp Contact" : "Contacto WhatsApp",
		},
		{
			faceIndex: 18,
			link: "https://github.com/TEstebanGQ",
			top: 820 / pageHeight,
			left: 365 / pageWidth,
			width: 115 / pageWidth,
			height: 50 / pageHeight,
		},
		{
			faceIndex: 19,
			link: "https://github.com/TEstebanGQ/campuslands-inteligente",
			top: 232.5 / pageHeight,
			left: 115.0 / pageWidth,
			width: 110.0 / pageWidth,
			height: 28.0 / pageHeight,
			title: isEn ? "GitHub - Campuslands Intelligent" : "GitHub - Campuslands Inteligente",
		},
		{
			faceIndex: 21,
			link: "https://github.com/TEstebanGQ/logitrack-wms-springboot",
			top: 245.0 / pageHeight,
			left: 115.0 / pageWidth,
			width: 110.0 / pageWidth,
			height: 28.0 / pageHeight,
			title: "GitHub - LogiTrack WMS",
		},
		{
			faceIndex: 21,
			link: "https://logitrack.34.70.8.165.sslip.io",
			top: 245.0 / pageHeight,
			left: 250.0 / pageWidth,
			width: 185.0 / pageWidth,
			height: 28.0 / pageHeight,
			title: isEn ? "Live Demo - LogiTrack WMS" : "Demo en vivo - LogiTrack WMS",
		},
		{
			faceIndex: 22,
			link: "https://github.com/TEstebanGQ/n8n-attendance-ai-workflow",
			top: 240.0 / pageHeight,
			left: 115.0 / pageWidth,
			width: 110.0 / pageWidth,
			height: 28.0 / pageHeight,
			title: "GitHub - n8n Attendance AI",
		},
		{
			faceIndex: 23,
			link: "https://github.com/TEstebanGQ/github-mcp-server",
			top: 232.5 / pageHeight,
			left: 115.0 / pageWidth,
			width: 110.0 / pageWidth,
			height: 28.0 / pageHeight,
			title: "GitHub - GitHub MCP Server",
		},
		{
			faceIndex: 25,
			link: "https://github.com/TEstebanGQ/HelpDeskAI",
			top: 240.0 / pageHeight,
			left: 115.0 / pageWidth,
			width: 110.0 / pageWidth,
			height: 28.0 / pageHeight,
			title: "GitHub - HelpDesk AI",
		},
		{
			faceIndex: 26,
			link: "https://github.com/TEstebanGQ/ecommerce-database-4nf",
			top: 237.5 / pageHeight,
			left: 115.0 / pageWidth,
			width: 110.0 / pageWidth,
			height: 28.0 / pageHeight,
			title: "GitHub - Ecommerce Database 4NF",
		},
		{
			faceIndex: 27,
			link: "https://github.com/TEstebanGQ/softskills-quest",
			top: 240.0 / pageHeight,
			left: 115.0 / pageWidth,
			width: 110.0 / pageWidth,
			height: 28.0 / pageHeight,
			title: "GitHub - SoftSkills Quest",
		},
		{
			faceIndex: 28,
			link: "https://github.com/TEstebanGQ/lms-learning-platform",
			top: 240.0 / pageHeight,
			left: 115.0 / pageWidth,
			width: 110.0 / pageWidth,
			height: 28.0 / pageHeight,
			title: "GitHub - LMS ABC Platform",
		},
		{
			faceIndex: 28,
			link: "https://proyecto-d1-js.netlify.app/",
			top: 240.0 / pageHeight,
			left: 250.0 / pageWidth,
			width: 185.0 / pageWidth,
			height: 28.0 / pageHeight,
			title: isEn ? "Live Demo - LMS ABC" : "Demo en vivo - LMS ABC",
		},
		{
			faceIndex: 29,
			link: "https://github.com/TEstebanGQ/PORTAFOLIO",
			top: 240.0 / pageHeight,
			left: 115.0 / pageWidth,
			width: 110.0 / pageWidth,
			height: 28.0 / pageHeight,
			title: isEn ? "GitHub - 3D Portfolio" : "GitHub - Portafolio 3D",
		},
		{
			faceIndex: 30,
			link: "https://github.com/TEstebanGQ/PORTAFOLIO",
			top: 232.5 / pageHeight,
			left: 115.0 / pageWidth,
			width: 110.0 / pageWidth,
			height: 28.0 / pageHeight,
			title: isEn ? "GitHub - Official Repository" : "GitHub - Repositorio Oficial",
		},
		{
			faceIndex: 30,
			link: "https://github.com/TEstebanGQ/PORTAFOLIO",
			top: 232.5 / pageHeight,
			left: 250.0 / pageWidth,
			width: 185.0 / pageWidth,
			height: 28.0 / pageHeight,
			title: isEn ? "Official Repository" : "Repositorio Oficial",
		},
		{
			faceIndex: 5,
			zoom: {
				top: 187 / pageHeight,
				left: 47 / pageWidth,
				width: 668 / pageWidth,
				height: 668 / pageHeight,
			},
			top: 0,
			left: 0,
			width: 1,
			height: 1,
			preserveDefaultCursor: true,
		},
	];
}

function getPageTextureUrls(lang: Language, _url: (path: string) => string): string[] {
	const dir = lang === "en" ? "/img/pages-en/" : "/img/pages/";
	return [
		_url(`${dir}cover-front.jpg`),
		_url(`${dir}welcome.jpg`),
		_url(`${dir}about.jpg`),
		_url(`${dir}who-am-i.jpg`),
		_url(`${dir}my-story.jpg`),
		_url(`${dir}skills.jpg`),
		_url(`${dir}interests.jpg`),
		_url(`${dir}blank.jpg`),
		_url(`${dir}journey.jpg`),
		_url(`${dir}map-1.jpg`),
		_url(`${dir}map-2.jpg`),
		_url(`${dir}blank.jpg`),
		_url(`${dir}career.jpg`),
		_url(`${dir}thor-systems.jpg`),
		_url(`${dir}thor-systems-2.jpg`),
		_url(`${dir}freelance.jpg`),
		_url(`${dir}freelance-2.jpg`),
		_url(`${dir}blank.jpg`),
		_url(`${dir}projects.jpg`),
		_url(`${dir}qyou.jpg`),
		_url(`${dir}qyou-2.jpg`),
		_url(`${dir}iq-tester.jpg`),
		_url(`${dir}betting-tarot.jpg`),
		_url(`${dir}autoposter.jpg`),
		_url(`${dir}autoposter-2.jpg`),
		_url(`${dir}export-robot.jpg`),
		_url(`${dir}six-dot-bot.jpg`),
		_url(`${dir}autoreply.jpg`),
		_url(`${dir}time-recorder.jpg`),
		_url(`${dir}fifteen-js.jpg`),
		_url(`${dir}the-book.jpg`),
		_url(`${dir}cover-back.jpg`),
	];
}

function init() {
	const containerEl = document.getElementById("flipbook-container");

	const pageWidth = 764;
	const pageHeight = 1080;
	if (!containerEl) {
		console.error("No container element found");
		return;
	}

	const baseUrl = import.meta.env.BASE_URL || "";
	const _url = (path: string) => {
		if (baseUrl.endsWith("/") && path.startsWith("/")) {
			return baseUrl + path.slice(1);
		}
		return baseUrl + path;
	};

	const initialLang = ((localStorage.getItem("portfolio_lang") as Language) || "es") === "en" ? "en" : "es";

	window.flipbook = new Flipbook({
		containerEl,
		textureUrls: {
			pages: getPageTextureUrls(initialLang, _url),
			spineInner: _url("/img/pages/spine.jpg"),
			spineOuter: _url("/img/pages/spine.jpg"),
			coverEdgeTB: _url("/img/pages/cover-edge-tb.jpg"),
			coverEdgeLR: _url("/img/pages/cover-edge-lr.jpg"),
			spineEdgeTB: _url("/img/pages/spine-edge-tb.jpg"),
			spineEdgeLR: _url("/img/pages/cover-edge-tb.jpg"),
			desk: _url("/img/desk.jpg"),
		},
		pageEdgeColor: 0xb1a283,
		pageWidth,
		pageHeight,
		coverThickness: 5,
		pageRootThickness: 5,
		pageThickness: 1,
		coverMarginX: 8,
		coverMarginY: 10,
		pageActiveAreas: getActiveAreas(initialLang, pageWidth, pageHeight),
	});

	const nav = initChaptersNav(window.flipbook);
	nav.onLanguageChange(newLang => {
		window.flipbook.setActiveAreas(getActiveAreas(newLang, pageWidth, pageHeight));
		window.flipbook.updatePageTextures(getPageTextureUrls(newLang, _url));
	});
}

if (document.readyState === "loading") {
	document.addEventListener("DOMContentLoaded", init);
} else {
	init();
}
