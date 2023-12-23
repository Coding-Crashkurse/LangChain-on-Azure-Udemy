docker build -t <registryname>.azurecr.io/backend:latest ./backend
docker build -t <registryname>.azurecr.io/frontend:latest ./frontend
docker build -t <registryname>.azurecr.io/uploadservice:latest ./uploadservice

az acr login --name <registryname>

docker push <registryname>.azurecr.io/backend:latest
docker push <registryname>.azurecr.io/frontend:latest
docker push <registryname>.azurecr.io/uploadservice:latest

az acr repository list --name <registryname> --output table
