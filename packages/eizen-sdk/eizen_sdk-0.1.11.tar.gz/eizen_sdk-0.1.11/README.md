# EizenSDK

EizenSDK is a Python package that provides a simple interface to interact with the Eizen Analytics API. It handles authentication using Keycloak and provides methods to fetch analytics, zones, sources, and video summaries.

## Installation

Ensure you have Python 3.7+ installed. Then, install the package:

```sh
pip install eizen-sdk
```

## Usage

### Importing and Initializing the SDK

```python
from eizen_sdk import EizenSDK

sdk = EizenSDK(
    username="your_email@example.com",
    password="your_password"
)
```

### Fetching Analytics

```python
analytics = sdk.get_analytics()
print(analytics)
```

### Fetching Zones for an Analytic

```python
zones = sdk.get_analytic_zones(analytic_id=123)
print(zones)
```

### Fetching Sources for a Zone

```python
sources = sdk.get_zone_sources(zone_id=456)
print(sources)
```

### Fetching Sources for an Analytic

```python
sources = sdk.get_analytic_sources(analytic_id=123)
print(sources)
```

### Fetching Source Details

```python
source_details = sdk.get_source_details(source_id=789)
print(source_details)
```

### Fetching Source Summary

```python
source_summary = sdk.get_source_summary(source_id=789)
print(source_summary)
```

## Authentication

EizenSDK handles authentication using Keycloak. It fetches an access token during initialization and refreshes it automatically when expired.

## Error Handling

If any request fails, an exception is raised with the HTTP status code and error message.

## License

This project is licensed under the MIT License.
