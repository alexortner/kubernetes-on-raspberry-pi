# IoT example app for a LED Strip

## LED Strip specs

We use a ws2813 strip used which uses two signal cabels and is quit bad documented for a Raspbery Pi
It also works the documentation for the ws2815 strip but not the one for ws2811 or ws2812b
We us only 10 LEDs which allows us to power them directly from the Raspberry Pi pins, longer strips would need an external power device

## Wiring

The Strip has 4 contacts marked as

- GND
- BI
- DI
- 5V 

 They are wired to the following GPIO pins from the Raspbery Pi  
- GND --> one of the GND pins
- BI --> GPIO 10
- DI --> GPIO 18
- 5V --Y one of the 5V pins

## Build docker image

The Docker images are very basic. 
We just install a libary to grace fully shotdown the Python app, some hardware driver for Python and copy in the Python code to switch the LED on and off.

```
FROM python

RUN apt-get update && apt-get install dumb-init -y

RUN pip install rpi-ws281x RPi.GPIO

COPY LEDStrip_ws2813_blue.py ./

# use the program dumb-init to rewrite pod terminaton to ctrl-c signal to shutdown led array again
# https://tasdikrahman.me/2019/04/24/handling-singals-for-applications-in-kubernetes-docker/
# https://github.com/Yelp/dumb-init
ENTRYPOINT ["dumb-init", "--rewrite", "15:2", "--"]

CMD ["python","./LEDStrip_ws2813_blue.py","-c"]
```

Build and push the image via

```
# login to dockerhub or another repo
docker login <user and repo>

# build the image
docker build -t <repo>:ws2813-party -f Dockerfile.party .

# push the image
docker push <repo>:ws2813-party
```

## Create a Pod yaml with privileged container

In order to access hardware of a node, the Raspberry Pi where we connected the LED, we need to allow the container to access the hardware. This is typically not allowed for containers.  
A quick and dirty way (BUT ABSOLUTELY NOT RECOMENDED for anything beside of experiments. !!NOT FOR PRODUCTION) is to grant the container `privileged` root rights.
Second we need to force the Pod to run only on the node where the hardware is connected
The simplest approach is to use a nodeSelector via label.
For that first label the node
```
kubectl label node <node-name-where-LED-strip-is-connected> device=led-node
```
And then use this label in the node selector of the Pod

```
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: led-blue
  name: led-blue
spec:
  nodeSelector:
    device: led-node
  containers:
    - image: <repo>:ws2813-party
      imagePullPolicy: Always
      name: led-party
      # give container root access to underlying hardware
      securityContext:
        privileged: true
```
