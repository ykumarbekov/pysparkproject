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
helm install sparkoperator spark-operator/spark-operator --namespace spark-operator --create-namespace --set sparkJobNamespace=default --set enableWebhook=true
View: helm ls --all-namespaces
```