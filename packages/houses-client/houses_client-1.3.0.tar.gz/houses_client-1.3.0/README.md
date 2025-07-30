# HOUSES Client
A Python Client SDK for the [Mayo Clinic HOUSES API](https://www.mayo.edu/research/centers-programs/mayo-clinic-houses-program/overview)

# Requirements
Python 3.11+

# Installation
```shell script
pip install houses-client
```


| Houses Client Property | Main function option | Description                                                  |
|------------------------|----------------------|--------------------------------------------------------------|
| api_endpoint           | -e, --endpoint       | HOUSES api endpoint                                          |
| client_id              | -u, --clientid       | OIDC Client ID - required unless using self_hosted mode      |
| client_secret          | -s,  --clientsecret  | OIDC Client Secret - required, unless using self_hosted mode |
| self_hosted            | -h,  --selfhosted    | Self Hosted Mode - No Auth                                   |
| log_level              | N/A                  | Client log level                                             |
|                        | -i, --ifile          | input file path                                              | 
|                        | -o, --ofile          | output file  path                                            |                                              
|                        | -y, --year           | request year [global]                                        |
|                        | -d, --delimiter      | input file record delimiter, default = ,                     |

# Example Usage
```python
from houses_client import client

#Create a client passing in your API client id and client secret
client = client.HousesClient(api_endpoint="https://houses.konfidential.io", 
  client_id="my oidc client id", 
  client_secret="my oidc client secret",
  self_hosted=False,                             
  log_level="INFO")

# Submit batch request reading from myinput.csv and writing results to myoutput.csv
# year is applied to records if the csv format doesn not include year
client.batch(input_path="myinput.csv", output_path="myoutput.csv", year=2021, delimiter=',')
```

## Example Usage - CLI

Example processing with custom endpoint, input file=sample1.csv, output_file=sample1_output.csv, year=2021, delimiter=, and self hosted mode (no auth):
```shell
 python -m houses_client.client \
  -e https://localhost:9000 \
  -i sample1.csv \
  -o sample1_output.csv \
  -y 2021 \
  -d , \
  --selfhosted

```

# Input Data Schema
## Single Address Format
- id: user defined unique id
- address: single address string; e.g. 123 main st anycity NY 12345. The address should contain one of the following combinations:
    - city and state
    - city 
    - state 
    - zipcode
- year: the requested year. This is an optional field and if provided overrides the request level year
- referenceAddress: the requested reference address. This is an optional field and if provided overrides the request level reference address

Example:
```
id,address,year
1,"123 main st anytown ny 5555",2019
2,"456 main st anytown ny 55555",2018
```

Example With referenceAddress:
```
id,address,year,referenceAddress
1,"123 main st anytown ny 5555",2019,"789 main st anytown y 55555"
2,"456 main st anytown ny 55555",2018,"678 main st anytown y 55555"
```

### Full Component Address Format
- id: user defined unique id
- address: Street Address
- secondary: Optional Secondary Street Address; e.g. Apartment or Suite number
- city
- state
- zip
- year: the requested year. This is an optional field and if provided overrides the request level year
- referenceAddress: the requested reference address. This is an optional field and if provided overrides the request level reference address

# Build
```shell script
python3 -m pip install --upgrade build
```
```shell script
python3 -m build
```
