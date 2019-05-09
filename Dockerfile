FROM floydhub/dl-docker:cpu

ENV PORT 8080
ENV HOST 0.0.0.0


RUN apt-get update && apt-get install -y \
    curl apt-utils apt-transport-https debconf-utils gcc build-essential g++\
    && rm -rf /var/lib/apt/lists/*

# adding custom MS repository
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/14.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# install SQL Server drivers
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql unixodbc-dev

# install SQL Server tools
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y mssql-tools
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
RUN /bin/bash -c "source ~/.bashrc"

RUN pip install --upgrade pip

RUN apt-get remove -y python-chardet python-numpy python-scipy

RUN apt-get install -y unixodbc unixodbc-dev

COPY requirements.txt /
RUN pip install -r /requirements.txt

RUN apt-get install -y locales \
    && echo "nb_NO.UTF-8 UTF-8" > /etc/locale.gen \
    && echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
    && locale-gen

RUN locale-gen "en_US.UTF-8"

WORKDIR /usr/src/app

COPY . /usr/src/app



EXPOSE 8080

CMD ["python", "application.py"]
