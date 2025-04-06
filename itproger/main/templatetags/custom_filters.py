from django import template

register = template.Library()

@register.filter
def pluralize_year(value):
    if not value:
        return ""
    value = int(value)
    if value % 10 == 1 and value % 100 != 11:
        return "год"
    elif 2 <= value % 10 <= 4 and (value % 100 < 10 or value % 100 >= 20):
        return "года"
    else:
        return "лет"

@register.filter
def get_spec_name(value):
    spec_names = {
        'stress': 'Стресс',
        'low_self-esteem': 'Низкая самооценка',
        'relationship_difficulties': 'Трудности в построении отношений',
        'relations_with_surroundings': 'Отношения с окружающими',
        'depressive_state': 'Депрессивное состояние',
        'panic_attacks_anxiety': 'Панические атаки, тревога',
        'social_adaptation_sociophobia': 'Социальная адаптация, социофобия',
        'adapting_to_new_conditions': 'Адаптация к новым условиям (переезд, поступление в ВУЗ)',
        'family_problems': 'Семейные проблемы',
        'parental_pressure': 'Давление со стороны родителей (учеба, выбор профессии)',
        'academic_performance_fear_of_exams': 'Проблемы с успеваемостью, страх экзаменов',
        'first_love_breakups': 'Первая любовь, расставания',
        'expressing_desires_assertiveness': 'Проявление желаний и отстаивание собственного мнения',
        'decision_making_goal_setting': 'Принятие решения, постановка цели',
        'burnout': 'Выгорание',
        'fears_phobias': 'Страхи и фобии',
        'loneliness': 'Одиночество',
        'neuroses_emotional_disorders': 'Неврозы и эмоциональные расстройства',
        'bullying': 'Буллинг',
        'aggressiveness_outbursts_of_anger': 'Агрессивность, приступы гнева',
        'sex_sexuality': 'Секс, сексуальность',
        'sleep_disorders_insomnia': 'Нарушения сна, бессонница',
        'bad_habits': 'Вредные привычки',
        'violence_trauma': 'Травма насилия',
        'obsessive_behavior_thoughts': 'Навязчивое поведение, мысли',
        'conflicts_with_teachers_professors': 'Конфликты с учителями/преподавателями',
        'death_of_a_close_person': 'Смерть близкого человека',
    }
    return spec_names.get(value, value)
