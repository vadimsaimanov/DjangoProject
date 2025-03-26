document.addEventListener('DOMContentLoaded', function() {
    const agreeButton = document.getElementById('agreeButton');
    if (agreeButton) {
        agreeButton.addEventListener('click', function() {
            document.getElementById('id_agreed_to_terms').checked = true;
            const modal = bootstrap.Modal.getInstance(document.getElementById('termsModal'));
            modal.hide();
        });
    }
});

function togglePassword(id) {
    const passwordField = document.getElementById(id);
    const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordField.setAttribute('type', type);

    // Toggle the eye icon
    const eyeIcon = passwordField.nextElementSibling.querySelector('i');
    eyeIcon.classList.toggle('fa-eye');
    eyeIcon.classList.toggle('fa-eye-slash');
}

// для лайка
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.btn-like').forEach(btn => {
        btn.addEventListener('click', async function() {
            const articleId = this.dataset.articleId;
            const icon = this.querySelector('i');
            const countSpan = this.querySelector('.likes-count');

            try {
                const response = await fetch(`/news/${articleId}/like/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': '{{ csrf_token }}',
                        'Content-Type': 'application/json'
                    },
                    credentials: 'same-origin'
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();

                if (data.error) {
                    console.error('Error:', data.error);
                    return;
                }

                if (data.liked) {
                    icon.classList.remove('bi-heart');
                    icon.classList.add('bi-heart-fill', 'text-danger');
                    // Анимация пульсации
                    icon.style.transform = 'scale(1.3)';
                    setTimeout(() => {
                        icon.style.transform = 'scale(1)';
                    }, 300);
                } else {
                    icon.classList.remove('bi-heart-fill', 'text-danger');
                    icon.classList.add('bi-heart');
                }

                countSpan.textContent = data.likes_count;
            } catch (error) {
                console.error('Error:', error);
                if (error.message.includes('401')) {
                    window.location.href = '/accounts/login/?next=' + window.location.pathname;
                }
            }
        });
    });
});
