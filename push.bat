@echo off
title Pushing on github...

set /p commit="Commit : "

git add .
git commit -m "%commit%"
git push origin master

PAUSE