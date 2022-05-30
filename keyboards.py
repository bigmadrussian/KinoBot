import typing as tp
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from urllib.parse import quote


def film_choice(response_json: tp.Dict[str, tp.Any], choice_limit: int = 5) -> (InlineKeyboardMarkup, tp.List[tp.Any]):
    kb = InlineKeyboardMarkup(row_width=1)

    assert 'films' in response_json, "Not found films, but should"
    films_json = response_json['films']
    assert isinstance(films_json, list) and len(films_json) > 0, "Not films, but should"

    films = []
    for i, film_json in enumerate(films_json):
        if i >= choice_limit:
            break
        try:
            names = [film_json['nameRu'], film_json['nameEn'], film_json['year']]
            film = ', '.join([name for name in names if name is not None and len(name) > 0])
        except (KeyError, TypeError):
            film = "NONAME"

        button = InlineKeyboardButton(film, callback_data=f"film {i}")
        kb.add(button)
        films.append(film_json)

    cancel = InlineKeyboardButton('Cancel', callback_data="film cancel")
    kb.add(cancel)

    return kb, films


def source_choice(film_name: str) -> InlineKeyboardMarkup:
    film_encoded = quote(film_name)

    kb = InlineKeyboardMarkup(row_width=2)
    # Paid
    ivi = InlineKeyboardButton('💰IVI', url=f"https://www.ivi.ru/search/?q={film_encoded}")
    okko = InlineKeyboardButton('💰OKKO', url=f"https://okko.tv/search/{film_encoded}")
    kinopoisk = InlineKeyboardButton('🎥Кинопоиск', url=f"https://www.kinopoisk.ru/index.php?kp_query={film_encoded}")
    kb.row(ivi, okko, kinopoisk)
    # Free
    hdrezka = InlineKeyboardButton('🆓HDREZKA',
                                   url=f"http://ikinopoisk.com/index.php?do=search&subaction=search&q={film_encoded}")
    baskino_url = f"http://baskino.me/index.php?do=search&mode=advanced&subaction=search&story={film_encoded}"
    baskino = InlineKeyboardButton('🆓BASKINO',
                                   url=baskino_url)
    lordFilm = InlineKeyboardButton('🎬LordFilm', url=f"https://p.mxfilm.top/index.php?do=search")
    more_tv = InlineKeyboardButton('ⓂMail', url=f"https://kino.mail.ru/search/?region_id=54&q={film_encoded}")
    kb.row(hdrezka, baskino, lordFilm, more_tv)
    return kb