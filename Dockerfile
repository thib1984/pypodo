FROM python:3.8
WORKDIR /pypodo
COPY pypodo/ pypodo/
COPY setup.py .
COPY .coveragerc .
COPY LICENSE.txt .
COPY README.md .
RUN mkdir ci_cd
COPY ci_cd/.todo_mise_en_forme.expected ci_cd/.
RUN python setup.py install
RUN pip3 install --user .
COPY pypodo/ .
#ENTRYPOINT [ "python", "./__pypodo__.py" ]
ENTRYPOINT ["pypodo"]