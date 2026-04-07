# Сборка образа:(Предварительно можете перейти в папку с проектом)
```
 docker build . -t <Ваше название:версия>
```

" . " -- Точка обозначает директорию сборки. Либо можете указать абсолютный путь

# Запуск(через команду):
```
docker run -v ./todo-data:/todo-app/data -d -p 80:5000 --name <Название контейнера> <Ваше название:версия>
```
 
`-p 80:5000` -- Проброс портов в контейнер. 5000 должен быть обязателен если вы не меняли порт внутри кода приложения. 80 порт можете заменять на более удобный.

# Запуск(через compose):
**В репозитории есть готовый docker-compose.yml**
```
version: '3.8'
services:
  todo-app:
    image: <Ваше название:версия>
    ports:
      - '80:5000'
    volumes:
      - ./todo-data:/todo-app/data # <== Директории базы данных
    container_name: todo # <== Название контейнера
    restart: 'unless-stopped'
```
# Главное помните
```
80:5000 <= Внутрений порт (контейнер)
 ^
Внешний порт

```
# Nginx.conf
```
events {
   worker_connections 1024;
}
http {
 server {
       listen 80;
       server_name todo.local; # <== Доменное имя
       location / {
           proxy_pass http://192.168.0.3:200; # <== Внешний порт контейнера (у меня 200)
           proxy_set_header Host $host; # <== Этот блок отвечает за логирование(1)
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For proxy_add_x_forwarded_for; # <== (1)
                  }
          }
}         
```