#!bin/bash

sudo systemctl restart flask-codex
#sudo rm -r react-frontend/
sudo docker rm -f codex-react
sudo docker build -t codex-react /home/metamorf/react-frontend
sudo docker run -p 80:80 -d --name codex-react codex-react
sudo docker ps

#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