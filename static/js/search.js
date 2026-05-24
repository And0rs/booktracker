// --- Поиск по каталогу (index.html) ---
(() => {
    const searchInput = document.getElementById('search');
    if (!searchInput) return;
    searchInput.addEventListener('input', ({ target }) => {
        const query    = target.value.toLowerCase();
        const wrappers = document.querySelectorAll('.book-card-wrapper');
        let foundAny   = false;
        wrappers.forEach((wrapper) => {
            const matches = wrapper.textContent.toLowerCase().includes(query);
            wrapper.style.display = matches ? '' : 'none';
            if (matches) foundAny = true;
        });
        const noBooksMessage = document.getElementById('no-books');
        if (noBooksMessage) {
            noBooksMessage.style.display = foundAny ? 'none' : '';
        }
    });
})();

