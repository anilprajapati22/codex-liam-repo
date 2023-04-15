#!bin/bash

# sudo systemctl restart flask-codex
# sudo rm -r react-frontend/
sudo docker rm -f codex-react-chart-frontend
sudo docker build -t codex-react-chart-frontend  /home/metamorf/github/codex-liam-repo/frontend/
sudo docker run -p 8080:80 -d --name codex-react-chart-frontend codex-react-chart-frontend
sudo docker ps

