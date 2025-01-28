SIZE = WIDTH, HEIGHT = 800, 900

# Цвета для блоков
COLOR = [['#c34046', '#b33a41', '#69262a', '#d1686e'],  # red
         ['#a3d350', '#7da837', '#709732', '#dbff86'],  # green
         ['#5c4aae', '#5444a0', '#4a3998', '#8b7dc6'],  # blue
         ['#ba52b0', '#a948a0', '#863a7e', '#c77dbe'],  # pink
         ['#40c192', '#35a67d', '#1a4939', '#69cea9'],  # cyan
         ['#c87644', '#aa6337', '#58341f', '#cf9674'],  # orange-brown
         ['#e5c749', '#d1b12f', '#947f27', '#c3b267'],  # yellow
         ]

# Цвет тени блока
SHADOW_COLOR = '#00DF00'

difficulty_list = ["Easy", "Medium", "Impossible"]
language_list = ["English", "Русский"]
theme_list = ["Light", "Dark"]

translations = {
    "en": {
        "Settings": "Settings",
        "Music Volume": "Music Volume",
        "Block Volume": "Block Volume",
        "Difficulty": "Difficulty",
        "Language": "Language",
        "Theme": "Theme",
        "Back": "Back",
        "Easy": "Easy",
        "Medium": "Medium",
        "Impossible": "Impossible",
        "Pause": "Pause",
        "Continue": "Continue",
        "Quit": "Quit",
        "Results": "Results",
        "Save and Exit": "Save and Exit",
        "YOU LOSE!": "YOU LOSE!",
        "Score": "Score",
        "Next": "Next",
        "Time": "Time",
        "Back to menu": "Back to menu",
        "Restart": "Restart",
        "PAUSED": "PAUSED",
    },
    "ru": {
        "Settings": "Настройки",
        "Music Volume": "Музыка",
        "Block Volume": "Блоки",
        "Difficulty": "Сложность",
        "Language": "Язык",
        "Theme": "Тема",
        "Back": "Назад",
        "Easy": "Легко",
        "Medium": "Средне",
        "Impossible": "Невозможно",
        "Pause": "Пауза",
        "Continue": "Продолжить",
        "Quit": "Выход",
        "Results": "Результаты",
        "Save and Exit": "Сохранить и выйти",
        "YOU LOSE!": "ВЫ ПРОИГРАЛИ!",
        "Score": "Очки",
        "Next": "Следующий",
        "Time": "Время",
        "Back to menu": "Выйти в меню",
        "Restart": "Перезапуск",
        "PAUSED": "ПАУЗА",
    },
}


def get_translation(key, language="en"):
    return translations.get(language, {}).get(key, key)
