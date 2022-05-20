# Setup a MQTT Broker

## Install Mosquitto via Helm

prerequisit is a workin Helm installation
Install Mosquitto MQTT Broker via

```
helm install mosquitto k8s-at-home/mosquitto
```

but this default helm chart does not have

## Test on Mac

install Mosquitto via brew

```
brew install mosquitto
```

either forward the port to the localhost or use the Cluster IP

```
kubectl port-forward service/mosquitto 1883:1883
```

subscribe to a topic via

```
# port forwarding
mosquitto_sub -h localhost -p 1883 -t test

# on cluster nodeport
mosquitto_sub -h kmaster.local -p 31349 -t test
```

and publish via

```
mosquitto_pub -h localhost -p 1883 -t test -m "my message, Suckers!!"

# on cluster nodeport
mosquitto_pub -h kmaster.local -p 31349 -t test -m "Geilomat"
```
