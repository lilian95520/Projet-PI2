<template>
  <div class="app">
    <!-- Header -->
    <header class="header">
      <h1 class="header-title">Help center</h1>
    </header>

    <!-- Messages Container -->
    <main class="messages-container" ref="messagesEl">
      <div class="messages-wrapper">
        <div v-for="m in messages" :key="m.id" class="message-line" :class="m.role">
          <div v-if="m.role === 'assistant'" class="message assistant-message">
            <div class="avatar">🌐</div>
            <div class="content">
              <div class="bubble assistant-bubble">
                <div v-if="m.isHtml" v-html="m.text" class="html-content"></div>
                <div v-else>{{ m.text }}</div>
              </div>
            </div>
          </div>

          <div v-else class="message user-message">
            <div class="content">
              <div class="bubble user-bubble">{{ m.text }}</div>
            </div>
            <div class="avatar">👤</div>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="message-line assistant">
          <div class="message assistant-message">
            <div class="avatar">🌐</div>
            <div class="content">
              <div class="bubble assistant-bubble typing">
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Input Footer -->
    <footer class="footer">
      <div class="input-section">
        <div class="input-wrapper">
          <input
            v-model="query"
            type="text"
            class="input-field"
            placeholder="Posez votre question..."
            @keydown.enter.prevent="send"
            :disabled="loading"
          />
          <button class="btn-send" :disabled="loading || !query.trim()" @click="send">
            <span v-if="!loading">➤</span>
            <span v-else class="mini-spinner"></span>
          </button>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { nextTick, ref } from "vue";
import axios from "axios";

const API_BASE = "http://localhost:8000";
const query = ref("");
const loading = ref(false);
const messagesEl = ref(null);

const messages = ref([
  {
    id: crypto.randomUUID(),
    role: "assistant",
    text: "Bonjour ! Je suis votre assistant Helpcenter. Comment puis-je vous aider ?",
    isHtml: false,
  },
]);

function clear() {
  messages.value = [
    {
      id: crypto.randomUUID(),
      role: "assistant",
      text: "Conversation réinitialisée. Comment puis-je vous aider ?",
      isHtml: false,
    },
  ];
}

async function send() {
  const q = query.value.trim();
  if (!q || loading.value) return;

  messages.value.push({
    id: crypto.randomUUID(),
    role: "user",
    text: q,
    isHtml: false,
  });

  query.value = "";
  loading.value = true;

  try {
    const res = await axios.post(`${API_BASE}/ask`, { query: q });
    const html = res.data?.html ?? "";

    messages.value.push({
      id: crypto.randomUUID(),
      role: "assistant",
      text: html || "<p>Pas de réponse disponible.</p>",
      isHtml: true,
    });
  } catch (e) {
    messages.value.push({
      id: crypto.randomUUID(),
      role: "assistant",
      text: `Erreur: ${e?.message || e}`,
      isHtml: false,
    });
  } finally {
    loading.value = false;
    await nextTick();
    if (messagesEl.value) {
      messagesEl.value.scrollTop = messagesEl.value.scrollHeight;
    }
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #ffffff;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
  color: #1f2937;
}

/* ===== HEADER ===== */
.header {
  background: #2563eb;
  padding: 1rem 1.5rem;
  flex-shrink: 0;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: white;
  margin: 0;
}

/* ===== MESSAGES CONTAINER ===== */
.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 1rem 1.5rem;
  display: flex;
  flex-direction: column;
}

.messages-wrapper {
  max-width: 900px;
  margin: 0 auto;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.message-line {
  display: flex;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message {
  display: flex;
  gap: 0.75rem;
  width: 100%;
}

.assistant-message {
  justify-content: flex-start;
}

.user-message {
  justify-content: flex-end;
}

.avatar {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.message.assistant-message .avatar {
  background: #f3f4f6;
  border-radius: 50%;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-width: 600px;
}

.message.user-message .content {
  align-items: flex-end;
}

.bubble {
  padding: 0.6rem 0.85rem;
  line-height: 1.4;
  word-wrap: break-word;
  border-radius: 0.75rem;
  font-size: 0.95rem;
}

.assistant-bubble {
  background: #f3f4f6;
  color: #1f2937;
}

.user-bubble {
  background: #4f46e5;
  color: white;
}

/* HTML Content Styling */
.html-content {
  word-wrap: break-word;
}

.html-content :deep(p) {
  margin: 0.5rem 0;
}

.html-content :deep(p:first-child) {
  margin-top: 0;
}

.html-content :deep(p:last-child) {
  margin-bottom: 0;
}

.html-content :deep(a) {
  color: #4f46e5;
  text-decoration: none;
  font-weight: 500;
}

.html-content :deep(a:hover) {
  text-decoration: underline;
}

.html-content :deep(strong) {
  font-weight: 600;
}

/* Typing Indicator */
.typing {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.5rem 0.75rem;
}

.typing-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #d1d5db;
  animation: bounce 1.4s infinite;
}

.typing-dot:nth-child(1) {
  animation-delay: 0s;
}

.typing-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%, 60%, 100% {
    opacity: 0.5;
    transform: translateY(0);
  }
  30% {
    opacity: 1;
    transform: translateY(-8px);
  }
}

/* ===== FOOTER ===== */
.footer {
  background: white;
  padding: 0.75rem 1.5rem;
  flex-shrink: 0;
  border-top: 1px solid #f0f0f0;
}

.input-section {
  max-width: 900px;
  margin: 0 auto;
}

.input-wrapper {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.input-field {
  flex: 1;
  border: none;
  outline: none;
  padding: 0.6rem 0.85rem;
  font-size: 0.95rem;
  font-family: inherit;
  color: #1f2937;
  background: white;
  border-bottom: 1px solid #d1d5db;
  transition: all 0.2s;
}

.input-field:focus {
  border-bottom-color: #2563eb;
}

.input-field::placeholder {
  color: #9ca3af;
}

.input-field:disabled {
  color: #9ca3af;
}

.btn-send {
  background: none;
  border: none;
  color: #2563eb;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-send:hover:not(:disabled) {
  transform: scale(1.1);
  color: #1d4ed8;
}

.btn-send:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* Mini Spinner */
.mini-spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Scrollbar */
.messages-container::-webkit-scrollbar {
  width: 6px;
}

.messages-container::-webkit-scrollbar-track {
  background: transparent;
}

.messages-container::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}

/* Responsive */
@media (max-width: 640px) {
  .header {
    padding: 1rem;
  }

  .header-content {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }

  .messages-container {
    padding: 1rem;
  }

  .footer {
    padding: 1rem;
  }

  .content {
    max-width: 85vw;
  }

  .btn-reset {
    padding: 0.5rem 0.75rem;
    font-size: 0.75rem;
  }
}
</style>