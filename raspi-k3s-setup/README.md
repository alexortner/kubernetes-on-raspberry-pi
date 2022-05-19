# Setup Raspberry Pi headless

For our Kubernetes Cluster we need at least two better three or more Raspberry Pi 3 oder 4. One serves as master node and the others as worker nodes.

To have a proper cluster we need at least one master and one worker node. We start from the scratch first installing an operating system on our Raspberry Pi where we preconfigure Wifi, ssh and hostname. Luckily, since the Raspberry Pi imager exists, it became super easy to create an SD card with everything preconfigured without having to go into config files and modifying anything. 

First step download the [Raspberry Pi Imager](https://medium.com/r/?url=https%3A%2F%2Fwww.raspberrypi.com%2Fsoftware%2F). This wonderful piece of software allows directly to select an image and to preconfigure everything. After installation on your computer start it and click `CHOOSE OS` and then the  entry `Raspberry OS (Other)`. Here choose the 64 bit version `Raspberry Pi OS Lite (64-bit)`. Why using 64-bit and not the default 32-bit version? The reason is there are just more public docker images onARM64as for ARMv7 available and we need images correctly build for our architecture. And also because I do have a Mac Book with an M1 chip and do not need to cross compile.
