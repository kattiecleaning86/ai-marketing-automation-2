// Render a JSON block spec into a branded .docx  —  usage: node render_docx.js spec.json out.docx
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  AlignmentType, HeadingLevel, LevelFormat, PageBreak, Header, Footer, PageNumber, ExternalHyperlink,
  TableOfContents, VerticalAlign,
} = require("docx");

const [, , specPath, outPath] = process.argv;
const spec = JSON.parse(fs.readFileSync(specPath, "utf8"));
const FONT = "Arial", BLACK = "0A0A0A", RED = "D23030", GREY = "595959", LIGHT = "F2F2F2";
const CONTENT_W = 9360; // US Letter, 1" margins

// inline: **bold** and URLs -> runs
function runs(text, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|https?:\/\/[^\s)]+)/g;
  let last = 0, m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), font: FONT, ...base }));
    const tok = m[0];
    if (tok.startsWith("**")) out.push(new TextRun({ text: tok.slice(2, -2), bold: true, font: FONT, ...base }));
    else {
      let url = tok.replace(/[.,;]+$/, "");
      out.push(new ExternalHyperlink({ link: url, children: [new TextRun({ text: url, style: "Hyperlink", font: FONT, ...base })] }));
      if (url.length < tok.length) out.push(new TextRun({ text: tok.slice(url.length), font: FONT, ...base }));
    }
    last = m.index + tok.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), font: FONT, ...base }));
  return out;
}

const border = { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" };
const cellBorders = { top: border, bottom: border, left: border, right: border };

function table(b) {
  const n = b.headers.length;
  let widths = b.widths && b.widths.length === n ? b.widths.slice() : Array(n).fill(Math.floor(CONTENT_W / n));
  const sum = widths.reduce((a, c) => a + c, 0);
  widths = widths.map((w) => Math.floor((w * CONTENT_W) / sum));
  widths[n - 1] += CONTENT_W - widths.reduce((a, c) => a + c, 0);
  const mk = (txt, i, hdr, shade) =>
    new TableCell({
      width: { size: widths[i], type: WidthType.DXA },
      borders: cellBorders,
      shading: hdr ? { fill: BLACK, type: ShadingType.CLEAR, color: "auto" } : shade ? { fill: LIGHT, type: ShadingType.CLEAR, color: "auto" } : undefined,
      margins: { top: 60, bottom: 60, left: 100, right: 100 },
      verticalAlign: VerticalAlign.TOP,
      children: String(txt ?? "").split("\n").map((line) =>
        new Paragraph({ spacing: { after: 40 }, children: runs(line, hdr ? { bold: true, color: "FFFFFF", size: 18 } : { size: 18 }) })),
    });
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: widths,
    rows: [
      new TableRow({ tableHeader: true, children: b.headers.map((h, i) => mk(h, i, true)) }),
      ...b.rows.map((r, ri) => new TableRow({ cantSplit: false, children: r.map((c, i) => mk(c, i, false, ri % 2 === 1)) })),
    ],
  });
}

function callout(b) {
  const fill = b.tone === "warn" ? "FDECEC" : b.tone === "action" ? "FFF8E1" : "EEF3F8";
  const bar = b.tone === "warn" ? RED : b.tone === "action" ? "C9A227" : "2F5597";
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: [CONTENT_W],
    rows: [new TableRow({ children: [new TableCell({
      width: { size: CONTENT_W, type: WidthType.DXA },
      borders: { top: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" }, bottom: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" }, right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" }, left: { style: BorderStyle.SINGLE, size: 24, color: bar } },
      shading: { fill, type: ShadingType.CLEAR, color: "auto" },
      margins: { top: 100, bottom: 100, left: 180, right: 140 },
      children: [new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: b.label, bold: true, font: FONT, size: 19, color: bar })] }),
                 new Paragraph({ children: runs(b.text, { size: 19 }) })],
    })] })],
  });
}

function codeBlock(text) {
  const lines = text.split("\n");
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: [CONTENT_W],
    rows: [new TableRow({ children: [new TableCell({
      width: { size: CONTENT_W, type: WidthType.DXA }, borders: cellBorders,
      shading: { fill: "FAFAFA", type: ShadingType.CLEAR, color: "auto" },
      margins: { top: 120, bottom: 120, left: 160, right: 160 },
      children: lines.map((l) => new Paragraph({ spacing: { after: 20 }, children: runs(l || " ", { size: 20 }) })),
    })] })],
  });
}

const spacer = () => new Paragraph({ spacing: { after: 80 }, children: [] });
const body = [];
for (const b of spec.blocks) {
  switch (b.t) {
    case "h1": body.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: b.text, font: FONT })] })); break;
    case "h2": body.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun({ text: b.text, font: FONT })] })); break;
    case "h3": body.push(new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun({ text: b.text, font: FONT })] })); break;
    case "p": body.push(new Paragraph({ spacing: { after: 120 }, children: runs(b.text) })); break;
    case "ul": b.items.forEach((it) => body.push(new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 60 }, children: runs(it) }))); body.push(spacer()); break;
    case "ol": b.items.forEach((it) => body.push(new Paragraph({ numbering: { reference: "numbers", level: 0 }, spacing: { after: 60 }, children: runs(it) }))); body.push(spacer()); break;
    case "table": body.push(table(b)); body.push(spacer()); break;
    case "callout": body.push(callout(b)); body.push(spacer()); break;
    case "code": body.push(codeBlock(b.text)); body.push(spacer()); break;
    case "pagebreak": body.push(new Paragraph({ children: [new PageBreak()] })); break;
  }
}
// drop trailing page break
while (body.length && body[body.length - 1] instanceof Paragraph && spec.blocks[spec.blocks.length - 1].t === "pagebreak") { body.pop(); spec.blocks.pop(); }

const c = spec.cover;
const cover = [
  new Paragraph({ spacing: { before: 2400, after: 120 }, children: [new TextRun({ text: "APEX WEB STUDIOS", font: FONT, bold: true, size: 22, color: RED, characterSpacing: 60 })] }),
  new Paragraph({ spacing: { after: 200 }, border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: RED, space: 8 } }, children: [new TextRun({ text: c.title, font: FONT, bold: true, size: 56, color: BLACK })] }),
  new Paragraph({ spacing: { after: 600 }, children: [new TextRun({ text: c.subtitle, font: FONT, size: 28, color: GREY })] }),
  new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "Client: ", font: FONT, bold: true, size: 22 }), new TextRun({ text: c.client, font: FONT, size: 22 })] }),
  new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "Period: ", font: FONT, bold: true, size: 22 }), new TextRun({ text: c.period, font: FONT, size: 22 })] }),
  new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "Version: ", font: FONT, bold: true, size: 22 }), new TextRun({ text: c.version, font: FONT, size: 22 })] }),
  new Paragraph({ spacing: { before: 600 }, children: [new TextRun({ text: c.status, font: FONT, bold: true, size: 20, color: RED })] }),
  new Paragraph({ spacing: { before: 120 }, children: [new TextRun({ text: "Organic (non-paid) social media. Prepared for internal review and approval. All statistics are sourced and linked; unverified items are labelled.", font: FONT, size: 18, color: GREY })] }),
  new Paragraph({ children: [new PageBreak()] }),
  new Paragraph({ spacing: { after: 200 }, children: [new TextRun({ text: "Contents", font: FONT, bold: true, size: 32 })] }),
  ...spec.blocks.filter((x) => x.t === "h1").map((x) => new Paragraph({ spacing: { after: 80 }, border: { bottom: { style: BorderStyle.DOTTED, size: 4, color: "BFBFBF", space: 2 } }, children: [new TextRun({ text: x.text, font: FONT, size: 20 })] })),
  new Paragraph({ children: [new PageBreak()] }),
];

const doc = new Document({
  creator: "Apex Web Studios — Organic Social",
  title: `Apex Web Studios — ${c.title}`,
  
  styles: {
    default: { document: { run: { font: FONT, size: 20 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FONT, size: 30, bold: true, color: BLACK }, paragraph: { spacing: { before: 320, after: 140 }, keepNext: true, outlineLevel: 0, border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: RED, space: 4 } } } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FONT, size: 24, bold: true, color: RED }, paragraph: { spacing: { before: 240, after: 100 }, keepNext: true, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FONT, size: 21, bold: true, color: GREY }, paragraph: { spacing: { before: 160, after: 60 }, keepNext: true, outlineLevel: 2 } },
    ],
  },
  numbering: { config: [
    { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] },
    { reference: "numbers", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] },
  ] },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: `Apex Web Studios · ${c.title} · December 2026`, font: FONT, size: 16, color: GREY })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
      new TextRun({ text: "Pending Review · Not for publication without written approval · Page ", font: FONT, size: 16, color: GREY }),
      new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: GREY }),
      new TextRun({ text: " of ", font: FONT, size: 16, color: GREY }),
      new TextRun({ children: [PageNumber.TOTAL_PAGES], font: FONT, size: 16, color: GREY }),
    ] })] }) },
    children: [...cover, ...body],
  }],
});
Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(outPath, buf); console.log("wrote", outPath); });
