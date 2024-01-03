#!/bin/bash

sourceResourceGroup="<source_group>"
sourceAppName="<source_name>"

targetResourceGroup="<target_group>"
targetServerName="<target_name>"

outboundIPs=$(az webapp show --resource-group $sourceResourceGroup --name $sourceAppName --query outboundIpAddresses --output tsv)
additionalOutboundIPs=$(az webapp show --resource-group $sourceResourceGroup --name $sourceAppName --query possibleOutboundIpAddresses --output tsv)

combinedIPs=$(echo "$outboundIPs,$additionalOutboundIPs" | tr ',' '\n' | sort -u)

for ip in $combinedIPs; do
  az postgres flexible-server firewall-rule create --resource-group $targetResourceGroup --name $targetServerName --rule-name "Allow$(echo $ip | tr '.' '_')" --start-ip-address $ip --end-ip-address $ip
done
