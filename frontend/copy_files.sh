#!bin/bash
# bash copy-files.sh sgnons-commit-message
rm -r codex-liam-repo/frontend
rm -r codex-liam-repo/backend
scp -r presidio@192.168.1.11:/Users/presidio/sgn/metamorf/codex-code/frontend /home/sgnons/codex-liam-repo/
scp -r presidio@192.168.1.11:/Users/presidio/sgn/metamorf/codex-code/backend /home/sgnons/codex-liam-repo/
cd /home/sgnons/codex-liam-repo/
git add .
git commit -m $1
git push origin sgnons-chart 
