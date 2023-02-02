#!/bin/bash
touch log.txt
helm --kubeconfig $1 -n cattle-fleet-system uninstall fleet-agent
kubectl --kubeconfig $1 get deployments --all-namespaces >> log.txt
if [ grep "fleet-agent" log.txt ]
then
    rm log.txt
    exit 1
else
    rm log.txt
    kubectl delete namespace cattle-fleet-system
    exit 0
fi