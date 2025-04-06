document.addEventListener('DOMContentLoaded', function() {
    const ratingInput = document.getElementById('rating');
    const calculateBtn = document.getElementById('calculate-btn');
    const resultContainer = document.getElementById('result-container');
    const resultContent = document.getElementById('result-content');
    const actionButtons = document.getElementById('action-buttons');

    // Ограничиваем ввод только допустимыми значениями
    ratingInput.addEventListener('input', function() {
        let value = parseInt(this.value);
        if (isNaN(value)) {
            this.value = '';
        } else if (value < 0) {
            this.value = 0;
        } else if (value > 10) {
            this.value = 10;
        }
    });

    calculateBtn.addEventListener('click', function() {
        const score = parseInt(ratingInput.value);

        if (isNaN(score) || score < 0 || score > 10) {
            alert('Пожалуйста, введите число от 0 до 10');
            return;
        }

        showResult(score);
    });

    function showResult(score) {
        let resultText = '';
        let buttonHtml = '';

        if (score === 0) {
            resultText = `
                <h5 class="text-success">Оптимальное эмоциональное благополучие (0 баллов)</h5>
                <p>Ваши результаты свидетельствуют о прекрасном эмоциональном состоянии. Вы демонстрируете высокий уровень психологического комфорта, уверенности в себе и позитивного настроя.</p>
                <p>Вы, скорее всего, легко справляетесь со стрессовыми ситуациями, обладаете хорошей эмоциональной устойчивостью и позитивным взглядом на жизнь. Такое состояние позволяет вам эффективно решать повседневные задачи и наслаждаться жизнью.</p>
                <p><strong>Рекомендации:</strong> Продолжайте практики, которые помогают вам поддерживать это состояние. Возможно, вам будет интересно узнать больше о психологии и методах поддержания эмоционального благополучия.</p>
            `;
            buttonHtml = `
                <a href="/news/" class="btn btn-success btn-lg">
                    <i class="bi bi-book"></i> Почитать статьи
                </a>
            `;
        }
        else if (score >= 1 && score <= 3) {
            resultText = `
                <h5 class="text-success">Высокий уровень благополучия (${score} балл(ов))</h5>
                 <p>Ваше эмоциональное состояние можно охарактеризовать как очень хорошее. Вы в основном чувствуете себя уверенно и спокойно, хотя иногда можете испытывать незначительные колебания настроения.</p>
                <p>Вы достаточно хорошо справляетесь со стрессом и в целом удовлетворены своей жизнью. Возможны редкие периоды дискомфорта, но они не оказывают существенного влияния на ваше общее состояние.</p>
                <p><strong>Рекомендации:</strong> Обратите внимание на методы поддержания эмоционального баланса. Полезные материалы по психологии могут помочь вам сохранить и улучшить ваше состояние.</p>
            `;
            buttonHtml = `
                <a href="/news/" class="btn btn-success btn-lg">
                    <i class="bi bi-book"></i> Почитать статьи
                </a>
            `;
        }
        else if (score >= 4 && score <= 7) {
            resultText = `
                <h5 class="text-primary">Умеренное благополучие (${score} балл(ов))</h5>
                <p>Ваши результаты находятся в пределах средних значений. Серьёзные проблемы отсутствуют, но и о полном эмоциональном комфорте говорить нельзя.</p>
                <p>Вы можете периодически испытывать стресс, тревогу или подавленность, но в целом справляетесь с этими состояниями. Возможно, вам не хватает некоторых навыков эмоциональной саморегуляции или есть внешние обстоятельства, влияющие на ваше состояние.</p>
                <p><strong>Рекомендации:</strong> Обратите внимание на методы саморегуляции и стресс-менеджмента. Если трудности сохраняются, рассмотрите возможность консультации со специалистом.</p>
            `;
            buttonHtml = `
                <a href="/news/" class="btn btn-primary btn-lg me-3">
                    <i class="bi bi-book"></i> Почитать статьи
                </a>
                <a href="/searchpsy/" class="btn btn-outline-primary btn-lg">
                    <i class="bi bi-people"></i> Поиск психологов
                </a>
            `;
        }
        else if (score >= 8 && score <= 9) {
            resultText = `
                <h5 class="text-warning" style="color: #d35400 !important;">Субъективное неблагополучие (${score} балл(ов))</h5>
                <p>Ваши результаты указывают на выраженный эмоциональный дискомфорт. Вы, скорее всего, часто испытываете подавленность, тревогу или раздражительность.</p>
                <p>Такое состояние может быть связано с трудностями в личной жизни, профессиональными проблемами или внутренними конфликтами. Возможно, вам трудно контролировать свои эмоции или справляться со стрессовыми ситуациями.</p>
                <p><strong>Рекомендации:</strong> Настоятельно рекомендуем обратиться за профессиональной психологической помощью. Своевременная поддержка поможет вам разобраться в причинах вашего состояния и найти пути улучшения.</p>
            `;
            buttonHtml = `
                <a href="/searchpsy/" class="btn btn-warning btn-lg me-3" style="background-color: #d35400; border-color: #d35400;">
                    <i class="bi bi-people"></i> Поиск психологов
                </a>
                <a href="/help/" class="btn btn-outline-warning btn-lg" style="border-color: #d35400; color: #d35400;">
                    <i class="bi bi-house-heart"></i> Помощь
                </a>
            `;
        }
        else if (score === 10) {
            resultText = `
                <h5 class="text-danger">Выраженное эмоциональное неблагополучие (10 баллов)</h5>
                <p>Ваши результаты свидетельствуют о крайне низком уровне эмоционального благополучия. Вы, вероятно, испытываете сильную подавленность, чувство безнадежности или постоянную раздражительность.</p>
                <p>Такое состояние может значительно влиять на все аспекты вашей жизни: отношения, работу, повседневную активность. Возможно, вы чувствуете себя опустошенным, одиноким или не видите перспектив улучшения.</p>
                <p><strong>Рекомендации:</strong> Немедленно обратитесь за профессиональной помощью. Вы не должны оставаться с этим один на один. Помните, что ваше состояние временное, и при правильной поддержке вы сможете с ним справиться.</p>
            `;
            buttonHtml = `
                <a href="/help/" class="btn btn-danger btn-lg me-3">
                    <i class="bi bi-telephone"></i> Помогите мне
                </a>
                <a href="/searchpsy/" class="btn btn-outline-danger btn-lg">
                    <i class="bi bi-people"></i> Поиск психологов
                </a>
            `;
        }

        resultContent.innerHTML = resultText;
        actionButtons.innerHTML = buttonHtml;
        resultContainer.style.display = 'block';
        resultContainer.scrollIntoView({ behavior: 'smooth' });
    }
});