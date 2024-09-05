https://learn.microsoft.com/en-us/azure/web-application-firewall/ag/application-gateway-crs-rulegroups-rules?tabs=drs21

Start and Stop Application Gateway:
Use Azure Powershell Docker
https://learn.microsoft.com/en-us/powershell/module/az.network/stop-azapplicationgateway?view=azps-11.4.0

```
docker run -it mcr.microsoft.com/azure-powershell pwsh

# Connect to Azure Account
Connect-AzAccount -UseDeviceAuthentication -Subscription "<Subscription ID>"

# Start ApplicationGateway (Takes some long time for the command to finish)
$AppGw = Get-AzApplicationGateway -Name ag -ResourceGroupName rg1
Start-AzApplicationGateway -ApplicationGateway $AppGw

# Stop ApplicationGateway
$AppGw = Get-AzApplicationGateway -Name ag -ResourceGroupName rg1
Stop-AzApplicationGateway -ApplicationGateway $AppGw
```

