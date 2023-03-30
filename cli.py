import subprocess
import time
import typer
from rich.console import Console
from rich.table import Table
from entities import Cluster, Service, Application, Rollout
from database import insert_cluster, get_cluster, list_cluster, delete_cluster, update_cluster, list_all_clusters, \
    insert_service, get_service, delete_service, update_service_deps, list_all_services, \
    insert_application, delete_application, update_rollout_plan, get_application, list_all_applications, \
    insert_rollout, finish_rollout, get_rollout, list_all_rollouts, update_rollout_status
app = typer.Typer()
console = Console()

# Cluster operations
@app.command(short_help="Register an existing cluster")
def add_cluster(name: str, ring: int, config_file: str):
    typer.echo(f"Adding Cluster {name} on Ring {ring}...")
    insert_cluster(Cluster(name, ring, config_file))
    """
    if subprocess.call(["scripts/add-cluster.sh", "ring"+str(ring), "config-files/"+config_file]):
        delete_cluster(name)
        typer.echo(f"Adding Clutser {name} failed")
    """

@app.command(short_help="Remove a registered cluster")
def remove_cluster(name: str):
    typer.echo(f"Removing Cluster {name}...")
    cluster = delete_cluster(name)
    if subprocess.call(["scripts/remove-cluster.sh", "config-files/"+cluster.config]):
        insert_cluster(cluster)
        typer.echo(f"Removing Clutser {name} failed")

@app.command(short_help="Get a cluster's info")
def get_cluster_info(name: str):
    cluster = get_cluster(name)
    table = build_cluster_table()
    table.add_row(cluster.name, str(cluster.ring), cluster.config, cluster.timestamp)
    console.print(table)

@app.command(short_help="List the clusters on the same ring")
def list_cluster_siblings(name: str):
    clusters = list_cluster(name)
    table = build_cluster_table()
    for cluster in clusters:
        table.add_row(cluster.name, str(cluster.ring), cluster.config, cluster.timestamp)
    console.print(table)

@app.command(short_help="Update the ring a cluster is on")
def update_cluster_ring(name: str, ring: int, config_file: str):
    old_cluster = get_cluster(name)
    if old_cluster.ring == ring:
        typer.echo(f"Cluster {name} is already on Ring {ring}")
        return
    subprocess.call(["scripts/update-cluster-ring.sh", "config-files/"+config_file, \
        "ring"+str(old_cluster.ring), "ring"+str(ring)])
    new_cluster = update_cluster(name, ring)
    typer.echo(f"Cluster {new_cluster.name} is now on Ring {new_cluster.ring}")

@app.command(short_help="Display all the registered clusters")
def display_clusters():
    clusters = list_all_clusters()
    table = build_cluster_table()
    for cluster in clusters: 
        table.add_row(cluster.name, str(cluster.ring), cluster.config, cluster.timestamp)
    console.print(table)

def build_cluster_table():
    table = Table(show_header=True, header_style="blue")
    table.add_column("Name")
    table.add_column("Ring")
    table.add_column("Config File")
    table.add_column("Creation Timestamp")
    return table

# Service operations
# Format for dependencies: A/B/C
@app.command(short_help="Create a service from a GitHub repository")
def create_service(application: str, service: str, repo: str, version: str, dependencies: str):
    typer.echo(f"Creating Service {service} in Application {application} from {repo}...")
    insert_service(Service(application, service, repo, version, dependencies))
    """
    if subprocess.call(["scripts/create-service.sh", repo, repo.split('/')[-1]]):
        remove_service(application, service)
        typer.echo(f"Creating Service {service} in Application {application} failed")
    """

@app.command(short_help="Set a service's dependencies")
def set_dependencies(application: str, service: str, dependencies: str):
    updated_service = update_service_deps(application, service, dependencies)
    typer.echo(f"Service {updated_service.service} now depends on {updated_service.dependencies}")

@app.command(short_help="Get a service's info")
def get_service_info(app_name: str, service_name: str):
    service = get_service(app_name, service_name)
    table = build_service_table()
    table.add_row(service.application, service.service, service.repo, service.version, \
                  service.dependencies, service.rollout_plan, service.timestamp)
    console.print(table)

@app.command(short_help="Remove a service")
def remove_service(application: str, service: str):
    typer.echo(f"Deleting Service {service}...")
    services = list_all_services()
    for serv in services:
        if serv.application == application:
            if service in serv.dependencies.split('/'):
                typer.echo(f"Deletion failed: the service requested to be deleted has dependents")
                return
    delete_service(application, service)
    subprocess.call(["scripts/remove-service.sh", service])

@app.command(short_help="Display all the services of an application \
             (Input 'all' if all the services in the database are wanted)")
def display_services(application):
    services = list_all_services()
    table = build_service_table()
    for service in services:
        if application == "all" or service.application == application:
            table.add_row(service.application, service.service, service.repo, \
                          service.version, service.dependencies, service.rollout_plan, service.timestamp)
    console.print(table)

def build_service_table():
    table = Table(show_header=True, header_style="blue")
    table.add_column("Application")
    table.add_column("Service")
    table.add_column("Repository Link")
    table.add_column("Version")
    table.add_column("Service Dependencies")
    table.add_column("Rollout Plan")
    table.add_column("Creation Timestamp")
    return table

# Application operations
@app.command(short_help="Create an empty application")
def create_application(name: str):
    typer.echo(f"Creating Application {name}...")
    insert_application(Application(name))

@app.command(short_help="Remove an application")
def remove_application(name: str):
    typer.echo(f"Removing Application {name}...")
    delete_application(name)

@app.command(short_help="Add a rollout plan for a service of the application")
def set_rollout_plan(application: str, service: str, rollout_plan: str):
    typer.echo(f"Setting a rollout plan for Service {service}...")
    updated_service = update_rollout_plan(application, service, rollout_plan)
    typer.echo(f"Service {updated_service.service} will be rolled out to Version {updated_service.rollout_plan}")

@app.command(short_help="Display an application's information")
def get_application_info(name: str):
    application = get_application(name)
    typer.echo(f"Application Name: {application.name}   Creation Timestamp: {application.timestamp}   Services:")
    table = build_service_table()
    for service in application.services:
        table.add_row(service.application, service.service, service.repo, service.version, service.dependencies, \
            service.rollout_plan, service.timestamp)
    console.print(table)

@app.command(short_help="Topologically sort an application's service dependency map")
def get_service_map(application: str):
    def top_sort(service: Service, visited: dict, results: list, top_num: int):
        visited[service.service] = True
        if len(service.dependencies) > 0:
            deps = service.dependencies.split('/')
            for dep in deps:
                if not visited[dep]:
                    top_num = top_sort(get_service(application, dep), visited, results, top_num)
        results[top_num] = service.service
        return top_num + 1
    
    services = get_application(application).services
    n_services = len(services)
    results = [None] * n_services
    if n_services > 0:
        visited = {}
        for service in services:
            visited[service.service] = False
        top_num = 0
        for i in range(n_services):
            if not visited[services[i].service]:
                top_num = top_sort(services[i], visited, results, top_num)
    service_map = " -> ".join(results)
    typer.echo(f"{service_map}")
    return results

@app.command(short_help="Display all the applications")
def display_applications():
    apps = list_all_applications()
    table = build_application_table()
    for app in apps:
        table.add_row(app.name, app.timestamp)
    console.print(table)

def build_application_table():
    table = Table(show_header=True, header_style="blue")
    table.add_column("Application Name")
    table.add_column("Creation Timestamp")
    return table

# Rollout operations
@app.command(short_help="Start the rollout for an application on the specified ring")
def create_rollout(application: str, ring: int):
    typer.echo(f"Starting rollout for Application {application} on Ring {str(ring)}...")
    if insert_rollout(Rollout(application)):
        service_map = get_service_map(application)
        for serv in service_map:
            service = get_service(application, serv)
            if service.rollout_plan is not None:
                typer.echo(f"Start rolling out Service {service.service} on Ring {str(ring)}...")
                time.sleep(5)
                subprocess.call(["scripts/create-rollout.sh", service.repo.split('/')[-1], \
                                service.version, service.rollout_plan, "ring"+str(ring)])
                clusters = list_all_clusters()
                for i in range(len(clusters)):
                    if clusters[i].ring == ring:
                        clusters.pop(i)
                while len(clusters) > 0:
                    for i in range(len(clusters)):
                        if subprocess.call(["scripts/check-version.sh", "config-files/"+clusters[i].config, \
                                        service.repo.split('/')[-1], service.rollout_plan]):
                            typer.echo(f"Finished Rolling out Service {service.service} on \
                                       Cluster {clusters[i].name}")
                            time.sleep(5)
                            clusters.pop(i)
        rollout = get_rollout(application)
        table = build_rollout_table()
        table.add_row(rollout.guid, rollout.application, str(rollout.status), rollout.timestamp, \
                      rollout.rollout_plans)
        console.print(table)
        finish_rollout(application, ring)
        get_application_info(application)

@app.command(short_help="Get (an application's) rollout history\
             (Input 'all' if all the services in the database are wanted)")
def get_rollout_history(application):
    rollouts = list_all_rollouts()
    table = build_rollout_table()
    for rollout in rollouts:
        if application == "all" or rollout.application == application:
            table.add_row(rollout.guid, rollout.application, str(rollout.status), rollout.timestamp, \
                          rollout.rollout_plans)
    console.print(table)

@app.command(short_help="Cancel an application's running rollout")
def cancel_rollout(application: str):
    typer.echo(f"Cancelling Application {application}'s running rollout...")
    update_rollout_status(application)

def build_rollout_table():
    table = Table(show_header=True, header_style="blue")
    table.add_column("guid")
    table.add_column("Application")
    table.add_column("Status")
    table.add_column("Creation Time")
    table.add_column("Rollout Plans")
    return table

if __name__ == "__main__":
    app()
