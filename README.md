# 2048 в терминале

Классическая головоломка 2048 с меню, цветными плитками, отменой хода и
сохранением рекорда.

## Готовые сборки

Все файлы лежат в папке `dist/`:

| Файл | Платформа |
| --- | --- |
| `2048-windows-x86_64.exe` | Windows 10/11, x86-64 |
| `2048-x86_64.AppImage` | Linux, x86-64 |
| `2048-linux-x86_64` | Linux, x86-64, обычный бинарник |

Python на компьютер устанавливать не нужно — всё уже внутри.

### Windows

Запустите `2048-windows-x86_64.exe` двойным щелчком или из командной строки:

```bat
2048-windows-x86_64.exe
```

Файл не подписан электронной подписью, поэтому SmartScreen может показать
предупреждение: нажмите «Подробнее» → «Выполнить в любом случае».

Рекорд хранится в `%USERPROFILE%\.2048_best`.

### Linux — AppImage

```bash
chmod +x 2048-x86_64.AppImage
./2048-x86_64.AppImage
```

Если запустить AppImage двойным щелчком, игра сама откроет окно терминала
(alacritty, kitty, konsole, gnome-terminal, xfce4-terminal или xterm).

Для систем без FUSE:

```bash
APPIMAGE_EXTRACT_AND_RUN=1 ./2048-x86_64.AppImage
```

### Linux — обычный бинарник

```bash
chmod +x 2048-linux-x86_64
./2048-linux-x86_64
```

Рекорд хранится в `~/.2048_best`.

## Управление

| Клавиши | Действие |
| --- | --- |
| `←` `↑` `→` `↓`, `WASD`, `HJKL` | двигать плитки |
| `U` | отменить ход |
| `R` | начать заново |
| `Q` | вернуться в меню |

В меню: `↑` / `↓` — выбор, `Enter` — подтвердить.

## Запуск из исходников

```bash
python3 game_2048.py
```

Нужен Python 3.9 или новее. Внешние библиотеки не требуются.

## Пересборка

Linux:

```bash
pip install pyinstaller
pyinstaller --onefile --console --name 2048 game_2048.py
```

Windows (в Windows, из папки проекта):

```bat
py -m pip install pyinstaller
py -m PyInstaller --onefile --console --name 2048 --icon assets\2048.ico game_2048.py
```

Готовый AppImage собирается из `dist/2048-linux-x86_64` и файлов из
`packaging/` с помощью [appimagetool](https://github.com/AppImage/appimagetool):

```bash
APPIMAGETOOL=/путь/к/appimagetool ./packaging/build_appimage.sh
```
