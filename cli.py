import subprocess
import typer
from rich.console import Console
from rich.table import Table
from entities import Cluster, Service
from database import insert_cluster, get_cluster, list_cluster, delete_cluster, update_cluster, list_all_clusters, \
    insert_service, get_service, delete_service, update_service, list_all_services

app = typer.Typer()
console = Console()

# Cluster operations
@app.command(short_help="Register an existing cluster")
def add_cluster(name: str, ring: int, config_file: str):
    typer.echo(f"Adding Cluster {name} on Ring {ring}...")
    insert_cluster(Cluster(name, ring, config_file))

@app.command(short_help="Remove a registered cluster")
def remove_cluster(name: str):
    typer.echo(f"Removing Cluster {name}...")
    delete_cluster(name)

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
def update_cluster_ring(name: str, ring: int):
    cluster = update_cluster(name, ring)
    typer.echo(f"Cluster {cluster.name} is now on Ring {cluster.ring}")

@app.command(short_help="Display all the registered clusters")
def display_clusters():
    clusters = list_all_clusters()
    table = build_cluster_table()
    for cluster in clusters: 
        table.add_row(cluster.name, str(cluster.ring), cluster.config, cluster.timestamp)
    console.print(table)
    print(subprocess.call(["scripts/add-cluster.sh","../config-files/carrot.yaml", "ring0"]))

def build_cluster_table():
    table = Table(show_header=True, header_style="blue")
    table.add_column("Name")
    table.add_column("Ring")
    table.add_column("Config File")
    table.add_column("Last Update")
    return table

# Service operations
@app.command(short_help="Create a service from a GitHub repository")
def create_service(name: str, repo: str, dependencies: list):
    typer.echo(f"Creating Service {name} from {repo}...")
    insert_service(Service(name, repo, dependencies))

@app.command(short_help="Set a service's dependencies")
def set_dependencies(name: str, dependencies: list):
    service = update_service(name, dependencies)
    typer.echo(f"Service {service.name} now depends on {service.dependencies}")

@app.command(short_help="Remove a service")
def remove_service(name: str):
    typer.echo(f"Deleting Service {name}...")
    services = list_all_services()
    for service in services:
        deps = service.dependencies.split(" ")
        if name in deps:
            typer.echo(f"Deletion failed: the service requested to be deleted has child services")
            return
    delete_service(name)

@app.command(short_help="Display all the services")
def display_services():
    services = list_all_services()
    table = build_service_table()
    for service in services: 
        table.add_row(service.name, service.repo, " ".join(service.dependencies), service.timestamp)
    console.print(table)

def build_service_table():
    table = Table(show_header=True, header_style="blue")
    table.add_column("Name")
    table.add_column("Repo Link")
    table.add_column("Dependencies")
    table.add_column("Last Update")
    return table

if __name__ == "__main__":
    app()
