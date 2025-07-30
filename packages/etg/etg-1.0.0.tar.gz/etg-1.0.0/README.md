# etg

Библиотека для создания Telegram-ботов через собственный язык или команды.

## Пример использования

```python
import etg

etg.setToken("ТОКЕН")

etg.onCommand("/start", "Привет!")

etg.startBot()
