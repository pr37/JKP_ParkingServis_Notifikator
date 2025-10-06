1. Scraper fetches data from the parking website.
2. Scraper hashes md5 the data and updates the postgresql table.
3. Another agent screens postgresql for changed key-value, driver email-hash pairs.
4. If the key-value pair has been updated, agent will send an email with the updates to the driver trough google mail service.
