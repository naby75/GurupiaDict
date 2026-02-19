/**
 * vendor 의존성 로컬 번들링 스크립트 (#14)
 * CDN 리소스를 static/vendor/에 다운로드합니다.
 */
const fs = require('fs');
const path = require('path');
const https = require('https');

const VENDOR_DIR = path.join(__dirname, 'static', 'vendor');

const FILES = [
    {
        url: 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js',
        out: 'highlight.min.js'
    },
    {
        url: 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css',
        out: 'github-dark.min.css'
    },
    {
        url: 'https://cdnjs.cloudflare.com/ajax/libs/dompurify/3.1.6/purify.min.js',
        out: 'purify.min.js'
    }
];

function download(url, dest) {
    return new Promise((resolve, reject) => {
        const file = fs.createWriteStream(dest);
        https.get(url, { headers: { 'User-Agent': 'GurupiaDict-Setup/1.0' } }, (res) => {
            if (res.statusCode === 301 || res.statusCode === 302) {
                file.close();
                fs.unlink(dest, () => { });
                return download(res.headers.location, dest).then(resolve).catch(reject);
            }
            if (res.statusCode !== 200) {
                file.close();
                return reject(new Error(`HTTP ${res.statusCode} for ${url}`));
            }
            res.pipe(file);
            file.on('finish', () => file.close(resolve));
        }).on('error', (err) => {
            fs.unlink(dest, () => { });
            reject(err);
        });
    });
}

async function main() {
    if (!fs.existsSync(VENDOR_DIR)) {
        fs.mkdirSync(VENDOR_DIR, { recursive: true });
    }

    for (const { url, out } of FILES) {
        const dest = path.join(VENDOR_DIR, out);
        process.stdout.write(`📥 ${out}... `);
        try {
            await download(url, dest);
            const size = (fs.statSync(dest).size / 1024).toFixed(1);
            console.log(`✅ ${size} KB`);
        } catch (err) {
            console.log(`❌ ${err.message}`);
        }
    }
    console.log('\n✅ Vendor bundle complete! Files in static/vendor/');
}

main();
