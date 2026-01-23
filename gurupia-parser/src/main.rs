use quick_xml::events::Event;
use quick_xml::Reader;
use regex::Regex;
use serde::{Deserialize, Serialize};
use std::env;
use std::fs::File;
use std::io::{BufReader, BufWriter, Write};


/// Represents a single Wikipedia article node
#[derive(Debug, Serialize, Deserialize)]
struct WikiNode {
    title: String,
    content: String,
}

/// Wikipedia page data extracted from XML
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

    println!("🦀 GurupiaDict Parser v0.1.0");
    println!("📖 Reading: {}", input_path);
    println!("📝 Writing: {}", output_path);
    println!();

    parse_wikipedia_xml(input_path, output_path)?;

    println!("\n✅ Parsing completed successfully!");
    Ok(())
}

/// Parse Wikipedia XML dump and extract main namespace articles
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
    let mut page_count = 0;
    let mut processed_count = 0;

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
                    
                    // Only process main namespace (ns=0) articles
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
                    
                    // Reset for next page
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

/// Extract and clean the first paragraph from a Wikipedia page
fn extract_wiki_node(page: &WikiPage) -> Option<WikiNode> {
    let text = &page.text;
    
    // Skip redirect pages
    if text.trim().starts_with("#REDIRECT") || text.trim().starts_with("#redirect") {
        return None;
    }
    
    // Skip disambiguation pages
    if page.title.contains("(동음이의)") || text.contains("{{동음이의}}") {
        return None;
    }

    // Extract first paragraph (before first section header)
    let first_para = extract_first_paragraph(text);
    
    if first_para.is_empty() {
        return None;
    }

    // Clean wiki markup
    let cleaned = clean_wiki_markup(&first_para);
    
    // Ensure content is between 100-1500 characters and ends with sentence
    let truncated = smart_truncate(&cleaned, 500, 1500);
    
    if truncated.len() < 100 {
        return None;
    }

    Some(WikiNode {
        title: page.title.clone(),
        content: truncated,
    })
}

/// Extract the first paragraph before any section headers
fn extract_first_paragraph(text: &str) -> String {
    // Find content before first section header (==)
    let parts: Vec<&str> = text.split("\n==").collect();
    let intro = parts[0];
    
    // Remove infoboxes and other templates at the start
    let re_infobox = Regex::new(r"(?s)\{\{[^}]*\}\}").unwrap();
    let without_templates = re_infobox.replace_all(intro, "");
    
    // Get meaningful paragraphs (skip empty lines)
    let paragraphs: Vec<&str> = without_templates
        .split("\n\n")
        .map(|p| p.trim())
        .filter(|p| !p.is_empty() && !p.starts_with("{|") && !p.starts_with("|"))
        .collect();
    
    paragraphs.join("\n\n")
}

/// Remove wiki markup noise: File links, references, HTML tags, etc.
fn clean_wiki_markup(text: &str) -> String {
    // Remove File/Image references
    let re_file = Regex::new(r"\[\[(?:File|파일|Image|그림):[^\]]*\]\]").unwrap();
    let text = re_file.replace_all(text, "");
    
    // Remove <ref>...</ref> tags
    let re_ref = Regex::new(r"<ref[^>]*>.*?</ref>").unwrap();
    let text = re_ref.replace_all(&text, "");
    
    // Remove HTML comments
    let re_comment = Regex::new(r"<!--.*?-->").unwrap();
    let text = re_comment.replace_all(&text, "");
    
    // Remove HTML tags
    let re_html = Regex::new(r"<[^>]+>").unwrap();
    let text = re_html.replace_all(&text, "");
    
    // Clean up multiple newlines
    let re_newlines = Regex::new(r"\n{3,}").unwrap();
    let text = re_newlines.replace_all(&text, "\n\n");
    
    // Clean up multiple spaces
    let re_spaces = Regex::new(r" {2,}").unwrap();
    let text = re_spaces.replace_all(&text, " ");
    
    text.trim().to_string()
}

/// Smart truncation: cut at sentence boundary within min-max range
fn smart_truncate(text: &str, min_chars: usize, max_chars: usize) -> String {
    if text.len() <= max_chars {
        return text.to_string();
    }
    
    // Find sentence ending between min and max
    let search_range = &text[min_chars..max_chars.min(text.len())];
    
    // Look for Korean or English sentence endings
    let sentence_ends = [". ", ".\n", "다.", "다!\n", "다?\n", "요.", "음.", "임."];
    
    for ending in &sentence_ends {
        if let Some(pos) = search_range.rfind(ending) {
            let cut_point = min_chars + pos + ending.len();
            return text[..cut_point].trim().to_string();
        }
    }
    
    // If no sentence boundary found, cut at max_chars
    text[..max_chars].trim().to_string()
}
