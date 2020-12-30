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
# View installed Spark-operator: helm ls -n default
```
- Deploy and View status Steps:  
1) By using the spark-on-k8s-operator:  
   git clone https://github.com/...    
   // Workaround - using FTP as location for main application file  
   // Install, configure and start FTP server  
   // Put Main App file to the FTP directory  
   kubectl apply -f pysparkproject/code/k8s/spark-prime-py-ftp.yaml  
   View: kubectl describe SparkApplication pyspark-prime-ftp -n default  
   View pods: kubectl get pods  
   View pod logs: kubectl logs pyspark-prime-driver  
   Delete: kubectl delete SparkApplication pyspark-prime  
1.1) Configuring Hadoop Conf. access  
    Copy core-site.xml file from Hadoop cluster  
    Install configMap  
```
scp root@hadoop-nn1.reksoft.ru://etc/hadoop/conf/core-site.xml /root/folder/
kubectl create configmap spark-hadoop-configmap --from-file=/root/folder/core-site.xml
```
1.2) Configuring Hadoop Conf. parameters inside yaml file         
2) Alternate way to submit application on K8S Cluster:  
   https://spark.apache.org/docs/3.0.0-preview/running-on-kubernetes.html  
   https://stackoverflow.com/questions/63629870/apache-spark-spark-submit-k8s-api-https-error  
********
Useful links:  
Operator github: https://github.com/GoogleCloudPlatform/spark-on-k8s-operator  
Kubectl cheatsheet: https://kubernetes.io/docs/reference/kubectl/cheatsheet/  
