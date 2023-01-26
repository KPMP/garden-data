# based upon https://www.youtube.com/watch?v=s_o8dwzRlu4

# Minicube installation

$ brew install minikube

# start minikube


## NOTE --driver=hyperkit on mac
$ minikube start --driver docker

# get minikube [status](status)
$ minikube status

# show active nodes
$ kubectl get node

# get all running services
$ kubectl get all

# get pod information
$ kubectl get pod

# get pod log information
$ kubectl logs <pod name from kubectl get pod command> -f

# get service information
$ kubectl get svc

# get kube ip to access service
$ minikube ip
OR
$ kubectl get svc -o wide


# apply configs, ordered based on dependencies
$ kubectl apply -f mongo-config.yaml
$ kubectl apply -f mongo-secret.yaml
$ kubectl apply -f mongo.yaml
$ kubectl apply -f webapp.yaml

# delete minikube
$ minicube delete

# stop minicube
# minicube stop
