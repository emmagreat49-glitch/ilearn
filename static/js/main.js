// ── CSRF helper — reads token from meta tag ──────────────────────
function getCsrfToken() {
  var meta = document.querySelector('meta[name="csrf-token"]');
  return meta ? meta.getAttribute('content') : '';
}

// Wrap fetch to automatically include CSRF header on POST/DELETE requests
function apiFetch(url, options) {
  options = options || {};
  var method = (options.method || 'GET').toUpperCase();
  if (method !== 'GET') {
    options.headers = options.headers || {};
    options.headers['X-CSRF-Token'] = getCsrfToken();
  }
  return fetch(url, options);
}

/**
 * iLEARN — Global JavaScript
 * Covers: Toast, API helpers, Quiz, Chatbot, Reminders + Browser Notifications, Animations
 */

// ══════════════════════════════════════
// TOAST NOTIFICATION
// ══════════════════════════════════════
const Toast = {
  el: null,
  _timer: null,

  init() {
    if (!document.getElementById("toast")) {
      const t = document.createElement("div");
      t.id = "toast";
      document.body.appendChild(t);
    }
    this.el = document.getElementById("toast");
  },

  show(message, type, duration) {
    type = type || "info";
    duration = duration || 3500;
    if (!this.el) this.init();
    const icons = { success: "✅", error: "❌", info: "ℹ️", warning: "⏰" };
    this.el.innerHTML = "<span>" + (icons[type] || "ℹ️") + "</span> " + message;
    this.el.className = "show toast-" + type;
    clearTimeout(this._timer);
    this._timer = setTimeout(() => { this.el.className = ""; }, duration);
  },

  success(m) { this.show(m, "success"); },
  error(m)   { this.show(m, "error"); },
  info(m)    { this.show(m, "info"); },
  warning(m) { this.show(m, "warning", 8000); }
};

// ══════════════════════════════════════
// API HELPER
// ══════════════════════════════════════
const API = {
  async post(url, data) {
    try {
      const r = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
      return await r.json();
    } catch (e) { return { status: "error", message: "Network error" }; }
  },
  async get(url) {
    try { return await (await fetch(url)).json(); }
    catch (e) { return null; }
  },
  async del(url) {
    try { return await (await fetch(url, { method: "DELETE" })).json(); }
    catch (e) { return { status: "error" }; }
  }
};

// ══════════════════════════════════════
// REMINDERS + BROWSER NOTIFICATIONS
// ══════════════════════════════════════
const Reminders = {
  _interval: null,

  async add(text, time) {
    const result = await API.post("/api/add_reminder", { text: text, time: time });
    if (result.status === "ok") {
      Toast.success("Reminder saved! You will get a browser notification when it is time.");
      return true;
    }
    Toast.error(result.message || "Failed to save reminder.");
    return false;
  },

  async delete(id, rowEl) {
    const result = await API.del("/api/delete_reminder/" + id);
    if (result.status === "ok") {
      if (rowEl) {
        rowEl.style.transition = "all 0.3s ease";
        rowEl.style.opacity = "0";
        rowEl.style.transform = "translateX(20px)";
        setTimeout(function() { rowEl.remove(); }, 320);
      }
      Toast.success("Reminder deleted.");
    } else {
      Toast.error("Failed to delete reminder.");
    }
  },

  // Request notification permission from the browser and start the checker
  async initNotifications() {
    // Only run when a logged-in nav is present
    if (!document.querySelector(".nav-avatar")) return;
    if (!("Notification" in window)) return;

    // ── DO NOT call Notification.requestPermission() here ──
    // Chrome 74+ blocks permission prompts that are NOT triggered by a user
    // gesture (click/tap). Calling it in DOMContentLoaded silently fails.
    // The dashboard shows an "Enable Now" button — that click IS a user
    // gesture and is where permission gets requested.
    //
    // Here we only START the checker if the user already granted permission.
    if (Notification.permission === "granted") {
      this.checkDue();
      this._interval = setInterval(function() { Reminders.checkDue(); }, 30000);
    }
    // If permission is "default", the dashboard banner will appear and
    // the user can click "Enable Now" which calls requestNotifPerm().
    // After they grant it, the next page load will hit the "granted" branch.
  },

  async checkDue() {
    if (Notification.permission !== "granted") return;

    const reminders = await API.get("/api/reminders");
    if (!reminders || !Array.isArray(reminders)) return;

    const now = new Date();

    reminders.forEach(function(r) {
      // datetime-local stores "2026-03-11T14:30" with NO timezone suffix.
      // new Date("2026-03-11T14:30") is parsed as UTC in most browsers, which
      // is wrong — it shifts the time by the user's UTC offset.
      // Fix: append ":00" if needed then use Date.parse with a local-time trick:
      // splitting and constructing via new Date(y, m, d, h, min) which always
      // uses LOCAL time.
      var reminderTime;
      try {
        var t = r.time.replace("T", " "); // "2026-03-11 14:30" or "2026-03-11 14:30:00"
        var parts = t.split(/[\s:\-]/);
        // parts: [year, month, day, hour, minute, (second)]
        reminderTime = new Date(
          parseInt(parts[0]),
          parseInt(parts[1]) - 1,  // month is 0-indexed
          parseInt(parts[2]),
          parseInt(parts[3] || 0),
          parseInt(parts[4] || 0),
          0
        );
      } catch(e) {
        reminderTime = new Date(r.time); // fallback
      }

      var diffMs = reminderTime - now;

      // Fire if within a wider window: up to 10 minutes AFTER due time and
      // up to 2 minutes BEFORE (in case the poll fires slightly early).
      // 10 minutes past = -600000ms,  2 minutes early = +120000ms
      if (diffMs >= -600000 && diffMs <= 120000) {
        var key = "ilearn_fired_" + r.id;
        if (!sessionStorage.getItem(key)) {
          sessionStorage.setItem(key, "1");
          Reminders.fire(r);
        }
      }
    });
  },

  fire(reminder) {
    // Show desktop notification
    var notif = new Notification("iLEARN Study Reminder", {
      body: reminder.text,
      tag: "reminder-" + reminder.id,
      requireInteraction: true
    });

    notif.onclick = function() {
      window.focus();
      notif.close();
    };

    // Also show in-app toast
    Toast.warning("Reminder: " + reminder.text);
  }
};

// ══════════════════════════════════════
// PROGRESS BARS
// ══════════════════════════════════════
function animateProgressBars() {
  document.querySelectorAll(".progress-fill[data-pct]").forEach(function(bar) {
    var pct = parseInt(bar.dataset.pct) || 0;
    bar.style.width = "0%";
    setTimeout(function() { bar.style.width = pct + "%"; }, 150);
  });
}

// ══════════════════════════════════════
// SCROLL REVEAL
// ══════════════════════════════════════
function initScrollReveal() {
  if (!window.IntersectionObserver) return;
  var obs = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add("revealed");
        obs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08, rootMargin: "0px 0px -30px 0px" });

  document.querySelectorAll(".reveal").forEach(function(el) { obs.observe(el); });
}

// ══════════════════════════════════════
// LESSON COMPLETE + LIVE PROGRESS UPDATE
// ══════════════════════════════════════
async function markLessonComplete(lessonId, btn) {
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Saving...';
  const result = await API.post("/api/complete_lesson", { lesson_id: lessonId });
  if (result.status === "ok") {
    btn.innerHTML = "✅ Completed!";
    btn.className = btn.className.replace("btn-success", "btn-ghost");
    Toast.success("Lesson marked as complete!");

    // Update the completion status badge in the lesson header
    document.querySelectorAll(".completion-status").forEach(function(el) {
      el.textContent = "Completed";
      el.className = "badge badge-green completion-status";
    });

    // ── Live-update the course progress bar ─────────────────────
    // The lesson page stores COURSE_ID if set by the template.
    // After marking complete, we fetch fresh progress and animate
    // any .course-progress-bar or .prog-panel elements on the page.
    var courseId = window.COURSE_ID || null;
    if (courseId) {
      try {
        var prog = await API.get("/api/course_progress/" + courseId);
        if (prog && typeof prog.percent === "number") {
          // Update any progress fill bars tagged with data-course-id
          document.querySelectorAll("[data-course-id='" + courseId + "'] .progress-fill, .lesson-course-prog-fill").forEach(function(bar) {
            bar.style.width = prog.percent + "%";
            bar.dataset.pct  = prog.percent;
          });
          // Update the inline course progress text
          var progText = document.getElementById("course-prog-text");
          if (progText) {
            progText.textContent = prog.completed + " / " + prog.total + " lessons complete (" + prog.percent + "%)";
          }
          // Update the big percentage in the lesson header
          var progPct = document.getElementById("course-prog-pct");
          if (progPct) progPct.textContent = prog.percent + "%";

          // If course is now 100% done, show a congratulation toast
          if (prog.percent === 100) {
            setTimeout(function() {
              Toast.success("🏆 Course complete! Fantastic work!");
            }, 800);
          }
        }
      } catch (e) {
        // Non-critical — progress update can fail silently
        console.warn("[iLEARN] Progress update failed:", e);
      }
    }
  } else {
    btn.disabled = false;
    btn.innerHTML = "Mark Complete";
    Toast.error(result.message || "Failed to save. Please try again.");
  }
}

// ══════════════════════════════════════
// QUIZ
// ══════════════════════════════════════
const Quiz = {
  score: 0,
  answered: {},

  checkAnswer(questionId, selected, correct, optionEl) {
    if (this.answered[questionId]) return;
    this.answered[questionId] = true;

    var questionEl = optionEl.closest(".quiz-q") || optionEl.closest(".quiz-question");
    questionEl.querySelectorAll(".quiz-option").forEach(function(opt) {
      opt.disabled = true;
      if (opt.dataset.value === correct) opt.classList.add("correct");
    });

    if (selected === correct) {
      optionEl.classList.add("correct");
      Quiz.score++;
      Toast.success("Correct!");
    } else {
      optionEl.classList.add("wrong");
      Toast.error("Incorrect — correct answer is highlighted.");
    }

    var scoreEl = document.getElementById("quiz-score");
    if (scoreEl) {
      scoreEl.textContent = Quiz.score + " / " + Object.keys(Quiz.answered).length;
    }
  }
};

// ══════════════════════════════════════
// AI CHATBOT
// ══════════════════════════════════════
const Chatbot = {
  async send() {
    var input    = document.getElementById("chat-input");
    var messages = document.getElementById("chat-messages");
    var msg      = input.value.trim();
    if (!msg) return;

    this.addMessage(msg, "user");
    input.value = "";

    var typingId = "typing-" + Date.now();
    messages.insertAdjacentHTML("beforeend",
      '<div class="chat-msg bot" id="' + typingId + '"><span class="spinner"></span> Thinking...</div>');
    messages.scrollTop = messages.scrollHeight;

    // Include lesson context if set by the page (lesson.html sets window.LESSON_CONTEXT)
    var payload = { message: msg };
    if (window.LESSON_CONTEXT) {
      payload.lesson_title  = window.LESSON_CONTEXT.lesson_title  || "";
      payload.course_title  = window.LESSON_CONTEXT.course_title  || "";
    }

    var result   = await API.post("/api/chat", payload);
    var typingEl = document.getElementById(typingId);
    if (typingEl) typingEl.remove();
    this.addMessage((result && result.reply) ? result.reply : "Sorry, I could not process that.", "bot");
  },

  addMessage(text, role) {
    var messages = document.getElementById("chat-messages");
    var div      = document.createElement("div");
    div.className   = "chat-msg " + role;
    div.textContent = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  },

  handleKeypress(e) {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); this.send(); }
  }
};

// ══════════════════════════════════════
// TYPEWRITER CODE ANIMATION
// ══════════════════════════════════════
function initTypewriters() {
  if (!window.IntersectionObserver) return;
  document.querySelectorAll(".typewriter-code").forEach(function(block) {
    var code = block.dataset.code || block.textContent.trim();
    block.dataset.code = code;
    block.textContent = "";

    var obs = new IntersectionObserver(function(entries) {
      if (!entries[0].isIntersecting) return;
      obs.disconnect();

      var i = 0;
      var speed = parseInt(block.dataset.speed) || 18;

      function type() {
        if (i < code.length) {
          block.textContent += code[i++];
          var pre = block.closest("pre");
          if (pre) pre.scrollTop = pre.scrollHeight;
          setTimeout(type, speed);
        }
      }
      setTimeout(type, 400);
    }, { threshold: 0.4 });

    obs.observe(block);
  });
}

// ══════════════════════════════════════
// FLIP CARDS
// ══════════════════════════════════════
function initFlipCards() {
  document.querySelectorAll(".flip-card").forEach(function(card) {
    card.addEventListener("click", function() {
      card.classList.toggle("flipped");
    });
  });
}

// ══════════════════════════════════════
// STEP-BY-STEP ANIMATOR
// ══════════════════════════════════════
function initStepAnimators() {
  document.querySelectorAll(".step-animator").forEach(function(anim) {
    var steps = anim.querySelectorAll(".step-item");
    var counter = anim.querySelector(".step-counter");
    var current = 0;

    function showStep(idx) {
      steps.forEach(function(s, i) {
        s.classList.toggle("active", i === idx);
        s.classList.toggle("done", i < idx);
      });
      if (counter) counter.textContent = (idx + 1) + " / " + steps.length;
    }

    showStep(0);

    var nextBtn = anim.querySelector(".step-next");
    var prevBtn = anim.querySelector(".step-prev");

    if (nextBtn) nextBtn.addEventListener("click", function() {
      if (current < steps.length - 1) showStep(++current);
    });
    if (prevBtn) prevBtn.addEventListener("click", function() {
      if (current > 0) showStep(--current);
    });
  });
}

// ══════════════════════════════════════
// DOM READY
// ══════════════════════════════════════
document.addEventListener("DOMContentLoaded", function() {
  Toast.init();
  animateProgressBars();
  initScrollReveal();
  initFlipCards();
  initStepAnimators();
  initTypewriters();
  Reminders.initNotifications();

  // Reminder form submit
  var reminderForm = document.getElementById("reminder-form");
  if (reminderForm) {
    reminderForm.addEventListener("submit", async function(e) {
      e.preventDefault();
      var text = document.getElementById("reminder-text").value.trim();
      var time = document.getElementById("reminder-time").value;
      if (!text || !time) { Toast.error("Please fill in all fields."); return; }
      var ok = await Reminders.add(text, time);
      if (ok) setTimeout(function() { location.reload(); }, 1000);
    });
  }
});
