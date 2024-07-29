# CloudWAF Origin Detector

CloudWAF Origin Detector is a Python script that checks Fastly services for specific backends containing "sigscicloudwaf.com". It helps Fastly users quickly identify which of their services are configured with backends pointing to this domain.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher installed on your system.
- A Fastly API token with permissions to access service and backend information.
- The `pipenv` Python package installed in your environment.

## Installation

Clone this repository to your local machine using:

```bash
git clone https://github.com/ssiar-fastly/cloudwaf-origin-detector.git
```

Navigate to the cloned directory:

```bash
cd cloudwaf-origin-detector
```

Install the required Python packages using `pipenv`:

```bash
pipenv install requests
```

## Usage

To use the CloudWAF Origin Detector, run the script from the command line, providing your Fastly API token and the customer IDs you wish to check. Here's how you can do it:

```bash
pipenv run python cloudwaf-origin-detector.py --fastly_token $FST_TOKEN --customer_ids $CUSTOMER_ID1 $CUSTOMER_ID2 $CUSTOMER_ID3
```

Replace `YOUR_FASTLY_API_TOKEN`, `CUSTOMER_ID1`, `CUSTOMER_ID2`, and `CUSTOMER_ID3` with your actual Fastly API token and customer IDs. Use the `--verbose` flag if you wish to receive detailed output during the script's execution.

## Contributing

Contributions to the CloudWAF Origin Detector are welcome! Here's how you can contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -am 'Add some feature'`.
4. Push your changes to the branch: `git push origin <branch_name>`.
5. Create a pull request.

Please adhere to this project's `code of conduct` in your interactions with the project.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name - [@sinasiar](https://x.com/sinasiar) - ssiar@fastly.com

Project Link: [https://github.com/ssiar-fastly/cloudwaf-origin-detector](https://github.com/ssiar-fastly/cloudwaf-origin-detector)
