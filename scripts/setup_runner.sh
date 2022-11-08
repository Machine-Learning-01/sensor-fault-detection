#!bin/bash

sudo apt update

sudo apt-get update

mkdir actions-runner

cd actions-runner

curl -o actions-runner-linux-x64-2.298.2.tar.gz -L https://github.com/actions/runner/releases/download/v2.298.2/actions-runner-linux-x64-2.298.2.tar.gz

echo "0bfd792196ce0ec6f1c65d2a9ad00215b2926ef2c416b8d97615265194477117  actions-runner-linux-x64-2.298.2.tar.gz" | shasum -a 256 -c

tar xzf ./actions-runner-linux-x64-2.298.2.tar.gz

./config.sh --url https://github.com/Machine-Learning-01/sensor-fault-detection --token $1 --runnergroup Default --name self-hosted --labels ineuron --work _work --replace [--name self-hosted] 

sudo ./svc.sh install

sudo ./svc.sh start