# Auto Replenishment System (ARS)

Auto replenishment system (ARS) is a system that can detect the weight of the remains in containers everyday, store data in the cloud, predict the time when the remains will run out, and informing the user in time to purchase them. The code for the project can be divided into two parts:

 - Server APP
 - Hardware
 
## Hardware

The hardware program requires doesn't require any extra librarys installed on the Raspberry Pi. Download the code, open the terminal, and type:
```sh
$ python newWeight.py
```
The program will run continuously. It will output the value of the weight every 30 seconds and send the data to our [server](http://34.227.157.139:8000/linkall/dashboard/) for further storing and prediction.


## Server APP

### File Structure

We used the official APP template of django. All stuff are in it's recommanded position.

/ars/* is the website setting folder. It doesn't matter here

/linkall/* for main APP server codes
/linkall/urls.py pass the handle of HTTP request
/linkall/models.py defines the object structure
/linkall/views.py contains functions handle the request, including I/O data to/from DynamoDB, do linear regression
/linkall/scan.py is the watchdog code. It will be periodically run to find the stuff will soon runout. Then notice the user.
/linkall/template/* is HTML templates for front-end rendering
/linkall/static/* contians the solid files like CSS/JS and pictures used by web page

### Work Flow

The views.py under linkall folder is our main APP codes. And the urls is the caller of these functions.

When we login /linkall/sumbit/{weight} url, url.py will match it to the record

```python
path('submit/<int:weight>', views.submit, name="submit"),
```

Then the server will pass the handle to views.submit function.

In views.sumbit function, we will 
