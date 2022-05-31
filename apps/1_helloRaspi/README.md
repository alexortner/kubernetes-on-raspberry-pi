# Run some simple tests

## Single Pod that logs "Hello Raspi"

Start a new pod directly with the imperative command that prints a "Hello Raspi" every 2 seconds

```
kubectl run helloraspi --image=busybox -- /bin/sh -c 'while true; do echo $(date)": Hello Raspi"; sleep 2; done'

# check if it is running and on which node with
kubectl get nodes -o wide

# have a look at the live logs
kubectl logs helloraspi -f
```

## Single Pod that runs on a decicated node

By adding node selectors or taints and toleratins one can force a pod to run only on certain nodes.
Use case: In the IoT edge scenario you want to run a certain application only on a certain machine in the field.

The simplest approach is to use label based node selector to attach the pod to a node

Label the nodes via

```
kubectl label nodes kmaster device=kmaster
kubectl label nodes knode1 device=knode1
kubectl label nodes knode2 device=knode2
kubectl label nodes knode3 device=knode3

# check the labels with some custom colum magic
kubectl get nodes -o custom-columns='NAME:.metadata.name,DEVICE:.metadata.labels.device,IP:.status.addresses[0].address'
```

Now lets modify the same pod with a node selector to run on the second node `knode2`.
First create a yaml file via

```
k run helloraspi-knode2 --image=busybox --dry-run=client -o yaml -- /bin/sh -c 'while true; do echo $(date)": Hello Raspi"; sleep 2; done' > pod_singleNode_helloRaspi.yaml
```

and then edit the file and add a node selector to the label `device: knode2`

```
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: helloraspi
  name: helloraspi-knode2
spec:
  nodeSelector:
    device: knode2
  containers:
  - args:
    - /bin/sh
    - -c
    - 'while true; do echo $(date)": Hello Raspi"; sleep 2; done'
    image: busybox
    name: helloraspi
```

## Daemonset that runs one pod on each node

a daemonset takes care that the same pod runs on all nodes at least once
Use case: Basic Sensors should always monitor the edge device (eg. temperatur)

First we create a simple replica set that runs helloRaspi on each node

```
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: helloraspi
spec:
  selector:
    matchLabels:
      app: helloraspi # has to match .spec.template.metadata.labels
  template:
    metadata:
      labels:
        app: helloraspi # has to match .spec.selector.matchLabels
    spec:
      containers:
        - name: helloraspi
          args:
            - /bin/sh
            - -c
            - 'while true; do echo $(date)": Hello Raspi"; sleep 2; done'
          image: busybox
```
