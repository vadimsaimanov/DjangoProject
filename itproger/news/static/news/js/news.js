document.addEventListener('DOMContentLoaded', function() {
    // Обработка кнопок показа/скрытия ответов
    document.querySelectorAll('.btn-toggle-replies').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const commentId = this.dataset.commentId;
            const repliesContainer = document.getElementById(`replies-${commentId}`);
            const isCollapsed = this.dataset.state === 'collapsed';

            if (isCollapsed) {
                repliesContainer.style.display = 'block';
                this.dataset.state = 'expanded';
            } else {
                repliesContainer.style.display = 'none';
                this.dataset.state = 'collapsed';
            }

            // Получаем количество ответов из data-атрибута
            const replyCount = this.dataset.count;
            this.innerHTML = isCollapsed ? `Скрыть ответы (${replyCount})` : `Показать ответы (${replyCount})`;
        });
    });

    // Остальной код обработки комментариев...
    setupLikeButtons();
    setupCommentButtons();

    // Очистка формы после отправки
    const commentForms = document.querySelectorAll('.real-comment-form');
    commentForms.forEach(form => {
        form.addEventListener('submit', function() {
            setTimeout(() => {
                this.querySelector('textarea').value = '';
            }, 100);
        });
    });

    // Делегирование событий
    document.addEventListener('click', async function(e) {
        if (e.target.closest('.btn-like-comment')) await handleCommentLike(e.target.closest('.btn-like-comment'));
        if (e.target.closest('.btn-dislike-comment')) await handleCommentDislike(e.target.closest('.btn-dislike-comment'));
    });
});

function getCSRFToken() {
    const name = 'csrftoken=';
    const decodedCookie = decodeURIComponent(document.cookie);
    const cookieArray = decodedCookie.split(';');
    for (let i = 0; i < cookieArray.length; i++) {
        let cookie = cookieArray[i];
        while (cookie.charAt(0) === ' ') {
            cookie = cookie.substring(1);
        }
        if (cookie.indexOf(name) === 0) {
            return cookie.substring(name.length, cookie.length);
        }
    }
    return '';
}

// Общий обработчик лайков для всех страниц
function setupLikeButtons() {
    document.querySelectorAll('.btn-like').forEach(btn => {
        btn.addEventListener('click', async function(e) {
            e.preventDefault();
            const articleId = this.dataset.articleId;

            try {
                const response = await fetch(`/news/${articleId}/like/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken(),
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                });

                const data = await response.json();

                const icon = this.querySelector('i');
                const countSpan = this.querySelector('.likes-count');

                if (icon) {
                    icon.classList.toggle('bi-heart-fill', data.liked);
                    icon.classList.toggle('bi-heart', !data.liked);
                    icon.classList.toggle('text-danger', data.liked);
                }

                if (countSpan) {
                    countSpan.textContent = data.likes_count;
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });
}

// Функция для настройки обработчиков событий для кнопок комментариев
function setupCommentButtons() {
    document.querySelectorAll('.btn-reply').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const commentId = this.dataset.commentId;
            const form = document.getElementById(`reply-form-${commentId}`);
            form.style.display = form.style.display === 'none' ? 'block' : 'none';
            this.style.display = 'none';
        });
    });

    document.querySelectorAll('.cancel-reply').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const form = this.closest('.reply-form-container');
            form.style.display = 'none';
            const commentId = form.id.replace('reply-form-', '');
            document.querySelector(`.btn-reply[data-comment-id="${commentId}"]`).style.display = 'inline-block';
        });
    });
}

// Обновленные обработчики лайков/дизлайков комментариев
async function handleCommentLike(btn) {
    if (btn.disabled) return;
    btn.disabled = true;

    try {
        const response = await fetch(`/news/comment/${btn.dataset.commentId}/like/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
            },
            credentials: 'same-origin'
        });

        if (!response.ok) throw new Error('Network error');

        const data = await response.json();
        updateCommentLikeUI(btn, data);

        // Обновляем счетчик дизлайков, если нужно
        const dislikeBtn = btn.closest('.comment-votes').querySelector('.btn-dislike-comment');
        if (dislikeBtn && data.disliked === false) {
            dislikeBtn.querySelector('i').className = 'bi bi-hand-thumbs-down';
        }
    } catch (error) {
        console.error('Error:', error);
    } finally {
        btn.disabled = false;
    }
}

async function handleCommentDislike(btn) {
    if (btn.disabled) return;
    btn.disabled = true;

    try {
        const response = await fetch(`/news/comment/${btn.dataset.commentId}/dislike/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
            },
            credentials: 'same-origin'
        });

        if (!response.ok) throw new Error('Network error');

        const data = await response.json();
        updateCommentDislikeUI(btn, data);

        // Обновляем счетчик лайков, если нужно
        const likeBtn = btn.closest('.comment-votes').querySelector('.btn-like-comment');
        if (likeBtn && data.liked === false) {
            likeBtn.querySelector('i').className = 'bi bi-hand-thumbs-up';
            if (data.likes_count !== undefined) {
                likeBtn.querySelector('.likes-count').textContent = data.likes_count;
            }
        }
    } catch (error) {
        console.error('Error:', error);
    } finally {
        btn.disabled = false;
    }
}

// Обновление UI для лайков/дизлайков комментариев
function updateCommentLikeUI(btn, data) {
    const icon = btn.querySelector('i');
    const countSpan = btn.querySelector('.likes-count');
    icon.classList.toggle('bi-hand-thumbs-up-fill', data.liked);
    icon.classList.toggle('bi-hand-thumbs-up', !data.liked);

    if (countSpan) countSpan.textContent = data.likes_count;
}

function updateCommentDislikeUI(btn, data) {
    const icon = btn.querySelector('i');
    icon.classList.toggle('bi-hand-thumbs-down-fill', data.disliked);
    icon.classList.toggle('bi-hand-thumbs-down', !data.disliked);
}
