// Strip the @-moz-document wrapper from a compiled build so the CSS can be
// injected into a page in Chromium for preview (Chromium drops @-moz-document
// blocks). Only the domain() block is kept; the URL-scoped icon sections
// are per-page and left out. Usage: node tools/unwrap.js build/default.css out.css
const fs = require('fs');
const [,, src, dst] = process.argv;
let css = fs.readFileSync(src, 'utf8');
const start = css.indexOf('{', css.indexOf('@-moz-document domain'));
const end = css.indexOf('\n}\n/* ====', start);
css = css.slice(start + 1, end === -1 ? css.lastIndexOf('}') : end);
fs.writeFileSync(dst, css);
console.log('unwrapped', css.length, 'chars ->', dst);
