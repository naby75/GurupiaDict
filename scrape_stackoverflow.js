const fs = require('fs');
const path = require('path');

/**
 * Fetch top questions from StackOverflow for a specific tag
 */
async function fetchSOQuestions(tag, limit = 10) {
    const url = `https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&tagged=${encodeURIComponent(tag)}&site=stackoverflow&filter=withbody`;
    console.log(`🚀 Fetching Stack Overflow [${tag}]: ${url}`);

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const data = await response.json();
        const questions = data.items.slice(0, limit);

        const results = [];
        for (const q of questions) {
            // Fetch top answer for this question
            const answer = await fetchTopAnswer(q.question_id);

            let content = `# ${q.title}\n\n`;
            content += `**Tags:** ${q.tags.join(', ')}\n`;
            content += `**Votes:** ${q.score}\n\n`;
            content += `## Question\n\n${q.body}\n\n`;

            if (answer) {
                content += `## Top Answer (Votes: ${answer.score})\n\n${answer.body}\n`;
            }

            results.push({
                title: `so:${tag}:${q.title}`,
                content: content
            });

            // Wait slightly to avoid rate limiting
            await new Promise(resolve => setTimeout(resolve, 500));
        }

        return results;
    } catch (e) {
        console.error(`❌ Error fetching SO [${tag}]: ${e.message}`);
        return [];
    }
}

async function fetchTopAnswer(questionId) {
    const url = `https://api.stackexchange.com/2.3/questions/${questionId}/answers?order=desc&sort=votes&site=stackoverflow&filter=withbody`;
    try {
        const response = await fetch(url);
        if (!response.ok) return null;
        const data = await response.json();
        return data.items && data.items.length > 0 ? data.items[0] : null;
    } catch (e) {
        return null;
    }
}

async function main() {
    const tags = ['python', 'javascript', 'c#', 'rust'];
    const outputDir = path.join(process.cwd(), "so_data");
    if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir);

    const allDocs = [];

    for (const tag of tags) {
        const docs = await fetchSOQuestions(tag, 5); // 5 elite questions per tag
        allDocs.push(...docs);
    }

    const outputFile = path.join(outputDir, "stackoverflow_top.jsonl");
    const jsonl = allDocs.map(doc => JSON.stringify(doc)).join('\n');

    fs.writeFileSync(outputFile, jsonl, 'utf8');

    console.log(`\n✅ Successfully collected ${allDocs.length} Stack Overflow Q&A.`);
    console.log(`📁 Data saved to: ${outputFile}`);
}

main();
