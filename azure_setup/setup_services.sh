# Create App Service Plan
az appservice plan create --name myAppServicePlan --resource-group langchain --sku B1 --is-linux

# Create Web App for Backend Service
az webapp create --resource-group langchain --plan myAppServicePlan --name myBackendApp --deployment-container-image-name codinglangchainregistry.azurecr.io/backend:latest

# Create Web App for Frontend Service
az webapp create --resource-group langchain --plan myAppServicePlan --name myFrontendAppa --deployment-container-image-name codinglangchainregistry.azurecr.io/frontend:latest

# Create Web App for Upload Service
az webapp create --resource-group langchain --plan myAppServicePlan --name myUploadServiceApp --deployment-container-image-name codinglangchainregistry.azurecr.io/uploadservice:latest

# Set ACR Credentials for Backend Web App
az webapp config container set --name myBackendApp --resource-group langchain --docker-custom-image-name codinglangchainregistry.azurecr.io/backend:latest --docker-registry-server-url https://codinglangchainregistry.azurecr.io --docker-registry-server-user codinglangchainregistry --docker-registry-server-password /5CK4UYf2w5+nMwSUJ3916EhKc96pAMsbBW5YW0QF4+ACRB21KSk

# Set ACR Credentials for Frontend Web App
az webapp config container set --name myFrontendAppa --resource-group langchain --docker-custom-image-name codinglangchainregistry.azurecr.io/frontend:latest --docker-registry-server-url https://codinglangchainregistry.azurecr.io --docker-registry-server-user codinglangchainregistry --docker-registry-server-password /5CK4UYf2w5+nMwSUJ3916EhKc96pAMsbBW5YW0QF4+ACRB21KSk

# Set ACR Credentials for Upload Service Web App
az webapp config container set --name myUploadServiceApp --resource-group langchain --docker-custom-image-name codinglangchainregistry.azurecr.io/uploadservice:latest --docker-registry-server-url https://codinglangchainregistry.azurecr.io --docker-registry-server-user codinglangchainregistry --docker-registry-server-password /5CK4UYf2w5+nMwSUJ3916EhKc96pAMsbBW5YW0QF4+ACRB21KSk
