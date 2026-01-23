"""
GurupiaDict TTS Generator
Generate high-quality MP3 files using Google Cloud TTS
"""

import os
import sys
import json
import sqlite3
from pathlib import Path
from google.cloud import texttospeech

def generate_tts_audio(text, output_path, voice_name="ko-KR-Wavenet-A", speaking_rate=1.0):
    """Generate TTS audio using Google Cloud TTS"""
    
    # Initialize client
    client = texttospeech.TextToSpeechClient()
    
    # Set up synthesis input
    synthesis_input = texttospeech.SynthesisInput(text=text)
    
    # Set up voice parameters
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR",
        name=voice_name  # WaveNet for high quality
    )
    
    # Set up audio config
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speaking_rate
    )
    
    # Perform TTS
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    
    # Save to file
    with open(output_path, "wb") as out:
        out.write(response.audio_content)
    
    return len(text)

def generate_popular_articles(db_path, output_dir, limit=100):
    """Generate TTS for popular articles"""
    
    print(f"🎙️ GurupiaDict TTS Generator")
    print(f"📚 Database: {db_path}")
    print(f"📁 Output: {output_dir}")
    print(f"🎯 Generating top {limit} articles")
    print()
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get most referenced articles (popular ones)
    cursor.execute("""
        SELECT n.title, n.raw_content, COUNT(e.id) as ref_count
        FROM Nodes n
        LEFT JOIN Edges e ON e.target_title = n.title
        GROUP BY n.id
        ORDER BY ref_count DESC
        LIMIT ?
    """, (limit,))
    
    articles = cursor.fetchall()
    total_chars = 0
    generated = 0
    
    for i, article in enumerate(articles, 1):
        title = article['title']
        content = article['raw_content']
        ref_count = article['ref_count']
        
        # Create safe filename
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_title = safe_title[:100]  # Limit filename length
        output_path = os.path.join(output_dir, f"{safe_title}.mp3")
        
        # Skip if already exists
        if os.path.exists(output_path):
            print(f"⏭️  [{i}/{limit}] Skipped: {title} (already exists)")
            continue
        
        try:
            # Truncate content if too long (max 5000 chars for TTS)
            if len(content) > 5000:
                content = content[:5000] + "..."
            
            # Generate TTS
            chars = generate_tts_audio(content, output_path)
            total_chars += chars
            generated += 1
            
            print(f"✅ [{i}/{limit}] Generated: {title} ({chars:,} chars, {ref_count} refs)")
            
        except Exception as e:
            print(f"❌ [{i}/{limit}] Error: {title} - {e}")
    
    conn.close()
    
    print()
    print(f"📊 Summary:")
    print(f"   Generated: {generated} files")
    print(f"   Total characters: {total_chars:,}")
    print(f"   Estimated cost: ${total_chars / 1_000_000 * 16:.2f} (WaveNet)")
    print(f"   Free tier: {max(0, 1_000_000 - total_chars):,} chars remaining")
    print()
    print(f"✅ TTS generation completed!")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python tts_generator.py <database.db> [limit]")
        print("\nExample:")
        print("  python tts_generator.py GurupiaDict_Complete.db 100")
        sys.exit(1)
    
    db_path = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    output_dir = "gurupia-viewer/audio"
    
    if not Path(db_path).exists():
        print(f"❌ Database not found: {db_path}")
        sys.exit(1)
    
    # Check for Google Cloud credentials
    if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        print("⚠️  Warning: GOOGLE_APPLICATION_CREDENTIALS not set")
        print("   Please set up Google Cloud credentials first:")
        print("   1. Create a service account in Google Cloud Console")
        print("   2. Download JSON key file")
        print("   3. Set environment variable:")
        print("      $env:GOOGLE_APPLICATION_CREDENTIALS='path/to/key.json'")
        print()
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    generate_popular_articles(db_path, output_dir, limit)
