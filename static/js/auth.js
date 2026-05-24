// --- Переключение login/register (login.html) ---
const toggleForm = (e) => {
    e.preventDefault();
    const titleEl = document.getElementById('form-title');
    const emailGroup = document.getElementById('email-group');
    const submitBtn = document.getElementById('submit-btn');
    const toggleLink = document.getElementById('toggle-link');
    const actionInput = document.querySelector('input[name="action"]');
    const emailInput = document.querySelector('input[name="email"]');
    const isLoginMode = titleEl.textContent === 'Вход';
    if (isLoginMode) {
        titleEl.textContent = 'Регистрация';
        emailGroup.style.display = 'block';
        submitBtn.textContent = 'Зарегистрироваться';
        toggleLink.textContent = 'Уже есть аккаунт? Войти';
        actionInput.value = 'register';
    } else {
        titleEl.textContent = 'Вход';
        emailGroup.style.display = 'none';
        submitBtn.textContent = 'Войти';
        toggleLink.textContent = 'Нет аккаунта? Зарегистрироваться';
        actionInput.value = 'login';
        emailInput.classList.remove('is-valid', 'is-invalid');
        const fb = emailInput.parentElement.querySelector('.invalid-feedback');
        if (fb) fb.textContent = '';
    }
};

document.getElementById('toggle-link')?.addEventListener('click', toggleForm);

// --- Валидация регистрации ---
(() => {
    const actionInput = document.querySelector('input[name="action"]');
    if (!actionInput) return;
    const form = actionInput.closest('form');
    const username = form.querySelector('[name="username"]');
    const email = form.querySelector('[name="email"]');
    const password = form.querySelector('[name="password"]');

    function setValidity(input, valid, message) {
        const fb = input.parentElement.querySelector('.invalid-feedback');
        input.classList.remove('is-valid', 'is-invalid');
        if (valid) {
            input.classList.add('is-valid');
            if (fb) fb.textContent = '';
        } else {
            input.classList.add('is-invalid');
            if (fb) fb.textContent = message;
        }
    }

    function checkUsername() {
        const v = username.value.trim();
        if (!v) { setValidity(username, false, 'Логин обязателен'); return false; }
        if (v.length < 3) { setValidity(username, false, 'Логин — минимум 3 символа'); return false; }
        setValidity(username, true); return true;
    }

    function checkEmail() {
        const v = email.value.trim();
        if (!v) { setValidity(email, false, 'Email обязателен'); return false; }
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) { setValidity(email, false, 'Введите полный email'); return false; }
        setValidity(email, true); return true;
    }

    function checkPassword() {
        const v = password.value;
        if (!v) { setValidity(password, false, 'Пароль обязателен'); return false; }
        if (v.length < 6) { setValidity(password, false, 'Пароль — минимум 6 символов'); return false; }
        setValidity(password, true); return true;
    }

    username.addEventListener('input', checkUsername);
    email.addEventListener('input', checkEmail);
    password.addEventListener('input', checkPassword);

    form.addEventListener('submit', (e) => {
        if (actionInput.value !== 'register') return;
        const ok = checkUsername() && checkEmail() && checkPassword();
        if (!ok) e.preventDefault();
    });
})();

