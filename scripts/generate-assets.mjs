/**
 * Generates raster brand assets from the source SVGs in /public.
 *
 *   public/vAI.svg       -> vAI.png, vAI_512.png, apple-touch-icon.png, favicon.ico
 *   public/og-image.svg  -> og-image.png (1200x630)
 *
 * Runs automatically before `npm run build` (see the "prebuild" script).
 * Safe to run by hand:  node scripts/generate-assets.mjs
 *
 * If sharp/png-to-ico are unavailable it logs a warning and exits 0 so a
 * deploy is never blocked — the SVGs remain as the fallback.
 */
import { readFile, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const pub = join(root, "public");

async function main() {
  const { default: sharp } = await import("sharp");
  const { default: pngToIco } = await import("png-to-ico");

  const logoSvg = await readFile(join(pub, "vAI.svg"));
  const ogSvg = await readFile(join(pub, "og-image.svg"));

  const render = (svg, w, h) =>
    sharp(svg, { density: 384 })
      .resize(w, h, { fit: "contain", background: { r: 0, g: 0, b: 0, alpha: 0 } })
      .png()
      .toBuffer();

  // Logo PNGs (transparent background)
  const logo1024 = await render(logoSvg, 1024, 1024);
  const logo512 = await render(logoSvg, 512, 512);
  const logo180 = await render(logoSvg, 180, 180);
  await writeFile(join(pub, "vAI.png"), logo1024);
  await writeFile(join(pub, "vAI_512.png"), logo512);
  await writeFile(join(pub, "apple-touch-icon.png"), logo180);

  // favicon.ico (multi-resolution: 16, 32, 48)
  const icoSizes = await Promise.all([16, 32, 48].map((s) => render(logoSvg, s, s)));
  await writeFile(join(pub, "favicon.ico"), await pngToIco(icoSizes));

  // Social share card
  const og = await sharp(ogSvg, { density: 144 }).resize(1200, 630).png().toBuffer();
  await writeFile(join(pub, "og-image.png"), og);

  console.log("✓ Generated brand assets: vAI.png, vAI_512.png, apple-touch-icon.png, favicon.ico, og-image.png");
}

main().catch((err) => {
  console.warn("⚠ Skipping brand-asset generation:", err?.message || err);
  process.exit(0);
});
