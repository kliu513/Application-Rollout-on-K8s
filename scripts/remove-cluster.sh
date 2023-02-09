#!/bin/bash
touch log.txt
helm --kubeconfig $1 -n cattle-fleet-system uninstall fleet-agent
kubectl --kubeconfig $1 get deployments --all-namespaces > log.txt
export KUBECONFIG_MAN="config-files/manager.cfg"
export NODE=$(kubectl --kubeconfig $1 get pods -n cattle-fleet-system -l app=fleet-agent -o json \
    | jq '.items | .[0].spec.nodeName')
touch log.txt
kubectl --kubeconfig $KUBECONFIG_MAN get clusters.fleet.cattle.io -n clusters > log.txt
export NODE=$(sed -e 's/^"//' -e 's/"$//' <<< "$NODE")
IFS=' ' read -ra CLUSTER <<< "$(grep $NODE log.txt)"
export CLUSTER
rm log.txt
kubectl delete clusters.fleet.cattle.io $CLUSTER --kubeconfig $KUBECONFIG_MAN -n clusters
if [ grep "fleet-agent" log.txt ]
then
    rm log.txt
    exit 1
else
    rm log.txt
    kubectl delete namespace cattle-fleet-system
    exit 0
fi
