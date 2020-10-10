#!/bin/bash
green="\e[32m"
red="\e[31m"
./pypodo_ci_cd_docker.sh &&\
echo "" &&\
echo "" &&\
echo "" &&\
echo "*****DEBUT_PIP_BUILD******" &&\
pip3 install --user . &&\
echo "*****FIN_PIP_BUILD******"

if [[ $? = 0 ]]
then
echo -e "$green""CI_CD FULL OK""\e[39m"
else
echo -e "$red""CI_CD FULL KO - ERROR""\e[39m"
exit 1
fi