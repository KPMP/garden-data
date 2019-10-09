# REDCap API Test using Flask

## Running
1. If you're on a PC, you'll need to set the ENV_PYTHON_APPDIR in the .env to an absolute file path. Otherwise you can leave it alone. 
2. Apply for a token here: https://redcap.kpmp.org/redcap_v9.1.1/API/project_api.php?pid=14
3. Set the ENV_API_TOKEN in .env to your token once you are approved.
2. 'docker-compose up -d'
3. Browse to http://localhost:5000/

## API Help

* API documentation: https://redcap.kpmp.org/api/help/
* API playground: https://redcap.kpmp.org/redcap_v9.1.1/API/playground.php?pid=14
  * Hint: create your queries here, select the Python tab, and copy/paste the data object into the Python code. 
