What we need to do:

1) For each application that will use the user portal, we will need to create a client on the user portal
- go to http://userporta.kpmp.org/admin/clientsview
- click Create
- Fill in the name of the client, owner and email
- copy the token

2) The X-API-TOKEN header needs to be populated with the token from above for any request to the api

3) If you make a request for a user that does not exist, it will throw an exception, so we will need to handle that gracefully
