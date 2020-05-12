# Auto Replenishment System (ARS)

Auto replenishment system (ARS) is a system that can detect the weight of the remains in containers everyday, store data in the cloud, predict the time when the remains will run out, and informing the user in time to purchase them. The code for the project can be divided into two parts:

 - Server APP
 - Hardware
 
### Hardware

The hardware program requires doesn't require any extra librarys installed on the Raspberry Pi. Download the code, open the terminal, and type:
```sh
$ python newWeight.py
```
The program will run continuously. It will output the value of the weight every 30 seconds and send the data to our [server](http://34.227.157.139:8000/linkall/dashboard/) for further storing and prediction.


### Server APP