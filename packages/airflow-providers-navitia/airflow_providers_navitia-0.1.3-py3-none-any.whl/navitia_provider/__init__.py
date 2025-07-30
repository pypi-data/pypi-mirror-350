__version__ = "0.1.3"

## This is needed to allow Airflow to pick up specific metadata fields it needs for certain features.
def get_provider_info():
    return {
        "package-name": "airflow-providers-navitia",  # Required
        "name": "Navitia",  # Required
        "description": "Navitia hook and operator for Airflow based on the Navitia Python unofficial SDK.",  # Required
        "connection-types": [
            {
                "connection-type": "navitia",
                "hook-class-name": "navitia_provider.hooks.navitia.NavitiaHook",
            }
        ],
        "versions": [__version__],  # Required
    }
