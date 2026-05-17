FROM alpine:3.23 

WORKDIR /todo-app

# Копируем файлы
COPY app.py database.py requirements.txt ./
COPY static /todo-app/static
COPY templates /todo-app/templates
# Устанавливаем зависимости
RUN apk add --no-cache python3 py3-pip && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt

STOPSIGNAL SIGQUIT
CMD ["/venv/bin/python3", "app.py"]