FROM tensorflow/tensorflow

LABEL maintainer="Nguyen Hoang <htnguyen98.act@gmail.com>"

ENV GECKODRIVER_VER v0.29.0

RUN apt-get update
RUN python3 -m pip install --upgrade pip
RUN apt install -y \
    cron \
    python3-requests \
    python3-flask \
    firefox \
&& pip install selenium \
&& pip install Werkzeug==2.0.1 \
&& pip install webdriver-manager \
&& pip install Pillow \
&& pip install python-telegram-bot \
&& pip install urllib3==1.26.6 \
&& pip install chardet==4.0.0 \
&& pip install MarkupSafe==2.0.1 \
&& pip install requests==2.26.0 \
&& pip install flask \  
&& pip install pymongo \
&& pip install python-crontab \
&& pip install cffi \
&& pip install pyOpenSSL

# Add geckodriver
RUN set -x \
   && curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
   && tar zxf geckodriver-*.tar.gz \
   && mv geckodriver /usr/bin/ \
   && rm geckodriver-*.tar.gz  

COPY . /opt/In0ri
ADD start.sh /start.sh
RUN chmod 755 /start.sh
EXPOSE 8080 8088
WORKDIR /opt/In0ri/FlaskApp
CMD ["/start.sh"]
