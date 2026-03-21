const LOGIN_FORM = {
  username: document.getElementById("login"),
  password: document.getElementById("password"),
  error: document.getElementById("error"),
  button: document.getElementById("login-btn")
};

function bindEvents() {
  document.addEventListener("DOMContentLoaded", checkExistingSession);
  LOGIN_FORM.button.addEventListener("click", login);
  LOGIN_FORM.password.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      login();
    }
  });
}

async function checkExistingSession() {
  try {
    const response = await fetch("/api/v1/auth/me", {
      method: "GET",
      credentials: "include"
    });

    if (response.ok) {
      window.location.href = "/";
    }
  } catch (error) {
    console.error("Session check error:", error);
  }
}

async function login() {
  clearError();

  const username = LOGIN_FORM.username.value.trim();
  const password = LOGIN_FORM.password.value;

  if (!username || !password) {
    showError("Введите логин и пароль");
    return;
  }

  LOGIN_FORM.button.disabled = true;

  try {
    const response = await fetch("/api/v1/auth/login", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ username, password })
    });

    if (!response.ok) {
      const data = await safeJson(response);
      showError(data?.detail || "Неверный логин или пароль");
      return;
    }

    window.location.href = "/";
  } catch (error) {
    console.error("Login error:", error);
    showError("Ошибка сети или сервера");
  } finally {
    LOGIN_FORM.button.disabled = false;
  }
}

function showError(message) {
  LOGIN_FORM.error.textContent = message;
}

function clearError() {
  LOGIN_FORM.error.textContent = "";
}

async function safeJson(response) {
  try {
    return await response.json();
  } catch {
    return null;
  }
}

bindEvents();
