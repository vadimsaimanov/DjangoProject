// Только общие функции, используемые на всех страницах
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
}

// Общие обработчики модальных окон
document.addEventListener('DOMContentLoaded', function() {
    // Обработчик для модального окна входа
    const commentTrigger = document.getElementById('commentTrigger');
    if (commentTrigger) {
        commentTrigger.addEventListener('click', function() {
            new bootstrap.Modal(document.getElementById('loginModal')).show();
        });
    }

    // Общие обработчики лайков статей (если они нужны на других страницах)
    document.addEventListener('click', async function(e) {
        if (e.target.closest('.btn-like')) {
            const btn = e.target.closest('.btn-like');
            await handleArticleLike(btn);
        }
    });
});

async function handleArticleLike(btn) {
    btn.disabled = true;
    try {
        const response = await fetch(`/news/${btn.dataset.articleId}/like/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        });

        const data = await response.json();
        const icon = btn.querySelector('i');
        const countSpan = btn.querySelector('.likes-count');

        icon.classList.toggle('bi-heart-fill', data.liked);
        icon.classList.toggle('bi-heart', !data.liked);
        icon.classList.toggle('text-danger', data.liked);

        if (countSpan) countSpan.textContent = data.likes_count;
    } catch (error) {
        console.error('Error:', error);
    } finally {
        btn.disabled = false;
    }
}