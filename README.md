# worldline

This repository contains the code for Task 1: *Make Transaction API Endpoint*: Implement an endpoint to accept transaction requests from Merchants. The endpoint should validate the incoming payload, generate a unique transaction ID, and store the transaction details in a MySQL database.

## usage
The server side does not work. Supposedly, it would run on localhost, port 8000.
```
py -m http.server
```
When `accept.py` is run, it would create a database `test` and table `transacts` if they do not exist; then, add the sample payload into the database.

## contributing

Pull requests are welcome. 