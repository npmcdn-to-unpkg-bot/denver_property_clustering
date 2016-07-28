import os
import sys
import psycopg2
import run_denver_clustering


x = run_denver_clustering.run_yearly_clusters(sys.argv[1])
