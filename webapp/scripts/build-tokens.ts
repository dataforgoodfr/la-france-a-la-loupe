/**
 * Build CSS custom properties from the Figma token exports.
 *
 * Inputs:  tokens/{Mode 1,Ligth,Desktop,Mobil}.tokens.json
 * Output:  src/styles/tokens.css
 *
 * Runs directly with Node's built-in TypeScript type stripping.
 *
 * Usage: npm run tokens
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const projectDir = path.resolve(scriptDir, "..");
const tokenDir = path.join(projectDir, "tokens");
const outputFile = path.join(projectDir, "src", "styles", "tokens.css");

type FigmaColor = {
  colorSpace: string;
  components: number[];
  alpha: number;
  hex: string;
};

type TokenNode = {
  $type?: string;
  $value: string | number | FigmaColor;
  $extensions?: {
    "com.figma.aliasData"?: {
      targetVariableName?: string;
    };
  };
};

type TokenMap = Map<string, TokenNode>;

type Leaf = {
  path: string;
  node: TokenNode;
};

type Kind = "color" | "number" | "font-family" | "font-weight" | "font-size";

type ResolvedValue = {
  value: string;
  comment?: string;
};

const read = (name: string): Record<string, unknown> =>
  JSON.parse(fs.readFileSync(path.join(tokenDir, name), "utf8")) as Record<
    string,
    unknown
  >;

const mode = read("Mode 1.tokens.json");
const light = read("Ligth.tokens.json");
const desktop = read("Desktop.tokens.json");
const mobile = read("Mobil.tokens.json");

const kebab = (value: string): string =>
  value
    .toLowerCase()
    .replace(/\s+/g, "-")
    .replace(/[^a-z0-9-]/g, "");

/** Collect every `$value` leaf as a dotted path -> node map. */
function leaves(node: unknown, prefix: string[] = [], out: Leaf[] = []): Leaf[] {
  if (node && typeof node === "object") {
    if ("$value" in node) {
      out.push({ path: prefix.join("."), node: node as TokenNode });
      return out;
    }
    for (const [key, value] of Object.entries(node)) {
      if (key.startsWith("$")) continue;
      leaves(value, [...prefix, key], out);
    }
  }
  return out;
}

function walkMap(
  node: unknown,
  prefix: string[] = [],
  map: TokenMap = new Map(),
): TokenMap {
  for (const leaf of leaves(node, prefix)) map.set(leaf.path, leaf.node);
  return map;
}

const modeLeaves = walkMap(mode);
const lightLeaves = walkMap(light);
const desktopLeaves = walkMap(desktop);
const mobileLeaves = walkMap(mobile);
const handled = new Set<string>();

/* -------------------------------------------------------------------------- */
/* Names                                                                      */
/* -------------------------------------------------------------------------- */

const BASE_COLOR_ORDER = [
  "Imperial red",
  "Mint",
  "Bittersweet",
  "Light Sky Blue",
  "Charcoal",
  "Shell",
  "White",
  "Black",
];

const PALETTE_ORDER = [
  "Cherry",
  "Mint",
  "Coral Glow",
  "Raspberry",
  "Light Sky Blue",
  "Shell",
  "Gray",
];

const fontTokenNames: Record<string, string> = {
  Anton: "--font-family-title",
  Montserrat: "--font-family-text",
  "Libre Baskerville": "--font-family-quotation",
};

function modeName(dotted: string): string {
  const parts = dotted.split(".");
  if (parts[0] === "Colors") {
    return `--color-${parts.slice(1).map(kebab).join("-")}`;
  }
  if (parts[0] === "Spacing") return `--spacing-${parts[1]}`;
  if (parts[0] === "Radius") return `--radius-${parts[1]}`;
  if (parts[0] === "Fonts") {
    const name = fontTokenNames[parts[1]];
    if (!name) throw new Error(`Unmapped font token: ${dotted}`);
    return name;
  }
  return `--color-${kebab(parts[0])}`;
}

const semanticNames: Record<string, string> = {
  Black: "--color-black",
  White: "--color-white",
  "States.hover": "--color-state-hover",
  "States.pressed": "--color-state-pressed",
  "States.focus": "--color-state-focus",
  "States.disabled": "--color-state-disabled",
  "Primary.Brand.fill": "--color-primary",
  "Primary.Brand.outline": "--color-primary-outline",
  "Primary.Outline States.hover": "--color-primary-outline-hover",
  "Primary.Outline States.pressed": "--color-primary-outline-pressed",
  "Success.Brand.fill": "--color-success",
  "Success.Brand.outline": "--color-success-outline",
  "Success.Outline States.hover": "--color-success-outline-hover",
  "Success.Outline States.pressed": "--color-success-outline-pressed",
  "Warning.Brand.fill": "--color-warning",
  "Warning.Brand.outline": "--color-warning-outline",
  "Warning.Outline States.hover": "--color-warning-outline-hover",
  "Warning.Outline States.pressed": "--color-warning-outline-pressed",
  "Error.Brand.fill": "--color-error",
  "Error.Brand.outline": "--color-error-outline",
  "Error.Outline States.hover": "--color-error-outline-hover",
  "Error.Outline States.pressed": "--color-error-outline-pressed",
  "Default.Brand.fill": "--color-default",
  "Default.Brand.outline": "--color-default-outline",
  "Default.Outline States.hover": "--color-default-outline-hover",
  "Default.Outline States.pressed": "--color-default-outline-pressed",
  "Text.fill": "--color-text",
  "Text.placeholder": "--color-text-placeholder",
  "Surface.page": "--color-surface-page",
  "Surface.componants": "--color-surface-component",
  "Border.default": "--color-border-default",
  "Border.strong": "--color-border-strong",
  "Border.light": "--color-border-light",
  "Border.icon": "--color-border-icon",
};

function semanticName(dotted: string): string {
  const name = semanticNames[dotted];
  if (!name) throw new Error(`Unmapped semantic token: ${dotted}`);
  return name;
}

function typographyName(dotted: string): string {
  const parts = dotted.split(".");
  if (parts[0] === "font-family") return `--font-family-${kebab(parts[1])}`;
  if (parts[0] === "font-weight") return `--font-weight-${kebab(parts[1])}`;
  if (parts[0] === "font-size") {
    let rest = parts.slice(1).map(kebab).filter((part) => part !== "default");
    rest = rest.map((part) => (part === "txt" ? "text" : part));
    if (rest.length === 2 && rest[0] === rest[1]) rest.pop();
    return `--font-size-${rest.join("-")}`;
  }
  throw new Error(`Unmapped typography token: ${dotted}`);
}

function componentName(dotted: string): string {
  const parts = dotted.split(".");
  const component = kebab(parts.shift() ?? "");
  const rest: string[] = [];

  // Figma's size group becomes a suffix: alert.size.icon -> --alert-icon-size.
  if (component === "alert" && parts[0] === "size") {
    return `--alert-${kebab(parts[1])}-size`;
  }

  for (let index = 0; index < parts.length; index++) {
    let part = kebab(parts[index]);

    // Structural path segments do not belong in the CSS name.
    if (["space", "color", "typography", "size"].includes(part)) continue;

    // "shape" is structural for dimensions, but is a paint role in
    // search bar.selected.color.shape.
    if (part === "shape") {
      const next = kebab(parts[index + 1] ?? "");
      if (["radius", "border-width", "focus-width"].includes(next)) continue;
    }

    if (part === "fill-state" || part === "outline-state") {
      part = part === "fill-state" ? "state" : "outline";
    }
    if (part === "padding-end-action") part = "padding-end";
    if (part === "disable") part = "disabled";
    rest.push(part);
  }

  return `--${[component, ...rest].join("-")}`;
}

/* -------------------------------------------------------------------------- */
/* Alias lookups                                                              */
/* -------------------------------------------------------------------------- */

const aliasToVar = new Map<string, string>();

for (const dotted of modeLeaves.keys()) {
  const parts = dotted.split(".");
  if (
    parts[0] === "Colors" ||
    parts[0] === "Spacing" ||
    parts[0] === "Radius" ||
    parts[0] === "Fonts" ||
    BASE_COLOR_ORDER.includes(parts[0])
  ) {
    aliasToVar.set(dotted.replace(/\./g, "/"), modeName(dotted));
    if (parts[0] === "Fonts") handled.add(dotted);
  }
}

for (const dotted of lightLeaves.keys()) {
  aliasToVar.set(dotted.replace(/\./g, "/"), semanticName(dotted));
}

/* -------------------------------------------------------------------------- */
/* Values                                                                     */
/* -------------------------------------------------------------------------- */

/** Families injected by Astro, see astro.config.mjs. */
const fontValues: Record<string, string> = {
  Anton: "var(--font-anton)",
  Montserrat: "var(--font-montserrat)",
  "Libre Baskerville": "var(--font-libre-baskerville)",
};

/** A component font-family token points at the matching semantic family. */
const componentFontRoles: Record<string, string> = {
  "search bar": "text",
  "donut chart": "title",
};

function isColor(value: unknown): value is FigmaColor {
  return (
    typeof value === "object" &&
    value !== null &&
    "hex" in value &&
    "alpha" in value &&
    "components" in value
  );
}

/** Palette hex -> CSS variable, used for alpha variants with no Figma alias. */
const hexToVar = new Map<string, string>();

// Palette entries win over the base colors when a hex appears in both.
for (const dotted of modeLeaves.keys()) {
  if (!dotted.startsWith("Colors.")) continue;
  const node = modeLeaves.get(dotted)!;
  if (node.$type === "color" && isColor(node.$value)) {
    hexToVar.set(node.$value.hex.toLowerCase(), modeName(dotted));
  }
}
for (const name of BASE_COLOR_ORDER) {
  const node = modeLeaves.get(name);
  if (node?.$type === "color" && isColor(node.$value)) {
    const hex = node.$value.hex.toLowerCase();
    if (!hexToVar.has(hex)) hexToVar.set(hex, modeName(name));
  }
}

function fmtColor(value: FigmaColor): ResolvedValue {
  const hex = value.hex.toLowerCase();
  if (value.alpha >= 0.999) return { value: hex };
  const [r, g, b] = value.components.map((c) => Math.round(c * 255));
  const alpha = Number((value.alpha * 100).toFixed(2));
  return { value: `rgb(${r} ${g} ${b} / ${alpha}%)` };
}

function fmtNumber(number: number, suffix = ""): ResolvedValue {
  if (number === 0) return { value: "0" };
  const rem = Number((number / 16).toFixed(4));
  return {
    value: `${rem}rem`,
    comment: `${number}px${suffix}`,
  };
}

function resolve(dotted: string, node: TokenNode, kind: Kind): ResolvedValue {
  const alias = node.$extensions?.["com.figma.aliasData"]?.targetVariableName;
  if (alias) {
    const name = aliasToVar.get(alias);
    if (!name) throw new Error(`Unmapped alias "${alias}" for ${dotted}`);
    return { value: `var(${name})` };
  }

  const raw = node.$value;
  if (typeof raw === "string") {
    if (/^\{.+\}$/.test(raw)) {
      const reference = raw.slice(1, -1);
      return { value: `var(${typographyName(reference)})` };
    }
    if (kind === "font-family") {
      const font = fontValues[raw];
      if (!font) throw new Error(`Unmapped font "${raw}" for ${dotted}`);
      return { value: font };
    }
    return { value: raw };
  }

  if (node.$type === "color") {
    if (!isColor(raw)) throw new Error(`Invalid color for ${dotted}`);
    if (!modeLeaves.has(dotted)) {
      const token = hexToVar.get(raw.hex.toLowerCase());
      if (token) {
        const alpha = Number((raw.alpha * 100).toFixed(2));
        return alpha >= 99.9
          ? { value: `var(${token})` }
          : {
              value: `color-mix(in srgb, var(${token}) ${alpha}%, transparent)`,
            };
      }
    }
    return fmtColor(raw);
  }

  if (kind === "font-weight") return { value: String(raw) };
  if (typeof raw !== "number") {
    throw new Error(`Invalid numeric token for ${dotted}`);
  }
  return fmtNumber(raw);
}

/* -------------------------------------------------------------------------- */
/* Output                                                                     */
/* -------------------------------------------------------------------------- */

const lines: string[] = [];
const push = (line = ""): void => {
  lines.push(line);
};

function emit(
  dotted: string,
  node: TokenNode,
  name: string,
  kind: Kind,
  indent = "  ",
): void {
  handled.add(dotted);
  const resolved = resolve(dotted, node, kind);
  const comment = resolved.comment ? ` /* ${resolved.comment} */` : "";
  push(`${indent}${name}: ${resolved.value};${comment}`);
}

push('/* Design tokens from "[La France à la loupe] Design System" */');
push("/*");
push("   Source: webapp/tokens/*.tokens.json (Figma export).");
push("   Generated by webapp/scripts/build-tokens.ts; do not edit by hand.");
push("   Run `npm run tokens` after updating the Figma exports.");
push("");
push("   Layers:");
push("   1. Primitives  raw palette, spacing, radius and typography");
push("   2. Semantic    light-theme aliases (Primary, Success, Text, Surface...)");
push("   3. Components  button, chip, tag, search bar, input, alert, donut chart");
push("");
push("   Desktop values are the defaults; mobile overrides are at the end.");
push("   Figma expresses sizes in px; they are converted to rem against a 16px root.");
push("   Alpha variants reuse palette tokens through color-mix(); pure black state");
push("   overlays stay as rgb() because the palette Black is #262626.");
push("   Path segments space/shape/color/typography are omitted from component");
push("   names; Figma groups fill-state and outline-state become state and outline.");
push("*/");
push("");
push(":root {");

/* Base colors */
push("  /* Base colors */");
for (const name of BASE_COLOR_ORDER) {
  const node = modeLeaves.get(name);
  if (!node) continue;
  emit(name, node, modeName(name), "color");
}
push();

/* Palettes */
for (const palette of PALETTE_ORDER) {
  push(`  /* ${palette} */`);
  const prefix = `Colors.${palette}.`;
  const steps = [...modeLeaves.keys()]
    .filter((key) => key.startsWith(prefix))
    .sort(
      (a, b) => Number(a.slice(prefix.length)) - Number(b.slice(prefix.length)),
    );
  for (const dotted of steps) {
    emit(dotted, modeLeaves.get(dotted)!, modeName(dotted), "color");
  }
  push();
}

/* Spacing */
push("  /* Spacing */");
for (const dotted of [...modeLeaves.keys()].filter((key) =>
  key.startsWith("Spacing."),
)) {
  emit(dotted, modeLeaves.get(dotted)!, modeName(dotted), "number");
}
push();

/* Radius */
push("  /* Radius */");
for (const dotted of [...modeLeaves.keys()].filter((key) =>
  key.startsWith("Radius."),
)) {
  emit(dotted, modeLeaves.get(dotted)!, modeName(dotted), "number");
}
push();

/* Typography */
push("  /* Typography */");
push("  /* Astro injects --font-anton, --font-montserrat and --font-libre-baskerville");
push("     (see astro.config.mjs); semantic roles map to those families. */");
for (const dotted of [
  "font-family.title",
  "font-family.subtitle",
  "font-family.text",
  "font-family.btn",
  "font-family.tag",
  "font-family.input",
  "font-family.quotation",
  "font-family.chip",
  "font-family.alert",
]) {
  emit(
    dotted,
    desktopLeaves.get(dotted)!,
    typographyName(dotted),
    "font-family",
  );
}
push();

for (const [title, role] of [
  ["Title", "title"],
  ["Subtitle", "subtitle"],
]) {
  push(`  /* ${title} sizes */`);
  for (const level of ["h1", "h2", "h3", "h4"]) {
    const dotted = `font-size.${role}.${level}`;
    emit(
      dotted,
      desktopLeaves.get(dotted)!,
      typographyName(dotted),
      "font-size",
    );
  }
  push();
}

push("  /* Component and text sizes */");
for (const dotted of [
  "font-size.btn.default",
  "font-size.input.input",
  "font-size.input.label",
  "font-size.tag.default",
  "font-size.txt.large",
  "font-size.txt.medium",
  "font-size.txt.little",
  "font-size.chart.large",
  "font-size.chip.default",
  "font-size.alert.default",
]) {
  emit(dotted, desktopLeaves.get(dotted)!, typographyName(dotted), "font-size");
}
push();

push("  /* Weight */");
for (const dotted of [
  "font-weight.light",
  "font-weight.regular",
  "font-weight.semibold",
  "font-weight.bold",
]) {
  emit(
    dotted,
    desktopLeaves.get(dotted)!,
    typographyName(dotted),
    "font-weight",
  );
}
push();

/* Semantic colors */
const semanticSections: Array<[string, string[]]> = [
  ["States", ["States.hover", "States.pressed", "States.focus", "States.disabled"]],
  [
    "Primary",
    [
      "Primary.Brand.fill",
      "Primary.Brand.outline",
      "Primary.Outline States.hover",
      "Primary.Outline States.pressed",
    ],
  ],
  [
    "Success",
    [
      "Success.Brand.fill",
      "Success.Brand.outline",
      "Success.Outline States.hover",
      "Success.Outline States.pressed",
    ],
  ],
  [
    "Warning",
    [
      "Warning.Brand.fill",
      "Warning.Brand.outline",
      "Warning.Outline States.hover",
      "Warning.Outline States.pressed",
    ],
  ],
  [
    "Error",
    [
      "Error.Brand.fill",
      "Error.Brand.outline",
      "Error.Outline States.hover",
      "Error.Outline States.pressed",
    ],
  ],
  [
    "Default",
    [
      "Default.Brand.fill",
      "Default.Brand.outline",
      "Default.Outline States.hover",
      "Default.Outline States.pressed",
    ],
  ],
  ["Text", ["Text.fill", "Text.placeholder"]],
  ["Surface", ["Surface.page", "Surface.componants"]],
  ["Border", ["Border.default", "Border.strong", "Border.light", "Border.icon"]],
];

push("  /* ---------------------------------------------------------------------- */");
push("  /* Semantic colors (light theme)                                          */");
push("  /* ---------------------------------------------------------------------- */");
for (const [title, keys] of semanticSections) {
  push(`  /* ${title} */`);
  for (const dotted of keys) {
    const node = lightLeaves.get(dotted);
    if (!node) throw new Error(`Missing token ${dotted}`);
    emit(dotted, node, semanticName(dotted), "color");
  }
  push();
}

/* Components */
push("  /* ---------------------------------------------------------------------- */");
push("  /* Components                                                             */");
push("  /* ---------------------------------------------------------------------- */");

const componentSections: Array<[string, string]> = [
  ["Button", "btn"],
  ["Chip", "chip"],
  ["Tag", "tag"],
  ["Search bar", "search bar"],
  ["Input", "input"],
  ["Alert", "alert"],
  ["Donut chart", "donut chart"],
];

for (const [title, component] of componentSections) {
  push(`  /* ${title} */`);
  const keys = [...desktopLeaves.keys()].filter(
    (key) => key === component || key.startsWith(`${component}.`),
  );
  for (const dotted of keys) {
    if (dotted.endsWith(".typography.font-family")) {
      const role = componentFontRoles[component];
      if (!role) throw new Error(`No font role for component "${component}"`);
      handled.add(dotted);
      push(`  ${componentName(dotted)}: var(--font-family-${role});`);
      continue;
    }
    emit(dotted, desktopLeaves.get(dotted)!, componentName(dotted), "number");
  }
  push();
}

/* Mobile overrides */
const mobileOverrides: Array<[string, TokenNode, string, Kind]> = [];
for (const [dotted, node] of mobileLeaves) {
  const desktopNode = desktopLeaves.get(dotted);
  if (!desktopNode) throw new Error(`Mobile-only token: ${dotted}`);
  if (JSON.stringify(node.$value) === JSON.stringify(desktopNode.$value)) {
    continue;
  }
  const isTypography = dotted.startsWith("font-");
  const kind: Kind = dotted.startsWith("font-size")
    ? "font-size"
    : dotted.startsWith("font-weight")
      ? "font-weight"
      : dotted.startsWith("font-family")
        ? "font-family"
        : "number";
  const name = isTypography ? typographyName(dotted) : componentName(dotted);
  mobileOverrides.push([dotted, node, name, kind]);
}

lines.pop(); // remove trailing blank line from the last component group
push("}");
push("");
push("/* ------------------------------------------------------------------------ */");
push("/* Mobile overrides (< 48rem / 768px)                                       */");
push("/* ------------------------------------------------------------------------ */");
push("@media (width < 48rem) {");
push("  :root {");
for (const [dotted, node, name, kind] of mobileOverrides) {
  emit(dotted, node, name, kind, "    ");
}
push("  }");
push("}");

// Fail loudly if the Figma export gains a group the script does not map yet.
for (const [label, tokenMap] of [
  ["Mode 1", modeLeaves],
  ["Ligth", lightLeaves],
  ["Desktop", desktopLeaves],
] as Array<[string, TokenMap]>) {
  for (const dotted of tokenMap.keys()) {
    if (!handled.has(dotted)) {
      throw new Error(`Unhandled ${label} token: ${dotted}`);
    }
  }
}

const output = `${lines.join("\n")}\n`;
const previous = fs.existsSync(outputFile)
  ? fs.readFileSync(outputFile, "utf8")
  : "";
fs.writeFileSync(outputFile, output, "utf8");

const relativeOutput = path.relative(projectDir, outputFile);
console.log(
  previous === output
    ? `${relativeOutput} is already up to date`
    : `Wrote ${relativeOutput}`,
);
console.log(
  `  ${modeLeaves.size + lightLeaves.size + desktopLeaves.size} tokens, ` +
    `${mobileOverrides.length} mobile overrides`,
);
