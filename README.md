# Alma Global Project

File with descriptions code and access to pyRofex data

## Credentials

Each user needs to have a .env file at the root of his repository with the following information:

```bash
rofex_user=juanperez1234

rofex_password=szhtrF0@

rofex_account=REM1234
```
 

For more information about remarket account information: https://remarkets.primary.ventures/


### Running the arbitrage bot

if you have already set up the remarket environment credentials in the .env file, you can run the following command:
```
python src/main.py <inst_1> ... <inst_n>
```

for example:

```
python src/main.py GGAL/OCT23 DLR/OCT23 YPFD/OCT23 PAMP/OCT23 GGAL/DIC23 DLR/DIC23 YPFD/DIC23 PAMP/DIC23
```


