# Публичен сайт на Общество

Публичният сайт на http://www.obshtestvo.bg.

## Инсталация на проекта (за програмисти)

Проектът е написан на Python и Django, и използва MySQL.

### Development среда
#### Автоматича настройка

Нужни са ви единствено:

 - [Vagrant](http://www.vagrantup.com/), ако нямате - [сваляте и инсталирате](
https://ww.vagrantup.com/downloads.html)
 - [VirtualBox](https://www.virtualbox.org/), ако нямате - [сваляте и инсталирате](https://www.virtualbox.org/wiki/Downloads)

В директория на проекта пускате 1 команда:

```sh
vagrant up
```

Това може да отнеме няколко минути, след което имате работещ сайта на адрес:  [http://localhost:8888/](http://localhost:8888/)

Администратор на сайта е `admin` с парола `admin`, чрез който имате достъп до [административния панел](http://localhost:8888/admin/).

##### Детайли
Автоматичната настройка създава виртуална машина s заемаща 370mb. Може да я спирате и пускате с команди от директорията на проекта:

```sh
vagrant halt # изключва
vagrant up # включва
```

За още дейтали [вижте какво се инсталира в нея](bootstrap.sh).

#### Ръчна настройка

1. Нужен ви е Python 2.7. Проектът не е тестван на други версии.
2. Трябва да имате MySQL 5.x, плюс header файлове.
3. Инсталирайте pip, ако нямате – `easy_install pip` или `sudo easy_install pip`
4. Инсталирайте virtualenvwrapper – `pip install virtualenvwrapper` или `sudo pip install virtualenvwrapper`.
5. Заредете командите на virtualenvwrapper: `source /usr/local/bin/virtualenvwrapper.sh` – дава достъп до `mkvirtualenv` и други.
6. `mkvirtualenv obshtestvobg --no-site-packages` – ще създаде виртуална среда за инсталиране на pip пакети в `~/.virtualenvs/obshtestvobg`.
7. `workon obshtestvobg` за да превключите на това обкръжение.
8. Клонирайте хранилището и влезте в директорията на проекта.
9. Зависимостите на проекта: `pip install -r requirements.txt`

    Ако компилацията на MySQL адаптера не мине, може да се наложи да се изпълни `export CFLAGS=-Qunused-arguments` ([реф.](http://stackoverflow.com/questions/22313407/clang-error-unknown-argument-mno-fused-madd-python-package-installation-fa)) и да се стартира отново командата.
10. Създайте база данни в MySQL:

        CREATE DATABASE obshtestvo CHARACTER SET utf8 COLLATE utf8_general_ci
11. Създайте файл със специфичните за локалното ви копие настройки, като копирате `server/settings_app.py.sample` като `server/settings_app.py` и въведете там параметрите за достъп до MySQL базата данни.
12. Подгответе базата за първото пускане на миграциите: `python manage.py syncdb  --noinput`
13. Пуснете миграциите: `python manage.py migrate`
14. Направете си админ потребител с `python manage.py createsuperuser`
15. Пуснете си сървър с `python manage.py runserver`

Би трябвало да може да достъпите приложението на [http://localhost:8000/](http://localhost:8000/).

### Production среда

Инсталирайте приложението, използвайки инструкциите в предишната секция за ръчни настройки, с тези разлики:

1. В `server/settings_app.py`:

	- Променете `DEBUG = True` на `DEBUG = False`.
	- Генерирайте нова стойност на `SECRET_KEY`.

2. Настройте уеб сървъра си да сервира статичните файлове, намиращи се в `STATIC_ROOT` (обикновено папката `static/` в корена на проекта) на URL `/static/`.
3. Уверете се, че по време на deployment се изпълнява командата `python manage.py collectstatic -l`, за да се копират статичните файлове от приложението в `STATIC_ROOT`.
4. Използвайте Nginx или Apache сървър, плюс uwsgi server и uwsgi python plugin. Могат да се използват съответните конфигурационни файлове в папка `server/`.

##### Почистване на кеша на production системата

```
find /var/cache/nginx/ -type f | xargs rm
```

### Deployment

След първоначалната инсталация, проектът се качва на сървъра с `fab deploy`. Копирайте `fabric_settings.py.sample` във `fabric_settings.py` и го редактирайте, за да отговаря на вашите настройки за deploy. След това, процедурата е следната:

1. Правите промени.
2. `git commit` и `git push` на промените.
3. Изпълнявате `fab deploy` от корена на вашето локално копие.

Скриптът за deploy върши доста от нещата, описани в предишните секции.

### Примерна инсталация на Debian-базирана машина

Вижте командите в [инсталационния файл](bootstrap.sh) за Vagrant.
