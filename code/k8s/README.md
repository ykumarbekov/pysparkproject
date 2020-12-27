Spark operator on k8s  
Runs Spark applications specified in Kubernetes objects of the SparkApplication custom resource type  
Steps:  
- Install helm on K8s cluster  
- Add repo  
```
helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
helm search repo spark-operator

```
- Install Operator  
```
helm install autodataspark spark-operator/spark-operator --namespace default --set sparkJobNamespace=default --set enableWebhook=true
View: helm ls --all-namespaces
```
- Deploy and View status  
```
kubectl apply -f pysparkproject/code/k8s/spark-prime-py.yaml
View: kubectl describe SparkApplication pyspark-prime -n default
View pods: kubectl get pods --all-namespaces
View pod logs: kubectl logs pyspark-prime-driver
```