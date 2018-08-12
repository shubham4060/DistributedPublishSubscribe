# distributedPubSub
Distributed systems term project for distributed systems course in IIT Kharagpur

Team members : 
Apurv Kumar 14CS10006,
Shubham Sharma 14CS30034,
Asket Agarwal 14CS30006

To run on different systems in the institute network, type : (disables proxy in current terminal session) <br />
. env.sh <br />
in all the systems where the scripts are run

To generate proto files : <br />
python -m grpc_tools.protoc -I proto/ --python_out=. --grpc_python_out=. pr.proto <br />

To clean the dataBackup directory: <br />
. clean.sh

To setup mongodb : <br />
install mongodb version 3 or above <br />
make data/db in / directory using nautilus or sudo permissions <br />
type: <br />
python -m pip install pymongo <br />
sudo chown -R `id -u` /data/db <br />
install mogodb client like robomongo3t to view contents of the mongodb
