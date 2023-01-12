import sqlite3
from entities import Cluster

connection = sqlite3.connect("main.db")
cursor = connection.cursor()

print("End")