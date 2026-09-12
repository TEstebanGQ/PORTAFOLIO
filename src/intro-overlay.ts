export default class IntroOverlay {
	public dom: {
		container: HTMLDivElement;
		logo: HTMLImageElement;
		logoShine: HTMLImageElement;
		progress: HTMLDivElement;
		progressInner: HTMLDivElement;
	};

	constructor(container: HTMLDivElement) {
		this.dom = {
			container,
			logo: container.querySelector(".logo")!,
			logoShine: container.querySelector(".logo-shine")!,
			progress: container.querySelector(".progress")!,
			progressInner: container.querySelector(".progress-inner")!,
		};
	}

	public onProgress(newProgress: number) {
		const clamped = Math.min(Math.max(newProgress, 0), 1);
		this.dom.progressInner.style.transform = `scaleX(${clamped})`;
	}
}
