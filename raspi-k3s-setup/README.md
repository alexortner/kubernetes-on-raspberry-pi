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

If you can't reach the Raspberry Pi like this you have to find out the ip addresses by logging into your router and searching registered devices with the hostnames.

---

# Setup k3s Kubernetes Cluster
The lightweight Kubernetes distribution k3s is a free small size Kubernetes Version dedicated for Edge devices and ARM architectures developed and maintained from [Rancher](https://medium.com/r/?url=https%3A%2F%2Francher.com%2Fdocs%2Fk3s%2Flatest%2Fen%2F).
 
## Architecture
A server node is defined as a Raspberry Pi running the `k3s server` command. The worker node are defined as Raspberry Pi running the `k3s agent` command. The agents are registered on the server node and the cluster can be accessed via kubectl and the master node.
![image](https://user-images.githubusercontent.com/16557412/169331443-7579d5f4-f476-4e2e-bcef-0541a01b213c.png)

Further details about the architectures and the possibilities for high availability configurations can be found in the [official documentation](https://medium.com/r/?url=https%3A%2F%2Francher.com%2Fdocs%2Fk3s%2Flatest%2Fen%2Farchitecture%2F).

## Install k3s server on master node
First ssh into the first Raspberry Pi where you want to install the `k3s server` using the hostname or IP. Authenticated via password. If you did not change it the standard password is `raspberry`

```
# connect via your hostname
ssh pi@kmaster.local  
# or the ip address
ssh pi@192.168.1.123
```
Second install k3s with the install script
```
curl -sfL https://get.k3s.io | sh -
```

Typically the installation now throws a failure message that the `cgroup` is not correctly setup.
```
[INFO] Failed to find memory cgroup, you may need to add "cgroup_memory=1 cgroup_enable=memory" to your linux cmdline (/boot/cmdline.txt on a Raspberry Pi)
```
Just do exactly what the message says. Open the file */boot/cmdline.txt* and **append** the mentioned string at the end of the line. It is important that there is **no line break added.**


```


