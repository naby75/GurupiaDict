const fs = require('fs');
const path = require('path');

async function fetchMdnArticle(pathStr, category) {
    const url = `https://developer.mozilla.org/en-US/docs/${pathStr}/index.json`;
    console.log(`🚀 Fetching MDN (${category}): ${url}`);

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const data = await response.json();
        const doc = data.doc;
        const title = doc.title;
        const summary = doc.summary;

        let content = `# ${title}\n\n${summary}\n\n`;

        if (doc.body) {
            // Take first 3 sections
            doc.body.slice(0, 3).forEach(section => {
                if (section.title) content += `## ${section.title}\n`;
                if (section.value) content += `${section.value}\n\n`;
            });
        }

        return {
            title: `${category}:${title}`,
            content: content
        };
    } catch (e) {
        console.error(`❌ Error fetching ${pathStr}: ${e.message}`);
        return null;
    }
}

async function main() {
    const targets = {
        js: [
            'Web/JavaScript/Reference/Global_Objects/Array',
            'Web/JavaScript/Reference/Global_Objects/String',
            'Web/JavaScript/Reference/Global_Objects/Object',
            'Web/JavaScript/Reference/Global_Objects/Promise',
            'Web/JavaScript/Reference/Global_Objects/Function',
            'Web/JavaScript/Reference/Global_Objects/JSON',
            'Web/JavaScript/Reference/Global_Objects/Map',
            'Web/JavaScript/Reference/Global_Objects/Set',
            'Web/JavaScript/Reference/Global_Objects/Math',
            'Web/JavaScript/Reference/Global_Objects/Date',
        ],
        html: [
            'Web/HTML/Element/div',
            'Web/HTML/Element/span',
            'Web/HTML/Element/a',
            'Web/HTML/Element/img',
            'Web/HTML/Element/button',
            'Web/HTML/Element/input',
            'Web/HTML/Element/form',
            'Web/HTML/Element/video',
            'Web/HTML/Element/canvas',
        ],
        css: [
            'Web/CSS/CSS_Flexible_Box_Layout/Basic_Concepts_of_Flexbox',
            'Web/CSS/CSS_Grid_Layout/Basic_Concepts_of_Grid_Layout',
            'Web/CSS/box-model',
            'Web/CSS/color',
            'Web/CSS/background',
            'Web/CSS/font',
            'Web/CSS/position',
        ]
    };

    const outputDir = path.join(process.cwd(), "mdn_data");
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir);
    }

    const allDocs = [];

    for (const [category, paths] of Object.entries(targets)) {
        for (const pathStr of paths) {
            const doc = await fetchMdnArticle(pathStr, category);
            if (doc) {
                allDocs.push(doc);
            }
            // Add a small delay
            await new Promise(resolve => setTimeout(resolve, 500));
        }
    }

    const outputFile = path.join(outputDir, "mdn_reference.jsonl");
    const jsonl = allDocs.map(doc => JSON.stringify(doc)).join('\n');

    fs.writeFileSync(outputFile, jsonl, 'utf8');

    console.log(`\n✅ Successfully collected ${allDocs.length} MDN articles.`);
    console.log(`📁 Data saved to: ${outputFile}`);
}

main();
