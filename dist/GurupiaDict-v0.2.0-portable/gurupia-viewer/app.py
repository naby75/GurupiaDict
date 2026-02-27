#!/usr/bin/env python3
"""
GurupiaDict Web Viewer
Flask-based web interface for browsing the knowledge graph
"""

import argparse
import os
import sys
import webbrowser
from pathlib import Path
from flask import Flask, current_app, jsonify, render_template_string, request, send_from_directory
import sqlite3
from typing import Dict, List, Optional

# Add synthesizer to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'gurupia-synthesizer'))
from query import GurupiaQuery

app = Flask(__name__, static_folder='static')


@app.route('/')
def index():
    """Serve the main HTML page"""
    with open(Path(__file__).parent / 'static' / 'index.html', 'r', encoding='utf-8') as f:
        return f.read()


# #13: 중복 /static/<path> 라우트 제거 — Flask가 static_folder='static' 설정으로 자동 서빙


@app.route('/api/search')
def api_search():
    """Search for articles by title"""
    query = request.args.get('q', '')
    limit = request.args.get('limit', 20, type=int)
    
    if not query:
        return jsonify({'results': []})
    
    try:
        with GurupiaQuery(current_app.config['DB_PATH']) as gq:
            results = gq.search_titles(query, limit)
            return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/article/<path:title>')
def api_article(title):
    """Get article by title"""
    try:
        with GurupiaQuery(current_app.config['DB_PATH']) as gq:
            article = gq.get_article(title)
            
            if not article:
                return jsonify({'error': 'Article not found'}), 404
            
            # Get outgoing links and backlinks
            outgoing = gq.get_outgoing_links(title)
            backlinks = gq.get_backlinks(title, limit=50)
            
            return jsonify({
                'article': dict(article),
                'outgoing_links': outgoing,
                'backlinks': backlinks
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats')
def api_stats():
    """Get database statistics"""
    try:
        with GurupiaQuery(current_app.config['DB_PATH']) as gq:
            stats = gq.get_statistics()
            return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/audio/<path:title>')
def api_audio(title):
    """Get TTS audio file if available"""
    try:
        # Create safe filename
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_title = safe_title[:100]
        
        audio_path = Path(__file__).parent / 'audio' / f"{safe_title}.mp3"
        
        if audio_path.exists():
            return send_from_directory(
                Path(__file__).parent / 'audio',
                f"{safe_title}.mp3",
                mimetype='audio/mpeg'
            )
        else:
            return jsonify({'error': 'Audio file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/random')
def api_random():
    """Get a random article (#2: GurupiaQuery 사용으로 통일)"""
    try:
        with GurupiaQuery(current_app.config['DB_PATH']) as gq:
            title = gq.get_random_title()
            if title:
                return jsonify({'title': title})
            else:
                return jsonify({'error': 'No articles found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def main():
    parser = argparse.ArgumentParser(
        description='GurupiaDict Web Viewer - Browse your knowledge graph in a web browser'
    )
    parser.add_argument('database', help='Path to GurupiaDict SQLite database')
    parser.add_argument('--port', type=int, default=5000, help='Port to run server on (default: 5000)')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to (default: 127.0.0.1)')
    parser.add_argument('--no-browser', action='store_true', help='Don\'t open browser automatically')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    
    args = parser.parse_args()
    
    # Validate database
    if not Path(args.database).exists():
        print(f"❌ Database not found: {args.database}")
        sys.exit(1)
    
    # #2: app.config에 DB 경로 저장 (전역 변수 대신)
    app.config['DB_PATH'] = args.database
    
    print("\n" + "="*60)
    print("🌐 GurupiaDict Web Viewer")
    print("="*60)
    print(f"📁 Database: {args.database}")
    print(f"🌍 URL: http://{args.host}:{args.port}")
    print("="*60)
    print("\n💡 Press Ctrl+C to stop the server\n")
    
    # Open browser
    if not args.no_browser:
        url = f"http://{args.host}:{args.port}"
        print(f"🚀 Opening browser to {url}...\n")
        webbrowser.open(url)
    
    # Run server
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
