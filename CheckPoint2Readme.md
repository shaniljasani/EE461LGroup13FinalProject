URL to our deployed application: http://autocar.pythonanywhere.com/

User manual:
To run our application, the link will take you directly to the homepage of our application. From there, you will see a navigation bar that includes a link to the homepage, dashboard, downloads available, login and signup. Without logging in, you will be able to access any of these tabs. However, to work on or create any new projects (which are renting cars or joining/creating carshares in our appliocation), you will be directed to the login screen. If you do not have a login, there is an option to signup for our application. If you are not logged in, you can still see the dashboard of cars available for checkout. If you enter an invalid login, then the login screen will be reprompted. After you have logged in, the dashboard tab is where all of the HW sets checking in and out will happen. After going to the dashboard, you will see all of the available cars to checkout. If a car is already checked out, it will not show up on the dashboard (Each HW set only has 1 availability). The car will be connected to that car share id or rental id until it is returned. If another user wants to join one's carshare, they will be able to by entering the maker's groupID that they created when starting the car share. To download the list of datasets pulled from and the dataset being used, go to the downloads tab and click the two buttons. The datasets will be downloaded to your machine. To access projects created, scroll to the bottom of the dashboard page. When a car is checked out, it is removed from the dashboard page for others to view unless they have the group id to join the car share.

Issues still present in the application:
Error prompting when incorrect login entered, 

Division of work on this project checkpoint:
-Backend: Julian, Renzo
-Frontend: Shanil
-Database: Amy
-Cloud: Madilyn

Items to be accomplished during phase 3:
1. Carshare history
2. More page asthetics
3. Billing system
4. Error notification when incorrect login
5. Edge case testing
6. Encryption
7. Animations

Issues ran into during setup for cloud:
Originally, we had planned on using Google Cloud for the setup of deployment of the application. After using Heroku during lab, we decided to switch over to that. However, during Heroku deployment, our Heroku had issues connecting based on the branches found in the github repository. After much research into different cloud deployments, we ultimately decided to use PythonAnywhere to deploy our application. Ultimately, PythonAnywhere was very useful because during deployment, we are able to check the server and error logs if some systems are not working. Also we were able to set up a virtual environement to deploy MongoDB and other requirements and dependencies needed during the application.
