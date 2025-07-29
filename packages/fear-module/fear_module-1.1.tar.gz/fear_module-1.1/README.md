# fear_module ENG

![Python 3.8, 3.9, 3.10, 3.11, 3.12](https://img.shields.io/badge/Python-3.8|3.9|3.10|3.11|3.12-orange)

**fear_module** - this module is a Python library for creating troll applications!


**FEAR** - is an entertainment project. Be **careful** with him. **It is not subject to monetization**.


## Installation

Install the current version with [PyPI](https://pypi.org/project/fear-module/):

```bash
pip install fear_module
```

Or from [Github](https://github.com/Keker-dev/fear_module.git):
```bash
pip install https://github.com/Keker-dev/fear_module.git
```

## Usage

```python
app = Fear(main_text="text", main_image="/path_to_image")

if __name__ == '__main__':
    app.run()
```
**Warning!** The standard **on_quit** method shuts down the system!
If you want to change the method that occurs when you close the application, do the following:
```python
app.on_quit = lambda: print("End.")
```

## Example

Add one scene.

```python
from fear_module import Fear

app = Fear(main_text="text", main_image="/path_to_image")
app.add_scene(name="FirstScene", text="text", image="/path_to_image", sound="/path_to_sound", button_text="click me")

if __name__ == '__main__':
    app.run()
```


## Contributing

Bug reports and/or pull requests are welcome


## License

The module is available as open source under the terms of the **MIT License**


# fear_module RU

![Python 3.8, 3.9, 3.10, 3.11, 3.12](https://img.shields.io/badge/Python-3.8|3.9|3.10|3.11|3.12-orange)

Модуль **fear_module** - это библиотека Python для создания приложений-троллей. Он содержит класс Fear, который позволяет создавать окна с кнопками и изображениями, а также добавлять новые сцены с текстом, изображениями и звуками. Модуль также позволяет блокировать клавиатуру и воспроизводить звуки.

**Fear** - развлекательный проект. Будьте **_осторожны_** с ним. **Не для коммерческого использования.**

## Установка

Установите актуальную версию с помощью [PyPI](https://pypi.org/project/fear-module/):

```bash
pip install fear_module
```

Или [Github](https://github.com/Keker-dev/fear_module.git):
```bash
pip install https://github.com/Keker-dev/fear_module.git
```

## Использование

```python
app = Fear(main_text="text", main_image="/path_to_image")

if __name__ == '__main__':
    app.run()
```
**Осторожно!** Стандартный метод **on_quit** вырубает систему!
Если вы хотите изменить метод, который происходит, когда вы закрываете приложение, сделайте так:
```python
app.on_quit = lambda: print("End.")
```

## Пример

Простой пример с одной сценой.

```python
from fear_module import Fear

app = Fear(main_text="text", main_image="/path_to_image")
app.add_scene(name="FirstScene", text="text", image="/path_to_image", sound="/path_to_sound", button_text="click me")

if __name__ == '__main__':
    app.run()
```


## Сообщество

Отчеты об ошибках и/или запросы на вытягивание приветствуются.


## Лицензия

Модуль доступен как открытый исходный код по условиям лицензии **MIT License**