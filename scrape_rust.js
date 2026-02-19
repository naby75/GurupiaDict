const fs = require('fs');
const path = require('path');

/**
 * Rust 표준 라이브러리 문서 크롤러 v0.2.0
 * doc.rust-lang.org에서 실제 문서를 가져와 JSONL로 변환합니다 (#1).
 * 
 * 외부 의존성: 없음 (Node.js 내장 fetch 사용, Node 18+)
 */

// 수집 대상 표준 라이브러리 타입 목록
const TARGETS = [
    // 핵심 컬렉션/스마트 포인터
    { mod: 'vec', kind: 'struct', type: 'Vec' },
    { mod: 'string', kind: 'struct', type: 'String' },
    { mod: 'collections', kind: 'struct', type: 'HashMap' },
    { mod: 'collections', kind: 'struct', type: 'BTreeMap' },
    { mod: 'collections', kind: 'struct', type: 'HashSet' },
    { mod: 'collections', kind: 'struct', type: 'VecDeque' },
    { mod: 'boxed', kind: 'struct', type: 'Box' },
    { mod: 'rc', kind: 'struct', type: 'Rc' },
    { mod: 'sync', kind: 'struct', type: 'Arc' },
    { mod: 'sync', kind: 'struct', type: 'Mutex' },
    { mod: 'cell', kind: 'struct', type: 'RefCell' },
    // 핵심 열거형
    { mod: 'option', kind: 'enum', type: 'Option' },
    { mod: 'result', kind: 'enum', type: 'Result' },
    // I/O & 파일
    { mod: 'fs', kind: 'struct', type: 'File' },
    { mod: 'io', kind: 'trait', type: 'Read' },
    { mod: 'io', kind: 'trait', type: 'Write' },
    { mod: 'io', kind: 'struct', type: 'BufReader' },
    { mod: 'io', kind: 'struct', type: 'BufWriter' },
    { mod: 'path', kind: 'struct', type: 'PathBuf' },
    { mod: 'path', kind: 'struct', type: 'Path' },
    // 동시성
    { mod: 'thread', kind: 'fn', type: 'spawn' },
    { mod: 'sync/mpsc', kind: 'fn', type: 'channel' },
    // 트레이트
    { mod: 'iter', kind: 'trait', type: 'Iterator' },
    { mod: 'fmt', kind: 'trait', type: 'Display' },
    { mod: 'clone', kind: 'trait', type: 'Clone' },
    { mod: 'convert', kind: 'trait', type: 'From' },
];

/**
 * doc.rust-lang.org에서 HTML을 가져와 핵심 설명을 파싱합니다.
 */
async function fetchRustDoc(entry) {
    const { mod: moduleName, kind, type: typeName } = entry;
    const url = `https://doc.rust-lang.org/std/${moduleName}/${kind}.${typeName}.html`;
    console.log(`🚀 Fetching: ${url}`);

    try {
        const response = await fetch(url, {
            headers: { 'User-Agent': 'GurupiaDict-Crawler/0.2' }
        });

        if (!response.ok) {
            console.warn(`   ⚠️  HTTP ${response.status} — ${typeName}`);
            return null;
        }

        const html = await response.text();

        // <title> 추출
        const titleMatch = html.match(/<title>([^<]+)<\/title>/);
        const pageTitle = titleMatch ? titleMatch[1].replace(' - Rust', '').trim() : `std::${moduleName}::${typeName}`;

        // 핵심 설명 추출: docblock 영역에서 첫 번째 단락들 가져오기
        const content = extractDocContent(html, moduleName, typeName);

        if (!content || content.length < 50) {
            console.warn(`   ⚠️  Content too short for ${typeName}`);
            return null;
        }

        console.log(`   ✅ ${typeName}: ${content.length} chars`);
        return {
            title: `rust:${pageTitle}`,
            content: content
        };
    } catch (error) {
        console.error(`   ❌ Error fetching ${typeName}:`, error.message);
        return null;
    }
}

/**
 * Rust 문서 HTML에서 핵심 설명 텍스트를 추출합니다.
 * <div class="docblock"> 내의 텍스트를 마크다운 형태로 변환합니다.
 */
function extractDocContent(html, moduleName, typeName) {
    // docblock 영역 추출 (첫 번째 docblock = 타입 설명)
    const docblockMatch = html.match(/<div class="docblock"[^>]*>([\s\S]*?)<\/div>/);
    if (!docblockMatch) return null;

    let content = docblockMatch[1];

    // HTML → 텍스트 변환
    content = content
        // 코드 블록 보존
        .replace(/<pre[^>]*><code[^>]*>([\s\S]*?)<\/code><\/pre>/g, '\n```rust\n$1\n```\n')
        // 인라인 코드
        .replace(/<code>(.*?)<\/code>/g, '`$1`')
        // 링크 → 텍스트
        .replace(/<a[^>]*>(.*?)<\/a>/g, '$1')
        // 강조
        .replace(/<strong>(.*?)<\/strong>/g, '**$1**')
        .replace(/<em>(.*?)<\/em>/g, '*$1*')
        // 단락
        .replace(/<\/p>/g, '\n\n')
        .replace(/<p[^>]*>/g, '')
        // HTML 엔티티
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>')
        .replace(/&amp;/g, '&')
        .replace(/&quot;/g, '"')
        .replace(/&#39;/g, "'")
        // 나머지 HTML 태그 제거
        .replace(/<[^>]+>/g, '')
        // 연속 개행 정리
        .replace(/\n{3,}/g, '\n\n')
        .trim();

    // 헤더 추가
    const header = `# std::${moduleName}::${typeName}\n\n**Crate:** std\n**Module:** ${moduleName}\n\n`;

    // 최대 2000자로 제한 (문장 경계)
    if (content.length > 2000) {
        const cutPoint = content.lastIndexOf('.', 2000);
        content = cutPoint > 500 ? content.substring(0, cutPoint + 1) + '\n\n...' : content.substring(0, 2000);
    }

    return header + content;
}

/**
 * 메인: 모든 대상을 순차 크롤링 후 JSONL로 저장합니다.
 * Rate limit 준수를 위해 요청 간 500ms 딜레이를 적용합니다.
 */
async function main() {
    console.log('🦀 GurupiaDict Rust Scraper v0.2.0');
    console.log(`📋 Targets: ${TARGETS.length} types\n`);

    const outputDir = path.join(process.cwd(), "rust_data");
    if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

    const allDocs = [];
    for (const target of TARGETS) {
        const doc = await fetchRustDoc(target);
        if (doc) allDocs.push(doc);

        // Rate limit: 500ms 딜레이
        await new Promise(resolve => setTimeout(resolve, 500));
    }

    const outputFile = path.join(outputDir, "rust_reference.jsonl");
    const jsonl = allDocs.map(doc => JSON.stringify(doc)).join('\n');
    fs.writeFileSync(outputFile, jsonl + '\n', 'utf8');

    console.log(`\n✅ Successfully created ${allDocs.length}/${TARGETS.length} Rust reference documents.`);
    console.log(`📁 Data saved to: ${outputFile}`);
}

main().catch(console.error);
