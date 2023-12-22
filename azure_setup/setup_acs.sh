docker build -t udemylangchainregistry.azurecr.io/backend:latest ./backend
docker build -t udemylangchainregistry.azurecr.io/frontend:latest ./frontend
docker build -t udemylangchainregistry.azurecr.io/uploadservice:latest ./uploadservice

az acr login --name udemylangchainregistry

docker push udemylangchainregistry.azurecr.io/backend:latest
docker push udemylangchainregistry.azurecr.io/frontend:latest
docker push udemylangchainregistry.azurecr.io/uploadservice:latest

az acr repository list --name udemylangchainregistry --output table
