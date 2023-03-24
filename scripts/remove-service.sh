#!/bin/bash
export KUBECONFIG_MAN="config-files/manager.cfg"
kubectl --kubeconfig $KUBECONFIG_MAN -n clusters delete "gitrepo.fleet.cattle.io/$1"
