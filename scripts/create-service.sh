#!/bin/bash
export KUBECONFIG_MAN="config-files/manager.cfg"
touch log.txt
kubectl --kubeconfig $KUBECONFIG_MAN -n clusters get fleet > log.txt
n_lines_before=`wc --lines < log.txt`
echo $n_lines_before
git clone $1
cd $2
kubectl apply -f repo.yaml
kubectl --kubeconfig $KUBECONFIG_MAN -n clusters get fleet > log.txt
n_lines_after=`wc --lines < log.txt`
echo $n_lines_after
rm log.txt
if [ $n_lines_after -gt $n_lines_before ]
then
    exit 0
else
    exit 1
fi
