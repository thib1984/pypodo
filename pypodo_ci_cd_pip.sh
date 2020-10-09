#!/bin/bash
echo "" &&\
echo "" &&\
echo "" &&\
echo "*****DEBUT_PIP_BUILD******" &&\
pip3 install --user . &&\
echo "*****FIN_PIP_BUILD******" &&\
echo "" &&\
echo "" &&\
echo "" &&\
echo "*****DEBUT_PIP_TEST******" &&\
python3 -m unittest -v pypodo/__pypodo__test.py &&\
echo "*****FIN_PIP_TEST******" &&\
echo "" &&\
echo "" &&\
echo "" &&\
echo "*****DEBUT_PIP_COVERAGE******" &&\
coverage pypodo run -m unittest pypodo/__pypodo__test.py &&\
echo "*****FIN_PIP_COVERAGE******" &&\

if [[ $? = 0 ]]
then
echo ""
echo ""
echo ""
echo "CI_CD PIP OK"
else
echo ""
echo ""
echo ""
echo "CI_CD PIP KO - ERROR"
exit 1
fi