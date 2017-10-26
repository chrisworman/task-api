FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# I'm not sure if this is still needed for postgres ... my thought is no: TODO: try and remove it
EXPOSE 80
