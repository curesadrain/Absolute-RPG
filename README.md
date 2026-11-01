# Absolute RPG

Skills, traits and tasks for S.T.A.L.K.E.R. Anomaly / GAMMA / CLIKRAD.

**Current version: 1.7.5 TEST.**

- 66 skills, 224 ranks.
- A PDA skill window accessed through Launcher MAC.
- Russian and English in-game localisations.
- Three magazine profiles: GAMMA/No Mags, CLIKRAD and CLIKRAD with AML.

## Installation

Download the installable ZIP from Releases and install it through MO2.
GitHub's automatic Source code archives are not installation packages.

Required dependencies: Experience Framework 2.2c, Mod App Creator and MCM.
Absolute RPG must win the relevant file conflicts in MO2.
Disable the previous Absolute RPG version and the standalone skill packs
it replaces. Choose exactly one magazine profile. Fully reinstall the mod
and restart the game when switching profiles.

Individual skill requirements and warnings appear in red in the game.
The Russian installation instructions included in the package remain
available in `README_RU.txt`.

## Checks and build

Requires Python 3.10 or newer, with no additional packages.

```text
python -m unittest discover -s tests
python tools/build_release.py
```

File checks do not replace in-game testing. The `tests` and `tools`
directories are excluded from the installation ZIP.

## Credits

Sorano — assembly and development of Absolute RPG.
Experience Framework — Orleon. RPG Perks Pack and inherited skills —
ilrathCXV and Orleon. Full third-party credits are included in `CREDITS.txt`;
provided licences are preserved in `licenses`. Rights to third-party works
remain with their respective authors.

---

## Українська

Система навичок, особливостей і завдань для S.T.A.L.K.E.R. Anomaly / GAMMA / CLIKRAD.

**Поточна версія: 1.7.5 TEST.**

- 66 навичок, 224 ранги.
- Вікно навичок у ПДА через Launcher MAC.
- Російська й англійська локалізації моду.
- Три варіанти системи магазинів: GAMMA/No Mags, CLIKRAD і CLIKRAD з AML.

### Встановлення

Завантажте встановлювальний ZIP у розділі Releases та встановіть його через MO2.
Автоматичні архіви Source code не є встановлювальними пакетами.

Обов’язкові залежності: Experience Framework 2.2c, Mod App Creator і MCM.
Файли Absolute RPG мають перекривати відповідні файли залежностей у MO2.
Перед встановленням вимкніть попередню версію Absolute RPG та окремі пакети
навичок, які він замінює. Оберіть лише один варіант системи магазинів.
Після зміни варіанта повністю перевстановіть мод і перезапустіть гру.

Вимоги й обмеження окремих навичок позначено червоним у грі.
Російськомовна інструкція зі встановлювального пакета збережена
у `README_RU.txt`.

### Перевірки та збирання

Потрібен Python 3.10 або новіший. Додаткові пакети не потрібні.

```text
python -m unittest discover -s tests
python tools/build_release.py
```

Перевірки файлів не замінюють запуск у грі. Каталоги `tests` і `tools`
не потрапляють до встановлювального ZIP.

### Автори

Sorano — збирання й розвиток Absolute RPG.
Experience Framework — Orleon. RPG Perks Pack та успадковані навички —
ilrathCXV і Orleon. Повний перелік сторонніх робіт входить до
встановлювального пакета у файлі `CREDITS.txt`; наявні ліцензії
збережено в каталозі `licenses`. Права на сторонні роботи залишаються
за їхніми авторами.

---

## Русский

Система навыков, особенностей и заданий для S.T.A.L.K.E.R. Anomaly / GAMMA / CLIKRAD.

**Текущая версия: 1.7.5 TEST.**

- 66 навыков, 224 ранга.
- Окно навыков в ПДА через Launcher MAC.
- Русская и английская локализации мода.
- Три варианта системы магазинов: GAMMA/No Mags, CLIKRAD и CLIKRAD с AML.

### Установка

Скачайте установочный ZIP из раздела Releases и установите его через MO2.
Автоматические архивы Source code не являются установочными пакетами.

Обязательные зависимости: Experience Framework 2.2c, Mod App Creator и MCM.
Absolute RPG должен побеждать соответствующие конфликты файлов в MO2.
Отключите предыдущую версию Absolute RPG и отдельные пакеты навыков,
которые он заменяет. Выберите только один вариант системы магазинов.
При смене варианта полностью переустановите мод и перезапустите игру.

Требования и предупреждения отдельных навыков указаны красным в игре.
Русская инструкция из установочного пакета сохранена в `README_RU.txt`.

### Проверки и сборка

Требуется Python 3.10 или новее. Дополнительные пакеты не нужны.

```text
python -m unittest discover -s tests
python tools/build_release.py
```

Проверки файлов не заменяют запуск в игре. Каталоги `tests` и `tools`
не включаются в установочный ZIP.

### Авторы

Sorano — сборка и развитие Absolute RPG.
Experience Framework — Orleon. RPG Perks Pack и унаследованные навыки —
ilrathCXV и Orleon. Полный список сторонних работ включён в `CREDITS.txt`;
имеющиеся лицензии сохранены в `licenses`. Права на сторонние работы
остаются за их авторами.
