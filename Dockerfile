FROM python:3.8
WORKDIR /pypodo
COPY pypodo/ pypodo/
COPY setup.py .
RUN python setup.py install
RUN pip3 install --user .
COPY pypodo/ .
#ENTRYPOINT [ "python", "./__pypodo__.py" ]
ENTRYPOINT ["pypodo"]