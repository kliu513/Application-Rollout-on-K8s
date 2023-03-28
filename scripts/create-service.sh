#!/bin/bash
export KUBECONFIG_MAN="config-files/manager.cfg"
touch log.txt
kubectl --kubeconfig $KUBECONFIG_MAN -n clusters get fleet > log.txt
n_lines_before=`wc --lines < log.txt`
git clone $1
cd $2
kubectl apply -f repo.yaml
cd ..
kubectl --kubeconfig $KUBECONFIG_MAN -n clusters get fleet > log.txt
n_lines_after=`wc --lines < log.txt`
rm log.txt
kubectl --kubeconfig $KUBECONFIG_MAN -n clusters get fleet
if [ $n_lines_after -gt $n_lines_before ]
then
    exit 0
else
    exit 1
fi
