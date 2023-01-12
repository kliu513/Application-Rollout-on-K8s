import typer

app = typer.Typer()

# Cluster operations
@app.command(short_help="Register an existing cluster")
def add_cluster(name: str, ring: int, config_file: str):
    typer.echo(f"Adding Cluster {name} on Ring {ring}...")

@app.command(short_help="Delete a registered cluster")
def delete_cluster(name: str):
    typer.echo(f"Deleting Cluster {name}...")

@app.command(short_help="Get a cluster's info")
def get_cluster(name: str):
    cluster = [("bear", 1, "bear.yaml")]
    typer.echo(f"Name: {name}\nRing: {cluster[0][1]}\nConfig filename: {cluster[0][2]}")

@app.command(short_help="List the clusters on the same ring")
def list_cluster(name: str):
    clusters = [("bear", 1, "bear.yaml"), ("bunny", 1, "bunny.yaml")]
    typer.echo(f"Cluster {name} is on Ring {clusters[0][1]}. Its siblings are:")
    for cluster in clusters:
        typer.echo(f"Name: {cluster[0]}     Config filename: {cluster[2]}")

@app.command(short_help="Update the ring a cluster is on")
def update_cluster(name: str, ring: int):
    cluster = [("bear", 1, "bear.yaml")]
    typer.echo(f"Cluster {name} is now on Ring {cluster[0][1]}")

if __name__ == "__main__":
    app()