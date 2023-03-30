#!bin/bash
#  bash copy-files.sh sgnons-commit-message
git add .
git commit -m $1
git push origin sgnons-without-chart
