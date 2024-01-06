# Demo-Integration

## Description
Demo Integration project for practice. Online shop connected to backend inventory and user data, plus fake bank website with backend. To be written in python for backend and JS, HTML, and CSS for front end.

## Features
### Databases
> Using either Azure Data Studio or equivalent, excel doc, or csv
- Database of user info
- Database of inventory data
- Database for banking data
### Websites
- Online store
- Online bank
### APIs
#### SYSAPI-OnlineStore:  
- GET, POST, PUT, DELETE
- Endpoints: user and sale
#### SYSAPI-Bank:  
- GET, POST, PUT, DELETE
#### EXPAPI-OnlineStore:  
- Get inventory
- Purchase item (calls bankingAPI to check funds and process payment), adjusts inventory, adds purchase histroy)  
- Create user
- Adjust user data
- Show order/purchase history  
#### EXPAPI-OnlineBank:  
- Get all transactions
- Get one transaction
- Check sufficient funds
- Process Payment  
#### PROAPI-StoreManagemnt:
- Endpoints: user and sale
- EXPAPI-OnlineStore -> SYSAPI-UserDB and/or SYSAPI-InventoryDB
#### PROAPI-PaymentManagement:  
- EXPAPI-OnlineBank -> SYSAPI-BankDB

