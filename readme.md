1. Scraper fetches data from the parking website.
2. Scraper hashes md5 the data and updates the postgresql table.
3. Another agent screens postgresql for changed key-value, driver email-hash pairs.
4. If the key-value pair has been updated, agent will send an email with the updates to the driver trough google mail service.
5. Run these agents daily after 21:00h. This is when the parking people don't charge for parking anymore.

TODO:
1. Until postgre is set up, local .csv will do.
2. Use lambda to facilitate these agents. Use dynamodb to save hash results. Maybe even see if AWS has some free SMTP options.
