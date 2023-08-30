# aiogram_template

### About

---
#### Structure:

```bash
├───logs # logs folder
├───systemd 
└───tgbot
    ├───filters
    ├───handlers
    ├───keyboards
    ├───middlewares
    ├───misc # misc stuff
    ├───models # database models
    ├───services # services
    ├───translations # i18n translations
    └───utils
```

#### Files:

* The `tgbot` package is the root package for the bot, and it contains sub-packages for filters, handlers, and middlewares.

* The `filters` package contains classes that define custom filters for the bot's message handlers.

* The `handlers` package contains classes that define the bot's message handlers, which specify the actions to take in response to incoming messages.

* The `middlewares` package contains classes that define custom middlewares for the bot's dispatcher, which can be used to perform additional processing on incoming messages.

* The `misc` package contains miscellaneous stuff, such as the `config.py` file, which contains the bot's configuration settings, and the `db.py` file, which contains the bot's database connection.

* The `models` package contains database models.

* The `services` package contains services.

* The `translations` package contains i18n translations.

Inspired by [Tishka17&#39;s tgbot_template](https://github.com/Tishka17/tgbot_template) and customized with some useful things.

Simple template for bots written on [aiogram](https://github.com/aiogram/aiogram).

### Setting up

#### System dependencies

* Python 3.9+
* Redis (if you set `use_redis = true` in **bot.ini**)
* DB (if you set `use_db = true` in **bot.ini**). 
`False` by default **sqlite3** or you can use **PostgreSQL** by setting `use_postgres = True` in **bot.ini**

#### Preparations

* Clone this repo via `https://github.com/jakha921/aiogram_template.git`

Without Poetry:

* Create virtual environment: `python -m venv venv`
* Make **venv** your source: `source ./venv/bin/activate` (Linux) or `.\venv\Scripts\activate (Windows)`
* Install requirements: `pip install -r requirements.txt`

With Poetry:

* Just run `poetry install` (if you haven't installed poetry yet, you can find instructions **[here](https://python-poetry.org/docs/)**)

### Deployment

* Copy **bot.ini.example** to **bot.ini** and set your variables.

Without Systemd:

* Run bot: `python bot.py`

With Systemd:

* Copy systemd config to systemd system folder with: `sudo cp systemd/yourbotname.service.example /etc/systemd/system/mynewbot.service` "mynewbot" - you can change to any name.
* Open config and reconfigure with your parameters: `sudo nano /etc/systemd/system/mynewbot.service`
* Reload systemd daemon with: `sudo systemctl daemon-reload`
* Start your bot service with: `sudo systemctl start mynewbot.service`

### Useful

**Aiogram**

* Docs: https://docs.aiogram.dev/en/latest/
* Stable version: https://docs.aiogram.dev/en/stable/install.html
* Community: https://t.me/aiogram
* UZ Community: https://t.me/aiogram_uz
* Source code: https://github.com/aiogram/aiogram

**Test bot**: https://t.me/aiogram_template_bot
