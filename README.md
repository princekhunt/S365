***S365 is a web application that acts as an identity provider and focuses on giving users' identities to its clients so, they won't have to worry about user management, security, or privacy.***

**How to Setup environment**
1. Install python3 and pip3 on your computer
2. download the code from Github.
3. Edit your hosts file, if you're using a mac, then you'll find your hosts file at /etc/hosts. If you're using windows you'll find the hosts file at C:\Windows\System32\Drivers\etc\hosts.
    1. add the following lines in hosts file
      127.0.0.1       tech-blog.s365.com
      127.0.0.1       s365.com
      127.0.0.1       tech-blog.com
    2. Save the file(you may need administrative rights).
4. Now open install virtualenv on your computer and run the command **python3 -m venv venv**.
5. activate the venv **source /venv/bin/activate**
6. now install the requirements by the following commands
    1. python3 -m pip install requests
    2. python3 -m pip install django_hosts
7. Now open the folder named **S365**, and run the command **python3 manage.py runserver**
8. Open the folder named **TechBlog**, and run the command **python3 manage.py runserver 8001**
9. Now the project is ready.

**How it will work**
1. Let's assume, TechBlog is a demo client of S365, and it's dependent on S365 to manage its user's authentications.
2. Now go to https://tech-blog.com:8001, click on **verify yourself**, and then click on **verify me**, which will lead you to our main application **S365**.
3. Now as tech-blog is a client of S365, you'll see URL **http://tech-blog.S365.com**.
4. After you input your email address and press "submit," TechBlog will automatically determine whether or not you are already a registered user.
5. A name field and two password fields will appear if you are not logged in. After filling out the form, click "sign up." 
6. And it's done. It's quick and you won't have to bother about logging in after signing up because it will do it for you automatically.
7. If you register with temporary or incorrect emails, S365 won't let you sign up. 
8.  You will now be taken to the TechBlog to access its services.

1. Now click on logout to see its login functionalities.
2. After logging out, select the "Verify Me" button once more to be taken to S365, where you can input your registered email address.
3. a password field will come up. enter your password and you'll be redirected back to the TechBlog.
4. Two-factor authentication will be activated for that user if a malicious IP address attempts to enter into a user account, and the user may then be required to pass two-factor authentication to prove themselves.
5. If your IP belongs to TOR's exit nodes, then you might need to pass two-factor authentication.
6. On the second failed login attempt when a user enters an erroneous password, S365 sends an OTP to the user's email address to confirm the user's identity.

1. When a user request logout from TechBlog, TechBlog will erase the session and tell S365 to do that too.

**Logics**


1. When a user requests authentication on TechBlog, TechBlog creates a unique key at random, saves it in the database and browser as a form of cookie, and then refers the user to S365's URLs for authentication. It also transmits the ukey to S365 on the client side.

2. S365 requests the user's email address and then checks its database to see if the user already exists for the TechBlog client. If not, the name and password fields will be shown. 
3. After the user double-enters their password and name and clicks "sign up," S365 stores the information in its database for Client TechBlog and produces a special token.
4. S365 will transmit the user's token, ukey, name, and email address along with a post request to TechBlog's callback url, and redirects to TechBlog. 
5. The user's name and email address that are connected to the ukey will be saved by TechBlog.
6. When a user visits TechBlog, TechBlog will retrieve the name and email linked with the cookie-ukey from the user's browser.
7. TechBlog retains the user's name and email address together and encrypted token will saved in a form of a cookie on user's browser.

1. When a user requests to log in on TechBlog, TechBlog will redirect to S365, and after inputting an email address, S365 will display the password field when a user account for the Client-TechBlog is identified on S365's database.
2. When a user enters a password, S365 first checks to see if the account has ever encountered a failed login; if so, it switches to two-factor authentication. If not, it will then take the IP address, examine it for recent abusive behaviour, look it up in lists of abusive IPs, and if it finds any, it will switch to two-factor authentication.
3. If the user enters a bad password, the account will be moved to the TFA-required position, where the user must successfully complete TFA.
4. S365 will generate a token and send it to TechBlog after the user's password matches the database and all other necessary conditions are met.
5. When S365 determines that a user requires an additional layer of authentication to log in, it will send an OTP to the user's email address on behalf of TechBlog, display an OTP submission form, and save the OTP and key in a database.
6. S365 will remove all limitations and send TechBlog a special token when a user enters the right OTP.

1. TechBlog will submit a request with a token when a user wishes to log out, S365 will acknowledge the request and discard the token, and TechBlog will wipe the user's session data from user's browser.
