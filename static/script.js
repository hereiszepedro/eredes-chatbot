const chatMessages = document.getElementById("chat-messages");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const sendBtn = document.getElementById("send-btn");

const sessionId =
  "session-" + Math.random().toString(36).substring(2, 10);

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = chatInput.value.trim();
  if (!message) return;

  appendMessage(message, "user");
  chatInput.value = "";
  sendBtn.disabled = true;
  chatInput.disabled = true;

  const typingEl = showTyping();

  try {
    const resp = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId, message }),
    });

    if (!resp.ok) {
      const errData = await resp.json().catch(() => null);
      const detail = errData?.detail || `Erro ${resp.status}`;
      removeTyping(typingEl);
      appendMessage(detail, "bot");
      return;
    }

    const data = await resp.json();
    removeTyping(typingEl);
    appendMessage(data.reply, "bot");
  } catch (err) {
    removeTyping(typingEl);
    appendMessage(
      "Peço desculpa, ocorreu um erro ao processar o seu pedido. " +
        "Por favor, tente novamente ou contacte a Linha de Avarias: 800 506 506.",
      "bot"
    );
  } finally {
    sendBtn.disabled = false;
    chatInput.disabled = false;
    chatInput.focus();
  }
});

function appendMessage(text, sender) {
  const msgDiv = document.createElement("div");
  msgDiv.className = `message ${sender === "user" ? "user-message" : "bot-message"}`;

  const contentDiv = document.createElement("div");
  contentDiv.className = "message-content";

  if (sender === "bot") {
    contentDiv.innerHTML = formatMarkdown(text);
  } else {
    contentDiv.textContent = text;
  }

  msgDiv.appendChild(contentDiv);
  chatMessages.appendChild(msgDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTyping() {
  const typing = document.createElement("div");
  typing.className = "message bot-message typing-wrapper";
  typing.innerHTML =
    '<div class="typing-indicator"><span></span><span></span><span></span></div>';
  chatMessages.appendChild(typing);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return typing;
}

function removeTyping(el) {
  if (el && el.parentNode) {
    el.parentNode.removeChild(el);
  }
}

function formatMarkdown(text) {
  // Basic markdown-to-HTML conversion for bot responses
  let html = text
    // Bold
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    // Italic
    .replace(/\*(.+?)\*/g, "<em>$1</em>")
    // Links
    .replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
    // Line breaks
    .replace(/\n/g, "<br>");

  // Simple list handling: lines starting with - or *
  html = html.replace(
    /(?:(?:^|<br>)\s*[-*]\s+.+(?:<br>|$))+/g,
    (match) => {
      const items = match
        .split("<br>")
        .filter((line) => line.trim().match(/^[-*]\s+/))
        .map((line) => `<li>${line.trim().replace(/^[-*]\s+/, "")}</li>`)
        .join("");
      return `<ul>${items}</ul>`;
    }
  );

  return html;
}
