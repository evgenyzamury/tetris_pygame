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
        "Active player": "Active player",
        "Settings": "Settings",
        "Music Volume": "Music Volume",
        "SFX Volume": "SFX Volume",
        "Difficulty": "Difficulty",
        "Language": "Language",
        "Theme": "Theme",
        "Back": "Back",
        "Easy": "Easy",
        "Medium": "Medium",
        "Impossible": "Impossible",
        "Pause": "Pause",
        "Start Game": "Start Game",
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
        "NEW RECORD": "NEW RECORD",
        "Best score": "Best score",
        "All score": "All score",
        "Play time (min)": "Play time (min)",
        "Log in": "Log in",
        "Players in system": "Players in system",
    },
    "ru": {
        "Active player": "Активный игрок",
        "Settings": "Настройки",
        "Music Volume": "Музыка",
        "SFX Volume": "SFX Звуки",
        "Difficulty": "Сложность",
        "Language": "Язык",
        "Theme": "Тема",
        "Back": "Назад",
        "Easy": "Легко",
        "Medium": "Средне",
        "Impossible": "Невозможно",
        "Pause": "Пауза",
        "Start Game": "Начать игру",
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
        "NEW RECORD": "НОВЫЙ РЕКОРД",
        "Best score": "Лучший результат",
        "All score": "Все очки",
        "Play time (min)": "Игровое время(м)",
        "Log in": "Войти",
        "Players in system": "Игроки в системе"
    },
}


def get_translation(key, language="en"):
    return translations.get(language, {}).get(key, key)
