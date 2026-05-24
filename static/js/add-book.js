// --- Валидация добавления книги (add_book.html) ---
(() => {
    const form = document.querySelector(
        'form[action="/add-book"], form[method="POST"]'
    );
    if (!form || !document.querySelector('[name="title"]')) return;

    const title = form.querySelector('[name="title"]');
    const author = form.querySelector('[name="author_name"]');
    const year = form.querySelector('[name="year"]');
    const cover = form.querySelector('[name="cover_url"]');

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

    function checkTitle() {
        if (!title.value.trim()) { setValidity(title, false, 'Название обязательно'); return false; }
        setValidity(title, true); return true;
    }

    function checkAuthor() {
        if (!author.value.trim()) { setValidity(author, false, 'Автор обязателен'); return false; }
        setValidity(author, true); return true;
    }

    function checkYear() {
        const v = year.value.trim();
        if (!v) { setValidity(year, true); return true; }
        const n = Number(v);
        if (!Number.isInteger(n) || n < 1000 || n > 2100) {
            setValidity(year, false, 'Год — число от 1000 до 2100');
            return false;
        }
        setValidity(year, true); return true;
    }

    function checkCover() {
        const v = cover.value.trim();
        if (!v) { setValidity(cover, true); return true; }
        if (!/^https?:\/\/.+/.test(v)) {
            setValidity(cover, false, 'URL должен начинаться с http:// или https://');
            return false;
        }
        setValidity(cover, true); return true;
    }

    title.addEventListener('input', checkTitle);
    author.addEventListener('input', checkAuthor);
    year.addEventListener('input', checkYear);
    cover.addEventListener('input', checkCover);

    form.addEventListener('submit', (e) => {
        const ok = checkTitle() && checkAuthor() && checkYear() && checkCover();
        if (!ok) e.preventDefault();
    });
})();

