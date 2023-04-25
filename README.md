# A-T-Registration-System
This repo contains the A&amp;T Registration System project for my final project in COMP710

How to run
---
1. Clone the repo onto your machine
2. Either load the repo onto VSCode or the python CLI and navigate to the repo folder "flask-app"
3. Make sure you have at least python3(and pip)installed and have flask installed. To install flask simply without using and enviroment use the command `python -m pip install flask`
4. You must run init_db.py by entering into the console `python init_db.py` in order to setup the sqlite3 database for the first time before running the app. You no longer need to do this after the first run. 
5. Once everything is setup, all you have to do to run this app using the command `python -m flask --app app run`
6. Go into your favorite browser and enter `localhost:5000` into the URL and the A&amp;T Registation System site should load.

Current Note
---
There is currently no way to get through the login portal by normal means so when you load up the webapp on your `localhost:5000` you can just change the URL to go to the homepage and navigate through the rest of the current framework for the software. (`localhost:5000/home`)