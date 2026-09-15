import * as THREE from "three";
import { gsap } from "gsap";
import {
	lerpRectangles,
	rotateY,
	scaleRectangle,
	sleep,
	toggleVisibility,
} from "./util";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import Page from "./page";
import SlidingNumber, { ValueChangeEvent } from "./sliding-number";
import SwipeHandler from "./swipe-handler";
import IntroOverlay from "./intro-overlay";
import PageCurveHelper from "./page-curve-helper";

export default class Flipbook {
	private containerEl: HTMLElement;
	private wrapperLinkEl: HTMLElement;
	private pageWidth: number;
	private pageHeight: number;
	private pageThickness: number;
	private pageRootThickness: number;
	private coverThickness: number;
	private coverMarginX: number;
	private coverMarginY: number;
	private textureUrls;
	private pageActiveAreas: PageActiveArea[] = [];
	private pageEdgeColor: number;
	public readonly settings: FlipbookSettings = {
		cameraAngle: (Math.PI / 2) * 0.28,
		cameraDistance: 1.02,
		cameraFov: 14,

		spotLightX: 0,
		spotLightY: 550,
		spotLightZ: 1500,
		spotLightColor: 0xffffff,
		spotLightIntensity: 65,
		spotLightAngle: 0.75,
		spotLightPenumbra: 0.6,
		spotLightDecay: 0.4,
		spotLightNearClip: 500,
		spotLightFarClip: 3500,
		spotLightMapSize: 2048,

		ambientLightColor: 0xffffff,
		ambientLightIntensity: 0.42,

		showSpotLightHelper: false,
		showSpotShadowHelper: false,
		showPageCurveHelpers: false,
	};

	private pages: Page[] = [];
	private pageHelpers: PageCurveHelper[] = [];
	private group: THREE.Group;
	private scene: THREE.Scene;
	private camera: THREE.PerspectiveCamera;
	private renderer: THREE.WebGLRenderer;
	private spineMesh: THREE.Mesh;
	private spotLight: THREE.SpotLight;
	private ambientLight: THREE.AmbientLight;
	private raycaster: THREE.Raycaster;
	private sceneMousePos: THREE.Vector2;

	private progress = new SlidingNumber(0, 0.1, 4);
	private spineWidth: number;
	private spineZ: number;

	private controls: OrbitControls;
	private stats: any;
	private datGui: any;

	private spotLightHelper: THREE.SpotLightHelper | null = null;
	private spotShadowHelper: THREE.CameraHelper | null = null;
	private textureLoader: THREE.TextureLoader;
	private textureCache: Map<string, THREE.Texture> = new Map();
	private initCompleted: boolean = false;
	private introOverlay: IntroOverlay;

	private focusedActiveArea: PageActiveArea | null = null;
	private isChangingFocus = false;
	// @remark, css values should be changed individually
	private CAMERA_SIDE_GRAVITY = 4;
	private cameraSideShift = new SlidingNumber(1, 0.2);
	private isVerticalMode = false;
	private isMobile = false;
	private swipeHandler: SwipeHandler;

	// if this code is running, means the scripts are already loaded
	private scriptProgressWeight = 0.4;

	private introPhase: "LOADING" | "ANIMATING" | "COMPLETED" = "LOADING";
	private pageTurnTween: gsap.core.Tween | null = null;
	private onIntroCompleteCallbacks: (() => void)[] = [];
	private onProgressChangeCallbacks: ((progress: number) => void)[] = [];

	private loadedPageIndices: Set<number> = new Set();
	private loadingPageIndices: Set<number> = new Set();
	private preloadNextPageTimeout: number | null = null;
	private bgTextureLoader: THREE.TextureLoader = new THREE.TextureLoader(
		new THREE.LoadingManager(),
	);

	constructor(params: FlipBookParams) {
		this.containerEl = params.containerEl;
		this.pageWidth = params.pageWidth;
		this.pageHeight = params.pageHeight;
		this.pageThickness = params.pageThickness || 2;
		this.pageRootThickness = params.pageRootThickness || 4;
		this.coverThickness = params.coverThickness || 5;
		this.coverMarginX = params.coverMarginX || 8;
		this.coverMarginY = params.coverMarginY || 8;
		this.textureUrls = params.textureUrls;
		this.pageEdgeColor = params.pageEdgeColor;
		this.pageActiveAreas = params.pageActiveAreas || [];


		this.isMobile =
			/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
				navigator.userAgent,
			) || window.innerWidth <= 768;

		this.introOverlay = new IntroOverlay(
			this.containerEl.querySelector(".intro-overlay")!,
		);
		this.introOverlay.onProgress(this.scriptProgressWeight);

		let introStarted = false;
		const startIntroOnce = () => {
			if (
				introStarted ||
				this.introPhase === "COMPLETED" ||
				this.introPhase === "ANIMATING"
			) {
				return;
			}
			introStarted = true;
			this.introOverlay.onProgress(1);
			this.playIntro();
			this.onIntroCompleted(() => {
				const current = Math.round(this.progress.getValue());
				this.schedulePredictivePreload(current);
			});
		};

		const skipIntro = () => {
			if (this.introPhase !== "COMPLETED") {
				this.finishIntroImmediately();
			}
		};
		this.containerEl.addEventListener("pointerdown", skipIntro, { once: true });

		THREE.DefaultLoadingManager.onProgress = (
			_,
			itemsLoaded,
			itemsTotal,
		) => {
			if (introStarted || this.introPhase === "COMPLETED") return;

			const assetsProgress = itemsTotal > 0 ? itemsLoaded / itemsTotal : 1;
			const overallProgress =
				this.scriptProgressWeight +
				assetsProgress * (1 - this.scriptProgressWeight);
			this.introOverlay.onProgress(overallProgress);
			if (assetsProgress >= 1 || itemsLoaded >= itemsTotal) {
				startIntroOnce();
			}
		};

		THREE.DefaultLoadingManager.onLoad = () => {
			startIntroOnce();
		};

		THREE.DefaultLoadingManager.onError = (url) => {
			console.warn("Could not load asset:", url);
			// Do not block intro progression if an individual asset fails
		};

		// Safety timeout: If loading takes longer than expected, launch intro anyway
		setTimeout(() => {
			if (!introStarted) {
				console.warn("Loading timeout reached; starting intro");
				startIntroOnce();
			}
		}, this.isMobile ? 1800 : 2500);

		const initialAspect = window.innerWidth / window.innerHeight;
		let initialFov = this.settings.cameraFov;
		if (initialAspect < 1.0) {
			const targetHFOVRads = THREE.MathUtils.degToRad(25);
			const tanHalfHFOV = Math.tan(targetHFOVRads / 2);
			const requiredFovY = 2 * Math.atan(tanHalfHFOV / initialAspect) * (180 / Math.PI);
			initialFov = Math.min(Math.max(requiredFovY, this.settings.cameraFov), 75);
		}

		this.scene = new THREE.Scene();
		this.camera = new THREE.PerspectiveCamera(
			initialFov,
			initialAspect,
			50,
			60000,
		);

		this.renderer = new THREE.WebGLRenderer({
			antialias: !this.isMobile,
			powerPreference: this.isMobile ? "default" : "high-performance",
		});
		this.renderer.outputColorSpace = THREE.SRGBColorSpace;
		// this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
		// this.renderer.toneMappingExposure = 1.2;
		this.renderer.setPixelRatio(
			Math.min(window.devicePixelRatio, this.isMobile ? 1 : 2),
		);
		this.renderer.setSize(window.innerWidth, window.innerHeight);
		this.renderer.shadowMap.enabled = !this.isMobile;
		if (!this.isMobile) {
			this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
		}

		this.renderer.domElement.addEventListener(
			"webglcontextlost",
			event => {
				event.preventDefault();
				console.warn("WebGL context lost. Suppressing crash.");
			},
			false,
		);
		this.renderer.domElement.addEventListener(
			"webglcontextrestored",
			() => {
				console.info("WebGL context restored. Re-rendering...");
				this.render();
			},
			false,
		);

		this.renderer.domElement.classList.add("flipbook-canvas");
		this.wrapperLinkEl = document.createElement("a");
		this.wrapperLinkEl.draggable = false;
		this.wrapperLinkEl.classList.add("wrapper-link");
		this.wrapperLinkEl.setAttribute("role", "region");
		this.wrapperLinkEl.setAttribute("aria-label", "Interactive 3D Book");
		this.containerEl.appendChild(this.wrapperLinkEl);
		this.wrapperLinkEl.appendChild(this.renderer.domElement);

		THREE.Cache.enabled = true;
		this.textureLoader = new THREE.TextureLoader();

		this.raycaster = new THREE.Raycaster();
		this.sceneMousePos = new THREE.Vector2();

		const maxAnisotropy = this.isMobile
			? 1
			: Math.min(this.renderer.capabilities.getMaxAnisotropy(), 16);

		// add pages
		const totalPages = Math.ceil(this.textureUrls.pages.length / 2);

		for (let i = 0; i < totalPages; i++) {
			const isCover = i === 0 || i === totalPages - 1;
			const width = isCover
				? this.pageWidth + this.coverMarginX + this.coverThickness
				: this.pageWidth;
			const height = isCover
				? this.pageHeight + this.coverMarginY * 2
				: this.pageHeight;

			const edgeTextures: Record<string, string> = {};
			if (isCover) {
				edgeTextures.edgeLR = this.textureUrls.coverEdgeLR;
				edgeTextures.edgeTB = this.textureUrls.coverEdgeTB;
			}

			// All pages receive their authentic textures directly
			const frontUrl = this.textureUrls.pages[i * 2];
			const backUrl = this.textureUrls.pages[i * 2 + 1];
			this.loadedPageIndices.add(i);

			const page = new Page({
				textureUrls: {
					front: frontUrl,
					back: backUrl,
					...edgeTextures,
				},
				width,
				height,
				thickness: isCover ? this.coverThickness : this.pageThickness,
				rootThickness: isCover
					? this.coverThickness
					: this.pageRootThickness,
				isCover,
				isFrontCover: i === 0,
				edgeColor: this.pageEdgeColor,
				textureLoader: this.textureLoader,
				maxAnisotropy,
				isMobile: this.isMobile,
				textureCache: this.textureCache,
				onTextureLoaded: () => this.requestRender(),
			});
			this.pages.push(page);
		}

		this.ambientLight = new THREE.AmbientLight();
		this.scene.add(this.ambientLight);

		this.spotLight = new THREE.SpotLight();
		this.spotLight.castShadow = !this.isMobile;
		this.spotLight.shadow.bias = -0.0001;
		this.scene.add(this.spotLight);

		// this.controls = new OrbitControls(
		// 	this.camera,
		// 	this.renderer.domElement,
		// );

		this.group = new THREE.Group();
		this.scene.add(this.group);

		// init spine
		this.spineWidth = (this.pages.length - 2) * this.pageRootThickness;
		this.spineZ = this.coverThickness / 2;

		// init spine mesh
		const _texture = (url: string) => {
			const texture = this.textureLoader.load(url);
			texture.colorSpace = THREE.SRGBColorSpace;
			if (this.isMobile) {
				texture.generateMipmaps = false;
				texture.minFilter = THREE.LinearFilter;
				texture.magFilter = THREE.LinearFilter;
				texture.anisotropy = 1;
			} else {
				texture.generateMipmaps = true;
				texture.minFilter = THREE.LinearMipmapLinearFilter;
				texture.magFilter = THREE.LinearFilter;
				texture.anisotropy = maxAnisotropy;
			}
			return { map: texture };
		};

		const textures = {
			spineInner: _texture(this.textureUrls.spineInner),
			spineOuter: _texture(this.textureUrls.spineOuter),
			spineEdgeLR: _texture(this.textureUrls.spineEdgeLR),
			spineEdgeTB: _texture(this.textureUrls.spineEdgeTB),
		};
		const SpineMaterialClass = this.isMobile
			? THREE.MeshLambertMaterial
			: THREE.MeshStandardMaterial;

		const spineMaterials = [
			new SpineMaterialClass(textures.spineEdgeLR), // right face
			new SpineMaterialClass(textures.spineEdgeLR), // left face
			new SpineMaterialClass(textures.spineEdgeTB), // top face
			new SpineMaterialClass(textures.spineEdgeTB), // bottom face
			new SpineMaterialClass(textures.spineInner), // front face
			new SpineMaterialClass(textures.spineOuter), // back face
		];
		const spineGeometry = new THREE.BoxGeometry(
			this.spineWidth,
			this.pageHeight + this.coverMarginY * 2,
			this.coverThickness,
		);
		this.spineMesh = new THREE.Mesh(spineGeometry, spineMaterials);
		this.spineMesh.receiveShadow = !this.isMobile;
		this.spineMesh.castShadow = !this.isMobile;
		this.spineMesh.position.z = this.spineZ;
		this.spineMesh.renderOrder = 99;
		this.group.add(this.spineMesh);

		// init pages
		let spinePlacementStart = -this.spineWidth / 2;
		let spinePlacementShift = 0;
		this.pages.forEach((page, index) => {
			this.group.add(page.pivot);

			if (page.isCover) {
				page.pivot.position.z = this.coverThickness;
				page.pivot.position.x =
					(this.spineWidth / 2) * (index ? 1 : -1);
			} else {
				const elevationLeft =
					spinePlacementShift + page.rootThickness / 2;
				const elevationRight = this.spineWidth - elevationLeft;
				const elevationMultiplier = 0.7;
				page.setElevation(
					elevationLeft * elevationMultiplier,
					elevationRight * elevationMultiplier,
				);

				page.pivot.position.z = this.spineZ + this.coverThickness / 2;
				page.pivot.position.x =
					spinePlacementStart +
					spinePlacementShift +
					page.rootThickness / 2;
				spinePlacementShift += page.rootThickness;
			}
		});

		// create desk
		const deskGeometry = new THREE.PlaneGeometry(8000, 8000, 1, 1);
		const deskTexture = this.textureLoader.load(this.textureUrls.desk);
		deskTexture.colorSpace = THREE.SRGBColorSpace;
		if (this.isMobile) {
			deskTexture.generateMipmaps = false;
			deskTexture.minFilter = THREE.LinearFilter;
			deskTexture.magFilter = THREE.LinearFilter;
			deskTexture.anisotropy = 1;
		} else {
			deskTexture.generateMipmaps = true;
			deskTexture.minFilter = THREE.LinearMipmapLinearFilter;
			deskTexture.magFilter = THREE.LinearFilter;
			deskTexture.anisotropy = maxAnisotropy;
		}
		const DeskMaterialClass = this.isMobile
			? THREE.MeshLambertMaterial
			: THREE.MeshStandardMaterial;

		const deskMaterial = new DeskMaterialClass({
			map: deskTexture,
		});
		const deskMesh = new THREE.Mesh(deskGeometry, deskMaterial);
		deskMesh.receiveShadow = !this.isMobile;
		deskMesh.castShadow = !this.isMobile;
		deskMesh.renderOrder = 100;
		this.scene.add(deskMesh);

		this.updateVerticalMode();
		this.applySettings(params.settings || {}, true);

		if (import.meta.env.DEV) {
			// Dynamic import: Stats + dat.GUI are never bundled in production
			(async () => {
				const [{ default: Stats }, dat] = await Promise.all([
					import("stats.js"),
					import("dat.gui"),
				]);

				this.stats = new Stats();
				this.stats.showPanel(0);
				this.stats.dom.style.display = "none";
				document.body.appendChild(this.stats.dom);

				this.datGui = new dat.GUI();
				this.datGui.domElement.style.display = "none";

				const cameraFolder = this.datGui.addFolder("Camera");
				cameraFolder.open();
				cameraFolder.add(
					this.settings,
					"cameraAngle",
					Math.PI / -2,
					Math.PI / 2,
				);
				cameraFolder.add(this.settings, "cameraDistance", 0, 2);
				cameraFolder.add(this.settings, "cameraFov", 1, 90);

				const spotLightFolder = this.datGui.addFolder("Spot Light");
				const spotLightPosFolder = spotLightFolder.addFolder("Position");
				spotLightPosFolder.add(this.settings, "spotLightX", -1000, 1000);
				spotLightPosFolder.add(this.settings, "spotLightY", -1000, 1000);
				spotLightPosFolder.add(this.settings, "spotLightZ", 0, 2000);
				spotLightFolder.addColor(this.settings, "spotLightColor");
				spotLightFolder.add(this.settings, "spotLightIntensity", 0, 10000000);
				spotLightFolder.add(this.settings, "spotLightAngle", 0, Math.PI);
				spotLightFolder.add(this.settings, "spotLightPenumbra", 0, 1);
				spotLightFolder.add(this.settings, "spotLightDecay", 0, 10);
				spotLightFolder.add(this.settings, "spotLightNearClip", 1, 4000);
				spotLightFolder.add(this.settings, "spotLightFarClip", 1, 4000);
				spotLightFolder.add(this.settings, "spotLightMapSize", 0, 4096);

				const ambientLightFolder = this.datGui.addFolder("Ambient Light");
				ambientLightFolder.addColor(this.settings, "ambientLightColor");
				ambientLightFolder.add(this.settings, "ambientLightIntensity", 0, 1);

				const helpersFolder = this.datGui.addFolder("Helpers");
				helpersFolder.add(this.settings, "showSpotLightHelper");
				helpersFolder.add(this.settings, "showSpotShadowHelper");
				helpersFolder.add(this.settings, "showPageCurveHelpers");

				const addChangeListeners = (gui: any): void => {
					gui.__controllers.forEach((controller: any) => {
						controller.onChange((value: any) => {
							this.applySettings({ [controller.property]: value });
						});
					});
					for (const folderName in gui.__folders) {
						if (gui.__folders.hasOwnProperty(folderName)) {
							addChangeListeners(gui.__folders[folderName]);
						}
					}
				};
				addChangeListeners(this.datGui);
			})();
		}

		// event listeners
		window.addEventListener(
			"resize",
			this.onWindowResize.bind(this),
			false,
		);

		// process interactive areas
		this.renderer.domElement.addEventListener("mousemove", event => {
			this.sceneMousePos.x = (event.clientX / window.innerWidth) * 2 - 1;
			this.sceneMousePos.y =
				-(event.clientY / window.innerHeight) * 2 + 1;

			this.updateCursor();
		});

		this.swipeHandler = new SwipeHandler(this.renderer.domElement);
		this.swipeHandler.addCallback("swipeStart", () => {
			if (this.focusedActiveArea || this.isChangingFocus) return;
			if (this.pageTurnTween) {
				this.pageTurnTween.kill();
				this.pageTurnTween = null;
			}
			// continuing dropped turn or shift
			// TODO: refactor; make it more comprehendable
			this.isTurning() && this.progress.lock();
			!this.cameraSideShift.isSettled() && this.cameraSideShift.lock();
		});
		this.swipeHandler.addCallback("swipeEnd", () => {
			this.progress.release();
			this.cameraSideShift.release();
		});
		this.swipeHandler.addCallback("swipeMove", (swipe: Swipe) => {
			if (this.focusedActiveArea || this.isChangingFocus) return;
			this.onSwipeMove(swipe);
		});

		document.addEventListener("keydown", (event: KeyboardEvent) => {
			if (event.key === "Escape" || event.code === "Escape") {
				if (this.introPhase === "COMPLETED") {
					this.unfocusActiveArea();
				}
			} else if (
				event.key === "ArrowRight" ||
				event.key === "ArrowDown" ||
				event.code === "ArrowRight" ||
				event.code === "ArrowDown"
			) {
				event.preventDefault();
				this.nextPage();
			} else if (
				event.key === "ArrowLeft" ||
				event.key === "ArrowUp" ||
				event.code === "ArrowLeft" ||
				event.code === "ArrowUp"
			) {
				event.preventDefault();
				this.prevPage();
			} else if (event.key === "d" || event.code === "KeyD") {
				toggleVisibility(this.datGui.domElement);
			} else if (event.key === "f" || event.code === "KeyF") {
				toggleVisibility(this.stats.dom);
			}
		});

		this.renderer.domElement.addEventListener("click", event => {
			this.sceneMousePos.x = (event.clientX / window.innerWidth) * 2 - 1;
			this.sceneMousePos.y =
				-(event.clientY / window.innerHeight) * 2 + 1;
			this.onBookClick(this.sceneMousePos);
		});

		this.wrapperLinkEl.addEventListener("dblclick", () => {
			if (!document.fullscreenElement) {
				if (this.containerEl.requestFullscreen) {
					this.containerEl.requestFullscreen().catch(err => {
						console.error(
							"Failed to enter a full-screen mode",
							err,
						);
					});
				} else {
					console.error(
						"Fullscreen API is not supported in this browser.",
					);
				}
			} else {
				if (document.exitFullscreen) {
					document.exitFullscreen().catch(err => {
						console.error("Failed to exit a full-screen mode", err);
					});
				}
			}
		});

		this.cameraSideShift.setMin(-1); // look at the left page
		this.cameraSideShift.setMax(1); // look at the right page

		this.progress.setMin(-Infinity);
		this.progress.setMax(Infinity);

		this.progress.addCallback("settled", () => {
			this.progress.setMin(-Infinity);
			this.progress.setMax(Infinity);
		});

		// update cameraSideShift
		this.progress.addCallback(
			"valueChange",
			({ newValue: progress }: ValueChangeEvent) => {
				this.onProgressChangeCallbacks.forEach(cb => cb(progress));
				const current = Math.round(progress);
				this.schedulePredictivePreload(current);
				const bookOpenFactor = Math.min(
					progress,
					this.pages.length - progress,
					1,
				);

				this.cameraSideShift.setValue(1 - bookOpenFactor);
				if (progress + 1 > this.pages.length) {
					this.cameraSideShift.setValue(
						-this.cameraSideShift.getValue(),
					);
				}
				this.requestRender();
			},
		);

		this.cameraSideShift.addCallback("valueChange", () => {
			this.requestRender();
		});
	}

	private updateCursor() {
		let cursor = "grab";
		let href = "";
		let title = "";

		if (this.isChangingFocus) {
			cursor = "default";
		} else if (this.focusedActiveArea) {
			if (!this.focusedActiveArea.preserveDefaultCursor) {
				cursor = "pointer";
			}
		} else if (
			(this.isTurning() || this.isShifting()) &&
			this.swipeHandler.isPointerDown()
		) {
			cursor = "ew-resize";
		} else {
			const activeArea = this.getActiveAreaAt(this.sceneMousePos);

			if (activeArea) {
				if (!activeArea.preserveDefaultCursor) {
					cursor = "pointer";
				}
				title = activeArea.title || "";

				if (typeof activeArea.link === "function") {
					href = activeArea.link();
				} else {
					href = activeArea.link || "";
				}
			}
		}

		// applying cursor, href and title
		this.wrapperLinkEl.style.cursor = cursor;
		this.wrapperLinkEl.title = title;
		if (href) {
			this.wrapperLinkEl.setAttribute("href", href);
			this.wrapperLinkEl.setAttribute("target", "_blank");
			this.wrapperLinkEl.setAttribute("rel", "noopener noreferrer");
			this.wrapperLinkEl.removeAttribute("role");
			this.wrapperLinkEl.setAttribute("aria-label", title || "Interactive Link");
		} else {
			this.wrapperLinkEl.removeAttribute("href");
			this.wrapperLinkEl.removeAttribute("target");
			this.wrapperLinkEl.setAttribute("role", "region");
			this.wrapperLinkEl.setAttribute("aria-label", "Interactive 3D Book");
		}
	}

	private getTurningPage(): number | null {
		if (!this.isTurning()) return null;
		return this.progress.minValue;
	}

	private isTurning() {
		return !this.progress.isSettled();
	}

	private isShifting() {
		return !this.cameraSideShift.isSettled() && !this.isTurning();
	}

	private swipeDeltaToProgress(delta: number) {
		return delta / -500; // TODO:
	}

	private isDirty = true;
	private isLoopRunning = false;

	public requestRender(): void {
		this.isDirty = true;
		if (!this.isLoopRunning && this.introPhase !== "LOADING") {
			this.runAnimation();
		}
	}

	private shouldRender(): boolean {
		if (this.introPhase === "ANIMATING") return true;
		if (this.introPhase === "LOADING") return false;
		if (this.pageTurnTween !== null) return true;
		if (this.isTurning() || !this.progress.isSettled()) return true;
		if (this.isShifting() || !this.cameraSideShift.isSettled()) return true;
		if (this.isChangingFocus) return true;
		if (this.isDirty) return true;
		for (let i = 0; i < this.pages.length; i++) {
			if (this.pages[i].needsUpdate()) return true;
		}
		return false;
	}

	private runAnimation() {
		if (this.isLoopRunning) return;
		this.isLoopRunning = true;
		let previousTime = performance.now();

		const animate = ((currentTime: number) => {
			// Skip rendering when tab is hidden — saves GPU + main thread
			if (document.hidden) {
				previousTime = currentTime;
				requestAnimationFrame(animate);
				return;
			}
			let dt = (currentTime - previousTime) / 1000;
			previousTime = currentTime;

			if (this.shouldRender()) {
				this.stats?.begin?.();
				this.update(dt);
				this.stats?.end?.();
				this.controls?.update?.();

				if (
					this.introPhase === "COMPLETED" &&
					!this.pageTurnTween &&
					this.progress.isSettled() &&
					this.cameraSideShift.isSettled() &&
					!this.isChangingFocus
				) {
					let anyPageNeedsUpdate = false;
					for (let i = 0; i < this.pages.length; i++) {
						if (this.pages[i].needsUpdate()) {
							anyPageNeedsUpdate = true;
							break;
						}
					}
					if (!anyPageNeedsUpdate) {
						this.isDirty = false;
					}
				}
				requestAnimationFrame(animate);
			} else {
				this.isLoopRunning = false;
			}
		}).bind(this);

		requestAnimationFrame(animate);
	}

	private onSwipeMove(swipe: Swipe) {
		this.isDirty = true;
		const deltaX = swipe.x - swipe.prevX;
		if (!deltaX) return;
		const progressDelta = this.swipeDeltaToProgress(deltaX);

		if (!this.progress.locked) {
			// starting a turn directly
			this.progress.lock();

			if (progressDelta > 0) {
				this.progress.setMin(this.progress.getValue());
				this.progress.setMax(this.progress.getValue() + 1);
			} else {
				this.progress.setMin(this.progress.getValue() - 1);
				this.progress.setMax(this.progress.getValue());
			}

			// handling book beginning and ending
			if (this.progress.minValue < 0) {
				this.progress.setMin(0);
				this.progress.setMax(1);
			} else if (this.progress.maxValue > this.pages.length) {
				this.progress.setMin(this.pages.length - 1);
				this.progress.setMax(this.pages.length);
			}
		}

		if (this.isTurning()) {
			this.progress.nudge(progressDelta);
		}
	}

	private update(dt: number) {
		if (!dt) return;
		this.initCompleted = true;

		if (
			!this.isChangingFocus &&
			!this.focusedActiveArea &&
			this.introPhase === "COMPLETED"
		) {
			this.restoreCamera();
		}

		// TODO:
		// calculating visual turn progress to timely hide shadows
		// const topPage =
		// 	this.pages[Math.max(Math.ceil(this.progress.getValue()) - 1, 0)];
		// const visualProgress =
		// 	this.progress.getValue() +
		// 	(topPage.turnProgress - topPage.turnProgressLag) * 0.5;

		const bookOpenFactor = Math.min(
			this.progress.getValue(),
			this.pages.length - this.progress.getValue(),
			1,
		);

		this.pages.forEach((page, index) => {
			// TODO:
			// toggle shadow
			// if (index && index < this.pages.length - 1) {
			// 	page.mesh.castShadow = visualProgress < index + 1.9;
			// }

			let tp;
			if (this.introPhase === "ANIMATING" && index > 1) {
				tp = 1;
			} else if (index >= this.progress.getValue()) {
				tp = bookOpenFactor;
			} else if (index < Math.floor(this.progress.getValue())) {
				tp = -bookOpenFactor;
			} else {
				if (page.isCover) {
					tp = index ? bookOpenFactor : -bookOpenFactor;
				} else {
					tp = (this.progress.getValue() % 1) * -2 + 1;
				}
			}

			page.setTurnProgress(tp);

			page.bendingEnabled =
				this.progress.getValue() >= 1 &&
				this.progress.getValue() <= this.pages.length - 1;

			page.mesh.renderOrder = Math.abs(
				this.progress.getValue() - 0.5 - index,
			);

			if (page.needsUpdate()) {
				page.update(dt);
				this.pageHelpers[index]?.update();
			}
		});

		// handle book rotation
		let bookAngle = 0;
		if (this.progress.getValue() < 1) {
			bookAngle = 1 - this.progress.getValue();
		} else if (this.progress.getValue() > this.pages.length - 1) {
			bookAngle = this.pages.length - 1 - this.progress.getValue();
		}
		bookAngle *= Math.PI / 2;
		this.group.rotation.y = bookAngle;

		// handle book rotation shift (zero allocations)
		const pivotX = (bookAngle < 0 ? -this.spineWidth : this.spineWidth) / 2;
		const pivotZ = this.coverThickness;
		const cosA = Math.cos(-bookAngle);
		const sinA = Math.sin(-bookAngle);
		const transX = -pivotX;
		const transZ = -pivotZ;
		this.group.position.x = transX * cosA - transZ * sinA + pivotX;
		this.group.position.z = transX * sinA + transZ * cosA + pivotZ;

		if (!this.focusedActiveArea || this.isChangingFocus) {
			this.render();
		}
	}

	private render() {
		this.renderer.render(this.scene, this.camera);
	}

	private updateVerticalMode() {
		const screenAspect = window.innerWidth / window.innerHeight;
		this.isVerticalMode = screenAspect < 1.0;
		this.cameraSideShift.gravity = 0;
	}

	private onWindowResize() {
		this.updateVerticalMode();
		const aspect = window.innerWidth / window.innerHeight;
		this.camera.aspect = aspect;

		if (aspect < 1.0) {
			const targetHFOVRads = THREE.MathUtils.degToRad(25);
			const tanHalfHFOV = Math.tan(targetHFOVRads / 2);
			const requiredFovY = 2 * Math.atan(tanHalfHFOV / aspect) * (180 / Math.PI);
			this.camera.fov = Math.min(Math.max(requiredFovY, this.settings.cameraFov), 75);
		} else {
			this.camera.fov = this.settings.cameraFov;
		}

		this.camera.updateProjectionMatrix();
		this.renderer.setPixelRatio(
			Math.min(window.devicePixelRatio, this.isMobile ? 1 : 2),
		);
		this.renderer.setSize(window.innerWidth, window.innerHeight);
		if (this.introPhase === "COMPLETED" && !this.focusedActiveArea) {
			this.restoreCamera(0);
		}
		this.render();
	}

	public applySettings(
		newSettings: Partial<FlipbookSettings>,
		updateAll = false,
	) {
		Object.assign(this.settings, newSettings);
		if (updateAll) {
			newSettings = this.settings; // ensure all updates are triggered
		}

		if (
			newSettings.cameraDistance ||
			newSettings.cameraAngle ||
			newSettings.cameraFov
		) {
			this.restoreCamera();
		}

		if (newSettings.cameraFov) {
			this.camera.fov = this.settings.cameraFov;
			this.camera.updateProjectionMatrix();
			this.restoreCamera();
		}

		if (
			newSettings.spotLightX ||
			newSettings.spotLightY ||
			newSettings.spotLightZ
		) {
			this.spotLight.position.set(
				this.settings.spotLightX,
				this.settings.spotLightY,
				this.settings.spotLightZ,
			);
			this.spotLight.lookAt(new THREE.Vector3());

			this.spotLightHelper?.update();
			this.spotShadowHelper?.update();
		}

		if (newSettings.spotLightColor) {
			this.spotLight.color = new THREE.Color(
				this.settings.spotLightColor,
			);
		}

		if (newSettings.spotLightIntensity) {
			this.spotLight.intensity = this.settings.spotLightIntensity;
		}

		if (newSettings.spotLightAngle) {
			this.spotLight.angle = this.settings.spotLightAngle;
		}

		if (newSettings.spotLightPenumbra) {
			this.spotLight.penumbra = this.settings.spotLightPenumbra;
		}

		if (newSettings.spotLightDecay) {
			this.spotLight.decay = this.settings.spotLightDecay;
		}

		if (newSettings.spotLightNearClip || newSettings.spotLightFarClip) {
			this.spotLight.shadow.camera.near = this.settings.spotLightNearClip;
			this.spotLight.shadow.camera.far = this.settings.spotLightFarClip;
			this.spotLight.shadow.camera.updateProjectionMatrix();
		}

		if (newSettings.spotLightMapSize) {
			this.spotLight.shadow.mapSize.x = this.settings.spotLightMapSize;
			this.spotLight.shadow.mapSize.y = this.settings.spotLightMapSize;
			this.spotLight.shadow.map?.dispose?.();
			this.spotLight.shadow.map = null;
			this.spotLight.shadow.needsUpdate = true;
		}

		if (newSettings.ambientLightColor) {
			this.ambientLight.color = new THREE.Color(
				this.settings.ambientLightColor,
			);
		}

		if (newSettings.ambientLightIntensity) {
			this.ambientLight.intensity = this.settings.ambientLightIntensity;
		}

		if (typeof newSettings.showSpotLightHelper !== "undefined") {
			if (this.spotLightHelper && !newSettings.showSpotLightHelper) {
				this.scene.remove(this.spotLightHelper);
				this.spotLightHelper = null;
			}
			if (!this.spotLightHelper && newSettings.showSpotLightHelper) {
				this.spotLightHelper = new THREE.SpotLightHelper(
					this.spotLight,
				);
				this.scene.add(this.spotLightHelper);
			}
		}

		if (typeof newSettings.showSpotShadowHelper !== "undefined") {
			if (this.spotShadowHelper && !newSettings.showSpotShadowHelper) {
				this.scene.remove(this.spotShadowHelper);
				this.spotShadowHelper = null;
			}
			if (!this.spotShadowHelper && newSettings.showSpotShadowHelper) {
				this.spotShadowHelper = new THREE.CameraHelper(
					this.spotLight.shadow.camera,
				);
				this.scene.add(this.spotShadowHelper);
			}
		}

		if (typeof newSettings.showPageCurveHelpers !== "undefined") {
			if (!newSettings.showPageCurveHelpers) {
				this.pageHelpers.forEach(helper => helper.destroy());
				this.pageHelpers = [];
			}
			if (!this.spotShadowHelper && newSettings.showPageCurveHelpers) {
				this.pageHelpers = this.pages.map(
					page => new PageCurveHelper(page),
				);
			}
		}
	}

	public getActiveAreaAt(scenePos: THREE.Vector2) {
		if (!this.initCompleted) return;
		if (this.isTurning()) return;
		if (this.isShifting()) return;

		// determine a top pages
		const pr = Math.round(this.progress.getValue());
		const topPageIndices = [];
		if (pr !== 0) topPageIndices.push(pr - 1);
		if (pr !== this.pages.length) topPageIndices.push(pr);

		// run raycast
		this.raycaster.setFromCamera(scenePos, this.camera);
		const intersects = this.raycaster.intersectObjects(
			topPageIndices.map(i => this.pages[i].mesh),
		);
		if (!intersects.length) return;

		// check if ray hits one of the top pages
		const hoverPageIndex = topPageIndices.find(
			i => this.pages[i].mesh === intersects[0].object,
		);
		if (typeof hoverPageIndex !== "number") return;

		// prevent clicking bending pages
		const hoverPage = this.pages[hoverPageIndex];
		const hoverPageBend = Math.abs(
			hoverPage.turnProgress - hoverPage.turnProgressLag,
		);
		if (hoverPageBend > 0.01) return;

		// get face index
		let hoverFaceIndex;
		if (intersects[0].face?.materialIndex === 1) {
			hoverFaceIndex = hoverPageIndex * 2;
		} else if (intersects[0].face?.materialIndex === 0) {
			hoverFaceIndex = hoverPageIndex * 2 + 1;
		} else {
			return;
		}

		// find active area with given coords
		const faceX = intersects[0].uv?.x || 0;
		const faceY = 1 - (intersects[0].uv?.y || 0);
		return this.pageActiveAreas.find(
			area =>
				area.faceIndex === hoverFaceIndex &&
				faceY > area.top &&
				faceY < area.top + area.height &&
				faceX > area.left &&
				faceX < area.left + area.width,
		);
	}

	public async watchArea(
		corners: THREE.Vector3[],
		preset: "direct" | "page-zoom" | "page-unzoom" = "direct",
		duration = 0,
	) {
		const targetPos = this.getCameraPos(corners);

		if (duration === 0) {
			this.camera.position.set(
				targetPos.position.x,
				targetPos.position.y,
				targetPos.position.z,
			);
			this.camera.quaternion.set(
				targetPos.rotation.x,
				targetPos.rotation.y,
				targetPos.rotation.z,
				targetPos.rotation.w,
			);
			this.render();
			return;
		}

		let [zDuration, restDuration, restDelay] = [0, 0, 0];
		if (duration) {
			zDuration = duration;
			restDuration = duration * restFinishAt;

			if (preset === "page-unzoom") {
				restDelay = duration * (1 - restFinishAt);
			}
		}

		const ease = "power2.inOut";

		gsap.to(this.camera.position, {
			z: targetPos.position.z,
			duration: zDuration / 1000,
			ease,
		});

		const animateRest = () => {
			gsap.to(this.camera.position, {
				x: targetPos.position.x,
				duration: restDuration / 1000,
				ease,
			});

			gsap.to(this.camera.position, {
				y: targetPos.position.y,
				duration: restDuration / 1000,
				ease,
			});

			gsap.to(this.camera.quaternion, {
				x: targetPos.rotation.x,
				y: targetPos.rotation.y,
				z: targetPos.rotation.z,
				w: targetPos.rotation.w,
				duration: restDuration / 1000,
				ease,
			});
		};

		if (restDelay) {
			sleep(restDelay).then(animateRest);
		} else {
			// synchronous update is needed to prevent camera jittering
			animateRest();
		}
		await sleep(duration);
	}

	public getCameraPos(corners: THREE.Vector3[]) {
		const [TL, TR, BL, BR] = corners;

		const center = new THREE.Vector3()
			.addVectors(TL, TR)
			.add(BL)
			.add(BR)
			.multiplyScalar(0.25);

		// Calculate normal using cross product of diagonals
		let v1 = new THREE.Vector3().subVectors(BL, TR);
		let v2 = new THREE.Vector3().subVectors(BR, TL);
		const normal = new THREE.Vector3().crossVectors(v1, v2).normalize();

		const width = TL.distanceTo(TR);
		const height = TL.distanceTo(BL);

		// Calculate distance using camera's FOV and aspect ratio
		const fovYRadians = THREE.MathUtils.degToRad(this.camera.fov);
		const aspect = this.camera.aspect;
		const hFOV = 2 * Math.atan(Math.tan(fovYRadians / 2) * aspect);

		const distanceH = width / 2 / Math.tan(hFOV / 2);
		const distanceV = height / 2 / Math.tan(fovYRadians / 2);
		const distance = Math.max(distanceH, distanceV);

		const targetPosition = new THREE.Vector3(
			center.x + normal.x * distance,
			center.y + normal.y * distance,
			center.z + normal.z * distance,
		);

		// Calculate the quaternion for the target rotation
		const targetQuaternion = new THREE.Quaternion();
		const targetDirection = new THREE.Vector3()
			.subVectors(center, targetPosition)
			.normalize();
		targetQuaternion.setFromUnitVectors(
			new THREE.Vector3(0, 0, -1),
			targetDirection,
		);

		return {
			position: targetPosition,
			rotation: targetQuaternion,
		};
	}

	public async restoreCamera(duration = 0) {
		await this.watchArea(this.getBaseViewRect(), "page-unzoom", duration);
	}

	public getBaseViewRect(
		overrideSettings: null | Partial<FlipbookSettings> = null,
		overrideProgress?: number,
		overrideSideShift?: number,
	) {
		const totalMarginX = this.coverMarginX + this.coverThickness;
		const pw = this.pageWidth + totalMarginX;
		const ph = this.pageHeight + this.coverMarginY * 2;
		const yShift = -ph * 0.011; // 1.1% down

		const cornerTL = new THREE.Vector3(-pw, ph / 2 + yShift, 0);
		const cornerTR = new THREE.Vector3(pw, ph / 2 + yShift, 0);
		const cornerBL = new THREE.Vector3(-pw, ph / -2 + yShift, 0);
		const cornerBR = new THREE.Vector3(pw, ph / -2 + yShift, 0);

		const corners = [cornerTL, cornerTR, cornerBL, cornerBR];

		// applying transformations to the corners
		if (this.isVerticalMode) {
			// In portrait mode, provide comfortable padding so the full book fits elegantly
			corners.forEach(point => {
				point.x *= 1.15;
				point.y *= 1.15;
			});
		}

		const progressVal =
			overrideProgress !== undefined
				? overrideProgress
				: this.progress.getValue();

		// Center the book accurately based on progress:
		// At progress = 0 (closed front cover): shift +pageWidth/2 so front cover is centered.
		// At progress >= 1 and <= pages.length - 1 (open book): shift 0 so the 2-page spread is exactly centered!
		// At progress = pages.length (closed back cover): shift -pageWidth/2 so back cover is centered.
		let centerOffset = 0;
		if (progressVal < 1) {
			centerOffset = ((this.pageWidth + this.coverMarginX) / 2) * (1 - progressVal);
		} else if (progressVal > this.pages.length - 1) {
			centerOffset = (-(this.pageWidth + this.coverMarginX) / 2) * (progressVal - (this.pages.length - 1));
		}

		corners.forEach(point => {
			point.x += centerOffset;
		});

		// rotate the target rectangle
		const cameraAngle =
			overrideSettings?.cameraAngle || this.settings.cameraAngle;
		const cameraDistance =
			overrideSettings?.cameraDistance || this.settings.cameraDistance;
		let rotationMatrix = new THREE.Matrix4().makeRotationX(cameraAngle);
		corners.forEach(point => point.applyMatrix4(rotationMatrix));

		return scaleRectangle(corners, cameraDistance);
	}

	private async focusActiveArea(
		area: PageActiveArea,
		distanceMultiplier: number = 1,
	) {
		if (this.isChangingFocus) return;

		const page = this.pages[Math.floor(area.faceIndex / 2)];
		const isBackside = area.faceIndex % 2 === 1;
		const corners = page.getPageAreaCorners(area?.zoom || area, isBackside);

		this.focusedActiveArea = area;
		this.isChangingFocus = true;
		await this.watchArea(
			scaleRectangle(corners, distanceMultiplier),
			"page-zoom",
			1100,
		);
		this.isChangingFocus = false;

		this.updateCursor();
	}

	private async onBookClick(sceneMousePos: THREE.Vector2) {
		if (!this.isChangingFocus) {
			if (this.focusedActiveArea) {
				this.unfocusActiveArea();
			} else {
				// handle active area click
				const area = this.getActiveAreaAt(sceneMousePos);

				if (area?.link) {
					const href =
						typeof area.link === "function" ? area.link() : area.link;
					if (href) {
						if (
							href.endsWith(".pdf") ||
							area.title?.toLowerCase().includes("pdf") ||
							area.title?.toLowerCase().includes("hoja de vida") ||
							area.title?.toLowerCase().includes("resume")
						) {
							const downloadLink = document.createElement("a");
							downloadLink.href = href;
							downloadLink.download = "Tomas_Esteban_Gonzalez_Quintero_CV.pdf";
							downloadLink.target = "_blank";
							document.body.appendChild(downloadLink);
							downloadLink.click();
							downloadLink.remove();
						} else {
							window.open(href, "_blank", "noopener,noreferrer");
						}
						return;
					}
				}

				if (area?.zoom) {
					this.focusActiveArea(area, 1.05);
				}
			}
		}

		this.updateCursor();
	}
	private async unfocusActiveArea() {
		if (this.isChangingFocus) return;

		this.focusedActiveArea = null;
		this.isChangingFocus = true;
		await this.restoreCamera(1100);
		this.isChangingFocus = false;

		this.updateCursor();
	}

	private async playIntro() {
		const transitionToBottomView = async (durationMs: number) => {
			const bottomViewRect = this.getBaseViewRect(
				bottomViewSettings,
				0,
				1,
			);
			const target = this.getCameraPos(bottomViewRect);
			const dur = durationMs / 1000;
			const pTween = gsap.to(this.camera.position, {
				x: target.position.x,
				y: target.position.y,
				z: target.position.z,
				duration: dur,
				ease: "power2.inOut",
			});
			const qTween = gsap.to(this.camera.quaternion, {
				x: target.rotation.x,
				y: target.rotation.y,
				z: target.rotation.z,
				w: target.rotation.w,
				duration: dur,
				ease: "power2.inOut",
			});
			await Promise.all([pTween, qTween]);
		};

		const openFirstPage = async (durationMs: number) => {
			const animation = { progress: 0 };
			this.progress.lock();
			this.progress.setMin(0);
			this.progress.setMax(1);
			await gsap.to(animation, {
				progress: 1,
				duration: durationMs / 1000,
				ease: "power2.inOut",
				onUpdate: () => {
					this.progress.setValue(animation.progress);
				},
				onComplete: () => {
					this.progress.setValue(1);
					this.progress.setMin(-Infinity);
					this.progress.setMax(Infinity);
					this.progress.release();
					if (!this.isVerticalMode) {
						this.cameraSideShift.setValue(0);
					}
				},
			});
		};

		const transitionRaise = async (durationMs: number) => {
			const originalSettings = { ...this.settings };
			const openRect = this.getBaseViewRect(
				originalSettings,
				1,
				this.isVerticalMode ? -1 : 0,
			);
			const target = this.getCameraPos(openRect);
			const dur = durationMs / 1000;
			const pTween = gsap.to(this.camera.position, {
				x: target.position.x,
				y: target.position.y,
				z: target.position.z,
				duration: dur,
				ease: "power2.inOut",
			});
			const qTween = gsap.to(this.camera.quaternion, {
				x: target.rotation.x,
				y: target.rotation.y,
				z: target.rotation.z,
				w: target.rotation.w,
				duration: dur,
				ease: "power2.inOut",
			});
			await Promise.all([pTween, qTween]);
			this.settings.cameraDistance = originalSettings.cameraDistance;
			this.settings.cameraAngle = originalSettings.cameraAngle;
		};

		async function animateLogoFlash(durationMs: number): Promise<void> {
			const phase1Duration = durationMs * 0.45;
			const phase2Duration = durationMs * 0.3;
			const phase3Duration = durationMs * 0.25;

			// Phase 1: Fade in glow via opacity (compositable, no filter paint)
			logoEl.style.transition = `opacity ${phase1Duration}ms ease-out`;
			logoEl.style.opacity = "1";

			logoShineEl.style.transition = `opacity ${phase1Duration / 2}ms ease-out ${phase1Duration / 2}ms, transform ${phase1Duration}ms ease-out ${phase1Duration / 2}ms`;
			logoShineEl.style.opacity = "0.075";
			logoShineEl.style.transform =
				"translateX(-50%) translateY(-50%) scale(1.2)";

			await sleep(phase1Duration);

			// Phase 2: Hold
			await sleep(phase2Duration);

			// Phase 3: Fade out via opacity only
			logoEl.style.transition = `opacity ${phase3Duration}ms ease-in`;
			logoEl.style.opacity = "0";

			logoShineEl.style.transition = `opacity ${phase3Duration / 2}ms ease-in-out, transform ${phase3Duration / 2}ms ease-in-out`;
			logoShineEl.style.opacity = "0";
			logoShineEl.style.transform =
				"translateX(-50%) translateY(-50%) scale(1)";

			await sleep(phase3Duration);
		}

		const animateLightFlash = async (durationMs: number) => {
			const intensifyDurationMs = durationMs * 0.64;

			gsap.to(this.spotLight, {
				intensity: spotLightIntensity * 2,
				duration: intensifyDurationMs / 1000,
				ease: "power2.inOut",
				onComplete: () => {
					gsap.to(this.spotLight, {
						intensity: spotLightIntensity,
						duration: (durationMs - intensifyDurationMs) / 1000,
						ease: "power2.inOut",
					});
				},
			});

			gsap.to(this.ambientLight, {
				intensity: ambientLightIntensity,
				duration: intensifyDurationMs / 1000,
				ease: "power2.inOut",
			});

			await sleep(durationMs);
		};

		const bottomViewSettings = {
			cameraAngle: 0.8,
			cameraDistance: 0.85,
		};

		// remember the light values and turn them off
		const spotLightIntensity = this.spotLight.intensity;
		const ambientLightIntensity = this.ambientLight.intensity;

		this.spotLight.intensity = 0;
		this.ambientLight.intensity = 0;

		const logoEl = this.introOverlay.dom.logo;
		const logoShineEl = this.introOverlay.dom.logoShine;

		this.introPhase = "ANIMATING";

		// catch the current logo opacity value
		const currentOpacity = window.getComputedStyle(logoEl).opacity;
		logoEl.style.opacity = currentOpacity;
		logoEl.style.animation = "none";

		requestAnimationFrame(() => {
			logoEl.style.opacity = "1";
		});

		await sleep(500); // let logo and progress settle

		// perform initial setup
		this.update(1);

		// Pre-settle resting pages (2..N) to open pose so they don't calculate during intro
		for (let i = 2; i < this.pages.length; i++) {
			this.pages[i].setTurnProgress(1, true);
			this.pages[i].update(0);
			this.pages[i].settleImmediately();
		}

		// prepare camera for intro animation
		const logoArea: PageArea = {
			top: 582.5 / this.pageHeight,
			left: 279 / this.pageWidth,
			width: 204 / this.pageWidth,
			height: 204 / this.pageHeight,
		};
		const logoCorners = scaleRectangle(
			this.pages[0].getPageAreaCorners(logoArea),
			1.95,
		);
		await this.watchArea(logoCorners);

		// run the main loop
		this.runAnimation();

		this.introOverlay.dom.progress.style.opacity = "0";

		try {
			const flashDuration = this.isMobile ? 800 : 1200;
			const animDuration = this.isMobile ? 1000 : 1600;

			animateLightFlash(flashDuration);
			await animateLogoFlash(flashDuration);

			await transitionToBottomView(animDuration * 0.65);
			const openPromise = openFirstPage(animDuration);
			await sleep(animDuration * 0.15);
			const raisePromise = transitionRaise(animDuration * 0.85);
			await Promise.all([openPromise, raisePromise]);
		} finally {
			this.spotLight.intensity = spotLightIntensity;
			this.ambientLight.intensity = ambientLightIntensity;
			if (this.introOverlay?.dom?.container) {
				this.introOverlay.dom.container.style.opacity = "0";
				this.introOverlay.dom.container.style.pointerEvents = "none";
			}
			this.updateCursor();
			this.introPhase = "COMPLETED";
			this.isDirty = false;
			// Snap spring physics on all off-screen pages so the render loop stops immediately
			// update(0) first to initialize geometry without advancing physics
			const currentP = Math.round(this.progress.getValue());
			this.pages.forEach((page, i) => {
				if (Math.abs(i - currentP) > 1) {
					if (!page.hasTurnProgressUpdated) page.update(0);
					page.settleImmediately();
				}
			});
			this.onIntroCompleteCallbacks.forEach(cb => cb());
			setTimeout(() => this.startBackgroundPreload(), 4000);
		}
	}

	public finishIntroImmediately(): void {
		if (this.introPhase === "COMPLETED") return;
		this.introPhase = "COMPLETED";

		gsap.killTweensOf(this.camera.position);
		gsap.killTweensOf(this.camera.quaternion);
		gsap.killTweensOf(this.spotLight);
		gsap.killTweensOf(this.ambientLight);

		this.spotLight.intensity = this.settings.spotLightIntensity;
		this.ambientLight.intensity = this.settings.ambientLightIntensity;
		if (this.introOverlay?.dom?.container) {
			this.introOverlay.dom.container.style.opacity = "0";
			this.introOverlay.dom.container.style.pointerEvents = "none";
		}
		this.progress.setValue(1);
		this.progress.setMin(-Infinity);
		this.progress.setMax(Infinity);
		this.progress.release();
		if (!this.isVerticalMode) {
			this.cameraSideShift.setValue(0);
		} else {
			this.cameraSideShift.setValue(-1);
		}
		this.restoreCamera(0);
		this.update(1);
		this.updateCursor();
		this.isDirty = false;
		// Snap spring physics so the render loop stops at the next frame
		// update(0) first to initialize geometry without advancing physics
		const currentP = Math.round(this.progress.getValue());
		this.pages.forEach((page, i) => {
			if (Math.abs(i - currentP) > 1) {
				if (!page.hasTurnProgressUpdated) page.update(0);
				page.settleImmediately();
			}
		});
		this.onIntroCompleteCallbacks.forEach(cb => cb());
		setTimeout(() => this.startBackgroundPreload(), 4000);
	}

	public getContainerEl(): HTMLElement {
		return this.containerEl;
	}

	public getProgress(): number {
		return this.progress.getValue();
	}

	public onProgressChange(callback: (progress: number) => void): void {
		this.onProgressChangeCallbacks.push(callback);
	}

	public onIntroCompleted(callback: () => void): void {
		if (this.introPhase === "COMPLETED") {
			callback();
		} else {
			this.onIntroCompleteCallbacks.push(callback);
		}
	}

	public getIntroPhase(): "LOADING" | "ANIMATING" | "COMPLETED" {
		return this.introPhase;
	}

	public getPageCount(): number {
		return this.pages.length;
	}

	public async goToPage(targetProgress: number): Promise<void> {
		if (this.introPhase === "LOADING") return;

		const targetPage = Math.round(targetProgress);
		// Asynchronously preload target pages without blocking the 3D page turn
		this.ensurePageLoaded(targetPage);
		this.ensurePageLoaded(targetPage + 1);

		if (this.introPhase === "ANIMATING") {
			if (this.introOverlay?.dom?.container) {
				this.introOverlay.dom.container.style.opacity = "0";
				this.introOverlay.dom.container.style.pointerEvents = "none";
			}
			this.updateCursor();
			this.introPhase = "COMPLETED";
			this.onIntroCompleteCallbacks.forEach(cb => cb());
		}

		if (this.focusedActiveArea) {
			await this.unfocusActiveArea();
		}

		if (this.pageTurnTween) {
			this.pageTurnTween.kill();
			this.pageTurnTween = null;
		}

		const start = this.progress.getValue();
		if (Math.abs(targetProgress - start) < 0.05) return;

		this.progress.lock();
		this.progress.setMin(-Infinity);
		this.progress.setMax(Infinity);

		const distance = Math.abs(targetProgress - start);
		// Dynamic duration: snappy yet graceful flipping through pages
		const duration = Math.min(Math.max(distance * 0.28, 0.7), 2.2);

		const animation = { progress: start };
		this.requestRender();
		return new Promise<void>(resolve => {
			this.pageTurnTween = gsap.to(animation, {
				progress: targetProgress,
				duration,
				ease: "power2.inOut",
				onUpdate: () => {
					this.progress.setValue(animation.progress);
				},
				onComplete: () => {
					this.progress.setValue(targetProgress);
					this.progress.setMin(-Infinity);
					this.progress.setMax(Infinity);
					this.progress.release();
					this.pageTurnTween = null;
					this.requestRender();
					resolve();
				},
			});
		});
	}

	public async nextPage(): Promise<void> {
		if (this.introPhase === "LOADING") return;
		const current = Math.round(this.progress.getValue());
		const max = this.pages.length;
		if (current < max) {
			await this.goToPage(current + 1);
		}
	}

	public async prevPage(): Promise<void> {
		if (this.introPhase === "LOADING") return;
		const current = Math.round(this.progress.getValue());
		if (current > 0) {
			await this.goToPage(current - 1);
		}
	}

	public setActiveAreas(areas: PageActiveArea[]): void {
		this.pageActiveAreas = areas;
		this.updateCursor();
	}

	public updatePageTextures(pageUrls: string[]): void {
		const totalPages = Math.ceil(pageUrls.length / 2);
		this.textureUrls.pages = pageUrls;
		for (let i = 0; i < totalPages; i++) {
			const frontUrl = pageUrls[i * 2];
			const backUrl = pageUrls[i * 2 + 1];
			if (this.pages[i] && frontUrl && backUrl) {
				const frontTex = this.textureCache.get(frontUrl);
				const backTex = this.textureCache.get(backUrl);
				this.pages[i].updateTextures(
					frontTex || frontUrl,
					backTex || backUrl,
					() => this.requestRender(),
				);
			}
		}
		this.requestRender();
	}

	public preloadTextures(urls: string[]): void {
		const maxAnisotropy = this.isMobile
			? 1
			: Math.min(this.renderer?.capabilities?.getMaxAnisotropy() || 8, 8);

		urls.forEach(url => {
			if (!url || this.textureCache.has(url)) return;
			this.bgTextureLoader.load(url, (loadedTex) => {
				loadedTex.colorSpace = THREE.SRGBColorSpace;
				if (this.isMobile) {
					loadedTex.generateMipmaps = false;
					loadedTex.minFilter = THREE.LinearFilter;
					loadedTex.magFilter = THREE.LinearFilter;
					loadedTex.anisotropy = 1;
				} else {
					loadedTex.generateMipmaps = true;
					loadedTex.minFilter = THREE.LinearMipmapLinearFilter;
					loadedTex.magFilter = THREE.LinearFilter;
					loadedTex.anisotropy = maxAnisotropy;
				}
				loadedTex.needsUpdate = true;
				this.textureCache.set(url, loadedTex);
			});
		});
	}

	private async loadTextureAsync(url: string): Promise<THREE.Texture> {
		if (this.textureCache.has(url)) {
			return this.textureCache.get(url)!;
		}

		const maxAnisotropy = this.isMobile
			? 1
			: Math.min(this.renderer?.capabilities?.getMaxAnisotropy() || 16, 16);

		// Modern off-main-thread ImageBitmap decoding
		if (typeof window.createImageBitmap === "function") {
			try {
				const response = await fetch(url);
				const blob = await response.blob();
				const bitmap = await createImageBitmap(blob, {
					imageOrientation: "flipY",
					premultiplyAlpha: "none",
				});
				const texture = new THREE.Texture(bitmap);
				texture.colorSpace = THREE.SRGBColorSpace;
				if (this.isMobile) {
					texture.generateMipmaps = false;
					texture.minFilter = THREE.LinearFilter;
					texture.magFilter = THREE.LinearFilter;
					texture.anisotropy = 1;
				} else {
					texture.generateMipmaps = true;
					texture.minFilter = THREE.LinearMipmapLinearFilter;
					texture.magFilter = THREE.LinearFilter;
					texture.anisotropy = maxAnisotropy;
				}
				texture.needsUpdate = true;
				this.textureCache.set(url, texture);
				return texture;
			} catch (_) {
				// Fallback to standard loader
			}
		}

		return new Promise(resolve => {
			this.bgTextureLoader.load(
				url,
				(loadedTex: THREE.Texture) => {
					loadedTex.colorSpace = THREE.SRGBColorSpace;
					if (this.isMobile) {
						loadedTex.generateMipmaps = false;
						loadedTex.minFilter = THREE.LinearFilter;
						loadedTex.magFilter = THREE.LinearFilter;
						loadedTex.anisotropy = 1;
					} else {
						loadedTex.generateMipmaps = true;
						loadedTex.minFilter = THREE.LinearMipmapLinearFilter;
						loadedTex.magFilter = THREE.LinearFilter;
						loadedTex.anisotropy = maxAnisotropy;
					}
					loadedTex.needsUpdate = true;
					this.textureCache.set(url, loadedTex);
					resolve(loadedTex);
				},
				undefined,
				() => {
					resolve(new THREE.Texture());
				},
			);
		});
	}

	public async ensurePageLoaded(pageIndex: number): Promise<void> {
		if (
			pageIndex < 0 ||
			pageIndex >= this.pages.length ||
			this.loadedPageIndices.has(pageIndex) ||
			this.loadingPageIndices.has(pageIndex)
		) {
			return;
		}

		this.loadingPageIndices.add(pageIndex);
		const frontUrl = this.textureUrls.pages[pageIndex * 2];
		const backUrl = this.textureUrls.pages[pageIndex * 2 + 1];

		try {
			let frontTex: THREE.Texture | null = null;
			let backTex: THREE.Texture | null = null;

			if (this.isMobile) {
				// On mobile: load sequentially and yield between textures to avoid main thread spikes
				if (frontUrl) {
					frontTex = await this.loadTextureAsync(frontUrl);
					await new Promise(resolve => setTimeout(resolve, 0));
				}
				if (backUrl) {
					backTex = await this.loadTextureAsync(backUrl);
				}
			} else {
				[frontTex, backTex] = await Promise.all([
					frontUrl ? this.loadTextureAsync(frontUrl) : Promise.resolve(null),
					backUrl ? this.loadTextureAsync(backUrl) : Promise.resolve(null),
				]);
			}

			if (this.pages[pageIndex]) {
				this.pages[pageIndex].updateTextures(
					frontTex || frontUrl,
					backTex || backUrl,
					() => this.requestRender(),
				);
				this.loadedPageIndices.add(pageIndex);
				this.requestRender();
			}
		} finally {
			this.loadingPageIndices.delete(pageIndex);
		}
	}

	private schedulePredictivePreload(currentPage: number) {
		if (this.preloadNextPageTimeout) {
			window.clearTimeout(this.preloadNextPageTimeout);
		}
		this.preloadNextPageTimeout = window.setTimeout(() => {
			if (this.introPhase === "COMPLETED" && !this.isTurning() && !this.pageTurnTween) {
				const nextPageIndex = currentPage + 1;
				if (nextPageIndex < this.pages.length && !this.loadedPageIndices.has(nextPageIndex)) {
					this.ensurePageLoaded(nextPageIndex);
				}
			}
		}, this.isMobile ? 3000 : 800);
	}

	private startBackgroundPreload(): void {
		// On mobile: no background preload at all.
		// Pages are loaded on-demand via ensurePageLoaded() when the user turns them.
		if (this.isMobile) return;

		const totalPages = Math.ceil(this.textureUrls.pages.length / 2);
		let index = 2;
		// Desktop: preload next 5 pages only (avoid preloading the whole book at once)
		const limit = Math.min(totalPages, index + 5);

		const preloadNext = () => {
			if (index >= limit) return;
			const p = index++;
			if (!this.loadedPageIndices.has(p)) {
				this.ensurePageLoaded(p).finally(() => {
					if ("requestIdleCallback" in window) {
						window.requestIdleCallback(preloadNext, { timeout: 2000 });
					} else {
						setTimeout(preloadNext, 400);
					}
				});
			} else {
				preloadNext();
			}
		};

		if ("requestIdleCallback" in window) {
			window.requestIdleCallback(preloadNext, { timeout: 2000 });
		} else {
			setTimeout(preloadNext, 1500);
		}
	}
}
