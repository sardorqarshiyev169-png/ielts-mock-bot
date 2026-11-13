// Telegram Mini App - IELTS Computer-Delivered Mock Platform

// Global State
let tg = window.Telegram?.WebApp;
let currentView = 'home';
let availableTests = [];
let activeTest = null;
let userAnswers = {};
let reviewedQuestions = new Set();
let timerInterval = null;
let secondsRemaining = 0;
let currentQuestionIndex = 0;
let flatQuestions = [];

// Initialize on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
  initTelegram();
  lucide.createIcons();
  loadTests();
  setupAudioPlayer();
});

// Telegram WebApp Setup
function initTelegram() {
  if (tg) {
    tg.ready();
    tg.expand();
    if (tg.enableClosingConfirmation) {
      tg.enableClosingConfirmation();
    }
    
    // Set candidate details if launched from Telegram
    if (tg.initDataUnsafe?.user) {
      const u = tg.initDataUnsafe.user;
      const cName = document.getElementById('candidateName');
      if (cName) {
        cName.textContent = `Candidate: ${u.first_name} ${u.last_name || ''} (${u.id})`;
      }
    }
  }
}

// Haptic Feedback Helper
function triggerHaptic(type = 'light') {
  if (tg?.HapticFeedback) {
    if (type === 'light') tg.HapticFeedback.impactOccurred('light');
    if (type === 'medium') tg.HapticFeedback.impactOccurred('medium');
    if (type === 'success') tg.HapticFeedback.notificationOccurred('success');
    if (type === 'warning') tg.HapticFeedback.notificationOccurred('warning');
  }
}

// View Routing
function switchView(viewName) {
  currentView = viewName;
  ['viewHome', 'viewExam', 'viewResults', 'viewAdmin'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.classList.add('hidden');
  });

  const timerBox = document.getElementById('examTimerContainer');

  if (viewName === 'home') {
    document.getElementById('viewHome')?.classList.remove('hidden');
    timerBox?.classList.add('hidden');
    timerBox?.classList.remove('flex');
    stopExamTimer();
    loadTests();
  } else if (viewName === 'exam') {
    document.getElementById('viewExam')?.classList.remove('hidden');
    timerBox?.classList.remove('hidden');
    timerBox?.classList.add('flex');
  } else if (viewName === 'results') {
    document.getElementById('viewResults')?.classList.remove('hidden');
    timerBox?.classList.add('hidden');
    timerBox?.classList.remove('flex');
    stopExamTimer();
  } else if (viewName === 'admin') {
    document.getElementById('viewAdmin')?.classList.remove('hidden');
    timerBox?.classList.add('hidden');
    timerBox?.classList.remove('flex');
    stopExamTimer();
  }

  lucide.createIcons();
  window.scrollTo(0, 0);
}

// ==================== TEST LOADING & CATALOG ====================

async function loadTests(typeFilter = 'all') {
  const grid = document.getElementById('testsGrid');
  const counter = document.getElementById('testCounter');
  if (!grid) return;

  grid.innerHTML = `
    <div class="col-span-2 text-center py-12 text-slate-500">
      <div class="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
      Yuklanmoqda...
    </div>
  `;

  try {
    const res = await fetch(`/api/tests?type=${typeFilter}`);
    const data = await res.json();
    if (data.status === 'success') {
      availableTests = data.data;
      if (counter) counter.textContent = `${availableTests.length} ta test mavjud`;
      renderTestCards(availableTests);
    }
  } catch (err) {
    grid.innerHTML = `
      <div class="col-span-2 text-center py-12 text-rose-400 text-xs">
        Testlarni yuklab bo'lmadi. Server ishlayotganini tekshiring.
      </div>
    `;
  }
}

function filterTests(type) {
  triggerHaptic('light');
  document.querySelectorAll('.tab-btn').forEach(b => {
    b.classList.remove('active', 'bg-indigo-600', 'text-white');
    b.classList.add('bg-slate-800', 'text-slate-300');
  });
  event.target.classList.add('active', 'bg-indigo-600', 'text-white');
  event.target.classList.remove('bg-slate-800', 'text-slate-300');
  loadTests(type);
}

function renderTestCards(tests) {
  const grid = document.getElementById('testsGrid');
  if (!grid) return;

  if (tests.length === 0) {
    grid.innerHTML = `
      <div class="col-span-2 text-center py-12 bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <i data-lucide="inbox" class="w-10 h-10 text-slate-600 mx-auto mb-2"></i>
        <p class="text-sm font-semibold text-slate-300">Hozircha testlar yo'q</p>
        <p class="text-xs text-slate-500 mt-1">Materiallar bo'limidan yangi test qo'shing yoki AI orqali yarating</p>
      </div>
    `;
    lucide.createIcons();
    return;
  }

  grid.innerHTML = tests.map(test => {
    const isListening = test.type === 'listening';
    const icon = isListening ? 'headphones' : 'book-open';
    const badgeBg = isListening ? 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30' : 'bg-indigo-500/20 text-indigo-400 border-indigo-500/30';
    
    return `
      <div class="bg-slate-900/80 hover:bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-2xl p-5 shadow-lg transition flex flex-col justify-between group">
        <div>
          <div class="flex items-center justify-between mb-3">
            <span class="text-[10px] uppercase font-bold px-2 py-0.5 rounded-full border ${badgeBg}">
              ${test.type.toUpperCase()}
            </span>
            <div class="flex items-center gap-1 text-[11px] text-slate-400">
              <i data-lucide="clock" class="w-3.5 h-3.5"></i>
              <span>${test.time_limit_minutes} min</span>
            </div>
          </div>
          <h3 class="font-bold text-base text-white group-hover:text-indigo-400 transition leading-snug">
            ${test.title}
          </h3>
          <p class="text-xs text-slate-400 mt-1.5 line-clamp-2 leading-relaxed">
            ${test.description || 'Haqiqiy IELTS formati bo\'yicha tuzilgan rasmiy test.'}
          </p>
        </div>

        <div class="mt-4 pt-4 border-t border-slate-800/80 flex items-center justify-between">
          <div class="text-[11px] text-slate-400 flex items-center gap-1">
            <i data-lucide="${icon}" class="w-3.5 h-3.5 text-slate-500"></i>
            <span>${test.question_count || 10} ta savol</span>
          </div>
          <button onclick="startExam(${test.id})" class="bg-indigo-600 hover:bg-indigo-500 active:scale-95 text-white text-xs font-bold px-4 py-2 rounded-xl transition shadow flex items-center gap-1.5">
            <span>Boshlash</span>
            <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
          </button>
        </div>
      </div>
    `;
  }).join('');

  lucide.createIcons();
}

// ==================== EXAM ENGINE ====================

async function startExam(testId) {
  triggerHaptic('medium');
  try {
    const res = await fetch(`/api/tests/${testId}`);
    const data = await res.json();
    if (data.status !== 'success') {
      showToast('Testni yuklab bo\'lmadi');
      return;
    }

    activeTest = data.data;
    userAnswers = {};
    reviewedQuestions.clear();
    currentQuestionIndex = 0;

    // Flatten questions list
    flatQuestions = [];
    activeTest.sections.forEach(sec => {
      sec.questions.forEach(q => {
        flatQuestions.push({ ...q, section_id: sec.id });
      });
    });

    // Setup Header & Passage
    document.getElementById('examTestTitle').textContent = activeTest.title;
    const sec1 = activeTest.sections[0] || {};
    document.getElementById('passageTitle').textContent = sec1.title || 'Passage 1';
    
    // Render Passage text with formatting
    renderPassageText(sec1.passage_text || '');

    // Setup Audio if Listening
    const audioControls = document.getElementById('examAudioControls');
    const audioPlayer = document.getElementById('examAudioPlayer');
    if (activeTest.type === 'listening' && sec1.audio_file) {
      audioControls.classList.remove('hidden');
      audioControls.classList.add('flex');
      audioPlayer.src = sec1.audio_file;
      audioPlayer.load();
    } else {
      audioControls.classList.add('hidden');
      audioControls.classList.remove('flex');
      audioPlayer.pause();
    }

    // Render questions
    renderQuestions(flatQuestions);
    renderQuestionPalette(flatQuestions);

    // Start Timer
    startExamTimer(activeTest.time_limit_minutes || 60);

    // Switch view
    switchView('exam');
    lucide.createIcons();
  } catch (err) {
    console.error(err);
    showToast('Xatolik yuz berdi');
  }
}

function renderPassageText(rawText) {
  const container = document.getElementById('passageContent');
  if (!container) return;
  
  // Format paragraphs nicely
  const paragraphs = rawText.split('\n\n').filter(p => p.trim());
  container.innerHTML = paragraphs.map(p => {
    // If line starts with "Paragraph X", emphasize it
    if (p.startsWith('Paragraph ')) {
      const parts = p.split('\n');
      const header = parts[0];
      const rest = parts.slice(1).join(' ');
      return `<p class="mb-4"><span class="font-bold text-indigo-400 block mb-1">${header}</span>${rest}</p>`;
    }
    return `<p class="mb-4 text-justify">${p}</p>`;
  }).join('');
}

function renderQuestions(questions) {
  const container = document.getElementById('questionsContainer');
  if (!container) return;

  container.innerHTML = questions.map((q, idx) => {
    return `
      <div id="qCard_${q.id}" class="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-3 transition duration-200">
        <div class="flex items-start justify-between gap-3">
          <div class="flex items-center gap-2">
            <span class="w-6 h-6 rounded-lg bg-indigo-600/30 text-indigo-400 border border-indigo-500/40 font-mono font-bold text-xs flex items-center justify-center">
              ${q.question_number}
            </span>
            <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">${formatQuestionType(q.question_type)}</span>
          </div>
          <button onclick="toggleReviewQuestion(${q.id})" class="text-[11px] text-slate-400 hover:text-amber-400 flex items-center gap-1 transition" title="Belgilab qo'yish">
            <i data-lucide="flag" class="w-3.5 h-3.5 ${reviewedQuestions.has(q.id) ? 'text-amber-400 fill-amber-400' : ''}"></i>
            <span>Review</span>
          </button>
        </div>

        <p class="text-sm font-medium text-slate-100 leading-snug">
          ${q.prompt}
        </p>

        <!-- Question Input Types -->
        <div class="mt-2">
          ${renderQuestionInput(q)}
        </div>
      </div>
    `;
  }).join('');
}

function formatQuestionType(type) {
  if (type === 'true_false_not_given') return 'True / False / Not Given';
  if (type === 'multiple_choice') return 'Multiple Choice';
  if (type === 'fill_blanks') return 'Completion';
  return 'Question';
}

function renderQuestionInput(q) {
  if (q.question_type === 'true_false_not_given') {
    const opts = ['TRUE', 'FALSE', 'NOT GIVEN'];
    return `
      <div class="grid grid-cols-3 gap-2">
        ${opts.map(opt => `
          <button type="button" onclick="selectAnswer(${q.id}, '${opt}')" id="ansBtn_${q.id}_${opt.replace(' ', '_')}" class="ans-btn px-3 py-2 rounded-xl text-xs font-bold border border-slate-800 bg-slate-950/70 text-slate-300 hover:bg-slate-800 transition active:scale-95">
            ${opt}
          </button>
        `).join('')}
      </div>
    `;
  } else if (q.question_type === 'multiple_choice') {
    const opts = q.options && q.options.length ? q.options : ['A) Option 1', 'B) Option 2', 'C) Option 3', 'D) Option 4'];
    return `
      <div class="space-y-2">
        ${opts.map((opt, i) => {
          const letter = opt.substring(0, 1);
          return `
            <div onclick="selectAnswer(${q.id}, '${letter}')" id="ansBtn_${q.id}_${letter}" class="ans-btn flex items-center gap-3 p-3 rounded-xl border border-slate-800 bg-slate-950/70 hover:bg-slate-800/70 cursor-pointer transition active:scale-[0.99]">
              <span class="w-6 h-6 rounded-full bg-slate-800 text-slate-300 text-xs font-bold flex items-center justify-center border border-slate-700">
                ${letter}
              </span>
              <span class="text-xs text-slate-200">${opt.replace(/^[A-D]\)\s*/, '')}</span>
            </div>
          `;
        }).join('')}
      </div>
    `;
  } else {
    // Fill in the blanks
    return `
      <div>
        <input type="text" oninput="inputAnswer(${q.id}, this.value)" placeholder="Javobni yozing..." class="w-full bg-slate-950 border border-slate-700 focus:border-indigo-500 rounded-xl px-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none">
      </div>
    `;
  }
}

function selectAnswer(qId, val) {
  triggerHaptic('light');
  userAnswers[qId] = val;

  // Clear previous button highlights for this question
  document.querySelectorAll(`[id^="ansBtn_${qId}_"]`).forEach(el => {
    el.classList.remove('bg-indigo-600', 'border-indigo-500', 'text-white');
    el.classList.add('bg-slate-950/70', 'border-slate-800', 'text-slate-300');
  });

  const selectedBtn = document.getElementById(`ansBtn_${qId}_${val.replace(' ', '_')}`);
  if (selectedBtn) {
    selectedBtn.classList.add('bg-indigo-600', 'border-indigo-500', 'text-white');
    selectedBtn.classList.remove('bg-slate-950/70', 'border-slate-800', 'text-slate-300');
  }

  updatePaletteStatus(qId);
}

function inputAnswer(qId, val) {
  if (val.trim()) {
    userAnswers[qId] = val.trim();
  } else {
    delete userAnswers[qId];
  }
  updatePaletteStatus(qId);
}

function toggleReviewQuestion(qId) {
  triggerHaptic('medium');
  if (reviewedQuestions.has(qId)) {
    reviewedQuestions.delete(qId);
  } else {
    reviewedQuestions.add(qId);
  }
  updatePaletteStatus(qId);
  renderQuestions(flatQuestions);
  lucide.createIcons();
}

// Palette rendering
function renderQuestionPalette(questions) {
  const palette = document.getElementById('questionPalette');
  if (!palette) return;

  palette.innerHTML = questions.map((q, idx) => {
    return `
      <button onclick="scrollToQuestion(${q.id}, ${idx})" id="paletteBtn_${q.id}" class="palette-btn unanswered">
        ${q.question_number}
      </button>
    `;
  }).join('');
}

function updatePaletteStatus(qId) {
  const btn = document.getElementById(`paletteBtn_${qId}`);
  if (!btn) return;

  const isAnswered = !!userAnswers[qId];
  const isReviewed = reviewedQuestions.has(qId);

  btn.className = 'palette-btn';
  if (isAnswered) {
    btn.classList.add('answered');
  } else {
    btn.classList.add('unanswered');
  }

  if (isReviewed) {
    btn.classList.add('reviewed');
  }
}

function scrollToQuestion(qId, index) {
  triggerHaptic('light');
  currentQuestionIndex = index;
  const card = document.getElementById(`qCard_${qId}`);
  if (card) {
    card.scrollIntoView({ behavior: 'smooth', block: 'center' });
    card.classList.add('ring-2', 'ring-indigo-500');
    setTimeout(() => card.classList.remove('ring-2', 'ring-indigo-500'), 1500);
  }
}

function navigateQuestion(step) {
  const nextIdx = currentQuestionIndex + step;
  if (nextIdx >= 0 && nextIdx < flatQuestions.length) {
    scrollToQuestion(flatQuestions[nextIdx].id, nextIdx);
  }
}

// ==================== HIGHLIGHTING TOOL ====================

function highlightSelection(color = '#fef08a') {
  triggerHaptic('light');
  const selection = window.getSelection();
  if (!selection.rangeCount || selection.isCollapsed) return;

  const range = selection.getRangeAt(0);
  const span = document.createElement('span');
  span.className = 'ielts-highlight';
  try {
    range.surroundContents(span);
    selection.removeAllRanges();
  } catch (e) {
    // Cross-block selection fallback
    showToast('Iltimos, bitta paragraf ichidagi matnni belgilang');
  }
}

function clearHighlights() {
  triggerHaptic('light');
  const highlights = document.querySelectorAll('.ielts-highlight');
  highlights.forEach(h => {
    const parent = h.parentNode;
    while (h.firstChild) parent.insertBefore(h.firstChild, h);
    parent.removeChild(h);
  });
}

// ==================== TIMER ====================

function startExamTimer(minutes) {
  stopExamTimer();
  secondsRemaining = minutes * 60;
  updateTimerDisplay();

  timerInterval = setInterval(() => {
    secondsRemaining--;
    updateTimerDisplay();
    if (secondsRemaining <= 0) {
      stopExamTimer();
      showToast('Vaqt tugadi! Test yakunlanmoqda...');
      submitExam();
    }
  }, 1000);
}

function stopExamTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}

function updateTimerDisplay() {
  const display = document.getElementById('timerDisplay');
  if (!display) return;
  const m = Math.floor(secondsRemaining / 60);
  const s = secondsRemaining % 60;
  display.textContent = `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

// ==================== AUDIO PLAYER ====================

function setupAudioPlayer() {
  const audio = document.getElementById('examAudioPlayer');
  const progress = document.getElementById('audioProgressBar');
  const timeDisplay = document.getElementById('audioTimeDisplay');

  if (!audio) return;

  audio.addEventListener('timeupdate', () => {
    if (audio.duration) {
      const pct = (audio.currentTime / audio.duration) * 100;
      if (progress) progress.style.width = `${pct}%`;
      const curM = Math.floor(audio.currentTime / 60);
      const curS = Math.floor(audio.currentTime % 60);
      if (timeDisplay) timeDisplay.textContent = `${String(curM).padStart(2, '0')}:${String(curS).padStart(2, '0')}`;
    }
  });

  audio.addEventListener('ended', () => {
    const icon = document.getElementById('audioPlayIcon');
    if (icon) icon.setAttribute('data-lucide', 'play');
    lucide.createIcons();
  });
}

function toggleAudio() {
  triggerHaptic('light');
  const audio = document.getElementById('examAudioPlayer');
  const icon = document.getElementById('audioPlayIcon');
  if (!audio) return;

  if (audio.paused) {
    audio.play();
    if (icon) icon.setAttribute('data-lucide', 'pause');
  } else {
    audio.pause();
    if (icon) icon.setAttribute('data-lucide', 'play');
  }
  lucide.createIcons();
}

// ==================== EXAM SUBMISSION & RESULTS ====================

function confirmFinishExam() {
  const unansweredCount = flatQuestions.length - Object.keys(userAnswers).length;
  let confirmMsg = "Testni yakunlashga ishonchingiz komilmi?";
  if (unansweredCount > 0) {
    confirmMsg = `Sizda hali ${unansweredCount} ta belgilanmagan savol bor. Testni yakunlaysizmi?`;
  }

  if (confirm(confirmMsg)) {
    submitExam();
  }
}

async function submitExam() {
  triggerHaptic('success');
  stopExamTimer();

  const tgId = tg?.initDataUnsafe?.user?.id || 12345;
  const uName = tg?.initDataUnsafe?.user?.username || 'candidate';

  try {
    const res = await fetch('/api/tests/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        test_id: activeTest.id,
        answers: userAnswers,
        tg_id: tgId,
        username: uName,
        time_spent_seconds: (activeTest.time_limit_minutes * 60) - secondsRemaining
      })
    });

    const data = await res.json();
    if (data.status === 'success') {
      renderResults(data);
      switchView('results');
    } else {
      showToast('Natijalarni hisoblashda xatolik');
    }
  } catch (err) {
    console.error(err);
    showToast('Tarmoq xatosi');
  }
}

function renderResults(resultData) {
  document.getElementById('resultBandScore').textContent = resultData.band_score;
  document.getElementById('resultRawScore').textContent = `${resultData.score} / ${resultData.max_score}`;

  const container = document.getElementById('resultsDetailedList');
  if (!container) return;

  container.innerHTML = resultData.itemized.map(item => {
    const isCorrect = item.is_correct;
    const badgeColor = isCorrect ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30' : 'bg-rose-500/20 text-rose-400 border-rose-500/30';
    const statusText = isCorrect ? "To'g'ri" : "Noto'g'ri";

    return `
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 space-y-2">
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-slate-300">Savol ${item.question_number}</span>
          <span class="text-[10px] font-bold px-2 py-0.5 rounded-full border ${badgeColor}">
            ${statusText}
          </span>
        </div>
        <p class="text-xs text-slate-200 font-medium">${item.prompt}</p>
        
        <div class="grid grid-cols-2 gap-2 text-xs pt-1">
          <div class="bg-slate-950 p-2 rounded-xl border border-slate-800">
            <span class="text-[10px] text-slate-500 block">Sizning javobingiz:</span>
            <span class="font-bold ${isCorrect ? 'text-emerald-400' : 'text-rose-400'}">
              ${item.user_answer || '(Belgilanmagan)'}
            </span>
          </div>
          <div class="bg-slate-950 p-2 rounded-xl border border-slate-800">
            <span class="text-[10px] text-slate-500 block">To'g'ri javob:</span>
            <span class="font-bold text-emerald-400">${item.correct_answer}</span>
          </div>
        </div>

        ${item.explanation ? `
          <div class="text-[11px] bg-indigo-950/30 border border-indigo-900/50 p-2.5 rounded-xl text-indigo-300 mt-2">
            <span class="font-semibold block mb-0.5">Izoh:</span>
            ${item.explanation}
          </div>
        ` : ''}
      </div>
    `;
  }).join('');

  lucide.createIcons();
}

function shareResultToTelegram() {
  triggerHaptic('light');
  const band = document.getElementById('resultBandScore').textContent;
  const score = document.getElementById('resultRawScore').textContent;
  const text = `🎯 Men hozirgina IELTS Mock Test topshirdim!\n\n🏅 Mening Natijam: IELTS Band ${band}\n📊 To'g'ri javoblar: ${score}\n\nSiz ham o'z darajangizni sinab ko'ring!`;
  
  if (tg?.openTelegramLink) {
    tg.openTelegramLink(`https://t.me/share/url?url=https://t.me/ielts_mock_bot&text=${encodeURIComponent(text)}`);
  } else {
    navigator.clipboard.writeText(text);
    showToast('Natija nusxalandi!');
  }
}

// ==================== ADMIN & MATERIAL CREATOR ====================

async function triggerAiMockGeneration() {
  switchView('admin');
  document.getElementById('aiTopicInput')?.focus();
}

async function generateWithAi() {
  triggerHaptic('medium');
  const topicInput = document.getElementById('aiTopicInput');
  const statusEl = document.getElementById('aiGenStatus');
  const btn = document.getElementById('btnAiGenerate');

  const topic = topicInput?.value.trim() || '';

  if (statusEl) statusEl.classList.remove('hidden');
  if (btn) btn.disabled = true;

  try {
    const res = await fetch('/api/tests/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic })
    });

    const data = await res.json();
    if (data.status === 'success') {
      showToast('Yangi IELTS test muvaffaqiyatli yaratildi!');
      if (topicInput) topicInput.value = '';
      switchView('home');
    } else {
      showToast('Generatsiyada xatolik: ' + data.message);
    }
  } catch (err) {
    showToast('Tarmoq xatosi yuz berdi');
  } finally {
    if (statusEl) statusEl.classList.add('hidden');
    if (btn) btn.disabled = false;
  }
}

async function importRawText() {
  triggerHaptic('medium');
  const textarea = document.getElementById('rawTextInput');
  const rawText = textarea?.value.trim();

  if (!rawText) {
    showToast('Iltimos, matn kiriting');
    return;
  }

  try {
    const res = await fetch('/api/tests/import', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ raw_text: rawText })
    });

    const data = await res.json();
    if (data.status === 'success') {
      showToast('Test muvaffaqiyatli import qilindi!');
      textarea.value = '';
      switchView('home');
    } else {
      showToast('Importda xatolik: ' + data.message);
    }
  } catch (err) {
    showToast('Tarmoq xatosi yuz berdi');
  }
}

function insertSampleFormat() {
  const textarea = document.getElementById('rawTextInput');
  if (!textarea) return;

  textarea.value = `TITLE: Climate Resilience in Modern Agriculture
PASSAGE:
Paragraph A
Over the past century, intensive agriculture has significantly increased global crop yields. However, extreme weather events and soil erosion are creating pressing vulnerabilities for smallholder farming communities. Modern agroecologists are exploring regenerative practices to revitalize soil microbiomes and optimize drought tolerance.

Paragraph B
Research conducted by agricultural scientists demonstrates that no-till farming reduces soil erosion by upwards of 60 percent. Furthermore, retaining crop residues on field surfaces prevents evaporative water loss, shielding root systems against sudden temperature spikes during heatwaves.

QUESTIONS:
1. Intensive farming techniques failed to increase crop output over the last 100 years.
ANSWER: FALSE
EXPLANATION: Paragraph A states that intensive agriculture significantly increased global crop yields.

2. No-till farming practices reduce soil erosion by over:
A) 30 percent
B) 45 percent
C) 60 percent
D) 80 percent
ANSWER: C
EXPLANATION: Paragraph B explicitly specifies that no-till farming reduces soil erosion by upwards of 60 percent.

3. Retaining crop residues helps stop evaporative ________ loss.
ANSWER: water
EXPLANATION: Paragraph B mentions preventing evaporative water loss.`;
}

// Toast Notification
function showToast(msg) {
  const toast = document.getElementById('toast');
  const msgEl = document.getElementById('toastMessage');
  if (!toast || !msgEl) return;

  msgEl.textContent = msg;
  toast.classList.remove('opacity-0', 'pointer-events-none');
  setTimeout(() => {
    toast.classList.add('opacity-0', 'pointer-events-none');
  }, 3000);
}
