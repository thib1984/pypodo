#not 3.8-alpine is not compatible with cryptoex
FROM python:3.8-slim-buster
WORKDIR /pypodo
COPY pypodo/ pypodo/
COPY setup.py .
#FIXME how copy all files excpect them in the .gitignore file?
#without this file, thie pip coverage don't work as in pip ci
COPY .coveragerc .
COPY .pylintrc .
COPY mutatest.ini .
COPY LICENSE.txt .
COPY README.md .
#FIXME END
RUN python setup.py install
RUN pip3 install coverage
RUN pip3 install mutatest
RUN pip3 install pylint
RUN pip3 install freezegun
RUN pip3 install --user .
#COPY pypodo/ .
ENTRYPOINT ["pypodo"]