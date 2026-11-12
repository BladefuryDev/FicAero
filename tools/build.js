// Compile ficaero.user.css the way the Stylus extension does:
// read the @var defaults from the UserStyle header, inject them as
// Stylus-language assignments, compile the body, and write plain CSS.
//
//   node build.js <stylus-module-dir> [name=value ...]
//
// Overrides let every branch be exercised, e.g.  theme=dark readsize=18px
// Output: build/<label>.css next to the theme (label from overrides).
const fs = require('fs');
const path = require('path');

const stylusDir = process.argv[2];
const stylus = require(path.join(stylusDir, 'node_modules', 'stylus'));
const overrides = Object.fromEntries(process.argv.slice(3).map(a => a.split('=')));

const root = path.join(__dirname, '..');
const src = fs.readFileSync(path.join(root, 'ficaero.user.css'), 'utf8');
const header = src.match(/\/\* ==UserStyle==([\s\S]*?)==\/UserStyle== \*\//)[1];
const body = src.slice(src.indexOf('==/UserStyle== */') + '==/UserStyle== */'.length);

// Parse @var lines (select blocks span several lines).
const vars = {};
const re = /@var\s+(\w+)\s+(\w+)\s+"[^"]*"\s+([\s\S]*?)(?=\n@var|\n*$)/g;
let m;
while ((m = re.exec(header))) {
  const [, type, name, rawValue] = m;
  const raw = rawValue.trim();
  if (type === 'select') {
    // { "Label*": value, ... }  -> the starred (or first) option's value
    const opts = [...raw.matchAll(/"([^"]*)"\s*:\s*("(?:[^"\\]|\\.)*"|[^,\n}]+)/g)].map(o => ({
      label: o[1], value: o[2].trim().replace(/^"|"$/g, '')
    }));
    const def = opts.find(o => o.label.endsWith('*')) || opts[0];
    vars[name] = def.value;
  } else if (type === 'range') {
    const parts = raw.replace(/[\[\]]/g, '').split(',').map(s => s.trim());
    const unit = parts[4] ? parts[4].replace(/'/g, '') : '';
    vars[name] = parts[0] + unit;
  } else {
    vars[name] = raw; // color hex, checkbox 0/1
  }
}
Object.assign(vars, overrides);

const prelude = Object.entries(vars).map(([k, v]) => `${k} = ${v}`).join('\n') + '\n';
const label = Object.keys(overrides).length ? Object.values(overrides).join('_').replace(/[^\w.-]+/g, '_') : 'default';
const outDir = path.join(root, 'build');
fs.mkdirSync(outDir, { recursive: true });

stylus(prelude + body).render((err, css) => {
  if (err) { console.error('STYLUS ERROR (' + label + '):', err.message); process.exit(1); }
  // An unexpanded {placeholder} means a selector was built from a quoted
  // string; the browser would drop every rule that carries it.
  const leftover = css.match(/\{[a-z][\w-]*\}/g);
  if (leftover) { console.error('UNEXPANDED PLACEHOLDER (' + label + '):', [...new Set(leftover)].join(' ')); process.exit(1); }
  fs.writeFileSync(path.join(outDir, label + '.css'), css);
  console.log('ok', label, css.length + ' chars', 'vars:', JSON.stringify(vars));
});
