#!/bin/bash
smoketest="$1"
echo pypodo list &&\
$smoketest list &&\
echo pypodo add "tache1" &&\
$smoketest add "tache1" &&\
echo pypodo add "tache2 #montag #20190101" &&\
$smoketest add "tache2 #montag #20190101" &&\
echo pypodo add "tache3 #urgent #30000101" &&\
$smoketest add "tache3 #urgent #30000101" &&\
echo pypodo list && $smoketest list &&\
echo pypodo del 2 &&\
$smoketest del 2 &&\
echo pypodo tag montag2 3 &&\
$smoketest tag montag2 3 &&\
echo pypodo ag urgente 3 &&\
$smoketest tag urgente 3 &&\
echo pypodo sort &&\
$smoketest sort &&\
$smoketest add "mon autre tache #tag #retag" &&\
echo pypodo list tag retag &&\
$smoketest list tag retag &&\
echo pypodo untag retag 3 &&\
$smoketest untag retag 3 &&\
echo pypodo tag newtag 3 3 2 &&\
$smoketest tag newtag 3 3 2 &&\
echo pypodo list &&\
$smoketest list &&\
echo pypodo tag &&\
$smoketest tag &&\
echo pypodo untag &&\
$smoketest untag &&\
echo pypodo find "t.*che" && $smoketest find "t.*che" &&\
echo pypodo list with config &&\
echo "[COLOR]" >> /tmp/.todo.rc &&\
echo "index = red" >> /tmp/.todo.rc &&\
echo "task = yellow" >> /tmp/.todo.rc &&\
echo "tag = grey" >> /tmp/.todo.rc &&\
$smoketest list