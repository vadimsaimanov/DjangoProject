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

    // Обработчик для кнопки редактирования профиля
    document.querySelector('[data-bs-target="#editProfileModal"]').addEventListener('click', function(e) {
        e.preventDefault();
        toggleEditForm(true);
    });

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

    if (aboutTextarea && aboutCounter) {
        // Жёсткое ограничение ввода
        aboutTextarea.addEventListener('input', function() {
            const text = this.value;
            if (text.length > 500) {
                this.value = text.substring(0, 500);
            }
            aboutCounter.textContent = this.value.length;

            // Визуальная индикация
            if (this.value.length >= 500) {
                aboutCounter.style.color = 'red';
                this.classList.add('is-invalid');
            } else {
                aboutCounter.style.color = '';
                this.classList.remove('is-invalid');
            }
        });

        // Инициализация при загрузке
        aboutCounter.textContent = aboutTextarea.value.length;
        if (aboutTextarea.value.length >= 500) {
            aboutCounter.style.color = 'red';
        }
    }

    // Исправление ошибки Bootstrap modal
    if (typeof bootstrap !== 'undefined' && bootstrap.Modal) {
        const modalElement = document.getElementById('editProfileModal');
        if (modalElement) {
            // Инициализация модального окна с правильными параметрами
            new bootstrap.Modal(modalElement, {
                backdrop: true,
                keyboard: true,
                focus: true
            });
        }
    }
});
