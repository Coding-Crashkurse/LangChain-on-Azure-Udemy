#!/bin/bash

# Definieren der Variablen für den Service, von dem die IPs abgerufen werden
sourceResourceGroup="myrestaurantapp_group"
sourceAppName="myrestaurantapp"

# Definieren der Variablen für den Service, für den die IP-Beschränkungen gesetzt werden sollen
targetResourceGroup="udemygroup"
targetAppName="codingudemybackend"
priority=100

# Outbound-IP-Adressen abrufen
outboundIPs=$(az webapp show --resource-group $sourceResourceGroup --name $sourceAppName --query outboundIpAddresses --output tsv)

# Zusätzliche Outbound-IP-Adressen abrufen
additionalOutboundIPs=$(az webapp show --resource-group $sourceResourceGroup --name $sourceAppName --query possibleOutboundIpAddresses --output tsv)

# Kombinieren beider Listen, Duplikate entfernen
combinedIPs=$(echo "$outboundIPs,$additionalOutboundIPs" | tr ',' '\n' | sort -u)

# IP-Beschränkungen für jede IP-Adresse setzen
for ip in $combinedIPs; do
  az webapp config access-restriction add --resource-group $targetResourceGroup --name $targetAppName --rule-name "Allow_$ip" --action Allow --ip-address $ip/32 --priority $priority
done

# "Deny All" Regel hinzufügen mit Priorität 500
az webapp config access-restriction add --resource-group $targetResourceGroup --name $targetAppName --rule-name "DenyAll" --action Deny --ip-address "0.0.0.0/0" --priority 500
