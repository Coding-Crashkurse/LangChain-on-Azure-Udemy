#!/bin/bash

sourceResourceGroup="<source_group>"
sourceAppName="<source_name>"

targetResourceGroup="<target_group>"
targetAppName="<target_name>"
priority=100

outboundIPs=$(az webapp show --resource-group $sourceResourceGroup --name $sourceAppName --query outboundIpAddresses --output tsv)

additionalOutboundIPs=$(az webapp show --resource-group $sourceResourceGroup --name $sourceAppName --query possibleOutboundIpAddresses --output tsv)

combinedIPs=$(echo "$outboundIPs,$additionalOutboundIPs" | tr ',' '\n' | sort -u)

for ip in $combinedIPs; do
  az webapp config access-restriction add --resource-group $targetResourceGroup --name $targetAppName --rule-name "Allow_$ip" --action Allow --ip-address $ip/32 --priority $priority
done

az webapp config access-restriction add --resource-group $targetResourceGroup --name $targetAppName --rule-name "DenyAll" --action Deny --ip-address "0.0.0.0/0" --priority 500
