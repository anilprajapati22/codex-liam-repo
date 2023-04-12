FROM python:3.8

COPY new_req.txt new_req.txt
RUN pip3 install -r new_req.txt
WORKDIR flask-app
COPY . .
EXPOSE 50001
VOLUME /templates
CMD ["flask","--app","CODEX","run","-h","0.0.0.0","-p","50001"]

# need to run nginx image on server to show chart and mount templates folder
# here also mount templates folder with local directory and mount same with ngix server to show chart



# docker build -t flask-codex-chart-backend .

# docker run -p 8081:80 -v /home/metamorf/github/codex-liam-repo/chart-html:/usr/share/nginx/html -d --name chart-html nginx:alpine

# docker run --env-file ../frontend/.env -p 50001:8083 -d -v /home/metamorf/github/codex-liam-repo/chart-html:/flask-app/templates  --name flask-codex-chart-backend flask-codex-chart-backend

# docker rm -f flask-codex-chart-backend
