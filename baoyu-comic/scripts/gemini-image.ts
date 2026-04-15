import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const DEFAULT_GEMINI_MODEL = process.env.GOOGLE_IMAGE_MODEL || "gemini-3-pro-image-preview";

function printUsage(): void {
  console.log(`Usage:
  npx -y bun scripts/gemini-image.ts --promptfiles prompts/01.md --image 01.png --ar 3:4 --ref characters/characters.png

Behavior:
  - Forces provider to Google (Gemini API)
  - Uses model ${DEFAULT_GEMINI_MODEL} by default
  - If --model gemini is passed, maps it to ${DEFAULT_GEMINI_MODEL}

Environment:
  - Set GEMINI_API_KEY (or GOOGLE_API_KEY)
  - Optional: GOOGLE_IMAGE_MODEL, GOOGLE_BASE_URL
`);
}

function normalizeGeminiArgs(argv: string[]): string[] {
  const out: string[] = [];
  let hasModel = false;

  for (let i = 0; i < argv.length; i++) {
    const a = argv[i]!;

    if (a === "--provider") {
      i += 1;
      continue;
    }
    if (a.startsWith("--provider=")) {
      continue;
    }

    if (a === "--model" || a === "-m") {
      const v = argv[++i];
      if (!v) throw new Error(`Missing value for ${a}`);
      hasModel = true;
      out.push(a, v === "gemini" ? DEFAULT_GEMINI_MODEL : v);
      continue;
    }

    if (a.startsWith("--model=")) {
      hasModel = true;
      const v = a.slice("--model=".length);
      out.push(`--model=${v === "gemini" ? DEFAULT_GEMINI_MODEL : v}`);
      continue;
    }

    out.push(a);
  }

  out.push("--provider", "google");
  if (!hasModel) {
    out.push("--model", DEFAULT_GEMINI_MODEL);
  }

  return out;
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  if (args.includes("-h") || args.includes("--help")) {
    printUsage();
    return;
  }

  const thisFile = fileURLToPath(import.meta.url);
  const scriptDir = path.dirname(thisFile);
  const imageGenEntry = path.resolve(scriptDir, "../../baoyu-image-gen/scripts/main.ts");
  const forwardedArgs = normalizeGeminiArgs(args);

  const proc = Bun.spawn([process.execPath, imageGenEntry, ...forwardedArgs], {
    stdin: "inherit",
    stdout: "inherit",
    stderr: "inherit",
    env: process.env,
  });

  const code = await proc.exited;
  process.exit(code);
}

main().catch((e) => {
  console.error(e instanceof Error ? e.message : String(e));
  process.exit(1);
});
