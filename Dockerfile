FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5432
