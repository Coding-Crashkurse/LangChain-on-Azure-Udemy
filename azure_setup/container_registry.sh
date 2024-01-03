docker build -t udemyserviceregistry.azurecr.io/backend:latest ./backend
docker build -t udemyserviceregistry.azurecr.io/frontend:latest ./frontend
docker build -t udemyserviceregistry.azurecr.io/uploadservice:latest ./uploadservice

az acr login --name udemyserviceregistry

docker push udemyserviceregistry.azurecr.io/backend:latest
docker push udemyserviceregistry.azurecr.io/frontend:latest
docker push udemyserviceregistry.azurecr.io/uploadservice:latest

az acr repository list --name udemyserviceregistry --output table
