import fs from "fs";
import path from "path";
import sharp from "sharp";

const DIRS = [
	path.resolve("public/img/pages-en"),
	path.resolve("public/img/pages"),
];

async function convertDirectory(dirPath) {
	if (!fs.existsSync(dirPath)) {
		console.log(`Directory not found: ${dirPath}`);
		return;
	}

	const files = fs.readdirSync(dirPath);
	let totalOld = 0;
	let totalNew = 0;

	console.log(`\nProcessing: ${path.basename(dirPath)}`);
	console.log("--------------------------------------------------");

	for (const file of files) {
		if (!file.endsWith(".jpg") && !file.endsWith(".jpeg")) continue;

		const srcPath = path.join(dirPath, file);
		const baseName = file.replace(/\.(jpg|jpeg)$/i, "");
		const destPath = path.join(dirPath, `${baseName}.webp`);

		const oldSize = fs.statSync(srcPath).size;
		totalOld += oldSize;

		// Convert to WebP using Google's recommended quality settings (quality 78, near-lossless compression)
		await sharp(srcPath)
			.webp({ quality: 78, effort: 6 })
			.toFile(destPath);

		const newSize = fs.statSync(destPath).size;
		totalNew += newSize;

		const saved = (((oldSize - newSize) / oldSize) * 100).toFixed(1);
		console.log(
			`${file} -> ${baseName}.webp: ${(oldSize / 1024).toFixed(0)}KB -> ${(newSize / 1024).toFixed(0)}KB (-${saved}%)`
		);
	}

	const totalSaved = (((totalOld - totalNew) / totalOld) * 100).toFixed(1);
	console.log("--------------------------------------------------");
	console.log(
		`TOTAL: ${(totalOld / (1024 * 1024)).toFixed(2)}MB -> ${(totalNew / (1024 * 1024)).toFixed(2)}MB (Saved ${totalSaved}%)\n`
	);
}

async function main() {
	for (const dir of DIRS) {
		await convertDirectory(dir);
	}

	// Also desk image
	const deskJpg = path.resolve("public/img/desk.jpg");
	const deskWebp = path.resolve("public/img/desk.webp");
	if (fs.existsSync(deskJpg)) {
		const oldSize = fs.statSync(deskJpg).size;
		await sharp(deskJpg).webp({ quality: 78, effort: 6 }).toFile(deskWebp);
		const newSize = fs.statSync(deskWebp).size;
		console.log(
			`desk.jpg -> desk.webp: ${(oldSize / 1024).toFixed(0)}KB -> ${(newSize / 1024).toFixed(0)}KB`
		);
	}
}

main().catch(console.error);
