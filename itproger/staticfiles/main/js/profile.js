document.addEventListener('DOMContentLoaded', function() {
    // Превью загружаемого фото
    const photoInput = document.getElementById('id_photo');
    if (photoInput) {
        photoInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(event) {
                    const preview = document.querySelector('.profile-photo-preview');
                    if (preview) {
                        preview.src = event.target.result;
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }

    const editProfileModal = document.getElementById('editProfileModal');
    const profileForm = document.getElementById('profileForm');
    let formChanged = false;

    if (editProfileModal && profileForm) {
        // Отслеживаем изменения в форме
        const formInputs = profileForm.querySelectorAll('input, textarea, select');
        formInputs.forEach(input => {
            input.addEventListener('change', () => {
                formChanged = true;
            });
        });

        // Предупреждение при закрытии модального окна без сохранения
        editProfileModal.addEventListener('hide.bs.modal', function(event) {
            if (formChanged && !profileForm.dataset.saved) {
                if (!confirm('Вы не сохранили изменения. Закрыть без сохранения?')) {
                    event.preventDefault();
                }
            }
        });

        // Отмечаем, что форма сохранена
        profileForm.addEventListener('submit', function() {
            this.dataset.saved = 'true';
            formChanged = false;
        });
    }

    // Валидация числовых полей
    const numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.validity.rangeOverflow) {
                this.setCustomValidity(`Максимальное значение: ${this.max}`);
            } else if (this.validity.rangeUnderflow) {
                this.setCustomValidity(`Минимальное значение: ${this.min}`);
            } else {
                this.setCustomValidity('');
            }
        });
    });
});
