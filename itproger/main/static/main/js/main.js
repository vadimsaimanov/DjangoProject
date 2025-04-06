document.addEventListener('DOMContentLoaded', function() {
    // Функция для показа/скрытия формы редактирования
    function toggleEditForm(show) {
        const editSection = document.getElementById('profileEditSection');
        editSection.style.display = show ? 'block' : 'none';

        // Прокрутка к форме при открытии
        if (show) {
            setTimeout(() => {
                editSection.scrollIntoView({ behavior: 'smooth' });
            }, 100);
        }
    }

    // Исправление ошибки Bootstrap modal
    const modalElement = document.getElementById('editProfileModal');
    if (modalElement) {
        // Проверяем, инициализировано ли уже модальное окно
        if (!modalElement._modal) {
            const modal = new bootstrap.Modal(modalElement, {
                backdrop: true,
                keyboard: true,
                focus: true
            });

            // Обработчик для кнопки открытия модального окна
            document.querySelector('[data-bs-target="#editProfileModal"]')?.addEventListener('click', function(e) {
                e.preventDefault();
                modal.show();
            });
        }
    }

    // Инициализация формы при загрузке
    let formChanged = false;

    // Отслеживание изменений в форме
    document.querySelectorAll('#profileForm input, #profileForm textarea, #profileForm select').forEach(input => {
        input.addEventListener('change', () => formChanged = true);
    });

    // Предупреждение при закрытии формы без сохранения
    document.querySelector('#profileForm button[type="button"]').addEventListener('click', function() {
        if (formChanged && !confirm('Вы не сохранили изменения. Закрыть без сохранения?')) {
            return;
        }
        toggleEditForm(false);
    });

    // Отметка о сохранении формы
    document.getElementById('profileForm').addEventListener('submit', function(e) {
        // Проверка заполнения поля "О себе"
        const aboutField = document.getElementById('id_about');
        if (aboutField.value.trim().length === 0) {
            e.preventDefault();
            alert('Поле "О себе" обязательно для заполнения');
            aboutField.focus();
            return false;
        }

        // Жёсткая проверка перед отправкой
        if (aboutField.value.length > 500) {
            e.preventDefault();
            aboutField.value = aboutField.value.substring(0, 500);
            aboutField.classList.add('is-invalid');
            aboutField.scrollIntoView({ behavior: 'smooth', block: 'center' });
            alert('Максимальная длина "О себе" - 500 символов');
            return false;
        }

        // Остальная логика отправки формы
        this.dataset.saved = 'true';
        formChanged = false;
    });

    // Валидация числовых полей
    const numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(input => {
        input.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9]/g, '');
        });
    });

    // Валидация текстовых полей
    const textInputs = document.querySelectorAll('input[type="text"]');
    textInputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.id === 'id_age' || this.id === 'id_experience') {
                this.value = this.value.replace(/[^0-9]/g, '');
            } else if (this.id === 'id_first_name' || this.id === 'id_last_name' || this.id === 'id_middle_name') {
                this.value = this.value.replace(/[^а-яА-ЯёЁa-zA-Z\s-]/g, '');
            }
        });
    });

    // Обработчик для текстового поля "О себе"
    const aboutTextarea = document.getElementById('id_about');
    const aboutCounter = document.getElementById('about-counter');

    function countChars() {
        let text = aboutTextarea.value;
        // Жёсткое ограничение
        if (text.length > 500) {
            text = text.substring(0, 500);
            aboutTextarea.value = text;
        }
        aboutCounter.textContent = text.length;

        // Визуальная индикация
        if (text.length >= 500) {
            aboutCounter.style.color = 'red';
            aboutTextarea.classList.add('is-invalid');
        } else {
            aboutCounter.style.color = '';
            aboutTextarea.classList.remove('is-invalid');
        }
    }

    if (aboutTextarea && aboutCounter) {
        aboutTextarea.addEventListener('input', countChars);
        countChars(); // Инициализация
    }
});
