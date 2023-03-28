#!/bin/bash
cd $2
export DIR=$(yq -r .spec.paths[0] repo.yaml)
cd $DIR
export NS=$(yq -r .namespace fleet.yaml)
cd
export IMAGE=$(kubectl --kubeconfig $1 get deployment -n $NS -o json\
 | jq '.items | .[0].spec.template.spec.containers | .[0].image')
export IMAGE=$(sed -e 's/^"//' -e 's/"$//' <<< $IMAGE)
IFS=':' read -ra version <<< $IMAGE
if [ ${version[-1]} = $3 ]
then
    exit 1
else
    exit 0
fi
