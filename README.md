# О проекте

Apload — это анонимный файлообменник, позволяющий анонимно загружать и скачивать файлы достаточно больших размеров. Это мой учебный проект для изучения новых для меня технологий и получения практических навыков.

## Используемый стек технологий
- Python
- Django
- Redis
- Docker

## Distributed Data Storage Network (DDSN)

Для обеспечения возможности хранения больших объемов данных реализована распределенная сеть хранения данных (далее DDSN) позволяющая храненить все данные не на одном, а сразу на нескольких серверах. Причем, важно отметить, что данные на них не дублируются, а наоборот: на разных серверах хранятся разные данные. Хоть данные и хранятся на разных серверах, но получить к ним доступ, как и загрузить файл можно просто обратившись к основному серверу сети.

### Архитектура DDSN

DDSN состоит из 2-х типов серверов:
- master сервер — основной узел сети. Он состоит из 3-х компонентов: вебсайт, поисковик и балансировщик нагрузки. Master сервер в сети может быть только один.
- сервер хранения — именно на нем хранятся данные.
