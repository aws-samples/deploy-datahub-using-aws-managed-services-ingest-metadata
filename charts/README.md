# Updating to the recent version of helm chart 

Note: If you want to use newer [helm chart](https://github.com/acryldata/datahub-helm/blob/master/charts/datahub/values.yaml,), replace the following chart values from your existing values.yaml

•	elasticsearchSetupJob

•	global : graph_service_impl

•	global : elasticsearch

•	global :kafka

•	global :sql

then execute
```
helm install prerequisites datahub/datahub-prerequisites --values ./charts/prerequisites/values.yaml

helm install datahub datahub/datahub --values ./charts/datahub/values.yaml

```


