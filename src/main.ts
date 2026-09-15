import Flipbook from "./flipbook";
import initChaptersNav, { ChaptersNav } from "./chapters-nav";
import { Language } from "./i18n";
import { MobileView } from "./mobile-view";

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
			link: "https://github.com/TEstebanGQ/dotnet-hexagonal-enterprise-security-api",
			top: 235.0 / pageHeight,
			left: 114.5 / pageWidth,
			width: 175.0 / pageWidth,
			height: 30.0 / pageHeight,
			title: isEn ? "GitHub - Enterprise Security API" : "GitHub - Enterprise Security API (.NET 9)",
		},
		{
			faceIndex: 29,
			link: "/Tomas_Esteban_Gonzalez_Quintero_CV.pdf",
			top: 235.0 / pageHeight,
			left: 310.0 / pageWidth,
			width: 195.0 / pageWidth,
			height: 30.0 / pageHeight,
			title: isEn ? "Download Resume (PDF)" : "Descargar Hoja de Vida (PDF)",
		},
		{
			faceIndex: 30,
			link: "https://github.com/TEstebanGQ/Campus-Hub-zero",
			top: 235.0 / pageHeight,
			left: 114.5 / pageWidth,
			width: 215.0 / pageWidth,
			height: 30.0 / pageHeight,
			title: isEn ? "GitHub - Campuslands Access Hub" : "GitHub - Campuslands Access Hub (Producción)",
		},
		{
			faceIndex: 30,
			link: "/Tomas_Esteban_Gonzalez_Quintero_CV.pdf",
			top: 235.0 / pageHeight,
			left: 350.0 / pageWidth,
			width: 195.0 / pageWidth,
			height: 30.0 / pageHeight,
			title: isEn ? "Download Resume (PDF)" : "Descargar Hoja de Vida (PDF)",
		},
		{
			faceIndex: 30,
			link: isEn
				? "https://wa.me/573167755887?text=Hello%20Tom%C3%A1s,%20I'm%20contacting%20you%20from%20your%20portfolio%20website"
				: "https://wa.me/573167755887?text=Hola%20Tom%C3%A1s,%20te%20contacto%20desde%20tu%20portafolio%20web",
			top: 980.0 / pageHeight,
			left: 120.0 / pageWidth,
			width: 190.0 / pageWidth,
			height: 25.0 / pageHeight,
			title: "WhatsApp: +57 316 775 5887",
		},
		{
			faceIndex: 30,
			link: "https://www.linkedin.com/in/tomas-esteban-gonzalez-quintero/",
			top: 980.0 / pageHeight,
			left: 325.0 / pageWidth,
			width: 90.0 / pageWidth,
			height: 25.0 / pageHeight,
			title: "LinkedIn - Tomás Esteban",
		},
		{
			faceIndex: 30,
			link: "mailto:tomasestebangonzalezquintero@gmail.com",
			top: 980.0 / pageHeight,
			left: 430.0 / pageWidth,
			width: 200.0 / pageWidth,
			height: 25.0 / pageHeight,
			title: "Email: tomasestebangonzalezquintero@gmail.com",
		},
		{
			faceIndex: 30,
			link: "/Tomas_Esteban_Gonzalez_Quintero_CV.pdf",
			top: 1005.0 / pageHeight,
			left: 80.0 / pageWidth,
			width: 604.0 / pageWidth,
			height: 35.0 / pageHeight,
			title: isEn ? "Download Official Resume (PDF)" : "Descargar Hoja de Vida Oficial (PDF)",
		},
		{
			faceIndex: 31,
			link: "https://github.com/TEstebanGQ",
			top: 1540 / 2200,
			left: 472 / 1544,
			width: 600 / 1544,
			height: 48 / 2200,
			title: "GitHub - TEstebanGQ",
		},
		{
			faceIndex: 31,
			link: "https://www.linkedin.com/in/tomas-esteban-gonzalez-quintero/",
			top: 1595 / 2200,
			left: 432 / 1544,
			width: 680 / 1544,
			height: 48 / 2200,
			title: "LinkedIn - Tomás Esteban",
		},
		{
			faceIndex: 31,
			link: isEn
				? "https://wa.me/573167755887?text=Hello%20Tom%C3%A1s,%20I'm%20contacting%20you%20from%20your%20portfolio%20website"
				: "https://wa.me/573167755887?text=Hola%20Tom%C3%A1s,%20te%20contacto%20desde%20tu%20portafolio%20web",
			top: 1650 / 2200,
			left: 482 / 1544,
			width: 580 / 1544,
			height: 48 / 2200,
			title: isEn ? "WhatsApp Contact" : "Contacto WhatsApp",
		},
		{
			faceIndex: 31,
			link: "/Tomas_Esteban_Gonzalez_Quintero_CV.pdf",
			top: 1730 / 2200,
			left: 390 / 1544,
			width: 764 / 1544,
			height: 105 / 2200,
			title: isEn ? "Download Official Resume (PDF)" : "Descargar Hoja de Vida Oficial (PDF)",
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
		_url(`${dir}cover-front.webp`),
		_url(`${dir}welcome.webp`),
		_url(`${dir}about.webp`),
		_url(`${dir}who-am-i.webp`),
		_url(`${dir}my-story.webp`),
		_url(`${dir}skills.webp`),
		_url(`${dir}interests.webp`),
		_url(`${dir}blank.webp`),
		_url(`${dir}journey.webp`),
		_url(`${dir}map-1.webp`),
		_url(`${dir}map-2.webp`),
		_url(`${dir}blank.webp`),
		_url(`${dir}career.webp`),
		_url(`${dir}thor-systems.webp`),
		_url(`${dir}thor-systems-2.webp`),
		_url(`${dir}freelance.webp`),
		_url(`${dir}freelance-2.webp`),
		_url(`${dir}blank.webp`),
		_url(`${dir}projects.webp`),
		_url(`${dir}qyou.webp`),
		_url(`${dir}qyou-2.webp`),
		_url(`${dir}iq-tester.webp`),
		_url(`${dir}betting-tarot.webp`),
		_url(`${dir}autoposter.webp`),
		_url(`${dir}autoposter-2.webp`),
		_url(`${dir}export-robot.webp`),
		_url(`${dir}six-dot-bot.webp`),
		_url(`${dir}autoreply.webp`),
		_url(`${dir}time-recorder.webp`),
		_url(`${dir}fifteen-js.webp`),
		_url(`${dir}the-book.webp`),
		_url(`${dir}cover-back.webp`),
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

	const urlParams = new URLSearchParams(window.location.search);
	const paramLang = urlParams.get("lang") as Language | null;
	let initialLang: Language = "es";
	if (paramLang === "en" || paramLang === "es") {
		initialLang = paramLang;
		localStorage.setItem("portfolio_lang", paramLang);
	} else {
		initialLang = ((localStorage.getItem("portfolio_lang") as Language) || "es") === "en" ? "en" : "es";
	}

	window.flipbook = new Flipbook({
		containerEl,
		textureUrls: {
			pages: getPageTextureUrls(initialLang, _url),
			spineInner: _url("/img/pages/spine.webp"),
			spineOuter: _url("/img/pages/spine.webp"),
			coverEdgeTB: _url("/img/pages/cover-edge-tb.webp"),
			coverEdgeLR: _url("/img/pages/cover-edge-lr.webp"),
			spineEdgeTB: _url("/img/pages/spine-edge-tb.webp"),
			spineEdgeLR: _url("/img/pages/cover-edge-tb.webp"),
			desk: _url("/img/desk.webp"),
			blank: _url(initialLang === "en" ? "/img/pages-en/blank.webp" : "/img/pages/blank.webp"),
		},
		pageEdgeColor: 0xb1a283,
		pageWidth,
		pageHeight,
		coverThickness: 5,
		pageRootThickness: 5,
		pageThickness: 1.5,
		coverMarginX: 12,
		coverMarginY: 10,
		pageActiveAreas: getActiveAreas(initialLang, pageWidth, pageHeight),
	});

	const isMobileDevice = (): boolean => {
		const ua = navigator.userAgent || "";
		const isMobileUA = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(ua);
		const hasTouch = (navigator.maxTouchPoints && navigator.maxTouchPoints > 0) || ("ontouchstart" in window);
		const isSmallScreen = window.innerWidth <= 820;
		return isSmallScreen || (isMobileUA && window.innerWidth <= 1024) || (hasTouch && isSmallScreen);
	};

	let nav: ChaptersNav | null = null;
	let userToggled3D = false;
	const shouldStartMobile = isMobileDevice();

	const onSwitchTo3D = () => {
		userToggled3D = true;
		sessionStorage.setItem("portfolio_view_mode", "3d");
		mobileView.hide();
		if (window.flipbook.getIntroPhase() !== "COMPLETED") {
			window.flipbook.finishIntroImmediately();
		} else {
			window.flipbook.restoreCamera(0);
		}
	};

	const onSwitchToMobile = () => {
		userToggled3D = false;
		sessionStorage.setItem("portfolio_view_mode", "mobile");
		mobileView.show();
	};

	const onLanguageChanged = (newLang: Language) => {
		initialLang = newLang;
		localStorage.setItem("portfolio_lang", newLang);
		const url = new URL(window.location.href);
		url.searchParams.set("lang", newLang);
		window.history.replaceState({}, "", url.toString());

		mobileView.setLanguage(newLang);
		window.flipbook.setActiveAreas(getActiveAreas(newLang, pageWidth, pageHeight));
		window.flipbook.updatePageTextures(getPageTextureUrls(newLang, _url));
		if (nav) {
			nav.applyLanguage(newLang);
		}
	};

	const mobileView = new MobileView(
		initialLang,
		onSwitchTo3D,
		onSwitchToMobile,
		onLanguageChanged,
	);

	if (shouldStartMobile) {
		mobileView.show();
	}

	window.flipbook.onIntroCompleted(() => {
		setTimeout(() => {
			nav = initChaptersNav(window.flipbook);
			nav.onLanguageChange(newLang => {
				onLanguageChanged(newLang);
			});
		}, 100);
	});

	window.addEventListener("resize", () => {
		const isNowMobile = isMobileDevice();
		if (isNowMobile && !mobileView.getIsVisible() && !userToggled3D) {
			mobileView.show();
		} else if (!isNowMobile && mobileView.getIsVisible() && !sessionStorage.getItem("portfolio_view_mode")) {
			onSwitchTo3D();
		}
		mobileView.updateSwitchBtnVisibility();
	});
}

function start() {
	// Yield to the browser so the logo, overlay, and initial frame are painted first
	requestAnimationFrame(() => {
		setTimeout(init, 0);
	});
}

if (document.readyState === "loading") {
	document.addEventListener("DOMContentLoaded", start);
} else {
	start();
}
