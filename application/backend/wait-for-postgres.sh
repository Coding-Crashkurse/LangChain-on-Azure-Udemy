#!/bin/sh
# wait-for-postgres.sh

set -e

# Fetch the host and port from the environment variables
host="$PG_VECTOR_HOST"
port="$PGPORT"
user="$PG_VECTOR_USER"
dbname="$PGDATABASE"
password="$PG_VECTOR_PASSWORD"

# Wait for PostgreSQL to become available
until PGPASSWORD=$password psql -h "$host" -U "$user" -d "$dbname" -p "$port" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

# Now we can execute the CMD passed to the Docker container
exec "$@"
