#!/bin/bash
smoketest="$1"
echo pypodo list &&\
$smoketest list &&\
echo pypodo add "task1" &&\
$smoketest add "task1" &&\
echo pypodo add "task2 #tag1 #20190101" &&\
$smoketest add "task2 #tag1 #20190101" &&\
echo pypodo add "task3 #urgent #30000101" &&\
$smoketest add "task3 #urgent #30000101" &&\
echo pypodo list && $smoketest list &&\
echo pypodo del 2 &&\
$smoketest del 2 &&\
echo pypodo tag tag2 3 &&\
$smoketest tag tag2 3 &&\
echo pypodo tag veryurgent 3 &&\
$smoketest tag veryurgent 3 &&\
echo pypodo sort &&\
$smoketest sort &&\
$smoketest add "task4 #tag #retag" &&\
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
echo pypodo find "t.*sk4" && $smoketest find "t.*sk4"