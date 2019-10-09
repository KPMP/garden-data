# REDCap API Test using Flask

## Running
1. If you're on a PC, you'll need to set the ENV_PYTHON_APPDIR in the .env to an absolute file path. Otherwise you can leave it alone. 
2. Apply for a token here: https://redcap.kpmp.org/redcap_v9.1.1/API/project_api.php?pid=14
3. Set the ENV_API_TOKEN in .env to your token once you are approved.
2. 'docker-compose up -d'
3. Browse to http://localhost:5000/

## API Notes

* If you don't plan on using the field value IDs, it's important to set the following values in the records export request to ensure you get the actual label/value of the field instead of the ID (multiple choice) or 0/1 (checkbox):
 ** `'rawOrLabel': 'label'`
 ** `'exportCheckboxLabel': 'true'`
* Setting the "type" value to "eav" instead of "flat" produces one row per field/value and also handles checkboxes differently: "checkboxes are exported with their true variable name (whereas the 'flat' type exports them as variable___code format)."

## API Help

* API documentation: https://redcap.kpmp.org/api/help/
* API playground: https://redcap.kpmp.org/redcap_v9.1.1/API/playground.php?pid=14
  * Hint: create your queries here, select the Python tab, and copy/paste the data object into the Python code.
  
  

