const HISTORY_LIMIT = 20;
const LOGIN_PAGE_URL = "/login.html";

const historyEl = document.getElementById("history-list");
const resultEl = document.getElementById("result");
const innInputEl = document.getElementById("value");
const generateButtonEl = document.getElementById("generate-btn");
const userNameEl = document.getElementById("user-name");
const logoutButtonEl = document.getElementById("logout-btn");

function bindEvents() {
  document.addEventListener("DOMContentLoaded", initPage);
  generateButtonEl.addEventListener("click", send);
  logoutButtonEl.addEventListener("click", logout);
}

async function initPage() {
  const me = await getCurrentUser();

  if (!me) {
    redirectToLogin();
    return;
  }

  renderUserName(me);
  await loadHistory();
}

async function authFetch(url, options = {}, retry = true) {
  const response = await fetch(url, { credentials: "include", ...options });

  if (response.status !== 401) {
    return response;
  }

  if (!retry) {
    redirectToLogin();
    return response;
  }

  const refreshed = await tryRefresh();
  if (!refreshed) {
    redirectToLogin();
    return response;
  }

  return fetch(url, { credentials: "include", ...options });
}

async function getCurrentUser() {
  try {
    const response = await authFetch("/api/v1/auth/me");

    if (!response.ok) {
      return null;
    }

    return await response.json();
  } catch (error) {
    console.error("Ошибка получения пользователя:", error);
    return null;
  }
}

function renderUserName(user) {
  const name =
    user.username ||
    user.email ||
    user.login ||
    user.full_name ||
    "Пользователь";

  userNameEl.textContent = name;
}

async function tryRefresh() {
  try {
    const response = await fetch("/api/v1/auth/refresh", {
      method: "POST",
      credentials: "include"
    });

    return response.ok;
  } catch {
    return false;
  }
}

async function logout() {
  try {
    await fetch("/api/v1/auth/logout", {
      method: "POST",
      credentials: "include"
    });
  } finally {
    redirectToLogin();
  }
}

async function loadHistory() {
  setHistoryState("loading");

  try {
    const response = await authFetch(`/api/v1/user-requests?limit=${HISTORY_LIMIT}&offset=0`);

    if (!response.ok) {
      setHistoryState("error");
      return;
    }

    const data = await response.json();
    renderHistory(data.items || []);
  } catch (error) {
    console.error("Ошибка загрузки истории:", error);
    setHistoryState("error");
  }
}

function renderHistory(items) {
  historyEl.innerHTML = "";

  if (!items.length) {
    setHistoryState("empty");
    return;
  }

  const fragment = document.createDocumentFragment();

  for (const item of items) {
    const isSuccess = item.status === "success";
    const element = document.createElement("div");

    element.className = "history-item";

    if (isSuccess && item.inn) {
      element.classList.add("history-item-clickable");
      element.title = "Подставить ИНН в поле ввода";
      element.addEventListener("click", () => fillInn(item.inn));
    }

    element.innerHTML = `
      <div class="history-item-header">
        <span class="status-dot ${isSuccess ? "status-success" : "status-failed"}"></span>
        <div class="history-date">${formatDate(item.created_at)}</div>
      </div>
      <div class="history-line">ИНН: ${escapeHtml(item.inn || "—")}</div>
      <div class="history-line history-name">${escapeHtml(item.name || "—")}</div>
      ${
        !isSuccess && item.error_message
          ? `<div class="history-line history-error">Ошибка: ${escapeHtml(item.error_message)}</div>`
          : ""
      }
    `;

    fragment.appendChild(element);
  }

  historyEl.appendChild(fragment);
}

function fillInn(inn) {
  innInputEl.value = inn;
  innInputEl.focus();
  innInputEl.select();
}

function formatDate(value) {
  if (!value) {
    return "—";
  }

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return `${String(date.getDate()).padStart(2, "0")}.${String(date.getMonth() + 1).padStart(2, "0")}.${date.getFullYear()} ${String(date.getHours()).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")}`;
}

function setHistoryState(state) {
  const states = {
    loading: "<div class=\"history-loading\">Загрузка истории...</div>",
    empty: "<div class=\"history-empty\">История запросов пока пуста</div>",
    error: "<div class=\"history-error-state\">Ошибка загрузки истории</div>"
  };

  historyEl.innerHTML = states[state] || states.error;
}

async function send() {
  const inn = innInputEl.value.trim();

  if (!inn) {
    resultEl.textContent = "Введите ИНН";
    return;
  }

  generateButtonEl.disabled = true;
  resultEl.textContent = "Выполняется запрос...";

  try {
    const response = await authFetch(`/api/v1/generate/?inn=${encodeURIComponent(inn)}`);

    if (!response.ok) {
      resultEl.textContent = (await safeText(response)) || "Ошибка генерации документа";
      return;
    }

    const blob = await response.blob();
    downloadBlob(blob, `document_${inn}.docx`);
    resultEl.textContent = "Документ успешно сгенерирован";
  } catch (error) {
    console.error("Ошибка генерации:", error);
    resultEl.textContent = "Ошибка сети или сервера";
  } finally {
    generateButtonEl.disabled = false;
    await loadHistory();
  }
}

function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");

  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

async function safeText(response) {
  try {
    return await response.text();
  } catch {
    return "";
  }
}

function redirectToLogin() {
  window.location.href = LOGIN_PAGE_URL;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

bindEvents();
