
___
[![Maintainability](https://api.codeclimate.com/v1/badges/8ef4277f4b10d1603ffe/maintainability)](https://codeclimate.com/github/DmGorokhov/Exchangerates-Converter/maintainability)
[![Github Actions Status](https://github.com//DmGorokhov/Exchangerates-Converter/workflows/Python%20CI/badge.svg)](https://github.com/DmGorokhov/Exchangerates-Converter/actions/pyci.yml)
### Main project stack:
*FastAPI (v.0.103.2), SQLAlchemy2.0, Pydantic2.0, Alembic, Postresql, Asyncpg, Redis, httpx*

___
### 1. Description
The project is a small API microservice for currency conversion. The service provides an opportunity to get actual currency rates and perform conversion between them.
___
### 2. Requirements
___
* Docker compose V2
* Poetry >1.2.2
* Make (is used to run shortcut console-command)

**Poetry** is setup by the commands:

**Linux, macOS, Windows (WSL):**

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Details on installing and using the **Poetry** package are available in [official documentation](https://python-poetry.org/docs/).

To install **Poetry** you need **Python 3.7+** use the information from the official website [python.org](https://www.python.org/downloads/)

To install **Docker**, use the information from the official website [docs.docker.com](https://docs.docker.com/engine/install/).
If you have installed compose, make sure it is upgraded to V2 version.

---

### 3. Installation

Cloning the repository

```bash
git clone git@github.com:DmGorokhov/Exchangerates-Converter.git
cd Exchangerates-Converter
```

Activate virtual environment

```bash
poetry shell
```
**Create .env file and set environment variables using file .env.example as example.
For development purposes you can leave these variables as suggested in example.  
If you would like leave example variables (do it only for developer and check purposes) type in terminal:**
```commandline
mv .env.example .env
```

Setup app
```bash
make setup
```
___
### 4. Usage

```
make start  # starts  web server, database, redis and pgadmin docker containers
```
```
make start-d  # starts  all docker containers as daemon process
```
```
make stop  # stops  all docker containers, which were started as daemon process
```

Open your browser at http://127.0.0.1:8000/docs.
You will see the automatic interactive API documentation and endpoints.  
You can try it right there in interactive mode, or you can query it in the terminal.  
In project are available 3 endpoints:
1. [http://localhost:8000/api/v1/convert]()  
Endpoint accepts 3 required request parameters, 
the amount of money and two currency codes from which currency to which one should be converted.  
Currency codes must comply with iso4217(you see these codes everywhere) standard.
Endpoint returns the result of conversion
of the specified amount of money.  
Full requset look like *http://localhost:8000/api/v1/convert?amount=34&from_base=usd&to_target=rub*  
Request example in terminal with curl:  
```
curl -X GET 'http://localhost:8000/api/v1/convert?amount=10&from_base=usd&to_target=rub'
```

2. [http://localhost:8000/api/v1/update_rates]()  
Endpoint updates the currency rates in the database. 
The request for latest exchange rates is executed through the api of an external service,  
which was specified at startup via environment variables. For more details on configuring 
the external api of currency rates, see point 5 below. Endpoint returns  
a successful update message or an error message if the update was not successful. When updating, the cache for 
currency pairs is deleted, if it exists.  
Request example in terminal with curl:  
```
curl -X GET 'http://localhost:8000/api/v1/update_rates'
```
3. [http://localhost:8000/api/v1/last_update]()  
Endpoint returns the date when the exchange rates were last updated from the database. 
If the database is empty, an empty object is returned.
Request example in terminal with curl:  
```
curl -X GET 'http://localhost:8000/api/v1/last_update'
```
___
### 5. Caching
The project provides caching of currency pairs rates via Redis. At the first conversion request, both forward (e.g. USDEUR) and reverse rates (EURUSD) are cached.
At the next conversion request for these currency pairs, the value is requested from the cache, which eliminates unnecessary requests to the database. At the same time,
the cache is deleted at each request to update currency rates.
___
### 6. Working with api of external exchange rate services
#### 6.1 Service selection.
The choice of service to request currency rates is specified by a pair of environment variables:
EXCHANGERATE_API_SERVICE specifies the name of the service,  
EXCHANGERATESAPI_API_KEY sets the api access key, if necessary.
Now in the project is realized work with two services, which also have free access plans - Exchangerates and  
Openexchangerates. To set a service you need to uncomment the corresponding pair of environment variables and
comment out all the others. If you forget to comment out  
unnecessary services, the last one from top to bottom will be installed, because the last variables will 
overwrite all previously installed ones.

#### 6.2 Adding a new service
Adding a new service is fairly straightforward:
-  6.2.1 In the */src/external_services/response_schemas/* folder in the *schemas.py* module, you need to 
add the Pydantic model inherited from **ExchangeRatesBase** for parsing data from the new service's api. 
- 6.2.2  In the */src/external_services/* folder create a new file for the interface adapter of the new service.
The name of the module usually contains the name of the service itself with the addition of "_api" at the end.  
In this module, import the **AbstractExchangeApiService** abstract class from *abstract_exchange_api_service.py* in
the same directory. This class defines the required service interface through properties and methods.  
Most of the properties are intuitive, the **get_latest_rates method** is worth paying attention to.
This method should perform a data request to the api of the new service 
(in general it is suggested to use  
the *make_async_httpx_request method* from */src/utils.py* ) and as
a response return an instance of the **ExchangeServiceAPIResponse** schema, which is the input interface for the 
main application code. In general,  
many exchange services are very similar, and it will probably be enough
for you to define the schema in the schemas.py module and alias the fields of the external api to match the 
ExchangeServiceAPIResponse schema.
- 6.2.3 Now you need to add the new service to your settings to be able to select it.
To do this, in the .env file create another instance of the **EXCHANGERATE_API_SERVICE** environment 
variable with the  
name of your new service, and in the same file add a new environment variable for
the name of the api key for the service. Add the name of the new variable for the api key to the list 
of variables in */src/config.py*.  In the */src/base_dependencies.py* file, in the **EXCHANGE_RATE_SERVICES** 
dictionary, add the service name that you specified in the **EXCHANGERATE_API_SERVICE** environment variable
as the dictionary key.  
As the value for this key, import and specify the class created in 5.2.2. 
You do not need to initialize the class in this place.  
**And that's it!!! Now you can connect and use your service in accordance with point 6.1, described above.**

___
### 6. Access to the database for development purposes (PgAdmin docker container)
When you have started the service with the ```make start``` command, you can 
go to http://127.0.0.1:5050/ in your browser to interactively access the PgAdmin tools. 
Enter the login and password you specified in the PGADMIN_MAIL and PGADMIN_PW environment variables. 
Then connect the database server according to the database settings you specified when starting
the service (in the .env file). Now you can also work with the project database in interactive mode.
