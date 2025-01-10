# О проекте

Apload — это файлообменник, позволяющий анонимно загружать и скачивать файлы достаточно больших размеров. Это мой учебный проект для изучения новых технологий и получения практических навыков.

## Используемый стек технологий
- Python
- Django
- Redis
- Docker

## Distributed Data Storage Network (DDSN)

Для обеспечения возможности хранения больших объемов данных реализована распределенная сеть хранения данных (далее DDSN) позволяющая хранить все данные не на одном, а сразу на нескольких серверах. Причем, важно отметить, что данные на них не дублируются, а наоборот: на разных серверах хранятся разные данные. Хоть данные и хранятся на разных серверах, но получить к ним доступ, как и загрузить файл можно просто обратившись к основному серверу сети.

### Архитектура DDSN

![Сетевая архитектура сервиса](https://github.com/Explorer-art/apload_project/blob)

DDSN состоит из 2-х типов серверов:
- Master сервер — основной узел сети. Master сервер в сети может быть только один.
- FS сервер — именно на нем хранятся данные. Серверов FS в сети может быть несколько (FS — File Storage).
