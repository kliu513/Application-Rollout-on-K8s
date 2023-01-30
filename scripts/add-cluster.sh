#!/bin/bash
touch log.txt
kubectl config use-context fleet-manager
kubectl --namespace clusters get fleet >> log.txt
n_lines_before=`wc --lines < log.txt`
helm -n cattle-fleet-system install --create-namespace --wait \
    --kubeconfig $1 \
    --set-string labels.group=$2 \
    --values values.yaml \
    fleet-agent https://github.com/rancher/fleet/releases/download/v0.5.0/fleet-agent-0.5.0.tgz
kubectl --namespace clusters get fleet > log.txt
n_lines_after=`wc --lines < log.txt`
rm log.txt
if [$n_lines_after > $n_lines_before]; then
    exit 0
else
    exit 1
fi
