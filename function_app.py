import azure.functions as func
import logging

app = func.FunctionApp()

@app.blob_trigger(arg_name="myblob", path="mycontainer", #Name des containers
                               connection="DefaultEndpointsProtocol=https;AccountName=langchainba95;AccountKey=ACvqz93vS5mCFH2J2Xj1s4P+8Opo/Udjlj0k8Qn/27fPfLugoDSo1ju4wEk5r4jDD5sLvhyLa2e4+AStn6my6A==;EndpointSuffix=core.windows.net")
def blob_trigger(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}"
                f"Blob Size: {myblob.length} bytes")
