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
sudo nano /boot/cmdline.txt
# and the following at the end of the line.
# IMPORTANT everything in ONE line, NO line break)
cgroup_memory=1 cgroup_enable=memory
# new line should look like the following 
# DO NOT COPY THIS LINE, it will be different on your Raspi
console=serial0,115200 console=tty1 root=PARTUUID=<UNIQUE_RASPI_ID> rootfstype=ext4 fsck.repair=yes rootwait cgroup_memory=1 cgroup_enable=memory
# exit nano via 
str+x and y + enter
```
In order to make the change effective reboot the system
```
sudo reboot
```
Finally you can check if Kubernetes works and the master node is available
```
sudo k3s kubectl get nodes
```
## Install k3s agents on worker nodes
In order to install the k3s agents on the other Raspberries we need first to get the IP address and the access token from the master node. Run the following commands on the master node.

```
# on kmaster
# show IP
hostname -I | awk '{print $1}'

# get token
sudo cat /var/lib/rancher/k3s/server/node-token
K101568b95ffbf1ddc0dfdsad1d87eb702eb04fce3376204be44d5eded02831a36f::server:83684b530e6562f86b84d5d5bf4a2eab
```


Now ssh into each worker node and install the k3s agent with the following commands.
```
# on knodesX
curl -sfL https://get.k3s.io | K3S_URL=https://<kmaster_IP>:6443 K3S_TOKEN=<token_from_above> sh -
```
This two environment variables directly start the k3s agent and registers the node on the master. Now you have again to add the `cgroup` in */boot/cmdline.txt* as show above. 

After reboot you can ssh into your master node and check if the nodes where registered correctly (can take a couple of minutes) via

```
sudo k3s kubectl get nodes
```
should look like this
![image](https://user-images.githubusercontent.com/16557412/169335337-fd7090a5-eecc-49f9-b791-897f3e8614be.png)

## Configure kubectl on client
I assume that you have a working kubectl setup on your local computer from where you want to access the cluster. If not you can for example install docker desktop with minicube and you will have kubectl available
The kube config file can be found on the master node

```
# on kmaster
sudo cat /etc/ranlcher/k3s/k3s.yaml
```
Copy the content and add it to your kube config file that can typically be found in the home folder `~/.kube/config`
Here it is important to replace the localhost IP *127.0.0.1* of the server with the actual IP address of the master node
the cube config could look like this

```
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0t....LS0K
    server: https://<MASTER IP>:6443
    name: k3s-cluster
contexts:
- context:
    cluster: k3s-cluster
    user: k3s-admin
    name: k3s
current-context: k3s
kind: Config
preferences: {}
users:
- name: k3s-admin
  user:
    client-certificate-data: LS0tL....LS0K
    client-key-data: LS0tLS...LQo=
```

now switch to the context and test if it works and you can see the nodes as above

```
kubectl config use-context k3s
kubectl get nodes
```


