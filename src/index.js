/**
 * find-lec - Gruvbox Edition Front End Logic
 * Contains light micro-interactions to make the page alive & dynamic
 * Fully integrated with Flask backend search functionality.
 */

document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('lecturerSearch');
    const searchButton = document.getElementById('searchButton');
    const statusEmoticon = document.getElementById('statusEmoticon');
    const statusText = document.getElementById('statusText');
    const searchForm = document.getElementById('searchForm');
    const resultsContainer = document.getElementById('resultsContainer');

    // Emoticon states for rich responsive interactivity
    const EMOTICONS = {
        idle: '┐(‘～` )┌',
        focused: '(o_O) 🔍',
        typing: '(•̀ᴗ•́)و 🌟',
        searching: '(⌐■_■)',
        buttonHover: '(* ^ ω ^) ⚡'
    };

    const STATUS_TEXTS = {
        idle: 'Ready to seek knowledge...',
        focused: 'Awaiting lecturer query...',
        typing: 'Looking for matching wisdom...',
        searching: 'Button clicked. Static state active.',
        buttonHover: 'Click to feel the lightning!'
    };

    // 1. Input Focus state changes
    searchInput.addEventListener('focus', () => {
        if (!searchInput.value.trim()) {
            updateStatus(EMOTICONS.focused, STATUS_TEXTS.focused);
        }
    });

    // 2. Input typing states
    searchInput.addEventListener('input', () => {
        const val = searchInput.value.trim();
        if (val.length > 0) {
            updateStatus(EMOTICONS.typing, `Targeting: "${val}"`);
        } else {
            updateStatus(EMOTICONS.focused, STATUS_TEXTS.focused);
            resultsContainer.innerHTML = ''; // Clear results if query is empty
        }
    });

    // 3. Input blur state reset
    searchInput.addEventListener('blur', () => {
        if (!searchInput.value.trim()) {
            updateStatus(EMOTICONS.idle, STATUS_TEXTS.idle);
        }
    });

    // 4. Search button hover effects
    searchButton.addEventListener('mouseenter', () => {
        updateStatus(EMOTICONS.buttonHover, STATUS_TEXTS.buttonHover);
    });

    searchButton.addEventListener('mouseleave', () => {
        const val = searchInput.value.trim();
        if (document.activeElement === searchInput) {
            if (val) {
                updateStatus(EMOTICONS.typing, `Targeting: "${val}"`);
            } else {
                updateStatus(EMOTICONS.focused, STATUS_TEXTS.focused);
            }
        } else {
            updateStatus(EMOTICONS.idle, STATUS_TEXTS.idle);
        }
    });

    // Helper to escape HTML to prevent XSS
    function escapeHTML(str) {
        return str.replace(/[&<>'"]/g, 
            tag => ({
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                "'": '&#39;',
                '"': '&quot;'
            }[tag] || tag)
        );
    }

    // 5. Backend Search Functionality
    const performSearch = async () => {
        const query = searchInput.value.trim();
        if (!query) {
            updateStatus(EMOTICONS.focused, STATUS_TEXTS.focused);
            resultsContainer.innerHTML = '';
            return;
        }

        // Show searching state
        updateStatus(EMOTICONS.searching, 'Seeking records in database...');
        resultsContainer.innerHTML = '';

        try {
            const hostUrl = (window.location.protocol === 'file:' || window.location.port !== '5000') 
                ? `${window.location.protocol === 'https:' ? 'https' : 'http'}://${window.location.hostname || '127.0.0.1'}:5000` 
                : '';
            const response = await fetch(`${hostUrl}/search?name=${encodeURIComponent(query)}`);
            if (!response.ok) {
                throw new Error('Server returned an error');
            }
            const data = await response.json();

            if (data.error) {
                throw new Error(data.error);
            }

            if (data.length === 0) {
                updateStatus('┐(￣ヘ￣)┌', `No matching lecturers found for "${query}"`);
                resultsContainer.innerHTML = `
                    <div class="result-card" style="border-color: var(--gruv-red); text-align: center;">
                        <span style="font-family: 'JetBrains Mono', monospace; color: var(--gruv-red); font-size: 0.9rem;">
                            No matching records found.
                        </span>
                    </div>
                `;
            } else {
                updateStatus('(っ◕‿◕)っ', `Found ${data.length} match${data.length > 1 ? 'es' : ''}!`);
                
                // Render beautiful results cards dynamically
                data.forEach((lec, index) => {
                    const card = document.createElement('div');
                    card.className = 'result-card';
                    card.style.animationDelay = `${index * 0.08}s`;
                    
                    const hasPhone = lec.phone && lec.phone.trim() !== '';
                    const phoneText = hasPhone ? lec.phone : 'No contact details';
                    const phoneClass = hasPhone ? 'result-phone' : 'result-phone empty';
                    
                    card.innerHTML = `
                        <div class="result-header">
                            <span class="result-name">${escapeHTML(lec.name)}</span>
                            <span class="result-badge">Lec</span>
                        </div>
                        <div class="result-body">
                            <span class="${phoneClass}">${escapeHTML(phoneText)}</span>
                            ${hasPhone ? `
                                <button class="copy-btn" data-phone="${escapeHTML(lec.phone)}">
                                    <span class="copy-icon">📋</span>
                                    <span class="copy-text">Copy</span>
                                </button>
                            ` : ''}
                        </div>
                    `;

                    // Clip-to-clipboard functionality
                    if (hasPhone) {
                        const copyBtn = card.querySelector('.copy-btn');
                        copyBtn.addEventListener('click', (e) => {
                            e.stopPropagation();
                            navigator.clipboard.writeText(lec.phone).then(() => {
                                const copyIcon = copyBtn.querySelector('.copy-icon');
                                const copyText = copyBtn.querySelector('.copy-text');
                                copyIcon.textContent = '✅';
                                copyText.textContent = 'Copied!';
                                copyBtn.style.backgroundColor = 'var(--gruv-green)';
                                copyBtn.style.color = 'var(--bg-darker)';
                                
                                setTimeout(() => {
                                    copyIcon.textContent = '📋';
                                    copyText.textContent = 'Copy';
                                    copyBtn.style.backgroundColor = '';
                                    copyBtn.style.color = '';
                                }, 1500);
                            }).catch(err => {
                                console.error('Failed to copy text: ', err);
                            });
                        });
                    }

                    resultsContainer.appendChild(card);
                });
            }
        } catch (error) {
            console.error('Search error:', error);
            updateStatus('(ノಠ益ಠ)ノ', 'Failed to retrieve details');
            resultsContainer.innerHTML = `
                <div class="result-card" style="border-color: var(--gruv-red); text-align: center;">
                    <span style="font-family: 'JetBrains Mono', monospace; color: var(--gruv-red); font-size: 0.9rem;">
                        An error occurred while communicating with the server.
                    </span>
                </div>
            `;
        }
    };

    // Attach search handlers to button and form submit
    searchButton.addEventListener('click', (e) => {
        e.preventDefault();
        performSearch();
    });

    searchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        performSearch();
    });

    /**
     * Helper to update the retro status indicator nicely
     */
    function updateStatus(emoticon, text) {
        statusEmoticon.style.transform = 'scale(0.8)';
        statusEmoticon.style.opacity = '0';
        
        setTimeout(() => {
            statusEmoticon.textContent = emoticon;
            statusText.textContent = text;
            statusEmoticon.style.transform = 'scale(1)';
            statusEmoticon.style.opacity = '1';
        }, 120);
    }
});
