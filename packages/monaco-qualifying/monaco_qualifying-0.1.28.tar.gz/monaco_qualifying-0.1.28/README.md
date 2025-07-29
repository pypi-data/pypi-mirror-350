# monaco-qualifying

[License: MIT](https://git.foxminded.ua/liliia-shpytsia-mentoring/task_6_report_of_monaco_2018_racing/-/blob/dev/LICENSE)  
[GitLab Repo](https://git.foxminded.ua/liliia-shpytsia-mentoring/task_6_report_of_monaco_2018_racing)

Python-пакет для аналізу даних кваліфікації Формули 1 - Monaco 2018, який читає дані з трьох файлів:
- [`start.log`](src/monaco_qualifying/data/start.log)
- [`end.log`](src/monaco_qualifying/data/end.log)
- [`abbreviations.txt`](src/monaco_qualifying/data/abbreviations.txt)

обчислює найкращі часи кіл, сортує гонщиків за часом кола та виводить звіт, що показує в таблиці топ-15 гонщиків та 
решту, яка не ввійшла до топ-15.

---

## Зміст

- [Посилання проекту](#посилання-проекту)
- [Встановлення](#встановлення)
- [Використання](#використання)
  - [CLI](#cli)
- [Приклади](#приклади)
- [Оновлення пакету](#оновлення-пакету)
- [Пошук проблем](#пошук-проблем)

---

## Посилання проекту

- **Домашня сторінка**: [monaco-qualifying на GitLab]
(https://git.foxminded.ua/liliia-shpytsia-mentoring/task_6_report_of_monaco_2018_racing)  
- **Випуски**: [Releases]
(https://git.foxminded.ua/liliia-shpytsia-mentoring/task_6_report_of_monaco_2018_racing/-/releases)  
- **Ліцензія**: [MIT License]
(https://git.foxminded.ua/liliia-shpytsia-mentoring/task_6_report_of_monaco_2018_racing/-/blob/dev/LICENSE)  
- **Відкрити Issue**: [Створити Issue]
(https://git.foxminded.ua/liliia-shpytsia-mentoring/task_6_report_of_monaco_2018_racing/-/issues)

---

## Встановлення

```bash
pip install monaco_qualifying
```

---

## Використання

### CLI

- Для виводу повного звіту гонщиків:

```bash
monaco_qualifying
```

---

## Приклади

### Приклад звіту

```
1. Sebastian Vettel | FERRARI | 1:4.415
2. Valtteri Bottas | MERCEDES | 1:12.434
3. Stoffel Vandoorne | MCLAREN RENAULT | 1:12.463
...
----------------------------------------------------------------------
16. Daniel Ricciardo | RED BULL RACING TAG HEUER | 2:47.987
17. Sergey Sirotkin | WILLIAMS MERCEDES | 4:47.294
```

---

## Оновлення пакету

```bash
pip install --upgrade monaco_qualifying
```

## Пошук проблем
- Якщо виникли проблеми, створити 
[Issue](https://git.foxminded.ua/liliia-shpytsia-mentoring/task_6_report_of_monaco_2018_racing/-/issues) на GitLab.

---
