const messagesEl = document.getElementById("messages");
const composer = document.getElementById("composer");
const input = document.getElementById("input");
const sendBtn = document.getElementById("send-btn");
const patternList = document.getElementById("pattern-list");
const clearFilter = document.getElementById("clear-filter");
const sidebar = document.getElementById("sidebar");
const menuBtn = document.getElementById("menu-btn");
const statusLine = document.getElementById("status-line");
const chatTitle = document.getElementById("chat-title");

let patterns = [];
let selectedPattern = null;
let history = [];

marked.setOptions({ breaks: true, gfm: true });

async function init() {
  try {
    const [healthRes, patternsRes] = await Promise.all([
      fetch("/api/health"),
      fetch("/api/patterns"),
    ]);
    const health = await healthRes.json();
    patterns = await patternsRes.json();
    renderPatterns();
    const mode = health.mock_mode ? "mock mode" : `${health.llm_provider} / ${health.llm_model}`;
    statusLine.textContent = `${health.chunks} chunks indexed · ${mode}`;
  } catch (err) {
    statusLine.textContent = "API unavailable";
    console.error(err);
  }

  appendWelcome();
}

function renderPatterns() {
  patternList.innerHTML = "";
  patterns.forEach((p) => {
    const btn = document.createElement("button");
    btn.className = "pattern-chip";
    btn.dataset.number = p.number;
    btn.innerHTML = `<span class="num">${String(p.number).padStart(2, "0")}</span>${p.name}`;
    btn.addEventListener("click", () => selectPattern(p));
    patternList.appendChild(btn);
  });
}

function selectPattern(pattern) {
  selectedPattern = pattern;
  chatTitle.textContent = `Pattern ${String(pattern.number).padStart(2, "0")}: ${pattern.name}`;
  clearFilter.hidden = false;
  document.querySelectorAll(".pattern-chip").forEach((el) => {
    el.classList.toggle("active", Number(el.dataset.number) === pattern.number);
  });
  sidebar.classList.remove("open");
}

clearFilter.addEventListener("click", () => {
  selectedPattern = null;
  chatTitle.textContent = "Pattern Assistant";
  clearFilter.hidden = true;
  document.querySelectorAll(".pattern-chip").forEach((el) => el.classList.remove("active"));
});

menuBtn.addEventListener("click", () => sidebar.classList.toggle("open"));

function appendWelcome() {
  const div = document.createElement("div");
  div.className = "message assistant welcome";
  div.innerHTML = `<div class="content"><p>Ask about any of the <strong>21 agentic design patterns</strong>. I can explain concepts, compare patterns, and provide runnable Python recipes from this repo.</p><p>Pick a pattern in the sidebar or try: <em>"Show me a prompt chaining recipe"</em></p></div>`;
  messagesEl.appendChild(div);
}

function addMessage(role, content) {
  const div = document.createElement("div");
  div.className = `message ${role}`;
  const inner = document.createElement("div");
  inner.className = "content";
  if (role === "assistant") {
    inner.innerHTML = renderMarkdown(content);
    attachCopyButtons(inner);
  } else {
    inner.textContent = content;
  }
  div.appendChild(inner);
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return inner;
}

function renderMarkdown(text) {
  return marked.parse(text || "");
}

function attachCopyButtons(container) {
  container.querySelectorAll("pre").forEach((pre) => {
    const btn = document.createElement("button");
    btn.className = "copy-btn";
    btn.textContent = "Copy";
    btn.addEventListener("click", async () => {
      const code = pre.querySelector("code");
      const text = code ? code.innerText : pre.innerText;
      await navigator.clipboard.writeText(text);
      btn.textContent = "Copied!";
      setTimeout(() => { btn.textContent = "Copy"; }, 1200);
    });
    pre.style.position = "relative";
    pre.appendChild(btn);
  });
}

composer.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;

  input.value = "";
  sendBtn.disabled = true;
  addMessage("user", text);
  history.push({ role: "user", content: text });

  const assistantContent = addMessage("assistant", "…");
  let full = "";

  try {
    const body = {
      messages: history,
      pattern_number: selectedPattern?.number ?? null,
      stream: true,
    };
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || res.statusText);
    }

    const contentType = res.headers.get("content-type") || "";
    if (contentType.includes("text/event-stream")) {
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        for (const line of chunk.split("\n")) {
          if (!line.startsWith("data: ")) continue;
          const payload = JSON.parse(line.slice(6));
          if (payload.token) {
            full += payload.token;
            assistantContent.innerHTML = renderMarkdown(full);
            attachCopyButtons(assistantContent);
            messagesEl.scrollTop = messagesEl.scrollHeight;
          }
        }
      }
    } else {
      const data = await res.json();
      full = data.message || "";
      assistantContent.innerHTML = renderMarkdown(full);
      attachCopyButtons(assistantContent);
    }
    history.push({ role: "assistant", content: full });
  } catch (err) {
    assistantContent.innerHTML = `<p style="color:#f88">Error: ${err.message}</p>`;
  } finally {
    sendBtn.disabled = false;
    input.focus();
  }
});

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    composer.requestSubmit();
  }
});

init();
