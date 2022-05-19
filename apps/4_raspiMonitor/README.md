# IoT example app running on each Raspi

To demonstrate a use case where an application (pod) should run on each device we just read some system parameters like cpu, memory and temperature and publish it a mqtt broker

## Build docker image for arm64

Depending on the system you are using you have either to use a crossbuilder or install Docker on a Raspberry Pi and build there.
If you are a user of a new Mac Book with M1 arm64 chip you are lucky and can build directly local

The Docker images are very basic. We just install a libary to grace fully shotdown the Python app, some hardware driver for Python and copy in the Pythin code

```
FROM python:3.9-slim

RUN pip install psutil pyembedded

COPY raspi_monitor.py ./

CMD ["python","./raspi_monitor.py"]
```

Build and push the image via

```
# login to dockerhub or another repo
docker login <user and repo>

# build the image
docker build -t tingelbuxe/k3s-meetup:raspi-monitor -f Dockerfile.monitor .

# push the image
docker push tingelbuxe/k3s-meetup:raspi-monitor

## Create a Pod yaml with privileged container

In order to execute something on the node hardware we need to allow the container to access the hardware. This is typically not allowed. A quick and dirty way (BUT ABSOLUTELY NOT RECOMENDED for anything beside of experiments. !NOT FOR PRODUCTION) is to grant the container `privileged` root rights.
Second we need to force the Pod only to run on the node where the hardware is connected
The simplest approach is to use a nodeSelector via label.

```

apiVersion: v1
kind: Pod
metadata:
labels:
run: led-blue
name: led-blue
spec:
nodeSelector:
device: kmaster
containers: - image: tingelbuxe/k3s-meetup:ws2813-blue
imagePullPolicy: Always
name: led-blue
securityContext:
privileged: true

```

```
