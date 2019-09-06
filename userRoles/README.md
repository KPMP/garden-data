What we need to do:

1) For each application that will use the user portal, we will need to create a client on the user portal
- go to http://userporta.kpmp.org/admin/clientsview
- click Create
- Fill in the name of the client, owner and email
- copy the token

2) The X-API-TOKEN header needs to be populated with the token from above for any request to the api

3) If you make a request for a user that does not exist, it will throw an exception, so we will need to handle that gracefully

4) We will have to define a group for each application (or one that can be used for all?) and make sure users are assigned to those groups

5) Querying the user portal will return a JSON object like this:
{"_id":"5cc9e10a2cda37d4db7d9b2d","active":true,"email":"jcarson@uw.edu","first_name":"Jonas","groups":["uw_rit_kpmp_role_developer","uw_rit_kpmp_app_userportal"],"last_name":"Carson","organization_id":"5cc9e10a2cda37d4db7d9b19","phone_numbers":null,"shib_id":"jcarson@washington.edu"}

6) We will use values from the 'groups' section to determine if a user has permission.  We should also interrogate the 'active' property to ensure it is set to true.
