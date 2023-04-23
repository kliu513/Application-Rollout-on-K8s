# Application-Rollout-on-K8s
There has long been a tension between the large amount of Kubernetes clusters needed and, on these clusters, the cumbersome application rollout process, which makes the development and deployment of applications extremely slow.

The [Rancher Fleet](https://fleet.rancher.io/) project cracks the problem in the aspect of cluster management, while the issues relevant to application management are left unresolved. This command line application, built on top of Rancher Fleet, provides a holistic solution to application rollout on Kubernetes clusters.

## What Makes it Better than Rancher Fleet
* **The concept of a service.** A complex, large-scale application usually comprises several components represented by a set of GitHub repositories, and each component may depend on one or several other components in the set. Hence, we implement a service entity alongside an application one. With an application instance, We can define a service dependency map to specify the dependency relationships among the services in the application, ensuring that a rollout process never updates a service until all the services it depends on have rolled out successfully.

* **The concept of a rollout ring.** A gradual rollout exposes users to the changes over time, validating the changes in production with fewer users. Developers can deploy the changes ring by ring to limit the affect on users. Therefore, we implement the concept of rollout rings. Users can specify the ring it is on while adding a Kubernetes cluster. Then we store the information as one of the cluster's labels for grouping. During a rollout, only the clusters on the specified ring will be updated.

* **Changeable cluster labels.** With Rancher Fleet, a cluster's labels, defined during the installation of a fleet agent on the cluster, are not subject to change later, making it difficult to effectively manage clusters in the face of the need to modify cluster grouping, which can pop up frequently in real-life scenarios. Rather, with this command line application, the rollout ring a cluster is on, stored as one of the labels, can be changed anytime. This is easily extensible if there is a need to make other cluster labels changeable.

* **Visualized rollout experience.** With Rancher Fleet, to upgrade an application's image to another version involves specifying the new version in `fleet.yaml`, committing the change to GitHub, and waiting for corresponding Kubernetes clusters to discover and deploy the change. To check whether the change has been reflected on a cluster, a user has to keep checking the deployments on the cluster using `kubectl`. However, in this command line application, we abstract the application rollout process and turn it into two steps: set a rollout plan and create a rollout. While setting the plan, users specify the version they want for one or several services in an application. Then they roll out the application on a specific ring and repeat these procedures on another ring if necessary. During rollout, users are clearly notified when the change has been committed to a service's repository and when the change has been reflected on a cluster. Users can also fetch the details of each rollout from rollout history.

* **Simplified operations.** Installing and using Rancher Fleet is quite confusing in spite of the documentation available. Following the steps and troubleshooting are difficult without concrete knowledge in Helm and `kubectl`. Nevertheless, with this command line applicaion, the cumbersome operations are implemented by scripts, thus users do not need background knowledge in anything other than the application's APIs, which are simple and straightforward.

## Components
* **Application.** An application is a represenation of a real-world application. Any other component belongs to an application.

* **Cluster.** A cluster is a representation of a Kubernetes cluster. When adding a cluster, users define which application it belongs to and which rollout ring it is on.

* **Service.** A service is a representation of a GitHub repository owned by a complex, large-scale application. When creating a service, users define which application it belongs to and which services in the application it depends on.

* **Rollout.** A rollout is a represenation of a real-life rollout process. After creating a rollout, changes are made to an application's services deployed in the clusters on the specified ring.

## Quick Start
To use this command line application, clone this repository locally. Here are a few prerequisites before you can get started:

* **A Fleet Controller cluster (Fleet Manager).** Fleet Manager does the actual work to manage clusters. Follow [this](https://fleet.rancher.io/installation) guide to finish multi-cluster setup on Fleet Manager and [this](https://fleet.rancher.io/cluster-registration#create-cluster-registration-tokens) to create a cluster registration token. After these steps, there should be three new files: `ca.pem`, `token.yaml`, and `values.yaml`. In the cloned repository, create a directory named `config-files` and copy these files to the new directory. Name Fleet Manager's configuration file `manager.cfg` and add it to the directory, too.

* **Structured GitHub repositories.** All GitHub repositories of the applications to be deployed need to be structured [this](https://fleet.rancher.io/gitrepo-content) way. Example repositories: [fleet-examples](https://github.com/kliu513/fleet-examples/tree/master/multi-cluster) and [rancher-fleet-demo](https://github.com/kliu513/rancher-fleet-demo).

## APIs
### Application
**Note:** For an application, the dependency relationships among its services must be a directed acyclic graph (DAG).

* Create an empty application:
`$ python3 cli.py create-application [APPLICATION NAME]`
* Remove an application: 
`$ python3 cli.py remove-application [APPLICATION NAME]`
* Display an appplication's information: 
`$ python3 cli.py get-application-info [APPLICATION NAME]`
* Topologically sort and display an application's service dependency relationships: 
`$ python3 cli.py get-service-map [APPLICATION NAME]`
* Display all applications: 
`$ python3 cli.py display-applications`

### Cluster
**Note:** Before adding a cluster, make sure the cluster's configuration file has been added to the `config-files` directory.  

* Register a cluster in an application: 
`$ python3 cli.py add-cluster [CLUSTER NAME] [ROLLOUT RING] [CONFIGURATION FILENAME] [APPLICATION NAME]`
* Remove a cluster: 
`$ python3 cli.py remove-cluster [CLUSTER NAME]`
* Get a cluster's information: 
`$ python3 cli.py get-cluster-info [CLUSTER NAME]`
* List all clusters on the rollout ring a cluster is on: 
`$ python3 cli.py list-cluster-siblings [CLUSTER NAME]`
* Update the rollout ring a cluster is on: 
`$ python3 cli.py update-cluster-ring [CLUSTER NAME] [NEW ROLLOUT RING] [CONFIGURATION FILENAME]`
* Display all clusters: 
`$ python3 cli.py display-clusters`

### Service
**Note:** Input a service's dependencies in the format of `ServiceA/ServiceB/ServiceC`. Input `""` if no dependencies.

* Create a service in an application: 
`$ python3 cli.py create-service [APPLICATION NAME] [SERVICE NAME] [REPOSITORY LINK] [IMAGE VERSION] [DEPENDENCIES]` 
* Reset a service's dependencies: 
`$ python3 cli.py set-dependencies [APPLICATION NAME] [SERVICE NAME] [NEW DEPENDENCIES]`
* Set a rollout plan for a service: 
`$ python3 cli.py set-rollout-plan [APPLICATION NAME] [SERVICE NAME] [NEW IMAGE VERSION]`
* Get a service's information: 
`$ python3 cli.py get-service-info [APPLICATION NAME] [SERVICE NAME]`
* Remove a service: 
`$ python3 cli.py remove-service [APPLICATION NAME] [SERVICE NAME]`
* Display all services of an application: 
`$ python3 cli.py display-services [APPLICATION NAME]`
* Display all services: 
`$ python3 cli.py display-services all`

### Rollout
* Start an application's rollout on a rollout ring: 
`$ python3 cli.py create-rollout [APPLICATION NAME] [ROLLOUT RING]`
* Get an application's rollout history: 
`$ python3 get-rollout-history [APPLICATION NAME]`
* Get rollout history of all applications: 
`$ python3 get-rollout-history all`
