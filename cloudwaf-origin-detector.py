import requests
import argparse
import time

# Constants
FASTLY_BASE_URL = "https://api.fastly.com"
MAX_RETRIES = 3
RETRY_WAIT = 10

def get_headers(fastly_token):
    # Generate headers for Fastly API requests
    return {
        "Fastly-Key": fastly_token,
        "Accept": "application/json"
    }

def retry_api_call(func):
    # Decorator to retry API calls upon failure
    def wrapper(*args, **kwargs):
        retries = 0
        verbose = kwargs.pop('verbose', False)
        while retries < MAX_RETRIES:
            response = func(*args, **kwargs)
            if response.status_code == 200:
                return response
            elif response.status_code == 401:
                if verbose:
                    print("API call failed with Unauthorized (401) error. No retry will be attempted.")
                return response
            retries += 1
            if verbose:
                error_message = response.text if response.text else "No additional error message provided"
                print(f"API call failed, response code: {response.status_code}. Error details: {error_message}. Retrying in {RETRY_WAIT}s... (Retry {retries}/{MAX_RETRIES})")
            time.sleep(RETRY_WAIT)
        return response
    return wrapper

@retry_api_call
def list_services(fastly_token, customer_id, verbose=False):
    if verbose:
        print(f"Requesting list of services for customer ID: {customer_id}...")
    url = f"{FASTLY_BASE_URL}/customer/{customer_id}/services"
    response = requests.get(url, headers=get_headers(fastly_token))
    if verbose and response.status_code == 200:
        print(f"Received {len(response.json())} services for customer ID: {customer_id}")
    return response

@retry_api_call
def list_backends(fastly_token, service_id, version_number, verbose=False):
    if verbose:
        print(f"Requesting list of backends for service ID {service_id}, version {version_number}...")
    url = f"{FASTLY_BASE_URL}/service/{service_id}/version/{version_number}/backend"
    response = requests.get(url, headers=get_headers(fastly_token))
    if verbose and response.status_code == 200:
        print(f"Received {len(response.json())} backends for service ID: {service_id}, version {version_number}")
    return response

def find_active_version(fastly_token, service_id, verbose=False):
    if verbose:
        print(f"Retrieving versions for service ID: {service_id}")
    url = f"{FASTLY_BASE_URL}/service/{service_id}/version"
    response = requests.get(url, headers=get_headers(fastly_token))
    if response.status_code == 200:
        versions = response.json()
        for version in versions:
            if version.get('active') == True:
                if verbose:
                    print(f"Active version for service ID {service_id} is {version['number']}")
                return version['number']
        if verbose:
            print(f"No active version found for service ID: {service_id}")
    else:
        if verbose:
            print(f"Failed to retrieve versions for service ID: {service_id}")
    return None

def main(fastly_token, customer_ids, verbose=False):
    for customer_id in customer_ids:
        services_response = list_services(fastly_token, customer_id, verbose=verbose)
        if services_response.status_code != 200:
            continue

        services = services_response.json()
        for service in services:
            service_id = service['id']
            active_version = find_active_version(fastly_token, service_id, verbose=verbose)
            if active_version is None:
                continue

            backends_response = list_backends(fastly_token, service_id, active_version, verbose=verbose)
            if backends_response.status_code == 200:
                backends = backends_response.json()
                for backend in backends:
                    if verbose:
                        print(f"Checking backend: {backend['hostname']} for service ID: {service_id}")
                    if "sigscicloudwaf.com" in backend['address']:
                        print(f"{customer_id}, {service_id}")
                        if verbose:
                            print(f"Service ID: {service_id} with customer ID: {customer_id} has a backend pointing to sigscicloudwaf.com")
                        break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List Fastly service IDs containing a specific backend.")
    parser.add_argument('--fastly_token', required=True, help='Fastly API token')
    parser.add_argument('--customer_ids', nargs='+', required=True, help='Customer IDs for Fastly services')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output for debugging')

    args = parser.parse_args()

    main(args.fastly_token, args.customer_ids, args.verbose)
