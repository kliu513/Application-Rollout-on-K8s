#!/bin/bash
export KUBECONFIG_MAN="config-files/manager.cfg"
export NODE=$(kubectl --kubeconfig $1 get pods -n cattle-fleet-system -l app=fleet-agent -o json \
    | jq '.items | .[0].spec.nodeName')
touch clusters.txt
kubectl --kubeconfig $KUBECONFIG_MAN get clusters.fleet.cattle.io -n clusters > log.txt
export NODE=$(sed -e 's/^"//' -e 's/"$//' <<< "$NODE")
IFS=' ' read -ra CLUSTER <<< "$(grep $NODE log.txt)"
export CLUSTER
rm clusters.txt
touch cluster.json
kubectl --kubeconfig $KUBECONFIG_MAN -n clusters get clusters.fleet.cattle.io $CLUSTER -o json > cluster.json
sed -i.bak "s/$2/$3/g" cluster.json
kubectl apply -f cluster.json
rm cluster.json
