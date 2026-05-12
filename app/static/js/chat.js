// Chat Application with Enhanced Features

class MedicalChat {
    constructor() {
        this.messageCount = 0;
        this.totalResponseTime = 0;
        this.isVoiceActive = false;
        this.currentCitations = [];
        
        this.initializeElements();
        this.initializeEventListeners();
        this.initMobileSidebar(); // Add mobile sidebar functionality
        this.showWelcomeMessage();
        this.startTimeTracking();
    }
    
    initializeElements() {
        this.chatBox = document.getElementById('chatBox');
        this.queryInput = document.getElementById('queryInput');
        this.typingIndicator = document.getElementById('typingIndicator');
        this.messageCountEl = document.getElementById('messageCount');
        this.responseTimeEl = document.getElementById('responseTime');
        this.citationPanel = document.getElementById('citationPanel');
        this.citationsList = document.getElementById('citationsList');
        this.themeToggle = document.getElementById('themeToggle');
        this.messageSound = document.getElementById('messageSound');
        
        // Voice recognition setup
        this.recognition = null;
        if ('webkitSpeechRecognition' in window) {
            this.recognition = new webkitSpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';
            
            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                this.queryInput.value = transcript;
                this.sendQuery();
            };
        }
    }
    
    initializeEventListeners() {
        // Enter key handling
        this.queryInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendQuery();
            }
        });
        
        // Theme toggle
        this.themeToggle.addEventListener('click', () => this.toggleTheme());
        
        // Input auto-resize
        this.queryInput.addEventListener('input', () => this.autoResizeInput());
        
        // Chat history navigation
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'k') {
                e.preventDefault();
                this.queryInput.focus();
            }
        });
    }
    
    // NEW: Mobile sidebar initialization
    initMobileSidebar() {
        // Check if mobile menu button already exists
        if (document.getElementById('mobileMenuBtn')) {
            return; // Already initialized
        }
        
        // Create mobile menu button
        const menuBtn = document.createElement('button');
        menuBtn.className = 'mobile-menu-btn';
        menuBtn.innerHTML = '<i class="fas fa-bars"></i>';
        menuBtn.id = 'mobileMenuBtn';
        menuBtn.title = 'Open Sidebar';
        menuBtn.setAttribute('aria-label', 'Toggle sidebar');
        
        // Create overlay
        const overlay = document.createElement('div');
        overlay.className = 'sidebar-overlay';
        overlay.id = 'sidebarOverlay';
        
        // Insert mobile menu button into header-right BEFORE other buttons
        const headerRight = document.querySelector('.header-right');
        if (headerRight) {
            headerRight.insertBefore(menuBtn, headerRight.firstChild);
        } else {
            console.error('Header-right element not found');
            return;
        }
        
        // Add overlay to body
        document.body.appendChild(overlay);
        
        const sidebar = document.querySelector('.chat-sidebar');
        const menuButton = document.getElementById('mobileMenuBtn');
        const sidebarOverlay = document.getElementById('sidebarOverlay');
        
        if (!sidebar || !menuButton || !sidebarOverlay) {
            console.error('Required elements not found');
            return;
        }
        
        // Toggle sidebar function
        const toggleSidebar = () => {
            const isActive = sidebar.classList.toggle('active');
            sidebarOverlay.classList.toggle('active');
            
            // Update menu button icon
            menuButton.innerHTML = isActive ? 
                '<i class="fas fa-times"></i>' : 
                '<i class="fas fa-bars"></i>';
            
            // Prevent body scroll when sidebar is open
            document.body.style.overflow = isActive ? 'hidden' : '';
            
            // Update accessibility attributes
            menuButton.setAttribute('aria-expanded', isActive);
            menuButton.title = isActive ? 'Close Sidebar' : 'Open Sidebar';
        };
        
        // Event listeners
        menuButton.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleSidebar();
        });
        
        sidebarOverlay.addEventListener('click', () => {
            if (sidebar.classList.contains('active')) {
                toggleSidebar();
            }
        });
        
        // Close sidebar on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && sidebar.classList.contains('active')) {
                toggleSidebar();
            }
        });
        
        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', (e) => {
            if (window.innerWidth <= 1024 && 
                sidebar.classList.contains('active') && 
                !sidebar.contains(e.target) && 
                !menuButton.contains(e.target)) {
                toggleSidebar();
            }
        });
        
        // Close sidebar when clicking on example buttons
        document.addEventListener('click', (e) => {
            if (e.target.closest('.example-btn') && window.innerWidth <= 1024) {
                if (sidebar.classList.contains('active')) {
                    toggleSidebar();
                }
            }
        });
        
        // Handle window resize
        const handleResize = () => {
            if (window.innerWidth <= 1024) {
                menuButton.style.display = 'flex';
            } else {
                menuButton.style.display = 'none';
                // Close sidebar if open
                if (sidebar.classList.contains('active')) {
                    toggleSidebar();
                }
            }
        };
        
        window.addEventListener('resize', handleResize);
        
        // Initial setup
        handleResize();
    }
    
    async sendQuery() {
        const query = this.queryInput.value.trim();
        if (!query) return;
        
        // Add user message
        this.addMessage(query, 'user');
        this.queryInput.value = '';
        this.autoResizeInput();
        
        // Show typing indicator
        this.showTypingIndicator();
        
        // Start response time tracking
        const startTime = Date.now();
        
        try {
            const response = await fetch('/api/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query })
            });
            
            const data = await response.json();
            const responseTime = Date.now() - startTime;
            
            // Update statistics
            this.updateStatistics(responseTime);
            
            // Hide typing indicator
            this.hideTypingIndicator();
            
            // Add bot response
            this.addMessage(
                data.response_html || data.response || 'No response available.',
                'bot',
                data.citations,
                false,
                data.academic_trace
            );

            // Play notification sound
            this.playNotificationSound();
            
            // Update message count
            this.messageCount++;
            this.messageCountEl.textContent = this.messageCount;
            
        } catch (error) {
            this.hideTypingIndicator();
            this.addMessage('⚠️ Network error. Please check your connection and try again.', 'bot');
            console.error('Error:', error);
        }
    }
    cleanSeparators(text) {
    return text
        .replace(/={5,}/g, '')
        .replace(/---+/g, '');
}

splitIntoSections(rawText) {
    const text = this.cleanSeparators(rawText);

    return {
        main: text.split(/Disclaimer:|Proof Trace:|Query:/)[0],

        legal: text.match(/Disclaimer:[\s\S]*?(?=Query:|$)/)?.[0] || '',

        debug: text.match(/Query:[\s\S]*$/)?.[0] || ''
    };
}

    addMessage(text, sender, citations = [], isHTML = false, academicTrace = null) {
        const academicEnabled = window.ACADEMIC_EXPLAINER_ENABLED === true;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        // Create avatar
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        avatarDiv.innerHTML = sender === 'bot' 
        ? '<i class="fas fa-robot"></i>' 
        : '<i class="fas fa-user"></i>';
        
        // Create message content container
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        // Create message bubble
        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = 'message-bubble';
        if (sender === 'bot') {
            bubbleDiv.innerHTML = `
                <div class="legal-section">
                    ${this.formatMessage(text)}
                </div>

                ${
                    academicEnabled && academicTrace
                        ? this.renderAcademicExplainer(academicTrace)
                        : ''
                }
            `;
        } else {
            bubbleDiv.innerHTML = this.formatMessage(text);
        }
    
        // Create timestamp
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = this.getCurrentTime();
        
        // Add citations if available
        if (citations && citations.length > 0) {
            this.currentCitations = citations;
            const citationDiv = document.createElement('div');
            citationDiv.className = 'message-citation';
            citationDiv.innerHTML = `<strong>📚 Sources:</strong> Based on ${citations.length} legal reference${citations.length > 1 ? 's' : ''}`;
            contentDiv.appendChild(citationDiv);
            
            // Show citation panel button
            this.showCitationButton();
        }
        
        // Assemble message based on sender
        if (sender === 'bot') {
            messageDiv.appendChild(avatarDiv);
            contentDiv.appendChild(bubbleDiv);
            contentDiv.appendChild(timeDiv);
            messageDiv.appendChild(contentDiv);
        } else {
            contentDiv.appendChild(bubbleDiv);
            contentDiv.appendChild(timeDiv);
            messageDiv.appendChild(contentDiv);
            messageDiv.appendChild(avatarDiv);
        }
        
        // Add to chat
        this.chatBox.appendChild(messageDiv);
        
        // Scroll to bottom with smooth animation
        this.scrollToBottom();
        
        // Add animation
        messageDiv.style.animation = 'fadeInUp 0.3s ease-out';
    }
    renderAcademicExplainer(trace) {
        return `
            <!-- 1️⃣ Input Interpretation -->
            <details class="academic-section">
                <summary>📂 Input Interpretation (Normalization)</summary>
                <pre><strong>Raw Query:</strong> ${trace.query}</pre>
                <pre><strong>Normalized Query:</strong> ${trace.normalized_query}</pre>
                <p class="academic-note">
                    Deterministic text normalization only.
                    <br><br>
                    <strong>Normalization rules applied:</strong><br>
                    • Leading and trailing whitespace removed<br>
                    • Multiple consecutive spaces collapsed into a single space
                    <br><br>
                    <strong>What is NOT done:</strong><br>
                    • No lowercasing<br>
                    • No grammar correction<br>
                    • No word deduplication<br>
                    • No semantic rewriting<br>
                    • No inference
                </p>
            </details>

            <!-- 2️⃣ Fact Extraction -->
            ${this.renderFactExtractionFromIntents(trace)}

            <!-- 3️⃣ Intent Mapping -->
            <details class="academic-section">
                <summary>🎯 Intent Mapping (Deterministic)</summary>

                <p class="academic-note">
                    Intents are matched using predefined legal indicators
                    (keywords, verbs, and negative patterns).
                    Each indicator contributes a fixed score.
                    No machine learning or probabilistic inference is used.
                </p>

                <div class="confidence-math">
                    <strong>Confidence Calculation:</strong><br>
                    Confidence = (Total Indicator Score) ÷ 6.0<br><br>

                    <em>Indicator Weights:</em>
                    <ul>
                        <li>Keyword match → +2</li>
                        <li>Negative pattern match → +3</li>
                        <li>Verb match → +1</li>
                    </ul>

                    Final confidence is capped at 1.0.
                </div>

                <div class="intent-results">
                    ${trace.matched_intents.map(i =>
                        `<div>
                            • <strong>${i.intent}</strong>
                            (confidence: ${i.confidence.toFixed(2)})
                        </div>`
                    ).join('')}
                </div>

                <p class="academic-note">
                    When multiple intents are matched, statutory priority
                    defined by NHRC rules determines final selection.
                </p>
            </details>


            <!-- 4️⃣ Clause Mapping -->
            <details class="academic-section">
                <summary>📚 Clause Mapping (Statutory)</summary>

                <p class="academic-note">
                    Once a primary intent is deterministically selected,
                    the system maps it to predefined legal provisions
                    from official NHRC / IMC documents.
                    <br><br>
                    This mapping is static and rule-based.
                    No legal interpretation or inference is performed at runtime.
                </p>

                <div class="clause-results">
                    ${trace.matched_clauses.map(c => `
                        <div class="clause-block">
                            <strong>Legal Provision:</strong><br>
                            • <strong>${c.id}</strong> — ${c.citation}
                        </div>
                    `).join('')}
                </div>

                <p class="academic-note">
                    Mapping basis:
                    The above legal provision(s) are pre-associated
                    with the selected intent in the system’s
                    legal knowledge base.
                </p>
            </details>


            <!-- 5️⃣ Template Selection -->
            <details class="academic-section">
                <summary>🧩 Template Selection (Deterministic)</summary>

                <p class="academic-note">
                    After intent and legal clause selection,
                    the system chooses a predefined response template.
                    <br><br>
                    Templates are written in advance and are
                    not generated dynamically at runtime.
                </p>

                <div class="template-block">
                    <strong>Selected Template:</strong><br>
                    ${trace.template_used}
                </div>

                <p class="academic-note">
                    Template selection is rule-based:
                    each intent is mapped to one or more
                    predefined response templates.
                    <br><br>
                    No language model or generative logic is used.
                </p>
            </details>


            <!-- 6️⃣ Variable Binding -->
            <details class="academic-section">
                <summary>🧪 Variable Binding (Deterministic)</summary>

                <p class="academic-note">
                    After selecting a response template,
                    the system fills predefined placeholders
                    using values derived from earlier stages.
                </p>

                <div class="variable-summary">
                    <strong>Total Variables Filled:</strong>
                    ${trace.variables_filled}
                </div>

                <p class="academic-note">
                    <strong>Sources of variables:</strong>
                    <ul>
                        <li>Observable facts from user input</li>
                        <li>Matched intent identifiers</li>
                        <li>Applicable legal clauses</li>
                    </ul>
                </p>

                <p class="academic-warning">
                    <strong>What is NOT allowed:</strong><br>
                    • No variable is invented<br>
                    • No external data is injected<br>
                    • No missing value is guessed<br>
                    • No probabilistic filling is performed
                </p>
            </details>

            <!-- 7️⃣ Legal Proof & Citations -->
            <details class="academic-section proof-section">
                <summary>⚖️ Legal Proof & Citations</summary>

                <p class="academic-note">
                    The response above is derived strictly from officially
                    notified legal and ethical documents.
                    No interpretation beyond documented provisions is performed.
                </p>

                <div class="legal-proof-list">
                    ${trace.matched_clauses.length > 0
                        ? trace.matched_clauses.map(c => `
                            <div class="legal-proof-item">
                                <strong>${c.id}</strong><br>
                                ${c.citation}<br>
                                <em>${c.title}</em>
                            </div>
                        `).join("")
                        : `<p class="academic-note">
                            No specific legal clause was triggered for this query.
                        </p>`
                    }
                </div>

                <p class="academic-warning">
                    <strong>Important:</strong><br>
                    • This system does not decide liability or guilt<br>
                    • This is legal awareness, not adjudication<br>
                    • Applicability depends on facts and authorities
                </p>
            </details>

            <!-- 8️⃣ System Determinism Check -->
            <details class="academic-section">
                <summary>🧬 System Determinism Check</summary>

                <p class="academic-note">
                    This system operates under a deterministic execution model.
                    For any identical input, the output will always remain identical.
                </p>

                <ul class="determinism-list">
                    <li>✔ Rule-based intent classification</li>
                    <li>✔ Fixed keyword, verb, and pattern sets</li>
                    <li>✔ Statutory priority ordering (NHRC hierarchy)</li>
                    <li>✔ Template-based response generation</li>
                    <li>✔ No machine learning models</li>
                    <li>✔ No probabilistic scoring beyond fixed weights</li>
                    <li>✔ No external knowledge retrieval</li>
                    <li>✔ No Large Language Model usage</li>
                </ul>

                <p class="academic-warning">
                    <strong>Determinism Guarantee:</strong><br>
                    Given the same input text, this system will always produce
                    the same legal mapping, template selection, and response.
                </p>
            </details>
        `;
    }

    renderFactExtractionFromIntents(trace) {
        if (!trace.matched_intents || trace.matched_intents.length === 0) {
            return `
                <details class="academic-section">
                    <summary>📂 Fact Extraction (Deterministic)</summary>
                    <p class="academic-note">
                        No observable fact indicators were triggered for this query.
                    </p>
                </details>
            `;
        }

        let blocks = "";

        trace.matched_intents.forEach(item => {
            const intent = item.intent;
            const indicators = this.getIntentIndicatorSummary(intent);
            if (!indicators) return;

            blocks += `
                <div class="fact-block">
                    <strong>Intent Context:</strong> ${intent}

                    <div class="fact-group">
                        <em>Triggered Legal Indicators (Rule-Based):</em>
                        <ul>
                            ${indicators.keywords.map(k => `<li>Keyword: ${k}</li>`).join("")}
                            ${indicators.verbs.map(v => `<li>Verb: ${v}</li>`).join("")}
                            ${indicators.negative_patterns.map(p => `<li>Negative Pattern: ${p}</li>`).join("")}
                        </ul>
                    </div>
                </div>
            `;
        });

        return `
            <details class="academic-section">
                <summary>📂 Fact Extraction (Deterministic)</summary>

                <p class="academic-note">
                    Observable facts are derived from predefined legal indicators
                    (keywords, verbs, and negative patterns) that triggered the matched intents.
                    No inference, probability model, or assumption is used.
                </p>

                ${blocks}
            </details>
        `;
    }


    getIntentIndicatorSummary(intentName) {
        const INTENT_INDICATORS = {
            emergency_care: {
                keywords: ["emergency", "urgent", "accident", "critical", "immediate"],
                verbs: ["refused", "denied"],
                negative_patterns: ["asked for advance", "demanded payment", "turned away"]
            },
            access_medical_records: {
                keywords: ["report", "record", "document"],
                verbs: ["refused", "denied"],
                negative_patterns: ["refused to give", "denied access"]
            }
            // ⛔ You can progressively add others later
        };

        return INTENT_INDICATORS[intentName] || null;
    }



    formatMessage(text) {
        // Format URLs as links
        let formatted = text.replace(
            /(https?:\/\/[^\s]+)/g,
            '<a href="$1" target="_blank" class="message-link">$1</a>'
        );
        
        // Format section numbers (e.g., Section 2.3)
        formatted = formatted.replace(
            /Section\s+(\d+\.\d+)/gi,
            '<strong class="section-ref">Section $1</strong>'
        );
        
        // Format important terms
        const importantTerms = ['NHRC', 'IMC', 'rights', 'obligations', 'medical records'];
        importantTerms.forEach(term => {
            const regex = new RegExp(`\\b${term}\\b`, 'gi');
            formatted = formatted.replace(regex, `<strong>${term}</strong>`);
        });
        
        return formatted;
    }
    
    cleanSeparators(text) {
    return text.replace(/={5,}/g, '');
    }

    splitIntoSections(rawText) {
        const text = this.cleanSeparators(rawText);

        const sections = {
            answer: '',
            actions: '',
            proof: '',
            debug: ''
        };

        // 1️⃣ MAIN ANSWER (before "What You Can Do")
        const answerMatch = text.match(
            /^(.*?)(?=\nWhat You Can Do:|\nDisclaimer:|\nProof Trace:|\nQuery:|$)/s
        );
        if (answerMatch) {
            sections.answer = answerMatch[1].trim();
        }

        // 2️⃣ ACTIONS
        const actionMatch = text.match(
            /What You Can Do:\s*([\s\S]*?)(?=\nDisclaimer:|\nProof Trace:|\nQuery:|$)/i
        );
        if (actionMatch) {
            sections.actions = actionMatch[1].trim();
        }

        // 3️⃣ LEGAL PROOF (keep for professor)
        const proofMatch = text.match(
            /(Disclaimer:|Proof Trace:|Legal Sources Cited:)[\s\S]*?(?=\nQuery:|$)/i
        );
        if (proofMatch) {
            sections.proof = proofMatch[0].trim();
        }

        // 4️⃣ DEBUG / SYSTEM TRACE
        const debugMatch = text.match(
            /Query:\s*[\s\S]*$/i
        );
        if (debugMatch) {
            sections.debug = debugMatch[0].trim();
        }

        return sections;
    }


    showWelcomeMessage() {
        const welcomeMessage = `
            Hello! I am <strong>PC-MLRA</strong> — your Proof-Carrying Medical Legal Rights Advisor.<br><br>
            I provide deterministic, zero-hallucination guidance strictly based on <strong>NHRC</strong> and <strong>IMC</strong> documents.<br><br>
            Ask me about:
            <ul>
                <li>Patient rights and responsibilities</li>
                <li>Doctor obligations and ethical conduct</li>
                <li>Medical record access procedures</li>
                <li>Billing disputes and transparency</li>
                <li>Privacy and confidentiality rights</li>
            </ul>
            <em>All responses include verifiable legal citations.</em>
        `;
        
        setTimeout(() => {
            this.addMessage(welcomeMessage, 'bot');
            this.messageCount = 1;
            this.messageCountEl.textContent = this.messageCount;
        }, 500);
    }
    
    showTypingIndicator() {
        this.typingIndicator.style.display = 'flex';
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        this.typingIndicator.style.display = 'none';
    }
    
    updateStatistics(responseTime) {
        this.totalResponseTime += responseTime;
        const avgTime = this.messageCount > 0 ? 
            Math.round(this.totalResponseTime / this.messageCount / 1000) : 0;
        this.responseTimeEl.textContent = `${avgTime}s`;
    }
    
    startTimeTracking() {
        setInterval(() => {
            const now = new Date();
            document.querySelectorAll('.message-time').forEach(el => {
                if (el.dataset.timestamp) {
                    const timeDiff = now - new Date(el.dataset.timestamp);
                    el.textContent = this.formatRelativeTime(timeDiff);
                }
            });
        }, 60000);
    }
    
    formatRelativeTime(timeDiff) {
        const minutes = Math.floor(timeDiff / 60000);
        const hours = Math.floor(minutes / 60);
        
        if (minutes < 1) return 'Just now';
        if (minutes < 60) return `${minutes}m ago`;
        if (hours < 24) return `${hours}h ago`;
        
        return new Date(Date.now() - timeDiff).toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }
    
    getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }
    
    scrollToBottom() {
        setTimeout(() => {
            if (this.chatBox) {
                this.chatBox.scrollTo({
                    top: this.chatBox.scrollHeight,
                    behavior: 'smooth'
                });
            }
        }, 100);
    }
    
    autoResizeInput() {
        if (this.queryInput) {
            this.queryInput.style.height = 'auto';
            this.queryInput.style.height = Math.min(this.queryInput.scrollHeight, 120) + 'px';
        }
    }
    
    toggleTheme() {
        const theme = document.documentElement.getAttribute('data-theme');
        const newTheme = theme === 'light' ? 'dark' : 'light';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        this.themeToggle.innerHTML = newTheme === 'light' ? 
            '<i class="fas fa-moon"></i>' : 
            '<i class="fas fa-sun"></i>';
        
        // Save theme preference
        localStorage.setItem('theme', newTheme);
    }
    
    toggleVoiceInput() {
        if (!this.recognition) {
            alert('Voice recognition is not supported in your browser.');
            return;
        }
        
        if (this.isVoiceActive) {
            this.recognition.stop();
            this.isVoiceActive = false;
            document.querySelector('.voice-btn')?.classList.remove('active');
        } else {
            this.recognition.start();
            this.isVoiceActive = true;
            document.querySelector('.voice-btn')?.classList.add('active');
        }
    }
    
    playNotificationSound() {
        if (this.messageSound) {
            this.messageSound.currentTime = 0;
            this.messageSound.play().catch(e => console.log('Audio play failed:', e));
        }
    }
    
    clearChat() {
        if (confirm('Are you sure you want to clear the chat history?')) {
            this.chatBox.innerHTML = '';
            this.messageCount = 0;
            this.messageCountEl.textContent = '0';
            this.totalResponseTime = 0;
            this.responseTimeEl.textContent = '0s';
            this.currentCitations = [];
            this.hideCitationPanel();
            this.showWelcomeMessage();
        }
    }
    
    exportChat() {
        const messages = Array.from(this.chatBox.querySelectorAll('.message')).map(msg => {
            const sender = msg.classList.contains('bot') ? 'AI' : 'You';
            const text = msg.querySelector('.message-bubble')?.textContent || '';
            const time = msg.querySelector('.message-time')?.textContent || '';
            return `[${time}] ${sender}: ${text}`;
        }).join('\n\n');
        
        const blob = new Blob([messages], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `medical-chat-${new Date().toISOString().split('T')[0]}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
    
    showCitationButton() {
        if (this.currentCitations.length > 0) {
            // Remove existing button if any
            const existingBtn = document.querySelector('.show-citations-btn');
            if (existingBtn) existingBtn.remove();
            
            // Add new button
            const btn = document.createElement('button');
            btn.className = 'show-citations-btn';
            btn.innerHTML = '<i class="fas fa-book"></i> View Citations';
            btn.onclick = () => this.showCitationPanel();
            
            const inputFooter = document.querySelector('.input-footer');
            if (inputFooter) {
                inputFooter.insertBefore(btn, inputFooter.querySelector('.send-btn'));
            }
        }
    }
    
    showCitationPanel() {
        this.citationsList.innerHTML = '';
        
        this.currentCitations.forEach(citation => {
            const item = document.createElement('div');
            item.className = 'citation-item';
            item.innerHTML = `
                <div class="citation-title">${citation.title || 'Citation'}</div>
                <div class="citation-content">${citation.content || 'No content available'}</div>
                <div class="citation-source">Source: ${citation.source || 'Unknown'}</div>
            `;
            this.citationsList.appendChild(item);
        });
        
        this.citationPanel.style.display = 'block';
    }
    
    hideCitationPanel() {
        this.citationPanel.style.display = 'none';
    }
    
    toggleCitations() {
        if (this.citationPanel.style.display === 'block') {
            this.hideCitationPanel();
        } else {
            this.showCitationPanel();
        }
    }
    
    useExample(button) {
        const text = button.querySelector('span').textContent;
        this.queryInput.value = `Can you explain my rights regarding "${text}"?`;
        this.queryInput.focus();
        this.autoResizeInput();
    }
}

// Initialize chat when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.chatApp = new MedicalChat();
    
    // Load saved theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.innerHTML = savedTheme === 'light' ? 
            '<i class="fas fa-moon"></i>' : 
            '<i class="fas fa-sun"></i>';
    }
    
    // Ensure chat interface is visible on load
    setTimeout(() => {
        const chatBox = document.getElementById('chatBox');
        if (chatBox && chatBox.children.length === 0) {
            // If no messages, trigger welcome message
            if (window.chatApp) {
                window.chatApp.showWelcomeMessage();
            }
        }
        
        // Scroll to show content
        if (chatBox) {
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }, 1000);
});

// Global functions for HTML onclick handlers
function sendQuery() {
    window.chatApp?.sendQuery();
}

function useExample(button) {
    window.chatApp?.useExample(button);
}

function clearChat() {
    window.chatApp?.clearChat();
}

function exportChat() {
    window.chatApp?.exportChat();
}

function toggleVoiceInput() {
    window.chatApp?.toggleVoiceInput();
}

function attachFile() {
    alert('File attachment feature coming soon!');
}

function handleKeyPress(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendQuery();
    }
}

function toggleCitations() {
    window.chatApp?.toggleCitations();
}

// Handle example button clicks from sidebar
document.addEventListener('click', function(e) {
    if (e.target.closest('.example-btn')) {
        const button = e.target.closest('.example-btn');
        const text = button.querySelector('span').textContent;
        const queryInput = document.getElementById('queryInput');
        if (queryInput) {
            queryInput.value = `Can you explain my rights regarding "${text}"?`;
            queryInput.focus();
            
            // Auto-resize input
            queryInput.style.height = 'auto';
            queryInput.style.height = Math.min(queryInput.scrollHeight, 120) + 'px';
        }
    }
});

// Close sidebar when clicking on example (on mobile)
if (window.innerWidth <= 1024) {
    document.addEventListener('click', function(e) {
        if (e.target.closest('.example-btn')) {
            const sidebar = document.querySelector('.chat-sidebar');
            const overlay = document.getElementById('sidebarOverlay');
            const menuBtn = document.getElementById('mobileMenuBtn');
            
            if (sidebar && sidebar.classList.contains('active')) {
                sidebar.classList.remove('active');
                if (overlay) overlay.classList.remove('active');
                if (menuBtn) menuBtn.innerHTML = '<i class="fas fa-bars"></i>';
                document.body.style.overflow = '';
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
  const modal = document.getElementById('pdfModal');
  const pdfViewer = document.getElementById('pdfViewer');
  const closeBtn = document.querySelector('.close-modal');
  const docLinks = document.querySelectorAll('.doc-link');
  
  // Open PDF in modal
  docLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const pdfFile = this.getAttribute('data-pdf');
      pdfViewer.src = `/static/documents/${pdfFile}`;
      modal.style.display = 'block';
    });
  });
  
  // Close modal
  closeBtn.addEventListener('click', function() {
    modal.style.display = 'none';
    pdfViewer.src = ''; // Clear iframe source
  });
  
  // Close modal when clicking outside
  window.addEventListener('click', function(e) {
    if (e.target === modal) {
      modal.style.display = 'none';
      pdfViewer.src = '';
    }
  });
});