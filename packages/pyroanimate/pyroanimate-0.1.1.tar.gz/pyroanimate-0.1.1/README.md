# PYROANIMATE

Pyroanimate - библиотека отправки через [Pyrogram](https://github.com/pyrogram/pyrogram) анимированных сообщений.

## Установка
Установка библиотеки с помощью pip:

```bash
pip install pyroanimate
```

Установка через git clone:

```bash
git clone https://github.com/dap3842/pyroanimate.git
```


## Пример использования

```python
from pyroanimate import Animate
from pyrogram import Client

chat_id = 123

app = Client("bot")

anim = Animate(app,delay = 0.3,sync = True)
anim.add_animations("walk", ["🚶", "🏃", "🚶‍♂️"])
anim.run(chat_id, default = True, frames = None, animation_id = "walk")

```

## Лицензия
MIT License

```
MIT License

Copyright (c) 2025 dap3842

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

