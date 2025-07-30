import argparse
import os
import logging
from .client import ScribeClient

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    parser = argparse.ArgumentParser(description="Scribe Client CLI")
    parser.add_argument("--api-call", choices=[
        "get-products",
        "get-datasets",
        "get-policy-results",
        "list-attestations",
        "get-attestation",
        "get-product-vulnerabilities",
        "get-latest-attestation",
        "query-vulnerabilities",
        "query-products",
        "query-policy-results",
        "query-lineage"
    ], help="Which API call to execute")
    parser.add_argument("--api-token", required=False, default=os.getenv('SCRIBE_TOKEN'), help="Your API token from ScribeHub integrations page (defaults to SCRIBE_TOKEN environment variable)")
    parser.add_argument("--env", default="prod", choices=["prod", "dev", "test", "ci"], help="Which environment to use")
    parser.add_argument("--product-name", required=False, help="The name of the product (required for specific API calls)")
    parser.add_argument("--attestation-id", required=False, help="The ID of the attestation (required for get-attestation API call)")
    parser.add_argument("--query", required=False, help="The query to run on the dataset (required for query commands)")

    args = parser.parse_args()

    if not args.api_token:
        logging.error("No API token provided. Please set the SCRIBE_TOKEN environment variable or pass --api-token.")
        exit(1)

    if args.api_call in ["get-policy-results", "get-product-vulnerabilities", "get-latest-attestation"] and not args.product_name:
        logging.error("The --product-name argument is required for the selected API call.")
        exit(1)

    if args.api_call == "get-attestation" and not args.attestation_id:
        logging.error("The --attestation-id argument is required for the get-attestation API call.")
        exit(1)

    if args.api_call in ["query-vulnerabilities", "query-products", "query-policy-results", "query-lineage"] and not args.query:
        logging.error("The --query argument is required for the selected API call.")
        exit(1)

    base_url = "https://api.scribesecurity.com"
    if args.env != "prod":
        base_url = f"https://api.{args.env}.scribesecurity.com"

    client = ScribeClient(api_token=args.api_token, base_url=base_url)

    logging.info(f"Executing API call: {args.api_call}")

    if args.api_call == "get-products":
        print(client.get_products_str())
    elif args.api_call == "get-datasets":
        print(client.get_datasets())
    elif args.api_call == "get-policy-results":
        print(client.get_policy_results_str(logical_app=args.product_name))
    elif args.api_call == "list-attestations":
        print(client.list_attestations())
    elif args.api_call == "get-attestation":
        print(client.get_attestation(args.attestation_id))
    elif args.api_call == "get-product-vulnerabilities":
        print(client.get_product_vulnerabilities_str(logical_app=args.product_name))
    elif args.api_call == "get-latest-attestation":
        criteria = {"name": args.product_name}
        print(client.get_latest_attestation(criteria=criteria))
    elif args.api_call == "query-vulnerabilities":
        print(client.query_vulnerabilities(querystr=args.query))
    elif args.api_call == "query-products":
        print(client.query_products(querystr=args.query))
    elif args.api_call == "query-policy-results":
        print(client.query_policy_results(querystr=args.query))
    elif args.api_call == "query-lineage":
        print(client.query_lineage(querystr=args.query))

if __name__ == "__main__":
    main()