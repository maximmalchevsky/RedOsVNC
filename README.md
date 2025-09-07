# Техподдержка

Простое GUI-приложение для предоставления удалённого доступа с помощью **x11vnc** на Linux.  
Приложение написано на Python с использованием **Tkinter**.

---

## 💻 Требования

- Python 3.8+  
- Модули Python:
  - `tkinter`
  - `netifaces`
- Linux-система с **x11vnc**
---
## Установка

1. Убедитесь, что система использует Python 3.8 и выше.
```python
python3 --version
```
2. Установите x11vnc:
```bash
sudo dnf install x11vnc  # для Red OS / Fedora
```

3. Установите необходимые модули Python:
```bash
sudo dnf install python3-tkinter python3-netifaces  # для Red OS / Fedora
```

4. Скачайте или клонируйте репозиторий:
```bash
git clone https://github.com/maximmalchevsky/RedOsVNC
```

5. Перейдите в директорию с приложением:
```bash
cd RedOsVNC
```
6. Скопируйте файлы проекта в /opt/techsupport:
```bash
sudo mkdir -p /opt/techsupport
sudo cp -r * /opt/techsupport/
sudo chmod -R 755 /opt/techsupport
```

7. Создайте ярлык на рабочем столе:
```bash
sudo cp techsupport.desktop /usr/share/applications/
```

8. Ярлык "Техподдержка" появится в меню приложений. Перенесите его на рабочий стол.

