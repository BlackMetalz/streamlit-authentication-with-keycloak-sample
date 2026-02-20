# Create new realm for testing purpose

- URL: http://localhost:8080/admin/master/console/#/master/add-realm

![alt text](01.png)

# Create new client

- URL: http://localhost:8080/admin/master/console/#/kienlt-demo/clients/add-client

![alt text](02.png)

![alt text](03.png)

Valid redirect URIs is wrong: please update to `http://localhost:8501/*`
![alt text](04.png)

# Copy client secret and paste to .env file

![alt text](05.png)

# Test Login

![alt text](06.png)

Umm, create account before login xD

![alt text](07.png)

Set password. I have no password policy so `123123` xDDD

![alt text](08.png)

Ok, time to login.

![alt text](09.png)

Success! Welcome to my dashboard xD

So issue in current state. Everytime I hit refresh/f5 button, it asked me to click button login again.

So worklog is create 3 dashboard with sidebar navigation for testing purpose.

Ok great. No issue after chaging dashboard

![alt text](10.png)