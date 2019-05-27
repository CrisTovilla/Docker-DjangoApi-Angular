FROM ubuntu:16.04


# Install required packages and remove the apt packages cache when done.

RUN apt-get update && \
    apt-get upgrade -y && \ 	
    apt-get install -y \
	python3 \
	python3-dev \
	python3-setuptools \
	python3-pip \
	nginx \
    supervisor \
	sqlite3 && \
	pip3 install -U pip setuptools && \
   rm -rf /var/lib/apt/lists/*



# Copy nginx configuration 
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
# Copy over static assets from the client application
COPY ./frontend/build /usr/share/nginx/html
# Copy supervisor configuration 
COPY supervisor-app.conf /etc/supervisor/conf.d/
# Copy static api files like admin 
COPY ./api/static/  /usr/share/nginx/html/static/


# Define mountable directories.
VOLUME ["/usr/share/nginx/html/static/",\
		"/etc/nginx/sites-enabled", \
		"/etc/nginx/certs", \
		"/etc/nginx/conf.d", \
		"/var/log/nginx", \
		"/var/www/html"]

# COPY requirements.txt and RUN pip install BEFORE adding the rest of your code, 
# this will cause Docker's caching mechanism
# to prevent re-installing (all your) dependencies when you made a change a line or two in your app.
RUN mkdir -p  /api
COPY ./api/requirements.txt  /api/
RUN pip3 install -r /api/requirements.txt

# add (the rest of) our code
COPY . /api/

EXPOSE 9000

CMD ["supervisord", "-n"]





