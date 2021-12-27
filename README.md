This repo contains two projects:

 - `postbook` small social network web app
 - `postbook_robot` bot app for creating users, posts and liking posts in `postbook`

For running `postbook`:

    docker-compose -f postbook/docker-compose.yml up -d
    docker exec -it postbook_web_1 python migrate.py 

For running `postbook_robot`:

    cd postrobot/
    pip install -r requirements.txt
    python robot.py
   
   You can change configurable parameters by updating `postrobot/config.json`

