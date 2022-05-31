# Setup a MQTT Broker
There are two ways installing the Mosquitto MQTT Broker on the Raspberry PI
First using a public Helm Chart or second setting it up yourself using a public docker image

## Install Mosquitto via Helm

Prerequisit is a workinb Helm installation on your lokal machine.
Then install Mosquitto MQTT Broker via

```
helm install mosquitto k8s-at-home/mosquitto
```

unfortunately this Helm chart creates by default a service of the type ClusterIP. 
Unfortunately the service type is not parameterised and can’t be changed by using the values.yaml file. 
So in order to access the MQTT Broker from outside the Kubernetes Cluster you need to change the type to NodePort manually by editing the service.
Therefore run
```
k edit svc -n mqtt
# this opens a VIM like editor
# to insert a value hit the key <i> and change 
type: ClusterIP
# to 
type: ClusterIP
# save by hitting first <esc> + <:> and then <w><q>
```
If you look now to the service it should have an nodePort assigned
```
k get svc -n mqtt
```
If you have a Mosquitto client installed on your local Laptop you can subscribe to the broker running on the cluster and publish messages.


## Test with Mosquitto on Mac OS

You can install a Mosquitto MQTT client on mac with brew

```
brew install mosquitto
```

to connect either forward the port to the localhost or use the Nodes IP/Hostname and the Node Port

```
kubectl port-forward service/mosquitto 1883:1883
```

subscribe to a topic via

```
# port forwarding
mosquitto_sub -h localhost -p 1883 -t test

# on cluster nodeport
mosquitto_sub -h 192.168.2.2 -p 31349 -t test

mosquitto_sub -h kmaster.local -p 31349 -t test
```

and publish via

```
mosquitto_pub -h localhost -p 1883 -t test -m "my message, Suckers!!"

# on cluster nodeport
mosquitto_pub -h 192.168.2.2 -p 31349 -t test -m "Geilomat"
mosquitto_pub -h kmaster.local -p 31349 -t test -m "Geilomat"

```
