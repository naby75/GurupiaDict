use quick_xml::events::Event;
use quick_xml::Reader;
use regex::Regex;
use serde::{Deserialize, Serialize};
use std::env;
use std::fs::File;
use std::io::{BufReader, BufWriter, Write};
use std::sync::LazyLock;

// ── 정규식 캐싱: 매 호출마다 재컴파일 방지 (#3) ──

/// 인포박스/템플릿 제거용
static RE_INFOBOX: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r"(?s)\{\{[^}]*\}\}").unwrap());

/// File/Image 링크 제거용
static RE_FILE: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r"\[\[(?:File|파일|Image|그림):[^\]]*\]\]").unwrap());

/// <ref>...</ref> 태그 제거용
static RE_REF: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r"<ref[^>]*>.*?</ref>").unwrap());

/// HTML 주석 제거용
static RE_COMMENT: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r"<!--.*?-->").unwrap());

/// HTML 태그 제거용
static RE_HTML: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r"<[^>]+>").unwrap());

/// 연속 개행 정리용
static RE_NEWLINES: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r"\n{3,}").unwrap());

/// 연속 공백 정리용
static RE_SPACES: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r" {2,}").unwrap());


/// 단일 위키백과 문서 노드를 표현
#[derive(Debug, Serialize, Deserialize)]
struct WikiNode {
    title: String,
    content: String,
}

/// XML에서 추출된 위키백과 페이지 데이터
#[derive(Debug, Default)]
struct WikiPage {
    title: String,
    ns: String,
    text: String,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 3 {
        eprintln!("Usage: {} <input.xml> <output.jsonl>", args[0]);
        eprintln!("\nExample:");
        eprintln!("  {} kowiki-latest-pages-articles.xml gurupia_nodes.jsonl", args[0]);
        std::process::exit(1);
    }

    let input_path = &args[1];
    let output_path = &args[2];

    println!("🦀 GurupiaDict Parser v0.2.0");
    println!("📖 Reading: {}", input_path);
    println!("📝 Writing: {}", output_path);
    println!();

    parse_wikipedia_xml(input_path, output_path)?;

    println!("\n✅ Parsing completed successfully!");
    Ok(())
}

/// 위키백과 XML 덤프를 파싱하여 메인 네임스페이스(ns=0) 문서만 추출
fn parse_wikipedia_xml(input_path: &str, output_path: &str) -> Result<(), Box<dyn std::error::Error>> {
    let file = File::open(input_path)?;
    let _file_size = file.metadata()?.len();
    let buf_reader = BufReader::new(file);
    
    let mut reader = Reader::from_reader(buf_reader);
    reader.config_mut().trim_text(true);

    let output_file = File::create(output_path)?;
    let mut writer = BufWriter::new(output_file);

    let mut buf = Vec::new();
    let mut current_page = WikiPage::default();
    let mut current_tag = String::new();
    let mut page_count = 0u64;
    let mut processed_count = 0u64;

    loop {
        match reader.read_event_into(&mut buf) {
            Ok(Event::Start(ref e)) => {
                current_tag = String::from_utf8_lossy(e.name().as_ref()).to_string();
            }
            Ok(Event::Text(e)) => {
                let text = e.unescape()?.to_string();
                
                match current_tag.as_str() {
                    "title" => current_page.title = text,
                    "ns" => current_page.ns = text,
                    "text" => current_page.text = text,
                    _ => {}
                }
            }
            Ok(Event::End(ref e)) => {
                let tag_name = String::from_utf8_lossy(e.name().as_ref()).to_string();
                
                if tag_name == "page" {
                    page_count += 1;
                    
                    // 메인 네임스페이스(ns=0) 문서만 처리
                    if current_page.ns == "0" && !current_page.title.is_empty() {
                        if let Some(node) = extract_wiki_node(&current_page) {
                            let json = serde_json::to_string(&node)?;
                            writeln!(writer, "{}", json)?;
                            processed_count += 1;
                            
                            if processed_count % 1000 == 0 {
                                print!("\r📊 Processed: {} articles (Total pages: {})", 
                                       processed_count, page_count);
                                std::io::stdout().flush()?;
                            }
                        }
                    }
                    
                    // 다음 페이지를 위해 초기화
                    current_page = WikiPage::default();
                }
            }
            Ok(Event::Eof) => break,
            Err(e) => {
                eprintln!("Error at position {}: {:?}", reader.buffer_position(), e);
                break;
            }
            _ => {}
        }
        buf.clear();
    }

    writer.flush()?;
    println!("\n📈 Final Stats:");
    println!("   Total pages scanned: {}", page_count);
    println!("   Main namespace articles extracted: {}", processed_count);

    Ok(())
}

/// 위키 페이지에서 첫 문단을 추출하고 정제
fn extract_wiki_node(page: &WikiPage) -> Option<WikiNode> {
    let text = &page.text;
    
    // 리디렉트 페이지 건너뛰기 (#11: 한국어 '#넘겨주기' 포함)
    let trimmed = text.trim();
    if trimmed.starts_with("#REDIRECT")
        || trimmed.starts_with("#redirect")
        || trimmed.starts_with("#넘겨주기")
    {
        return None;
    }
    
    // 동음이의어 페이지 건너뛰기
    if page.title.contains("(동음이의)") || text.contains("{{동음이의}}") {
        return None;
    }

    // 첫 문단 추출 (첫 번째 섹션 헤더 이전)
    let first_para = extract_first_paragraph(text);
    
    if first_para.is_empty() {
        return None;
    }

    // 위키 마크업 정리
    let cleaned = clean_wiki_markup(&first_para);
    
    // 콘텐츠 길이 제한: 100-1500자 범위, 문장 경계에서 절단
    let truncated = smart_truncate(&cleaned, 500, 1500);
    
    // UTF-8 char 기반 길이 검증 (#4)
    if truncated.chars().count() < 100 {
        return None;
    }

    Some(WikiNode {
        title: page.title.clone(),
        content: truncated,
    })
}

/// 첫 번째 섹션 헤더(==) 이전의 도입부를 추출
fn extract_first_paragraph(text: &str) -> String {
    // 첫 번째 섹션 헤더 이전 영역 추출
    let parts: Vec<&str> = text.split("\n==").collect();
    let intro = parts[0];
    
    // 인포박스 및 템플릿 제거 (캐싱된 정규식 사용)
    let without_templates = RE_INFOBOX.replace_all(intro, "");
    
    // 의미 있는 문단만 선별 (빈 줄, 테이블 마크업 제외)
    let paragraphs: Vec<&str> = without_templates
        .split("\n\n")
        .map(|p| p.trim())
        .filter(|p| !p.is_empty() && !p.starts_with("{|") && !p.starts_with("|"))
        .collect();
    
    paragraphs.join("\n\n")
}

/// 위키 마크업 노이즈 제거: File 링크, 참조, HTML 태그 등
fn clean_wiki_markup(text: &str) -> String {
    // 모든 정규식은 LazyLock으로 캐싱됨 (#3)
    let text = RE_FILE.replace_all(text, "");
    let text = RE_REF.replace_all(&text, "");
    let text = RE_COMMENT.replace_all(&text, "");
    let text = RE_HTML.replace_all(&text, "");
    let text = RE_NEWLINES.replace_all(&text, "\n\n");
    let text = RE_SPACES.replace_all(&text, " ");
    
    text.trim().to_string()
}

/// UTF-8 안전 스마트 절단: min~max 범위에서 문장 경계로 절단 (#4)
fn smart_truncate(text: &str, min_chars: usize, max_chars: usize) -> String {
    let char_count = text.chars().count();
    if char_count <= max_chars {
        return text.to_string();
    }
    
    // char 인덱스를 바이트 인덱스로 안전하게 변환
    let min_byte = text.char_indices()
        .nth(min_chars)
        .map(|(i, _)| i)
        .unwrap_or(0);
    let max_byte = text.char_indices()
        .nth(max_chars)
        .map(|(i, _)| i)
        .unwrap_or(text.len());
    
    let search_range = &text[min_byte..max_byte];
    
    // 한국어/영어 문장 종결 패턴
    let sentence_ends = [". ", ".\n", "다.", "다!\n", "다?\n", "요.", "음.", "임."];
    
    for ending in &sentence_ends {
        if let Some(pos) = search_range.rfind(ending) {
            let cut_point = min_byte + pos + ending.len();
            return text[..cut_point].trim().to_string();
        }
    }
    
    // 문장 경계를 찾지 못하면 max_byte 위치에서 절단
    text[..max_byte].trim().to_string()
}
