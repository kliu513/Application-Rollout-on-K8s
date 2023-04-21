#!/bin/bash
cd $2
export DIR=$(yq -r .spec.paths[0] repo.yaml)
cd $DIR
export NS=$(yq -r .namespace fleet.yaml)
cd ~/App-Rollout-on-K8s
kubectl --kubeconfig $1 get deployment -n $NS
