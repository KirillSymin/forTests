!!! local_settings.env выложен в целях упрощения запуска, в реальности его не должно быть !!!
### Инструкция по запуску:
 - Склонировать репозиторий: 
   - **git clone git@github.com:KirillSumin/YandexAcademyYandexDisk2022.git**
 - Перейти в папку с проектом: 
   - **cd YandexAcademyYandexDisk**
 - Запустить приложение: 
   - **make up**
 - (опционально) Создать администратора Django: 
   - **make createsuperuser**
``` 
git clone git@github.com:KirillSumin/YandexAcademyYandexDisk2022.git
cd YandexAcademyYandexDisk
make up
make createsuperuser
```

### Доступные команды make:
 - **build** (сборка проекта без его запуска)
 - **up** (сборка проекта и запуск)
 - **tests** (запуск тестов)
 - **migrate** (проведение миграций Django)
 - **createsuperuser** (создание администратора Django admin)
 - **stop** (остановка приложения без удаления контейнеров)
 - **clear** (остаовка приложения и удаление котнтейнеров)