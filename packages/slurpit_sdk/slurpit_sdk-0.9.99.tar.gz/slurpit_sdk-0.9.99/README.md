# Slurpit SDK

The Slurpit SDK is a Python package for interacting with the Slurpit API, enabling developers to easily manage devices and planning resources. It is designed for simplicity and flexibility, offering methods for listing devices, retrieving planning data, and exporting information to CSV format.

## Installation

You can install the Slurpit SDK using pip with the following command:

```bash
pip install slurpit_sdk
```

Alternatively, if you prefer to install from source, clone the repository and run the setup script:

```bash
git clone https://gitlab.com/slurpit.io/slurpit_sdk.git
cd slurpit
python setup.py install
```

## Quick Start

To use the SDK, start by importing the package and setting up the API client:

```python
import slurpit
api = slurpit.api(
    url="http://localhost:8000", 
    api_key="1234567890abcdefghijklmnopqrstuvwxqz"
)
```

Replace the `url` and `api_key` with the URL of your Slurpit instance and your API key respectively.

## Working with Devices

Retrieve and print the hostnames of all devices:

```python
devices = api.device.get_devices()
for device in devices:
    print(device.hostname)
```

## Exporting Data to CSV

To export planning data to a CSV file:

```python
plannings_csvdata = api.planning.get_plannings(export_csv=True)
result = api.device.save_csv_bytes(plannings_csvdata, "csv/plannings.csv")
```
## Exporting Data as Pandas DataFrame

To export planning data as a pandas dataframe

```python
plannings_df = api.planning.get_plannings(export_df=True)
```

## Pagination

Handle large sets of devices with pagination:

```python
devices = api.device.get_devices(offset=100, limit=1000)
for device in devices:
    print(device.hostname)
```