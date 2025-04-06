// Функции только для страницы с комментариями
document.addEventListener('DOMContentLoaded', function() {
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
        if (e.target.closest('.btn-reply')) handleReplyButton(e.target.closest('.btn-reply'));
        if (e.target.closest('.cancel-reply')) handleCancelReply(e.target.closest('.cancel-reply'));
        if (e.target.closest('.btn-toggle-replies')) handleToggleReplies(e.target.closest('.btn-toggle-replies'));
        if (e.target.closest('.btn-like-comment')) await handleCommentLike(e.target.closest('.btn-like-comment'));
        if (e.target.closest('.btn-dislike-comment')) await handleCommentDislike(e.target.closest('.btn-dislike-comment'));
    });
});

// Обработчики для комментариев
function handleReplyButton(btn) {
    const formId = `reply-form-${btn.dataset.commentId}`;
    document.querySelectorAll('.reply-form-container').forEach(f => f.style.display = 'none');
    document.getElementById(formId).style.display = 'block';
    btn.style.display = 'none';
}

function handleCancelReply(btn) {
    const form = btn.closest('.reply-form-container');
    form.style.display = 'none';
    const commentId = form.id.replace('reply-form-', '');
    document.querySelector(`.btn-reply[data-comment-id="${commentId}"]`).style.display = 'inline-block';
}

function handleToggleReplies(btn) {
    const container = document.getElementById(`replies-${btn.dataset.commentId}`);
    container.style.display = container.style.display === 'none' ? 'block' : 'none';
}

async function handleCommentLike(btn) {
    btn.disabled = true;
    try {
        const response = await fetch(`/news/comment/${btn.dataset.commentId}/like/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        });

        const data = await response.json();
        updateCommentLikeUI(btn, data);
    } catch (error) {
        console.error('Error liking comment:', error);
    } finally {
        btn.disabled = false;
    }
}

async function handleCommentDislike(btn) {
    btn.disabled = true;
    try {
        const response = await fetch(`/news/comment/${btn.dataset.commentId}/dislike/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        });

        const data = await response.json();
        updateCommentDislikeUI(btn, data);
        console.log('Dislike action:', {
            commentId: btn.dataset.commentId,
            status: data.disliked ? 'disliked' : 'canceled',
            time: new Date().toLocaleString()
        });
    } catch (error) {
        console.error('Error disliking comment:', error);
    } finally {
        btn.disabled = false;
    }
}

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