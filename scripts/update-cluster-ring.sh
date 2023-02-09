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
touch "$CLUSTER.json"
kubectl --kubeconfig $KUBECONFIG_MAN -n clusters get clusters.fleet.cattle.io $CLUSTER -o json > "$CLUSTER.json"
sed -i.bak "s/$2/$3/g" "$CLUSTER.json"
kubectl apply -f "$CLUSTER.json"
kubectl --kubeconfig $KUBECONFIG_MAN -n clusters get clusters.fleet.cattle.io $CLUSTER -o json > "$CLUSTER.json"
echo "here"
if [ grep $2 "$CLUSTER.json" ]
then
    rm "$CLUSTER.json"
    echo "Failed to change the cluster label"
    exit 1
else
    rm "$CLUSTER.json"
    echo "Changed the cluster label successfully"
    exit 0
fi
