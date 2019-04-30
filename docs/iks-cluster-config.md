# Manual cluster config

## Deploy Sysdig

### IBM Cloud CLI Auth

```'shell
$ ibmcloud login -sso -r eu-de
API endpoint: https://api.us-east.bluemix.net
Get One Time Code from https://identity-3.eu-central.iam.cloud.ibm.com/identity/passcode to proceed.
Open the URL in the default browser? [Y/n]> Y
One Time Code >
Authenticating...
OK

Select an account:
...
8. DEMO (4fd48221017bc3ae0817c113177133df) <-> 25146773
Enter a number> 8
Targeted account DEMO (4fd48221017bc3ae0817c113177133df) <-> 25146773

Targeted resource group Default

Targeted region eu-de


API endpoint:      https://api.eu-de.bluemix.net
Region:            eu-de
User:              <EMAIL>
Account:           DEMO (4fd48221017bc3ae0817c113177133df) <-> 25146773
Resource group:    Default
CF API endpoint:
Org:
Space:
```

### Get cluster config

```'shell
$ ibmcloud ks clusters
Clusters at version 1.11 and later run containerd instead of Docker as the Kubernetes container runtime. For more information and update actions, see <https://ibm.biz/Bd22hF>

If you have clusters that run Kubernetes versions 1.10 and earlier, update them now to continue receiving important security updates and support. Kubernetes version 1.10 is deprecated and will be unsupported 15 May 2019. Versions 1.9 and earlier are already unsupported. For more information and update actions, see <https://ibm.biz/iks-versions>

OK
Name                     ID                                 State    Created      Workers   Location    Version       Resource Group Name   
ibmcloud-meetup-dublin   a643ba904da949e5bc19ca671ebd4a37   normal   5 days ago   2         Frankfurt   1.12.7_1548   demos   

$ ibmcloud target -g demos
Targeted resource group demos

API endpoint:      https://api.eu-de.bluemix.net
Region:            eu-de
User:              <EMAIL>
Account:           DEMO (4fd48221017bc3ae0817c113177133df) <-> 25146773
Resource group:    demos   
CF API endpoint:      
Org:                  
Space:                

$ ibmcloud ks cluster-config ibmcloud-meetup-dublin
OK
The configuration for ibmcloud-meetup-dublin was downloaded successfully.

Export environment variables to start using Kubernetes.

export KUBECONFIG=/Users/gallomas/.bluemix/plugins/container-service/clusters/ibmcloud-meetup-dublin/kube-config-fra02-ibmcloud-meetup-dublin.yml

$ kubectl get nodes
NAME            STATUS   ROLES    AGE     VERSION
10.194.57.103   Ready    <none>   5d23h   v1.12.7+IKS
10.194.57.106   Ready    <none>   5d23h   v1.12.7+IKS
```

### Deploy Sysdig

```'shell
$ curl -sL https://ibm.biz/install-sysdig-k8s-agent | bash -s -- -a 6ba0210d-55ac-485b-9bd2-c2f219ee9a6d -c ingest.eu-de.monitoring.cloud.ibm.com -ac 'sysdig_capture_enabled: false'
* Detecting operating system
* Downloading Sysdig cluster role yaml
* Downloading Sysdig config map yaml
* Downloading Sysdig daemonset v2 yaml
* Creating namespace: ibm-observe
* Creating sysdig-agent serviceaccount in namespace: ibm-observe
* Creating sysdig-agent clusterrole and binding
clusterrole.rbac.authorization.k8s.io/sysdig-agent created
* Creating sysdig-agent secret using the ACCESS_KEY provided
* Retreiving the IKS Cluster ID and Cluster Name
* Setting cluster name as ibmcloud-meetup-dublin
* Setting ibm.containers-kubernetes.cluster.id a643ba904da949e5bc19ca671ebd4a37
* Updating agent configmap and applying to cluster
* Setting tags
* Setting collector endpoint
* Adding additional configuration to dragent.yaml
* Enabling Prometheus
configmap/sysdig-agent created
* Deploying the sysdig agent
daemonset.extensions/sysdig-agent created

$ kubectl get pods -n ibm-observe
NAME                 READY   STATUS    RESTARTS   AGE
sysdig-agent-8nm72   0/1     Pending   0          14s
sysdig-agent-cxw26   0/1     Pending   0          14s

$ kubectl describe pod sysdig-agent-8nm72 -n ibm-observe
Name:               sysdig-agent-8nm72
Namespace:          ibm-observe
Priority:           0
PriorityClassName:  <none>
Node:               <none>
Labels:             app=sysdig-agent
                    controller-revision-hash=69455dbbb
                    pod-template-generation=1
Annotations:        kubernetes.io/psp: ibm-privileged-psp
Status:             Pending
IP:
Controlled By:      DaemonSet/sysdig-agent
Containers:
  sysdig-agent:
    Image:      sysdig/agent
    Port:       <none>
    Host Port:  <none>
    Limits:
      memory:  1Gi
    Requests:
      cpu:        100m
      memory:     512Mi
    Readiness:    exec [test -e /opt/draios/logs/running] delay=10s timeout=1s period=10s #success=1 #failure=3
    Environment:  <none>
    Mounts:
      /dev/shm from dshm (rw)
      /host/boot from boot-vol (ro)
      /host/dev from dev-vol (rw)
      /host/etc/os-release from osrel (ro)
      /host/lib/modules from modules-vol (ro)
      /host/proc from proc-vol (ro)
      /host/run from run-vol (rw)
      /host/usr from usr-vol (ro)
      /host/var/run from varrun-vol (rw)
      /opt/draios/etc/kubernetes/config from sysdig-agent-config (rw)
      /opt/draios/etc/kubernetes/secrets from sysdig-agent-secrets (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from sysdig-agent-token-d4gz2 (ro)
Conditions:
  Type           Status
  PodScheduled   False 
Volumes:
  osrel:
    Type:          HostPath (bare host directory volume)
    Path:          /etc/os-release
    HostPathType:  FileOrCreate
  dshm:
    Type:    EmptyDir (a temporary directory that shares a pod's lifetime)
    Medium:  Memory
  dev-vol:
    Type:          HostPath (bare host directory volume)
    Path:          /dev
    HostPathType:  
  proc-vol:
    Type:          HostPath (bare host directory volume)
    Path:          /proc
    HostPathType:  
  boot-vol:
    Type:          HostPath (bare host directory volume)
    Path:          /boot
    HostPathType:  
  modules-vol:
    Type:          HostPath (bare host directory volume)
    Path:          /lib/modules
    HostPathType:  
  usr-vol:
    Type:          HostPath (bare host directory volume)
    Path:          /usr
    HostPathType:  
  run-vol:
    Type:          HostPath (bare host directory volume)
    Path:          /run
    HostPathType:  
  varrun-vol:
    Type:          HostPath (bare host directory volume)
    Path:          /var/run
    HostPathType:  
  sysdig-agent-config:
    Type:      ConfigMap (a volume populated by a ConfigMap)
    Name:      sysdig-agent
    Optional:  true
  sysdig-agent-secrets:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  sysdig-agent
    Optional:    false
  sysdig-agent-token-d4gz2:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  sysdig-agent-token-d4gz2
    Optional:    false
QoS Class:       Burstable
Node-Selectors:  <none>
Tolerations:     node-role.kubernetes.io/master:NoSchedule
                 node.kubernetes.io/disk-pressure:NoSchedule
                 node.kubernetes.io/memory-pressure:NoSchedule
                 node.kubernetes.io/network-unavailable:NoSchedule
                 node.kubernetes.io/not-ready:NoExecute
                 node.kubernetes.io/unreachable:NoExecute
                 node.kubernetes.io/unschedulable:NoSchedule
Events:
  Type     Reason            Age                  From               Message
  ----     ------            ----                 ----               -------
  Warning  FailedScheduling  20s (x9 over 3m18s)  default-scheduler  0/2 nodes are available: 1 node(s) didn't match node selector, 2 Insufficient memory.
```

### Configure cluster autoscaler

```'shell
$ kubectl get secrets -n kube-system | grep storage-secret-store
storage-secret-store                                    Opaque                                 1      5d23h

$ ibmcloud ks worker-pool-get --cluster ibmcloud-meetup-dublin --worker-pool default 
Retrieving worker pool default from cluster ibmcloud-meetup-dublin...
OK

Name:               default   
ID:                 a643ba904da949e5bc19ca671ebd4a37-d0e487f   
State:              active   
Hardware:           shared   
Zones:              fra02   
Workers per Zone:   2   
Labels:             ibm-cloud.kubernetes.io/worker-pool-id=a643ba904da949e5bc19ca671ebd4a37-d0e487f   
Machine Type:       u3c.2x4.encrypted

$ kubectl get serviceaccount -n kube-system tiller
NAME     SECRETS   AGE
tiller   1         4d

$ helm install ibm/ibm-iks-cluster-autoscaler --namespace kube-system --name ibm-iks-cluster-autoscaler
NAME:   ibm-iks-cluster-autoscaler
LAST DEPLOYED: Tue Apr 30 12:13:48 2019
NAMESPACE: kube-system
STATUS: DEPLOYED

RESOURCES:
==> v1/ClusterRole
NAME                        AGE
ibm-iks-cluster-autoscaler  7s

==> v1/ClusterRoleBinding
NAME                        AGE
ibm-iks-cluster-autoscaler  7s

==> v1/ConfigMap
NAME              DATA  AGE
iks-ca-configmap  1     9s

==> v1/Pod(related)
NAME                                        READY  STATUS             RESTARTS  AGE
ibm-iks-cluster-autoscaler-9c658b56f-bjlnr  0/1    ContainerCreating  0         5s

==> v1/Role
NAME                        AGE
ibm-iks-cluster-autoscaler  7s

==> v1/RoleBinding
NAME                        AGE
ibm-iks-cluster-autoscaler  7s

==> v1/Service
NAME                        TYPE       CLUSTER-IP     EXTERNAL-IP  PORT(S)   AGE
ibm-iks-cluster-autoscaler  ClusterIP  172.21.76.227  <none>       8085/TCP  6s

==> v1/ServiceAccount
NAME                        SECRETS  AGE
ibm-iks-cluster-autoscaler  1        8s

==> v1beta1/Deployment
NAME                        READY  UP-TO-DATE  AVAILABLE  AGE
ibm-iks-cluster-autoscaler  0/1    1           0          6s


NOTES:
Thank you for installing: ibm-iks-cluster-autoscaler. Your release is named: ibm-iks-cluster-autoscaler

For more information about using the cluster autoscaler, refer to the chart README.md file.

$ kubectl get pods --namespace=kube-system | grep ibm-iks-cluster-autoscaler
ibm-iks-cluster-autoscaler-9c658b56f-bjlnr                       1/1     Running   0          29s

$ kubectl get service --namespace=kube-system | grep ibm-iks-cluster-autoscaler
ibm-iks-cluster-autoscaler                       ClusterIP      172.21.76.227    <none>           8085/TCP                     42s

$ kubectl edit cm iks-ca-configmap -n kube-system -o yaml
apiVersion: v1
data:
  workerPoolsConfig.json: |
    [
     {"name": "default","minSize": 2,"maxSize": 6,"enabled":true}
    ]
kind: ConfigMap
metadata:
  annotations:
    workerPoolsConfigStatus: '{}'
  creationTimestamp: 2019-04-30T11:13:50Z
  name: iks-ca-configmap
  namespace: kube-system
  resourceVersion: "836411"
  selfLink: /api/v1/namespaces/kube-system/configmaps/iks-ca-configmap
  uid: 08472a39-6b39-11e9-888b-728e6b98356c
$ helm get values ibm-iks-cluster-autoscaler -a
expander: random
image:
  pullPolicy: Always
  repository: registry.bluemix.net/ibm/ibmcloud-cluster-autoscaler
maxNodeProvisionTime: 120m
resources:
  limits:
    cpu: 300m
    memory: 300Mi
  requests:
    cpu: 100m
    memory: 100Mi
scaleDownDelayAfterAdd: 10m
scaleDownDelayAfterDelete: 10m
scaleDownUnneededTime: 10m
scaleDownUtilizationThreshold: 0.5
scanInterval: 1m
skipNodes:
  withLocalStorage: true
  withSystemPods: true

$ helm upgrade --set scaleDownDelayAfterAdd=5m,scaleDownDelayAfterDelete=5m,scaleDownUnneededTime=5m,maxNodeProvisionTime=50m ibm-iks-cluster-autoscaler ibm/ibm-iks-cluster-autoscaler -i
WARNING: Namespace "default" doesn't match with previous. Release will be deployed to kube-system
Release "ibm-iks-cluster-autoscaler" has been upgraded. Happy Helming!
LAST DEPLOYED: Tue Apr 30 13:08:23 2019
NAMESPACE: kube-system
STATUS: DEPLOYED

RESOURCES:
==> v1/ClusterRole
NAME                        AGE
ibm-iks-cluster-autoscaler  54m

==> v1/ClusterRoleBinding
NAME                        AGE
ibm-iks-cluster-autoscaler  54m

==> v1/ConfigMap
NAME              DATA  AGE
iks-ca-configmap  1     54m

==> v1/Pod(related)
NAME                                         READY  STATUS             RESTARTS  AGE
ibm-iks-cluster-autoscaler-6df54c5dd5-7xlcp  0/1    ContainerCreating  0         3s
ibm-iks-cluster-autoscaler-7866c6f74b-q9pql  1/1    Terminating        0         12m

==> v1/Role
NAME                        AGE
ibm-iks-cluster-autoscaler  54m

==> v1/RoleBinding
NAME                        AGE
ibm-iks-cluster-autoscaler  54m

==> v1/Service
NAME                        TYPE       CLUSTER-IP     EXTERNAL-IP  PORT(S)   AGE
ibm-iks-cluster-autoscaler  ClusterIP  172.21.76.227  <none>       8085/TCP  54m

==> v1/ServiceAccount
NAME                        SECRETS  AGE
ibm-iks-cluster-autoscaler  1        54m

==> v1beta1/Deployment
NAME                        READY  UP-TO-DATE  AVAILABLE  AGE
ibm-iks-cluster-autoscaler  0/1    1           0          54m


NOTES:
Thank you for installing: ibm-iks-cluster-autoscaler. Your release is named: ibm-iks-cluster-autoscaler

For more information about using the cluster autoscaler, refer to the chart README.md file.


$ kubectl get nodes
NAME            STATUS   ROLES    AGE     VERSION
10.194.57.103   Ready    <none>   5d23h   v1.12.7+IKS
10.194.57.106   Ready    <none>   5d23h   v1.12.7+IKS

$ kubectl edit cm iks-ca-configmap -n kube-system -o yaml
apiVersion: v1
data:
  workerPoolsConfig.json: |
    [
     {"name": "default","minSize": 3,"maxSize": 6,"enabled":true}
    ]
kind: ConfigMap
metadata:
  annotations:
    workerPoolsConfigStatus: '{"2:6:default":"SUCCESS"}'
  creationTimestamp: 2019-04-30T11:13:50Z
  name: iks-ca-configmap
  namespace: kube-system
  resourceVersion: "842432"
  selfLink: /api/v1/namespaces/kube-system/configmaps/iks-ca-configmap
  uid: 08472a39-6b39-11e9-888b-728e6b98356c

$ kubectl describe configmap iks-ca-configmap -n kube-system
Name:         iks-ca-configmap
Namespace:    kube-system
Labels:       <none>
Annotations:  workerPoolsConfigStatus: {"3:6:default":"SUCCESS"}

Data
====
workerPoolsConfig.json:
----
[
 {"name": "default","minSize": 3,"maxSize": 6,"enabled":true}
]

Events:  <none>

$ ibmcloud ks worker-ls --cluster ibmcloud-meetup-dublin
OK
ID                                                 Public IP       Private IP      Machine Type        State          Status                                              Zone    Version   
kube-fra02-cra643ba904da949e5bc19ca671ebd4a37-w1   169.50.63.233   10.194.57.103   u3c.2x4.encrypted   normal         Ready                                               fra02   1.12.7_1549*   
kube-fra02-cra643ba904da949e5bc19ca671ebd4a37-w2   169.50.63.231   10.194.57.106   u3c.2x4.encrypted   normal         Ready                                               fra02   1.12.7_1549*   
kube-fra02-cra643ba904da949e5bc19ca671ebd4a37-w3   169.50.63.230   10.194.57.109   u3c.2x4.encrypted   provisioning   Waiting for IBM Cloud infrastructure: Assign Host   fra02   1.12.7_1550   

* To update to 1.12.7_1550 version, run 'ibmcloud ks worker-update'. Review and make any required version changes before you update: ibm.biz/upworker
```

