#!/bin/bash
cd $1
export DIR=$(yq -r .spec.paths[0] repo.yaml)
cd $DIR
sed -i "/name: $4/,/tag: $2/{s/tag: $2/tag: $3/}" fleet.yaml
git add .
git commit -m "$4 $3"
git push
