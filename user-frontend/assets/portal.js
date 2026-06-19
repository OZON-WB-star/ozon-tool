(function () {
  function setMessage(el, text, isError) {
    if (!el) return;
    el.textContent = text;
    el.style.display = text ? "block" : "none";
    el.style.color = isError ? "#d14343" : "#2b7a4b";
  }

  async function bindLoginForm() {
    const form = document.querySelector("[data-login-form]");
    if (!form || !window.DaeApi) return;

    const message = form.querySelector("[data-form-message]");
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(form);

      try {
        setMessage(message, "正在登录并同步用户信息...", false);
        const payload = {
          account: String(formData.get("account") || "").trim(),
          password: String(formData.get("password") || "").trim(),
        };
        const result = await window.DaeApi.login(payload);
        window.DaeApi.setSession(result.access_token, result.user_id);
        setMessage(message, "登录成功，正在进入用户中心。", false);
        window.setTimeout(() => {
          window.location.href = window.location.pathname.includes("admin-frontend") ? "index.html" : "account.html";
        }, 500);
      } catch (error) {
        setMessage(message, error.message || "登录失败，请检查账号信息。", true);
      }
    });
  }

  async function bindRegisterForm() {
    const form = document.querySelector("[data-register-form]");
    if (!form || !window.DaeApi) return;

    const message = form.querySelector("[data-form-message]");
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(form);

      const payload = {
        name: String(formData.get("name") || "").trim(),
        phone: String(formData.get("phone") || "").trim(),
        email: String(formData.get("email") || "").trim(),
        focus: String(formData.get("focus") || "").trim(),
        password: String(formData.get("password") || "").trim(),
        invite_code: String(formData.get("invite_code") || "").trim() || null,
      };

      try {
        setMessage(message, "正在创建账号...", false);
        await window.DaeApi.register(payload);
        const loginResult = await window.DaeApi.login({
          account: payload.email,
          password: payload.password,
        });
        window.DaeApi.setSession(loginResult.access_token, loginResult.user_id);
        setMessage(message, "注册成功，正在进入用户中心。", false);
        window.setTimeout(() => {
          window.location.href = window.location.pathname.includes("admin-frontend") ? "index.html" : "account.html";
        }, 500);
      } catch (error) {
        setMessage(message, error.message || "注册失败，请稍后重试。", true);
      }
    });
  }

  async function bindStoreForm() {
    const form = document.querySelector("[data-store-form]");
    if (!form || !window.DaeApi) return;

    const message = form.querySelector("[data-form-message]");
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(form);

      const payload = {
        name: String(formData.get("name") || "").trim(),
        site: String(formData.get("site") || "").trim(),
        auth: String(formData.get("auth") || "").trim(),
        client_id: String(formData.get("client_id") || "").trim() || null,
        api_key: String(formData.get("api_key") || "").trim() || null,
        owner_email: String(formData.get("owner_email") || "").trim(),
        note: String(formData.get("note") || "").trim() || null,
        test_now: formData.get("test_now") === "on",
      };

      try {
        setMessage(message, "正在提交店铺接入信息...", false);
        await window.DaeApi.connectStore(payload);
        setMessage(message, "店铺接入信息已提交，授权状态已写入系统，正在跳转。", false);
        window.setTimeout(() => {
          window.location.href = window.location.pathname.includes("admin-frontend") ? "index.html" : "account.html";
        }, 700);
      } catch (error) {
        setMessage(message, error.message || "提交失败，请检查参数。", true);
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => {
      bindLoginForm();
      bindRegisterForm();
      bindStoreForm();
    });
  } else {
    bindLoginForm();
    bindRegisterForm();
    bindStoreForm();
  }
})();
