#!/bin/bash
export KUBECONFIG_MAN="config-files/manager.cfg"
export NODE=$(kubectl --kubeconfig $1 get pods -n cattle-fleet-system -l app=fleet-agent -o json \
    | jq '.items | .[0].spec.nodeName')
echo "here"
touch clusters.txt
kubectl --kubeconfig $KUBECONFIG_MAN get clusters -n clusters > log.txt
echo "here"
export NODE=$(sed -e 's/^"//' -e 's/"$//' <<< "$NODE")
export CLUSTER=$(grep $NODE log.txt)
echo $CLUSTER
rm clusters.txt
touch cluster.json
kubectl --kubeconfig $KUBECONFIG_MAN -n clusters get cluster $CLUSTER -o json > cluster.json
echo "here"
sed -i.bak "s/$2/$3/g" cluster.json
kubectl apply -f cluster.json
rm cluster.json
