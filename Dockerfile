FROM python:3.8
WORKDIR /pypodo
COPY pypodo/ pypodo/
COPY setup.py .
#FIXME how copy all files excpect them in the .gitignore file?
#without this file, thie pip coverage don't work as in pip ci
COPY .coveragerc .
COPY mutatest.ini .
COPY LICENSE.txt .
COPY README.md .
RUN mkdir ci_cd
COPY ci_cd/.todo_mise_en_forme.expected ci_cd/.
#FIXME END
RUN python setup.py install
RUN pip3 install coverage
RUN pip3 install mutatest
RUN pip3 install pylint
RUN pip3 install --user .
COPY pypodo/ .
#ENTRYPOINT [ "python", "./__pypodo__.py" ]
ENTRYPOINT ["pypodo"]