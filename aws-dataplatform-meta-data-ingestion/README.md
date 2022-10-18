# Introduction to Metadata Ingestion

## Integration Options

DataHub supports both **push-based** and **pull-based** metadata integration. 

Push-based integrations allow you to emit metadata directly from your data systems when metadata changes, while pull-based integrations allow you to "crawl" or "ingest" metadata from the data systems by connecting to them and extracting metadata in a batch or incremental-batch manner. Supporting both mechanisms means that you can integrate with all your systems in the most flexible way possible. 

Few recipes are included in the [examples/recipes](./examples/recipes) directory. 

Ingesting Metadata through recipe, which will push the Metadata to a Rest Endpoint of Datahub.

Get the GMS_ENDPOINT by executing 
```
kubectl get svc
```

Get the loadbalance url for service - datahub-datahub-gms 

you url will look like this - 
http://{load balance url for gms service}:8080

Genrate a token from datahub UI:
Go to Settings on right top corner and genrate GMS_TOKEN and make a note of it
               


## Prerequisites

inside a virtualenv install 

```
python3 -m pip install 'acryl-datahub[datahub-rest]'
```


```
python3 -m pip install 'acryl-datahub'

```

For Glue
```
python3 -m pip install 'acryl-datahub[glue]'
```


installing a particular version

```
python3 -m pip install 'acryl-datahub==0.8.38'
```


## Running this recipe is as simple as:

cd examples/recipes
chnage the value for 

```shell
datahub ingest -c redshift_to_datahub_new.yml
```



or if you want to override the default endpoints, you can provide the environment variables as part of the command like below:
```shell
DATAHUB_GMS_HOST="https://my-datahub-server:8080" DATAHUB_GMS_TOKEN="my-datahub-token" datahub ingest -c recipe.yaml
```


### Programmatic Pipeline
In some cases, you might want to configure and run a pipeline entirely from within your custom Python script. Here is an example of how to do it.
 - [glue_ingestion.py](./examples/code/glue_ingestion.py) - a basic glue to REST programmatic pipeline.


