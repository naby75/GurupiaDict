// GurupiaDict Web Viewer - Frontend JavaScript

class GurupiaViewer {
    constructor() {
        this.currentArticle = null;
        this.searchTimeout = null;
        this.history = [];
        this.historyIndex = -1;

        // TTS
        this.tts = null;
        this.ttsUtterance = null;
        this.ttsVoices = [];
        this.currentAudio = null;  // For MP3 playback

        this.init();
    }

    init() {
        this.bindEvents();
        this.loadStats();
        this.setupKeyboardShortcuts();
        this.initTTS();
    }

    bindEvents() {
        // Search input
        const searchInput = document.getElementById('searchInput');
        searchInput.addEventListener('input', (e) => this.handleSearch(e.target.value));
        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                this.selectFirstResult();
            }
        });

        // Random button
        document.getElementById('randomBtn').addEventListener('click', () => this.loadRandomArticle());

        // Web search button
        document.getElementById('webSearchBtn').addEventListener('click', () => this.webSearch());

        // Dark mode toggle (currently always dark, but ready for future)
        // Dark mode toggle (#10: 라이트 모드 구현)
        document.getElementById('darkModeToggle').addEventListener('click', () => {
            document.body.classList.toggle('light-mode');
            const isLight = document.body.classList.contains('light-mode');
            localStorage.setItem('theme', isLight ? 'light' : 'dark');
        });

        // 저장된 테마 복원
        if (localStorage.getItem('theme') === 'light') {
            document.body.classList.add('light-mode');
        }

        // Handle browser back/forward
        window.addEventListener('popstate', (e) => {
            if (e.state && e.state.article) {
                this.loadArticle(e.state.article, false);
            }
        });
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl+K or / for search focus
            if ((e.ctrlKey && e.key === 'k') || e.key === '/') {
                e.preventDefault();
                document.getElementById('searchInput').focus();
            }

            // Ctrl+R for random
            if (e.ctrlKey && e.key === 'r') {
                e.preventDefault();
                this.loadRandomArticle();
            }
        });
    }

    async handleSearch(query) {
        clearTimeout(this.searchTimeout);

        if (!query.trim()) {
            this.showWelcomeMessage();
            return;
        }

        this.searchTimeout = setTimeout(async () => {
            try {
                const response = await fetch(`/api/search?q=${encodeURIComponent(query)}&limit=20`);
                const data = await response.json();

                this.displaySearchResults(data.results);
            } catch (error) {
                console.error('Search error:', error);
                this.showError('검색 중 오류가 발생했습니다.');
            }
        }, 300); // Debounce 300ms
    }

    displaySearchResults(results) {
        const container = document.getElementById('searchResults').querySelector('.sidebar-content');

        if (results.length === 0) {
            container.innerHTML = '<div class="welcome-message"><p>검색 결과가 없습니다</p></div>';
            return;
        }

        container.innerHTML = results.map(result => `
            <div class="search-result-item" data-title="${this.escapeHtml(result.title)}">
                <span class="result-icon">${this.getIconForTitle(result.title)}</span>
                ${this.escapeHtml(result.title)}
            </div>
        `).join('');

        // Add click handlers
        container.querySelectorAll('.search-result-item').forEach(item => {
            item.addEventListener('click', () => {
                this.loadArticle(item.dataset.title);
            });
        });
    }

    getIconForTitle(title) {
        const lowerTitle = title.toLowerCase();
        if (lowerTitle.startsWith('python:')) return '🐍';
        if (lowerTitle.startsWith('win32:')) return '🪟';
        if (lowerTitle.startsWith('js:') || lowerTitle.startsWith('javascript:')) return '📜';
        if (lowerTitle.startsWith('css:')) return '🎨';
        if (lowerTitle.startsWith('html:')) return '🌐';
        if (lowerTitle.startsWith('react:')) return '⚛️';
        if (lowerTitle.startsWith('rust:')) return '🦀';
        if (lowerTitle.startsWith('csharp:')) return '🎯';
        if (lowerTitle.startsWith('so:')) return '💬';
        return '📖'; // Default for Wiki
    }

    showWelcomeMessage() {
        const container = document.getElementById('searchResults').querySelector('.sidebar-content');
        container.innerHTML = `
            <div class="welcome-message">
                <p>🔍 검색어를 입력하여 문서를 찾아보세요</p>
                <p class="hint">또는 🎲 버튼으로 랜덤 문서를 탐색하세요!</p>
            </div>
        `;
    }

    async loadArticle(title, addToHistory = true) {
        this.showLoading(true);

        try {
            const response = await fetch(`/api/article/${encodeURIComponent(title)}`);
            const data = await response.json();

            if (data.error) {
                this.showError(data.error);
                return;
            }

            this.currentArticle = data;
            this.displayArticle(data);
            this.displayLinks(data);

            // Update history
            if (addToHistory) {
                window.history.pushState({ article: title }, '', `#${encodeURIComponent(title)}`);
            }

        } catch (error) {
            console.error('Article load error:', error);
            this.showError('문서를 불러오는 중 오류가 발생했습니다.');
        } finally {
            this.showLoading(false);
        }
    }

    displayArticle(data) {
        const container = document.getElementById('articleContent');
        const article = data.article;
        const icon = this.getIconForTitle(article.title);

        container.innerHTML = `
            <div class="article-header">
                <h1 class="article-title">
                    <span class="article-icon">${icon}</span>
                    ${this.escapeHtml(article.title)}
                </h1>
                <div class="article-meta">
                    ${article.created_at ? `등록일: ${new Date(article.created_at).toLocaleDateString('ko-KR')}` : ''}
                </div>
            </div>
            <div class="article-body">
                ${this.processHtml(article.html_content)}
            </div>
        `;

        // Highlight code blocks
        container.querySelectorAll('pre code').forEach((el) => {
            if (window.hljs) hljs.highlightElement(el);
        });

        // Add copy buttons to code blocks
        this.addCodeCopyButtons(container);

        // Add click handlers to dict:// links
        container.querySelectorAll('a.dict-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const href = link.getAttribute('href');
                if (href.startsWith('dict://')) {
                    const title = decodeURIComponent(href.substring(7));
                    this.loadArticle(title);
                }
            });
        });
    }

    addCodeCopyButtons(container) {
        const preBlocks = container.querySelectorAll('pre');
        preBlocks.forEach(pre => {
            const button = document.createElement('button');
            button.className = 'copy-btn';
            button.textContent = '📋 Copy';

            button.addEventListener('click', () => {
                const code = pre.querySelector('code');
                const text = code ? code.textContent : pre.textContent;

                navigator.clipboard.writeText(text).then(() => {
                    button.textContent = '✅ Copied!';
                    button.classList.add('copied');
                    setTimeout(() => {
                        button.textContent = '📋 Copy';
                        button.classList.remove('copied');
                    }, 2000);
                });
            });

            pre.appendChild(button);
        });
    }

    displayLinks(data) {
        const container = document.getElementById('linksPanel').querySelector('.sidebar-content');

        const outgoingHtml = data.outgoing_links.length > 0 ? `
            <div class="links-section">
                <h3>📚 참조 문서 (${data.outgoing_links.length})</h3>
                <ul class="link-list">
                    ${data.outgoing_links.slice(0, 20).map(link => `
                        <li class="link-item" data-title="${this.escapeHtml(link)}">
                            ${this.escapeHtml(link)}
                        </li>
                    `).join('')}
                    ${data.outgoing_links.length > 20 ?
                `<li class="link-item" style="color: var(--text-muted)">... 외 ${data.outgoing_links.length - 20}개</li>` : ''}
                </ul>
            </div>
        ` : '';

        const backlinksHtml = data.backlinks.length > 0 ? `
            <div class="links-section">
                <h3>🔗 역참조 문서 (${data.backlinks.length})</h3>
                <ul class="link-list">
                    ${data.backlinks.slice(0, 20).map(link => `
                        <li class="link-item backlink-item" data-title="${this.escapeHtml(link)}">
                            ${this.escapeHtml(link)}
                        </li>
                    `).join('')}
                    ${data.backlinks.length > 20 ?
                `<li class="link-item" style="color: var(--text-muted)">... 외 ${data.backlinks.length - 20}개</li>` : ''}
                </ul>
            </div>
        ` : '';

        if (outgoingHtml || backlinksHtml) {
            container.innerHTML = outgoingHtml + backlinksHtml;

            // Add click handlers
            container.querySelectorAll('.link-item[data-title]').forEach(item => {
                item.addEventListener('click', () => {
                    this.loadArticle(item.dataset.title);
                    // Scroll article to top
                    document.getElementById('articleContent').scrollTop = 0;
                });
            });
        } else {
            container.innerHTML = '<div class="info-message"><p>연결된 문서가 없습니다</p></div>';
        }
    }

    async loadRandomArticle() {
        this.showLoading(true);

        try {
            const response = await fetch('/api/random');
            const data = await response.json();

            if (data.title) {
                await this.loadArticle(data.title);
            }
        } catch (error) {
            console.error('Random article error:', error);
            this.showError('랜덤 문서를 불러오는 중 오류가 발생했습니다.');
        } finally {
            this.showLoading(false);
        }
    }

    webSearch() {
        let query = '';

        if (this.currentArticle) {
            // Use current article title
            query = this.currentArticle.article.title;
        } else {
            // Use search input
            query = document.getElementById('searchInput').value;
        }

        if (query) {
            const url = `https://www.google.com/search?q=${encodeURIComponent(query)}`;
            window.open(url, '_blank');
        } else {
            alert('검색어를 입력하거나 문서를 선택해주세요.');
        }
    }

    async loadStats() {
        try {
            const response = await fetch('/api/stats');
            const data = await response.json();

            document.getElementById('totalArticles').textContent =
                `문서: ${data.total_nodes?.toLocaleString() || '-'}`;
            document.getElementById('totalLinks').textContent =
                `링크: ${data.total_edges?.toLocaleString() || '-'}`;
        } catch (error) {
            console.error('Stats error:', error);
        }
    }

    selectFirstResult() {
        const firstResult = document.querySelector('.search-result-item');
        if (firstResult) {
            firstResult.click();
        }
    }

    processHtml(html) {
        // #8: DOMPurify로 XSS 방어
        if (typeof DOMPurify !== 'undefined') {
            return DOMPurify.sanitize(html, {
                ALLOWED_TAGS: ['p', 'br', 'a', 'strong', 'em', 'code', 'pre', 'mark',
                    'h1', 'h2', 'h3', 'h4', 'ul', 'ol', 'li', 'table',
                    'tr', 'td', 'th', 'thead', 'tbody', 'span', 'div', 'img'],
                ALLOWED_ATTR: ['href', 'class', 'src', 'alt', 'title']
            });
        }
        return html;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    showLoading(show) {
        document.getElementById('loadingOverlay').style.display = show ? 'flex' : 'none';
    }

    showError(message) {
        const container = document.getElementById('articleContent');
        container.innerHTML = `
            <div class="welcome-screen">
                <div style="font-size: 4rem;">❌</div>
                <h2>오류 발생</h2>
                <p class="welcome-description">${this.escapeHtml(message)}</p>
            </div>
        `;
    }

    initTTS() {
        if ('speechSynthesis' in window) {
            this.tts = window.speechSynthesis;

            // Load voices
            const loadVoices = () => {
                this.ttsVoices = this.tts.getVoices();
                const voiceSelect = document.getElementById('ttsVoice');
                if (!voiceSelect) return;

                voiceSelect.innerHTML = '';

                // Filter Korean voices
                const koreanVoices = this.ttsVoices.filter(v => v.lang.startsWith('ko'));

                koreanVoices.forEach(voice => {
                    const option = document.createElement('option');
                    option.value = voice.name;
                    option.textContent = `${voice.name}`;
                    voiceSelect.appendChild(option);
                });
            };

            loadVoices();
            if (this.tts.onvoiceschanged !== undefined) {
                this.tts.onvoiceschanged = loadVoices;
            }

            // Bind TTS controls
            const playBtn = document.getElementById('ttsPlayBtn');
            const pauseBtn = document.getElementById('ttsPauseBtn');
            const resumeBtn = document.getElementById('ttsResumeBtn');
            const stopBtn = document.getElementById('ttsStopBtn');

            if (playBtn) playBtn.addEventListener('click', () => this.playTTS());
            if (pauseBtn) pauseBtn.addEventListener('click', () => this.pauseTTS());
            if (resumeBtn) resumeBtn.addEventListener('click', () => this.resumeTTS());
            if (stopBtn) stopBtn.addEventListener('click', () => this.stopTTS());
        }
    }

    async playTTS() {
        if (!this.currentArticle) {
            alert('문서를 먼저 선택해주세요.');
            return;
        }

        const playBtn = document.getElementById('ttsPlayBtn');
        playBtn.textContent = '⏳ 로딩중...';
        playBtn.disabled = true;

        this.stopTTS();

        const title = this.currentArticle.article.title;

        // Check for pre-generated MP3 file first
        try {
            const response = await fetch(`/api/audio/${encodeURIComponent(title)}`);

            if (response.ok) {
                // MP3 file exists! Play it
                console.log('✅ Found pre-generated MP3');
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                const audio = new Audio(url);

                audio.onplay = () => {
                    console.log('🔊 Playing MP3');
                    playBtn.textContent = '▶️ 읽기';
                    playBtn.disabled = false;
                    playBtn.style.display = 'none';
                    document.getElementById('ttsPauseBtn').style.display = 'inline-block';
                };

                audio.onended = () => {
                    console.log('✅ MP3 ended');
                    document.getElementById('ttsPlayBtn').style.display = 'inline-block';
                    document.getElementById('ttsPauseBtn').style.display = 'none';
                    URL.revokeObjectURL(url);
                };

                audio.onerror = () => {
                    console.error('❌ MP3 error');
                    playBtn.textContent = '▶️ 읽기';
                    playBtn.disabled = false;
                    URL.revokeObjectURL(url);
                };

                this.currentAudio = audio;
                audio.play();
                return;
            }
        } catch (error) {
            console.log('ℹ️ No MP3, using browser TTS');
        }

        // Fallback to browser TTS
        const text = this.currentArticle.article.raw_content || '';
        if (!text) {
            alert('읽을 내용이 없습니다.');
            playBtn.textContent = '▶️ 읽기';
            playBtn.disabled = false;
            return;
        }

        this.ttsUtterance = new SpeechSynthesisUtterance(text);

        // Set voice
        const voiceSelect = document.getElementById('ttsVoice');
        if (voiceSelect && voiceSelect.value) {
            const voiceName = voiceSelect.value;
            const voice = this.ttsVoices.find(v => v.name === voiceName);
            if (voice) this.ttsUtterance.voice = voice;
        }

        // Set speed
        const speedSelect = document.getElementById('ttsSpeed');
        if (speedSelect) {
            this.ttsUtterance.rate = parseFloat(speedSelect.value);
        }

        this.ttsUtterance.lang = 'ko-KR';

        // Event handlers
        this.ttsUtterance.onstart = () => {
            console.log('🔊 Browser TTS started');
            playBtn.textContent = '▶️ 읽기';
            playBtn.disabled = false;
            playBtn.style.display = 'none';
            document.getElementById('ttsPauseBtn').style.display = 'inline-block';
        };

        this.ttsUtterance.onend = () => {
            console.log('✅ Browser TTS ended');
            document.getElementById('ttsPlayBtn').style.display = 'inline-block';
            document.getElementById('ttsPauseBtn').style.display = 'none';
        };

        this.ttsUtterance.onerror = (e) => {
            console.error('❌ TTS error:', e);
            playBtn.textContent = '▶️ 읽기';
            playBtn.disabled = false;
            document.getElementById('ttsPlayBtn').style.display = 'inline-block';
            document.getElementById('ttsPauseBtn').style.display = 'none';
        };

        console.log('🔊 Starting browser TTS...');
        this.tts.speak(this.ttsUtterance);

        setTimeout(() => {
            if (playBtn.textContent === '⏳ 로딩중...') {
                playBtn.textContent = '▶️ 읽기';
                playBtn.disabled = false;
            }
        }, 2000);
    }

    pauseTTS() {
        if (this.currentAudio) {
            this.currentAudio.pause();
            document.getElementById('ttsPauseBtn').style.display = 'none';
            document.getElementById('ttsResumeBtn').style.display = 'inline-block';
        } else if (this.tts && this.tts.speaking && !this.tts.paused) {
            this.tts.pause();
            document.getElementById('ttsPauseBtn').style.display = 'none';
            document.getElementById('ttsResumeBtn').style.display = 'inline-block';
        }
    }

    resumeTTS() {
        if (this.currentAudio) {
            this.currentAudio.play();
            document.getElementById('ttsPauseBtn').style.display = 'inline-block';
            document.getElementById('ttsResumeBtn').style.display = 'none';
        } else if (this.tts && this.tts.paused) {
            this.tts.resume();
            document.getElementById('ttsPauseBtn').style.display = 'inline-block';
            document.getElementById('ttsResumeBtn').style.display = 'none';
        }
    }

    stopTTS() {
        if (this.currentAudio) {
            this.currentAudio.pause();
            this.currentAudio.currentTime = 0;
            this.currentAudio = null;
        }
        if (this.tts) {
            this.tts.cancel();
        }
        document.getElementById('ttsPlayBtn').style.display = 'inline-block';
        document.getElementById('ttsPauseBtn').style.display = 'none';
        document.getElementById('ttsResumeBtn').style.display = 'none';
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    const viewer = new GurupiaViewer();

    // Check for hash in URL
    const hash = window.location.hash;
    if (hash && hash.length > 1) {
        const title = decodeURIComponent(hash.substring(1));
        viewer.loadArticle(title);
    }

    // Make viewer global for debugging
    window.viewer = viewer;

    console.log('🕸️ GurupiaDict Viewer initialized!');
    console.log('⌨️  Keyboard shortcuts:');
    console.log('   Ctrl+K or / : Focus search');
    console.log('   Ctrl+R      : Random article');
});
