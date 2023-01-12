import typer

app = typer.Typer()

# Cluster operations
@app.command(short_help="Register an existing cluster")
def add_cluster(name: str, ring: int, config_file: str):
    typer.echo(f"Adding Cluster {name} on Ring {ring}")

if __name__ == "__main__":
    app() 