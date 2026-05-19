const fs = require('fs');
const p = '/home/anjishnu-nandi/Documents/GitHub/get_smth/frontend/src/App.tsx';
let it = fs.readFileSync(p, 'utf8');
it = it.replace('className={\\`px-3', 'className={`px-3');
it = it.replace('semibold \\${', 'semibold ${');
it = it.replace('}\\`}>', '}`}>');
fs.writeFileSync(p, it);
