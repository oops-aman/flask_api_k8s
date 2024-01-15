* A basic RESTful CRUD movies api developed using flask.
* Created a docker image name: oopsaman/movie_api
* Deployed to kubernetes

To run this, follow the below steps:
* Run the following command:
  ```
  kubectl apply -f deployment.yaml
  kubectl apply -f busybox.yaml
  ```

* After to check the end points:
  ```
  kubectl exec -it <busy-box-name> -- /bin/sh
  ```
  This will lead to a shell inside your terminal, then run:
  ```
  wget http://<deployed-ip-address>:8080/movies
  ```

Note:
* To get busy-box-name, enter the following command:
  ```
  kubectl get pods
  ```
  Copy the NAME something like busybox

* To get deployed IP address, use the command:
  ```
  kubectl get pods -o wide
  ```
  Copy the IP of any pod.
