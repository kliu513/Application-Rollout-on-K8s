#!/bin/bash
touch log.txt
kubectl --kubeconfig config-files/fleet-manager.cfg use-context fleet-manager
kubectl -n clusters get clusters.fleet.cattle.io >> log.txt
n_lines_before=`wc --lines < log.txt`
echo "$n_lines_before"
kubectl --kubeconfig $1 use-context fleet-manager
helm -n cattle-fleet-system install --create-namespace --wait \
    --set-string labels.group=$2 \
    --values ../config-files/values.yaml \
    fleet-agent https://github.com/rancher/fleet/releases/download/v0.5.0/fleet-agent-0.5.0.tgz
kubectl --kubeconfig config-files/fleet-manager.cfg use-context fleet-manager
kubectl -n clusters get clusters.fleet.cattle.io > log.txt
n_lines_after=`wc --lines < log.txt`
echo "$n_lines_after"
rm log.txt
if [$n_lines_after -gt $n_lines_before]
then
    exit 0
else
    exit 1
fi
