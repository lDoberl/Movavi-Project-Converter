# Movavi Project Converter 🎬✨

**Конвертер проектов Movavi `.mepj` между версиями с удобным веб-интерфейсом.**

---

## 🇷🇺 Русский

### Быстрый старт

Вы можете сразу запустить приложение на Windows через готовый `.exe` файл из [раздела Releases](https://github.com/lDoberl/Movavi-Project-Converter/releases). Python устанавливать не нужно — просто двойной клик, и приложение откроется в браузере.

### Описание

Movavi Project Converter позволяет конвертировать файлы `.mepj` между версиями **23.3.0**, **25.3.0** и **25.9.0**. Приложение имеет удобный веб-интерфейс с поддержкой **Drag & Drop** и двух языков: **English** и **Русский**.

### Основные возможности

* 🗂 **Поддержка форматов:** конвертируй `.mepj` файлы между версиями 23.3.0, 25.3.0 и 25.9.0
* 🌐 **Web-интерфейс:** красивый браузерный интерфейс с TailwindCSS
* 🎨 **Drag & Drop:** перетаскивай файлы на страницу — дроп-зона растягивается на весь экран
* 🔄 **Автоматическое обновление `config.json`:** все настройки версии обновляются автоматически
* 🌍 **Многоязычность:** интерфейс поддерживает English и Русский
* ✅ **Уведомления:** информативные всплывающие сообщения о успешной конверсии
* ❌ **Безопасный выход:** кнопка Exit мгновенно закрывает приложение

### Системные требования

* Windows / Linux / MacOS
* Python 3.10+ (только для исходников, не требуется для `.exe`)
* Браузер для запуска веб-интерфейса

### Установка и запуск (из исходников)

1. Склонируйте репозиторий:

```bash
git clone https://github.com/lDoberl/Movavi-Project-Converter.git
cd Movavi-Project-Converter
```

2. Создайте виртуальное окружение и активируйте его:

```bash
python -m venv env
# Windows
env\Scripts\activate
# Linux / macOS
source env/bin/activate
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Запустите приложение:

```bash
python app.py
```

5. В браузере откроется интерфейс на `http://127.0.0.1:5000`. Перетащите `.mepj` файл, выберите версию и нажмите **Convert**.

---

## 🇬🇧 English

### Quick Start

You can immediately run the application on Windows using the ready-to-use `.exe` file from the [Releases](https://github.com/lDoberl/Movavi-Project-Converter/releases) section. Python is not required — just double-click the file, and the application will open in your browser.

### Description

Movavi Project Converter allows you to convert `.mepj` files between versions **23.3.0**, **25.3.0**, and **25.9.0**. The app features a user-friendly web interface with **Drag & Drop** support and multilingual interface: **English** and **Russian**.

### Features

* 🗂 **Format Support:** convert `.mepj` files between 23.3.0, 25.3.0, and 25.9.0
* 🌐 **Web Interface:** beautiful browser interface built with TailwindCSS
* 🎨 **Drag & Drop:** drag files directly onto the page — the drop zone expands to fullscreen
* 🔄 **Automatic `config.json` Update:** all version settings are updated automatically
* 🌍 **Multilingual Support:** interface available in English and Russian
* ✅ **Notifications:** informative pop-up messages on successful conversion
* ❌ **Safe Exit:** Exit button instantly closes the application

### System Requirements

* Windows / Linux / MacOS
* Python 3.10+ (only for source code, not required for `.exe`)
* Browser for web interface

### Installation and Usage (from source)

1. Clone the repository:

```bash
git clone https://github.com/lDoberl/Movavi-Project-Converter.git
cd Movavi-Project-Converter
```

2. Create and activate a virtual environment:

```bash
python -m venv env
# Windows
env\Scripts\activate
# Linux / macOS
source env/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python app.py
```

5. Web browser will open at `http://127.0.0.1:5000`. Drag and drop your `.mepj` file, select the target version, and click **Convert**.
