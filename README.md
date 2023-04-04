# App-Rollout-on-K8s
There has long been the tension between the large amount of deployed Kubernetes clusters and the complex application rollout process on these clusters, making application development and release extremely slow.

The [Rancher Fleet](https://fleet.rancher.io/) project cracks the problem on the cluster management side, while the issues relevant to application management are left unresolved. This application, based on Rancher Fleet, provides a holistic solution to application rollout on Kubernetes clusters.

## What makes a difference from Rancher Fleet?
* **The concept of a Service.** Considering big applications comprising several GitHub repositories, we define a Service, represented by one repository, as a component of an Application. We can specify the dependency relationships among services to ensure that any rollout process always rolls out a service after all the services it depends on have been rolled out successfully.
