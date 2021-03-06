# Auto Replenishment System (ARS)

Auto replenishment system (ARS) is a system that can detect the weight of the remains in containers everyday, store data in the cloud, predict the time when the remains will run out, and informing the user in time to purchase them. The code for the project can be divided into two parts:

 - Hardware
 - Server APP
 
## Hardware

The hardware program requires doesn't require any extra librarys installed on the Raspberry Pi. Download the code, open the terminal, and type:
```sh
$ python newWeight.py
```
The program will run continuously. It will output the value of the weight every 30 seconds and send the data to our [server](http://34.227.157.139:8000/linkall/dashboard/) for further storing and prediction.


## Server APP

To start server, go to root path, enter the following commands.

Start django server in background:
```sh
$ nohup python manage.py runserver 0:<port> &
```

Modify your notification recieve email address in linkall/scan.py L39.

Run watch dog in background:
```sh
$ nohup python linkall/scan.py loop &
```

If you just want to run watch dog once instead of continuously, use this command:
```sh
$ python linkall/scan.py noloop
```

Then you can start your device

To send your weight data to database, integrade your weight into url, send HTTP request to URL http://34.227.157.139:8000/linkall/submit/{positive int: weight}

To view your data manually, visit http://34.227.157.139:8000/linkall/dashboard/ via any mordern browser.


### File Structure

We used the official APP template of django. All stuff are in it's recommanded position.

Path | Usage
---- | -----
/ars/* | Website setting folder. It doesn't matter here
/linkall/* | For main APP server codes
/linkall/urls.py | Pass the handle of HTTP request
/linkall/models.py | Defines the object structure
/linkall/views.py | Contains functions handle the request, including I/O data to/from DynamoDB, do linear regression
/linkall/scan.py | The watchdog code. It will be periodically run to find the stuff will soon runout. Then notice the user.
/linkall/template/* | HTML templates for front-end rendering
/linkall/static/* | Contians the solid files like CSS/JS and pictures used by web page

### Work Flow

![Image of WorkFlow](./images/ARS.png)
