<template>
  <div class="app">
    <header class="topbar">
      <div class="left">
        <div class="avatar bot">🤖</div>
        <div>
          <div class="title">Helpcenter Bot</div>
          <div class="sub">En ligne · FastAPI</div>
        </div>
      </div>
      <div class="right">
        <button class="icon" @click="clear">🧹</button>
      </div>
    </header>

    <main class="chat" ref="chatEl">
      <div class="day">Aujourd’hui</div>

      <div v-for="m in messages" :key="m.id" class="row" :class="m.role">
        <div class="avatar" :class="m.role">
          <span v-if="m.role === 'assistant'">🤖</span>
          <span v-else>🧑</span>
        </div>

        <div class="bubble">
          <div v-if="m.isHtml" v-html="m.text"></div>
          <div v-else>{{ m.text }}</div>
          <div class="meta">{{ m.time }}</div>
        </div>
      </div>

      <div v-if="loading" class="row assistant">
        <div class="avatar assistant">🤖</div>
        <div class="bubble typing">
          <span class="dot"></span><span class="dot"></span><span class="dot"></span>
        </div>
      </div>
    </main>

    <footer class="composer">
      <button class="icon" title="Exemples" @click="fillExample">✨</button>

      <input
        v-model="query"
        class="input"
        placeholder="Écris ta question…"
        @keydown.enter.prevent="send"
      />

      <button class="send" :disabled="loading || !query.trim()" @click="send">
        ➤
      </button>
    </footer>
  </div>
</template>

<script setup>
import { nextTick, ref } from "vue";
import axios from "axios";

const API_BASE = "http://localhost:8000"; // ton FastAPI
const query = ref("");
const loading = ref(false);
const chatEl = ref(null);

const messages = ref([
  {
    id: crypto.randomUUID(),
    role: "assistant",
    text: "Salut 👋 Pose-moi une question.",
    isHtml: false,
    time: timeStr(),
  },
]);

function timeStr() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function clear() {
  messages.value = [
    {
      id: crypto.randomUUID(),
      role: "assistant",
      text: "OK, on repart de zéro. Pose ta question 🙂",
      isHtml: false,
      time: timeStr(),
    },
  ];
}

function fillExample() {
  query.value = "Je veux la bourse";
}

async function send() {
  const q = query.value.trim();
  if (!q || loading.value) return;

  messages.value.push({
    id: crypto.randomUUID(),
    role: "user",
    text: q,
    isHtml: false,
    time: timeStr(),
  });

  query.value = "";
  loading.value = true;

  try {
    const res = await axios.post(`${API_BASE}/ask`, { query: q });
    const html = res.data?.html ?? "";
    messages.value.push({
      id: crypto.randomUUID(),
      role: "assistant",
      text: html || "<p>(réponse vide)</p>",
      isHtml: true,
      time: timeStr(),
    });
  } catch (e) {
    messages.value.push({
      id: crypto.randomUUID(),
      role: "assistant",
      text: `Erreur API: ${e?.message || e}`,
      isHtml: false,
      time: timeStr(),
    });
  } finally {
    loading.value = false;
    await nextTick();
    chatEl.value?.scrollTo({ top: chatEl.value.scrollHeight, behavior: "smooth" });
  }
}
</script>

<style>
/* layout */
.app{
  height:100vh;
  display:flex;
  flex-direction:column;
  font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
  background:#0e141b;
  color:#e9eef5;
}

/* top bar */
.topbar{
  display:flex;
  justify-content:space-between;
  align-items:center;
  padding:12px 14px;
  background:#101a24;
  border-bottom:1px solid #1f2a37;
}
.left{ display:flex; gap:10px; align-items:center; }
.title{ font-weight:700; line-height:1.1; }
.sub{ font-size:12px; opacity:.75; }

/* chat area */
.chat{
  flex:1;
  overflow:auto;
  padding:14px;
  display:flex;
  flex-direction:column;
  gap:10px;
}
.day{
  align-self:center;
  font-size:12px;
  opacity:.7;
  background:#111b26;
  border:1px solid #1f2a37;
  padding:6px 10px;
  border-radius:999px;
}

/* message rows */
.row{
  display:flex;
  gap:10px;
  align-items:flex-end;
}
.row.user{
  flex-direction:row-reverse;
}
.avatar{
  width:34px;
  height:34px;
  border-radius:999px;
  display:flex;
  align-items:center;
  justify-content:center;
  border:1px solid #1f2a37;
  background:#111b26;
  flex:0 0 auto;
}
.avatar.user{ background:#17253a; }
.avatar.assistant{ background:#131f2c; }
.avatar.bot{ background:#131f2c; }

/* bubbles */
.bubble{
  max-width:min(820px, 85%);
  padding:10px 12px;
  border-radius:14px;
  border:1px solid #1f2a37;
  background:#111b26;
  position:relative;
}
.row.user .bubble{
  background:#17304a;
}
.meta{
  margin-top:6px;
  font-size:11px;
  opacity:.65;
  text-align:right;
}

/* typing */
.typing{ display:flex; gap:6px; align-items:center; }
.dot{
  width:8px; height:8px; border-radius:999px;
  background:#d6dde8;
  opacity:.5;
  animation: blink 1s infinite;
}
.dot:nth-child(2){ animation-delay:.2s; }
.dot:nth-child(3){ animation-delay:.4s; }
@keyframes blink{
  0%, 100%{ opacity:.25; transform: translateY(0); }
  50%{ opacity:.9; transform: translateY(-2px); }
}

/* composer */
.composer{
  display:flex;
  gap:10px;
  padding:12px;
  background:#101a24;
  border-top:1px solid #1f2a37;
  align-items:center;
}
.input{
  flex:1;
  padding:12px 14px;
  border-radius:999px;
  border:1px solid #1f2a37;
  background:#0e141b;
  color:#e9eef5;
  outline:none;
}
.icon{
  width:42px; height:42px;
  border-radius:999px;
  border:1px solid #1f2a37;
  background:#111b26;
  color:#e9eef5;
  cursor:pointer;
}
.send{
  width:46px; height:46px;
  border-radius:999px;
  border:1px solid #1f2a37;
  background:#1b3656;
  color:#e9eef5;
  cursor:pointer;
  font-size:18px;
}
.send:disabled{ opacity:.5; cursor:not-allowed; }
</style>