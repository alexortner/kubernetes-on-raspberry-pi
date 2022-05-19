# Setup Raspberry Pi headless

For our Kubernetes Cluster we need at least two better three or more Raspberry Pi 3 oder 4. One serves as master node and the others as worker nodes.

To have a proper cluster we need at least one master and one worker node. We start from the scratch first installing an operating system on our Raspberry Pi where we preconfigure Wifi, ssh and hostname. Luckily, since the Raspberry Pi imager exists, it became super easy to create an SD card with everything preconfigured without having to go into config files and modifying anything. 

First step download the [Raspberry Pi Imager](https://medium.com/r/?url=https%3A%2F%2Fwww.raspberrypi.com%2Fsoftware%2F). This wonderful piece of software allows directly to select an image and to preconfigure everything. After installation on your computer start it and click `CHOOSE OS` and then the  entry `Raspberry OS (Other)`. Here choose the 64 bit version `Raspberry Pi OS Lite (64-bit)`. Why using 64-bit and not the default 32-bit version? The reason is there are just more public docker images onARM64as for ARMv7 available and we need images correctly build for our architecture. And also because I do have a Mac Book with an M1 chip and do not need to cross compile.

![image](https://user-images.githubusercontent.com/16557412/169328354-fa136859-7e88-40fc-b106-7d6743d9e9c8.png)  
Next select the SD card to write on and then the configuration wheel to setup headless mode.

![image](https://user-images.githubusercontent.com/16557412/169328551-9b2340a3-f322-40c2-ace4-f2017d60c0aa.png)  
Here configure the wifi, activate ssh with password authentication and enter meaningful hostname. Like kmaster or controlplane for the master node and knode1 or worker1 for the second kubernetes node and so on.

![image](https://user-images.githubusercontent.com/16557412/169330201-afd69710-2635-4e3d-9676-082e8c6358e4.png)  

![image](https://user-images.githubusercontent.com/16557412/169330252-13f479ef-5e4d-4d6c-879f-22a9035ad675.png)  

In my setup I used two RasPi 3 and two RasPi 4. The master is running on a RasPi 4.  
![image](https://user-images.githubusercontent.com/16557412/169330375-30d5b94c-3a85-477c-af91-6e1658e9d6b0.png)

After flashing the SD cards for all the Raspberry Pi. Start up and check if you can find them in your network. Typically you can reach the Raspberry Pi via the hostname set during setup. Like in a personal wifi network via
```
ping kmaster.local
ping knode1.local
```
