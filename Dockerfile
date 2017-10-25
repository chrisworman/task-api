FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# temporary environment! TODO: move to 'docker run' command
ENV APP_SETTINGS development
ENV FLASK_APP run.py
ENV SECRET development-secret
ENV DATABASE_URL postgresql://localhost/tasks_api?user=root\&password=dev-password
