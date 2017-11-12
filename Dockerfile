FROM tiangolo/uwsgi-nginx-flask:python3.6

# Copy and install requirements first to make rebuilds quicker in some cases
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app source code into the container
COPY . /app

# The api listens on port 80
EXPOSE 80
