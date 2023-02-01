import sqlite3
from entities import Cluster, Service

connection = sqlite3.connect("main.db")
cursor = connection.cursor()

# Cluster operations
def create_cluster_table():
    cursor.execute("""CREATE TABLE IF NOT EXISTS CLUSTERS (
        name text PRIMARY KEY,
        ring int,
        file text,
        timestamp text
    )""")

def insert_cluster(cluster: Cluster):
    with connection:
        cursor.execute("INSERT OR IGNORE INTO CLUSTERS VALUES (:name, :ring, :config, :timestamp)", 
        {"name": cluster.name, "ring": cluster.ring, "config": cluster.config, "timestamp": cluster.timestamp})

def get_cluster(cluster_name: str):
    with connection:
        cursor.execute("SELECT * FROM CLUSTERS WHERE name = ?", (cluster_name,))
    cluster_info = cursor.fetchone()
    return Cluster(*cluster_info)

def list_cluster(cluster_name: str):
    with connection:
        cursor.execute("SELECT ring FROM CLUSTERS WHERE name = ?", (cluster_name,))
    cluster_ring = cursor.fetchone()
    with connection:
        cursor.execute("SELECT * FROM CLUSTERS WHERE ring = ?", (*cluster_ring,))
    siblings = cursor.fetchall()
    result = []
    for sibling in siblings:
        result.append(Cluster(*sibling))
    return result

def delete_cluster(cluster_name: str):
    with connection:
        cursor.execute("SELECT * FROM CLUSTERS WHERE name = ?", (cluster_name,))
    deleted_cluster = cursor.fetchone()
    with connection:
        cursor.execute("DELETE FROM CLUSTERS WHERE name = ?", (cluster_name,))
    return Cluster(*deleted_cluster)

def update_cluster(cluster_name: str, cluster_ring: int):
    with connection:
        cursor.execute("UPDATE CLUSTERS SET ring = ? WHERE name = ?", (cluster_ring, cluster_name,))
    with connection:
        cursor.execute("SELECT * FROM CLUSTERS WHERE name = ?", (cluster_name,))
    updated_cluster = cursor.fetchone()
    return Cluster(*updated_cluster)

def list_all_clusters():
    with connection:
        cursor.execute("SELECT * FROM CLUSTERS")
    clusters = cursor.fetchall()
    result = []
    for cluster in clusters:
        result.append(Cluster(*cluster))
    return result

# Service operations
def create_service_table():
    cursor.execute("""CREATE TABLE IF NOT EXISTS SERVICES (
        name text PRIMARY KEY,
        repo text,
        dependencies text,
        timestamp text
    )""")

def insert_service(service: Service):
    with connection:
        cursor.execute("INSERT OR IGNORE INTO SERVICES VALUES (:name, :repo, :dependencies, :timestamp)", 
        {"name": service.name, "repo": service.repo, "dependencies": " ".join(service.dependencies), "timestamp": service.timestamp})

def update_service(service_name: str, service_deps: list):
    with connection:
        cursor.execute("UPDATE SERVICES SET dependencies = ? WHERE name = ?", (" ".join(service_deps), service_name,))
    with connection:
        cursor.execute("SELECT * FROM SERVICES WHERE name = ?", (service_name,))
    updated_service = cursor.fetchone()
    return Service(*updated_service)

def delete_service(service_name: str):
    with connection:
        cursor.execute("SELECT * FROM SERVICES WHERE name = ?", (service_name,))
    deleted_service = cursor.fetchone()
    with connection:
        cursor.execute("DELETE FROM SERVICES WHERE name = ?", (service_name,))
    return Service(*deleted_service)

def get_service(service_name: str):
    with connection:
        cursor.execute("SELECT * FROM SERVICES WHERE name = ?", (service_name,))
    service_info = cursor.fetchone()
    return Service(*service_info)

def list_all_services():
    with connection:
        cursor.execute("SELECT * FROM SERVICES")
    services = cursor.fetchall()
    result = []
    for service in services:
        result.append(Service(*service))
    return result

create_cluster_table()
create_service_table()
