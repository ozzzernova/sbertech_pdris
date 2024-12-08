## Kubernetes

~~0. страдания с тем что snap плохо поставил minikube~~
1. Стартуем `minikube start`
![](img/1.png)
2. Поды через `kubectl`
 ```
kubectl create -f kube/postgres.yaml
kubectl create -f kube/deployment.yaml
 ```
3. Создаем сервис
 ![](img/2.png)
4. Лицезреем успех
 ![](img/3.png)
5. Напоследок посмотрим, что запущено
 ![](img/4.png)
