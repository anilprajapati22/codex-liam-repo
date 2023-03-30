#!bin/bash
sudo systemctl daemon-reload
sudo systemctl restart flask-codex-chart.service
sudo docker rm -f codex-react-chart
sudo docker build -t codex-react-chart .
sudo docker run -p 8080:80 -d --name codex-react-chart codex-react-chart
sudo docker ps
