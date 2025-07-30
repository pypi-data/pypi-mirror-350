# Navitia Provider Lokalise

This repository provides hook and operator to connect to the [Navitia API](https://doc.navitia.io/#getting-started) using the [Navitia Python library](https://github.com/jonperron/python-navitia-client).

## Installation

The package is available on [pip](https://pypi.org/project/airflow-providers-navitia/). It can be installed using

```bash
pip install airflow-providers-navitia
```

## Connection

Hook and operator are using the following parameter to connect to Lokalise API:

* `navitia_conn_id`: name of the connection in Airflow
* `auth_token`: personal API token to connect to the API. Can be obtained following [this documentation](https://doc.navitia.io/#authentication)

##  Repo organization

* Hook is located in the `navitia_provider/hooks` folder.
* Operator is located in the `navitia_provider/operator` folder.
* Tests for hook and operator are located in the `tests` folder.

## Dependencies

* Python >= 3.11
* Airflow >= 2.7
* python-lokalise-api>=1.1.4

Additional dependencies are described in the [pyproject.toml file](pyproject.toml).
