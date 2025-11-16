$account_id="256e5542-d5fd-46f1-b3cc-ab29ec375613"
$api_key=6GYUXtMtDmcySWEkzmBWozq7MWGCq20OvMv9E9LEyA7oF1TyMQaIJQQJ99BKACYeBjFXJ3w3AAAEACOGlFKC
$location=eastus

# Call the AccessToken method with the API key in the header to get an access token
$token = Invoke-RestMethod -Method "Get" -Uri "https://api.videoindexer.ai/auth/$location/Accounts/$account_id/AccessToken" -Headers @{'Ocp-Apim-Subscription-Key' = $api_key}

# Use the access token to make an authenticated call to the Videos method to get a list of videos in the account
Invoke-RestMethod -Method "Get" -Uri "https://api.videoindexer.ai/$location/Accounts/$account_id/Videos?accessToken=$token" | ConvertTo-Json
