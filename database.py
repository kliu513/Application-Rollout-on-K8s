import sqlite3
from entities import Cluster, Service, Application

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
        application text
        service text,
        repo text,
        version text
        dependencies text,
        rollout_plan text
        timestamp text
    )""")

def insert_service(service: Service):
    with connection:
        cursor.execute("INSERT OR IGNORE INTO SERVICES VALUES (:application, :service, :version, \
            :dependencies, :rollout_plan, :timestamp)", 
        {"application": service.application, "serice": service.service, "repo": service.repo, \
            "version": service.version, "dependencies": service.dependencies, \
            "rollout_plan": service.rollout_plan, "timestamp": service.timestamp})

def update_service(app_name: str, service_name: str, service_deps: str):
    with connection:
        cursor.execute("UPDATE SERVICES SET dependencies = ? WHERE application = ? AND service = ?", \
            (service_deps, app_name, service_name,))
    with connection:
        cursor.execute("SELECT * FROM SERVICES WHERE application = ? AND service = ?", (app_name, service_name,))
    updated_service = cursor.fetchone()
    return Service(*updated_service)

def delete_service(app_name: str, service_name: str):
    with connection:
        cursor.execute("SELECT * FROM SERVICES WHERE application = ? AND service = ?", (app_name, service_name,))
    deleted_service = cursor.fetchone()
    with connection:
        cursor.execute("DELETE FROM SERVICES WHERE application = ? AND service = ?", (app_name, service_name,))
    return Service(*deleted_service)

def get_service(app_name: str, service_name: str):
    with connection:
        cursor.execute("SELECT * FROM SERVICES WHERE application = ? AND service = ?", (app_name, service_name,))
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

# Application operations
def create_application_table():
    cursor.execute("""CREATE TABLE IF NOT EXISTS APPLICATIONS (
        name text PRIMARY KEY,
        timestamp text
    )""")

def insert_application(app: Application):
    with connection:
        cursor.execute("INSERT OR IGNORE INTO APPLICATIONS VALUES (:name, :timestamp)", 
        {"name": app.name, "timestamp": app.timestamp})

def delete_application(name: str):
    with connection:
        cursor.execute("SELECT * FROM APPLICATIONS WHERE name = ?", (name,))
    deleted_application = cursor.fetchone()
    with connection:
        cursor.execute("DELETE FROM APPLICATIONS WHERE name = ?", (name,))
        cursor.execute("DELETE FROM SERVICES WHERE application = ?", (name,))
        cursor.execute("DELETE FROM ROLLOUTPLANS WHERE application = ?" (name,))
    return Application(*deleted_application)

def update_rollout_plan(app_name: str, service_name: str, new_version: str):
    with connection:
        cursor.execute("UPDATE SERVICES SET rollout_plan = ? WHERE application = ? AND service = ?", \
            (new_version, app_name, service_name,))
    with connection:
        cursor.execute("SELECT * FROM SERVICES WHERE application = ? AND service = ?", (app_name, service_name,))
    updated_service = cursor.fetchone()
    return Service(*updated_service)

def get_application(name: str):
    with connection:
        cursor.execute("SELECT * FROM SERVICES WHERE application = ?", (name,))
    results = cursor.fetchall()
    services = []
    for res in results:
        services.append(Service(*res))
    with connection:
        cursor.execute("SELECT * FROM APPLICATIONS WHERE application = ?", (name,))
    result = cursor.fetchone()
    application = Application(*result)
    application.services = services
    return application

create_cluster_table()
create_service_table()
create_application_table()
