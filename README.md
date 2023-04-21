# Application-Rollout-on-K8s
There has long been the tension between the large amount of deployed Kubernetes clusters and the complex application rollout process on these clusters, making application development and release extremely slow.

The [Rancher Fleet](https://fleet.rancher.io/) project cracks the problem on the cluster management side, while the issues relevant to application management are left unresolved. This application, based on Rancher Fleet, provides a holistic solution to application rollout on Kubernetes clusters.

## What makes a difference from Rancher Fleet?
* **The concept of Service.** Considering big applications comprising several GitHub repositories, we define a Service, represented by one repository, as a component of an Application. We can define a service dependency map to specify the dependency relationships among services to ensure that any rollout process always rolls out a service after all the services it depends on have been rolled out successfully.
* **Changeable cluster labels.** Using Rancher Fleet, once a cluster's label is defined while installing a fleet agent on the cluster, the label is fixed and not subject to changes later. This causes great inconveniences as the grouping of clusters can vary frequently in real-life scenarios. In our application, this problem is resolved by making cluster labels changeable.
* **Visualized rollout experience.** With Rancher Fleet, the rollout experience of an application is by specifying image version and committing a change to GitHub and wait for clusters to align with their corresponding metadata on GitHub. To check whether the cluster is updated, a user has to manually check deployment details a few times using kubectl. With our application, the rollout process is consisted of two steps: set a rollout plan, and create a rollout process. A user specify the version they prefer to roll out to while setting the plan. After a rollout process, the user will be clearly notified which service of the application is being rolled out and the deployment status of each cluster involved. The user can also check the rollout history to fetch the details of each rollout.
* **Simplified operations.** The steps of deploying Rancher Fleet is quite confusing in spite of its official documentation. Following the steps requires some background knowledge in Helm and kubectl operations. While in this applicaion, these steps are completed by scripts, a user does not need to operate anything with kubectl. Rather, a single defined command can do the job.

## Components
* **Application.** An Application is a represenation of an real-world application possibly consisted of multiple GitHub repositories and deployed on multiple Kubernetes clusters. Any other component belongs to an Application.
* **Cluster.** A Cluster is a representation of a Kubernetes cluster to be managed by the pre-defined fleet manager cluster. When registering an Cluster, the user needs to define which Application it belongs to. The Cluster will also have to be specificed which ring it is on.
* **Service.** An big Application has multiple Services, each represented by a GitHub repository. They can possibly depend on each other, and these dependency relationships can be defined. When creating a Service, the user needs to define which Application it belongs to.
* **Rollout.** A Rollout is a process that updates the image of a specified Application on all the Clusters the Application owns on a specific ring.

## APIs
To start using this application, run:  
`$ git clone https://github.com/kliu513/Application-Rollout-on-K8s`  
`$ cd Application-Rollout-on-K8s`  
In the cloned repository, we can start using the APIs.
### Application
**Note:** In an application, the dependency relationships among its services have to be a directed acyclic graph (DAG).
* Create an empty application: `$ python3 cli.py create-application [APPLICATION NAME]`
* Remove an application: `$ python3 cli.py remove-application [APPLICATION NAME]`
* Display an appplication's information: `$ python3 cli.py get-application-info [APPLICATION NAME]`
* Topologically sort and display an application's service relationship map based on their dependency on each other: `$ python3 cli.py get-service-map [APPLICATION NAME]`
* Display all applications: `$ python3 cli.py display-applications`
### Cluster
**Note:** Before adding clusters, a user needs to have a Kubernetes cluster ready and follow [this](https://fleet.rancher.io/installation) tutorial to finish multi-cluster setup and [this](https://fleet.rancher.io/cluster-registration#create-cluster-registration-tokens) to create a cluster registration token.  
After finishing these steps, there should be three new files: `ca.pem`, `token.yaml`, and `values.yaml`. Create a new directory named `config-files` under `Application-Rollout-on-K8s` and copy these files to the directory. Add the configuration file of the Fleet manager to the directory. Before adding a cluster, make sure the cluster's configuration file has been added to the directory `config-files`.  
No need to include `config-files/` in a configuration filepath.
* Register a cluster in an application: `$ python3 cli.py add-cluster [CLUSTER NAME] [ROLLOUT RING] [CONFIGURATION FILEPATH] [APPLICATION]`.
* Remove a cluster: `$ python3 cli.py remove-cluster [CLUSTER NAME]`
* Get a cluster's information: `$ python3 cli.py get-cluster-info [CLUSTER NAME]`
* List the other clusters on a cluster's rollout ring: `python3 cli.py list-cluster-siblings [CLUSTER NAME]`
* Update the rollout ring a cluster is on: `python3 cli.py update-cluster-ring [CLUSTER NAME] [NEW ROLLOUT RING] [CONFIGURATION FILEPATH]`
* Display all clusters: `$ python3 cli.py display-clusters`
### Service
* Create a service in an existing application from a GitHub repository: `$ python3 cli.py create-service [APPLICATION NAME] [SERVICE NAME] [REPOSITORY LINK] [IMAGE VERSION] [DEPENDENCIES]` **Note:** Dependencies are a list of the services depended on in a format of `ServiceA/ServiceB/ServiceC`.
* Reset a service's dependencies: `$ python3 cli.py set-dependencies [APPLICATION NAME] [SERVICE NAME] [NEW DEPENDENCIES]`
* Set a rollout plan for a service: `$ python3 cli.py set-rollout-plan [APPLICATION NAME] [SERVICE NAME] [NEW IMAGE VERSION]`
* Get a service's information: `$ python3 cli.py get-service-info [APPLICATION NAME] [SERVICE NAME]`
* Remove a service: `$ python3 cli.py remove-service [APPLICATION NAME] [SERVICE NAME]`
* Display all services of an application: `$ python3 cli.py display-services [APPLICATION NAME]`
* Display all services: `$ python3 cli.py display-services all`
