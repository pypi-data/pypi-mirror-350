import os
import logging
import datetime
import json
import ast
import jwt
import urllib #Needed for avoiding using requests, which modified the S3 presigned URL

from .utils import convert_timestamps, send_post_request, send_get_request, decode_jwt_token, querystr_to_json, att2statement

from .constants import (
    SCRIBE_VULNERABILITIES_DATASET,
    SCRIBE_PRODUCTS_DATASET,
    SCRIBE_POLICY_DATASET,
    SCRIBE_TEAM_STAT_DATASET
)

class ScribeClient:
    scribe_vulnerabilities_dataset = "API Vulnerabilities"
    scribe_products_dataset = "asbom_filtered"
    scribe_policy_dataset = "Policy results v5"
    scribe_team_stat_dataset ="MARKETING Team activity"
    scribe_lineage_dataset="extended_lineage_new"

    def get_chache_data(self):
        return {
            "timestamp": datetime.datetime.now().isoformat(),
            "datasets": self.datasets,
            "product_list": self.product_list,
            "team_name": self.team_name,
            "team_info": self.team_info
        }
    
    def need_cache_data_update(self, cached_data):
        # if timestamp older than one day
        if cached_data and "timestamp" in cached_data:
            try:
                last_update = datetime.datetime.fromisoformat(cached_data["timestamp"])
            except Exception as e:
                logging.error(f"Error parsing timestamp: {e}")
                return True
            return (datetime.datetime.now() - last_update).days > 1

    def __init__(self, api_token=None, ignore_env = True, base_url="https://api.scribesecurity.com", refresh_interval=600, cached_data={}):
        def update_from_cached_data(cached_data):
            if "datasets" in cached_data:
                self.datasets = cached_data["datasets"]
                self.dataset_ids = self.create_dataset_id_map(self.datasets)
            else: 
                logging.error("No datasets in provided cached data")
            if "product_list" in cached_data:  
                self.product_list = cached_data["product_list"]
            else:
                logging.error("No product list in provided cached data")
            if "team_name" in cached_data:
                self.team_name = cached_data["team_name"]
            else:
                logging.error("No team name in provided cached data")
            if "team_info" in cached_data:
                self.team_info = cached_data["team_info"]
            else:
                logging.error("No team info in provided cached data")


        if ignore_env:
            self.api_token = api_token
        else:
            self.api_token = api_token or os.getenv('SCRIBE_TOKEN')
        self.base_url = base_url
        self.refresh_interval = refresh_interval
        self.last_refresh = datetime.datetime.now() - datetime.timedelta(days=5)  # Initialize to a time in the past

        self.jwt_token = None
        self.superset_token = None
        self.dataset_ids = None
        self.datasets = None
        self.product_list = None
        self.team_id = None
        self.team_name = None
        self.team_info = None
        p = None
        if self.api_token:
            self.last_refresh = datetime.datetime.now() # - datetime.timedelta(hours=5)
            self.refresh_data(force=True)
            
            if not cached_data or self.need_cache_data_update(cached_data):
                d = self.get_datasets()
                if not d:
                    logging.error("Refresh: Failed to update dataset IDs")
                else:
                    self.datasets = d
                    self.dataset_ids = self.create_dataset_id_map(d)
                    p = self.get_products(force=True)
                if not p:
                    logging.error("Refresh: Failed to update product list")
                    logging.error(f"Using previous product list\n{self.product_list}")
                else:
                    self.product_list = p

                t = self.get_team_info()
                if not t:
                    logging.error("Failed to get team data.")
            else:
                update_from_cached_data(cached_data)

    def validate_dataset(self, dataset_name):
        if not self.dataset_ids:
            self.refresh_data()
        if not self.dataset_ids:
            logging.error("Failed to get dataset IDs")
            return False
        if dataset_name not in self.dataset_ids:
            logging.error(f"Dataset {dataset_name} not found")
            return False
        return True
    def set_api_token(self, api_token):
        if self.is_api_token_set():
            return
        self.api_token = api_token
        if self.api_token:
            self.last_refresh = datetime.datetime.now()
            self.refresh_data(force=True)

    def is_api_token_set(self):
        return self.api_token is not None


    def refresh_data(self, force=False):
        if not self.api_token:
            logging.error("No API token provided")
            return
        
        need_refresh = (
            force or
            not self.dataset_ids or
            not self.product_list or
            (datetime.datetime.now() - self.last_refresh).seconds > self.refresh_interval
        )

        if not need_refresh:
            return

        self.last_refresh = datetime.datetime.now()

        self.jwt_token = self.login(self.api_token, self.base_url)
        if not self.jwt_token:
            logging.error("Refresh: Failed to get JWT token")

        try:
            decoded_token = jwt.decode(self.jwt_token, options={"verify_signature": False})
            self.decoded_token = decoded_token
        except jwt.InvalidTokenError as e:
            logging.error(f"Invalid JWT token: {e}")
            self.decoded_token = None
            return
        jwt_name = decoded_token.get("name")
        try:
            self.team_id = jwt_name.split("scribe-hub-team")[1].split("-")[0]
            logging.info(f"Team:{self.team_id}")
        except Exception as e:
            logging.error(f"Error extracting team ID: {e}")
            self.team_id = None


        self.superset_token = self.get_superset_token(self.jwt_token, self.base_url)
        if not self.superset_token:
            logging.error("Refresh: Failed to get Superset token")

    def send_post_request(self, url, token=None, body=None):
        """
        Deprecated: Use `send_post_request` from `utils.py` instead.
        """
        return send_post_request(url, token, body)

    def send_get_request(self, url, token=None):
        """
        Deprecated: Use `send_get_request` from `utils.py` instead.
        """
        return send_get_request(url, token)

    def decode_jwt_token(self, jwt_token):
        """
        Deprecated: Use `decode_jwt_token` from `utils.py` instead.
        """
        return decode_jwt_token(jwt_token)

    def querystr_to_json(self, query):
        """
        Deprecated: Use `querystr_to_json` from `utils.py` instead.
        """
        return querystr_to_json(query)

    def att2statement(self, data):
        """
        Deprecated: Use `att2statement` from `utils.py` instead.
        """
        return att2statement(data)

    def login(self, api_token, base_url):
        url = f"{base_url}/v1/login"
        body = {"api_token": api_token}
        response = self.send_post_request(url=url, body=body)

        if response and 'token' in response.json():
            return response.json()['token']
        else:
            logging.error("Token not found in the response.")
            return None

    def get_superset_token(self, jwt_token, base_url):
        url = f"{base_url}/dataset/token"
        response = self.send_get_request(url=url, token=jwt_token)
        if not response:
            return None

        response_json = json.loads(response.text)
        if 'access_token' in response_json:
            return response_json['access_token']
        else:
            logging.error("Access token not found in the response.")
            return None

    def create_dataset_id_map(self, datasets):
        data = datasets
        if not data:
            return {}

        try:
            result = data.get("result", [])
            datasource_id_map = {}
            for entry in result:
                datasource_name = entry.get("datasource_name")
                datasource_id = entry.get("id")
                if datasource_name and datasource_id:
                    datasource_id_map[datasource_name] = entry
            return datasource_id_map
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON: {e}")
            return {}

    def get_team_info(self):
        if not self.team_id:
            logging.error("Team ID not set.")
            return False
        if not self.validate_dataset(self.scribe_team_stat_dataset):
            return False
        query = {
            "columns": [
                "teamName"
            ],
            "filters": [
                {
                    "col": "teamId",
                    "op": "==",
                    "val": self.team_id
                }
            ],
            "metrics": [],
            "orderby": [],
            "row_limit": 1
        }
        r = self.query_superset(self.scribe_team_stat_dataset, query)
        try:
            self.team_name = r["result"][0]["data"][0]["teamName"]
            self.team_info = r["result"][0]["data"][0]
        except (KeyError, IndexError) as e:
            logging.error(f"Error accessing response data: {e}")
            return False
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON: {e}")
            return False

        return True
    
    def get_link(self, use = "products", text = "Link", params = {}):
        params_str = ""
        if params:
            # %3B is the URL encoded version of ';'
            params_str = ";;".join([f"{k}:{v}" for k, v in params.items()])
            params_str = "searchFilters=" + params_str

        if use == "products":
            return f"\n[{text}](https://scribe-security.github.io/redirect/redirect.html?path=%2Fproducer-products)"
        # Add here elif for all uses
        elif use == "product_vulnerabilities":
            if params:
                params_str = '&' + params_str
            # return f"\n[{text}](http://localhost:8090/redirect.html?path=%2Fsbom?redirectTabName=Vulnerabilities&{params_str})"
            return f"\n[{text}](https://scribe-security.github.io/redirect/redirect.html?path=%2Fsbom?redirectTabName=Vulnerabilities{params_str})"
        elif use == "product_policy_results":
            if params:
                params_str = '?' + params_str
            return f"\n[{text}](https://scribe-security.github.io/redirect/redirect.html?path=%2Fpolicy%2Fevaluation{params_str})"
        else:
            return f"\n[{text}](https://app.scribesecurity.com)"

    def get_products(self, all_versions=False, force=False):
        if not force:
            if (datetime.datetime.now() - self.last_refresh).seconds < self.refresh_interval and self.product_list:
                return self.product_list
        if not self.validate_dataset(self.scribe_products_dataset):
            return None

        url = f"{self.base_url}/dataset/data"
        body = {
            "superset_token": self.superset_token,
            "validate": False,
            "query": {
                "datasource": {
                    "id": self.dataset_ids[self.scribe_products_dataset]["id"],
                    "type": "table"
                },
                "force": "false",
                "queries": [
                    {
                        "columns": [
                            "logical_app",
                            "logical_app_version",
                            "version_timestamp"
                        ],
                        "filters": [],
                        "metrics": [],
                        "orderby": [["logical_app", True], ["version_timestamp", False]],
                        "row_limit": 0
                    }
                ],
                "result_format": "json",
                "result_type": "results"
            }
        }

        r = self.send_post_request(url=url, token=self.jwt_token, body=body)
        if not r:
            return self.product_list

        try:
            o = r.json()
            o = convert_timestamps(o, "version_timestamp")
            result = []
            for product in o["result"][0]["data"]:
                item = {"name": product["logical_app"], "version": product["logical_app_version"], "timestamp": product["version_timestamp"]}
                result.append(item)
            self.product_list = result
        except Exception as e:
            logging.error(f"Error decoding JSON: {e}")
            return self.product_list

        if all_versions:
            return result

        # Keep only latest version per product
        latest = []
        last_product = ""
        for product in result:
            if product['name'] == last_product:
                continue
            last_product = product['name']
            latest.append(product)

        # sort by timestamp
        latest.sort(key=lambda x: x['timestamp'], reverse=True)
 
        return latest

    def format_table(self, headers, rows):
        """
        Format a table with aligned columns for better readability in plain text.

        Parameters:
            headers (list): List of column headers.
            rows (list of lists): List of rows, where each row is a list of column values.

        Returns:
            str: Formatted table as a string.
        """
        # Calculate the maximum width of each column
        column_widths = [len(header) for header in headers]
        for row in rows:
            for i, value in enumerate(row):
                column_widths[i] = max(column_widths[i], len(str(value)))

        # Create a format string for each row
        row_format = " | ".join(f"{{:<{width}}}" for width in column_widths)

        # Format the header and rows
        header_line = row_format.format(*headers)
        separator_line = "-+-".join("-" * width for width in column_widths)
        row_lines = [row_format.format(*[str(value) for value in row]) for row in rows]

        # Combine all parts into a single string
        return "\n".join([header_line, separator_line] + row_lines)

    def format_query_result_table(self, query_result):
        """
        Format query results into an aligned table for better readability.

        Parameters:
            query_result (dict): The query result containing columns and data.

        Returns:
            str: Formatted table as a string.
        """
        try:
            data = query_result["result"][0]["data"]
            if not data:
                return "No data found"

            columns = query_result["result"][0]["colnames"]
            if not columns:
                return "No columns information found"

            # Prepare headers and rows for the table
            headers = columns
            rows = [[row[col] for col in columns] for row in data]

            # Format the table using the existing format_table method
            return self.format_table(headers, rows)

        except Exception as e:
            logging.error(f"Error formatting query result: {e}")
            return "Error formatting query result"

    def get_products_str(self, with_link=True):
        r = self.get_products()
        if not r:
            return "No products found"

        try:
            # Prepare headers and rows for the table
            headers = ["App", "Version", "Version Timestamp"]
            rows = [[row['name'], row['version'], row['timestamp']] for row in r]

            # Format the table
            table = self.format_table(headers, rows)

            if with_link:
                table += self.get_link(use="products", text="Product page")

        except Exception as e:
            logging.error(f"Error decoding JSON: {e}")
            table = "Error getting product list"

        logging.info(table)
        return table

    def get_logical_app_version(self, logical_app):
        if not self.product_list:
            self.refresh_data()
            if not self.product_list:
                return "I have issues getting data from Scribe, Sorry"
        for product in self.product_list:
            if product["name"] == logical_app:
                latest = product["version"]
                logging.info(f"Latest version for {logical_app} is {latest}")
                return latest
        return None

    def get_product_vulnerabilities(self, logical_app, logical_app_version=None):
        self.refresh_data()
        if not logical_app_version:
            v = self.get_logical_app_version(logical_app)
            if v:
                logical_app_version = v
            else:
                logging.error(f"Failed to get version for {logical_app}")
                return None, None

        if not self.validate_dataset(self.scribe_vulnerabilities_dataset):
            return None
        url = f"{self.base_url}/dataset/data"
        body = {
            "superset_token": self.superset_token,
            "validate": False,
            "query": {
                "datasource": {
                    "id": self.dataset_ids[self.scribe_vulnerabilities_dataset]["id"],
                    "type": "table"
                },
                "force": False,
                "queries": [
                    {
                        "columns": [
                            "vulnerability_id",
                            "severity",
                            "epssProbability",
                            "targetName",
                            "component_name",
                            "logical_app",
                        ],
                        "filters": [
                            {
                                "col": "logical_app",
                                "op": "==",
                                "val": logical_app
                            },
                            {
                                "col": "logical_app_version",
                                "op": "==",
                                "val": logical_app_version
                            },
                            {
                                "col": "vulnerability_id",
                                "op": "like",
                                "val": "CVE-%"
                            }
                        ],
                        "metrics": [],
                        "orderby": [["severity", False], ["epssProbability", False]],
                        "row_limit": 10
                    }
                ],
                "result_format": "json",
                "result_type": "results"
            },
            "validate": False
        }

        r = self.send_post_request(url=url, token=self.jwt_token, body=body)
        if r:
            try:
                return r.json(), logical_app_version
            except Exception as e:
                logging.error(f"Error decoding JSON: {e}")
                return {}, logical_app_version
        return {}, logical_app_version

    def get_product_vulnerabilities_str(self, logical_app, logical_app_version=None, with_link=True):
        r, logical_app_version = self.get_product_vulnerabilities(logical_app, logical_app_version)
        if not r:
            return "Failed getting vulnerability data"

        try:
            vuln_list = r["result"][0]["data"]
            if not vuln_list:
                return "No vulnerabilities found"

            # Prepare headers and rows for the table
            headers = ["ID", "Severity", "EPSS", "Vulnerable Component", "Artifact"]
            rows = [
                [
                    f"[{vuln['vulnerability_id']}](https://nvd.nist.gov/vuln/detail/{vuln['vulnerability_id']})",
                    vuln['severity'],
                    vuln['epssProbability'],
                    vuln['component_name'],
                    vuln['targetName']
                ]
                for vuln in vuln_list
            ]

            # Format the table
            table = self.format_table(headers, rows)

            if with_link:
                table += self.get_link(
                    use="product_vulnerabilities",
                    text="Product vulnerabilities",
                    params={"product": logical_app, "product_version": logical_app_version, "show_file_components": "false"}
                )

        except Exception as e:
            logging.error(f"Error decoding JSON: {e}")
            table = "Error getting vulnerability list"

        logging.info(table)
        return table

    def get_product_vulnerability_distribution(self, logical_app, logical_app_version=None):
        def severity_label(severity):
            print(f"Assigning severity label for severity: {severity}")
            if severity <= 3.9:
                return "Low"
            elif severity <= 6.9:
                return "Medium"
            elif severity <= 8.9:
                return "High"
            else:
                return "Critical"
            
        self.refresh_data()
        if not logical_app_version:
            v = self.get_logical_app_version(logical_app)
            if v:
                logical_app_version = v
            else:
                return None

        if not self.validate_dataset(self.scribe_vulnerabilities_dataset):
            return None
        url = f"{self.base_url}/dataset/data"

        body = {
            "superset_token": self.superset_token,
            "validate": False,
            "query": {
                "datasource": {
                    "id": self.dataset_ids[self.scribe_vulnerabilities_dataset]["id"],
                    "type": "table"
                },
                "force": False,
                "queries": [
                    {
                        "columns": [
                            "logical_app",
                            "logical_app_version",
                            "vulnerability_id",
                            "severity"
                        ],
                        "filters": [
                            {
                                "col": "logical_app",
                                "op": "==",
                                "val": logical_app
                            },
                            {
                                "col": "logical_app_version",
                                "op": "==",
                                "val": logical_app_version
                            },
                            {
                                "col": "vulnerability_id",
                                "op": "like",
                                "val": "CVE-%"
                            }
                        ],
                        "metrics": [
                            {
                                "label": "vulnerabilities",
                                "expressionType": "SQL",
                                "sqlExpression": "COUNT(DISTINCT vulnerability_id)"
                            },
                        ],
                        "post_processing": [],
                        "groupby": ["severity"],
                        "orderby": [["severity", False]],
                        "row_limit": 10
                    }
                ],
                "result_format": "json",
                "result_type": "results"
            }
        }

        r = self.send_post_request(url=url, token=self.jwt_token, body=body)
        if r:
            try:
                r = r.json()
                data = r["result"][0]["data"]
                for row in data:
                    row["severity_label"] = severity_label(row["severity"])
                return data
            except Exception as e:
                logging.error(f"Error decoding JSON: {e}")
                return []
        return []


    def get_datasets(self):
        url = f"{self.base_url}/dataset"
        body = {
            "superset_token": self.superset_token
        }

        r = self.send_post_request(url=url, token=self.jwt_token, body=body)
        if r:
            r = r.json()
            os.makedirs("tmp", exist_ok=True)  # Ensure the tmp directory exists

            with open("tmp/datasets.json", "w") as f:
                json.dump(r, f)
            
        return r
    
    def query_superset(self, dataset, query, time_tokens=[]):
        dataset_name = dataset
        id = None
        if self.dataset_ids and dataset in self.dataset_ids:
            id = self.dataset_ids[dataset]["id"]
        else:
            logging.error(f"Dataset {dataset} not found in dataset IDs")
            return None
        
        url = f"{self.base_url}/dataset/data"
        body = {
            "superset_token": self.superset_token,
            "validate": False, 
            "query": {
                "datasource": {
                    "id": id,
                    "type": "table"
                },
                "force": "false",
                "queries": [
                    query
                ],
                "result_format": "json",
                "result_type": "results"
            },
            "validate": False
        }

        r = self.send_post_request(url=url, token=self.jwt_token, body=body)
        if r:
            try:
                r = r.json()
                for t in time_tokens:
                    r = convert_timestamps(r, col_substr=t)
                return r
            except Exception as e:
                logging.error(f"Error decoding JSON: {e}")
                return {}
            
    def query_result_to_str(self, header, r):
        if not header:
            header = ""
        try:
            data = r["result"][0]["data"]
            if not data:
                return "No data found"
            columns = r["result"][0]["colnames"]
            if not columns:
                return "No columns information found"
            
            md_table = ["| " + " | ".join(columns) + " |", "| ---" * len(columns) + " |"]
            for row in data:
                md_table.append("| " + " | ".join([str(row[col]) for col in columns]) + " |")
            o = header + '\n' + "\n".join(md_table)
        except Exception as e:
            logging.error(f"Error decoding JSON: {e}")
            o = "Error getting data"

        return o
            
    def query_str(self, dataset, query, header = "Query results:"):
        r = self.query_superset(dataset, query, time_tokens = ["timestamp", "time_evaluated", "Time", "created", "published_on", "LastModified",
                                                               "date_changed", "advisory_modified"])
        if not r:
            return "Failed getting data"
        o = self.query_result_to_str(header,r)
        return o
    
    def get_policy_results(self, logical_app="Scribot", logical_app_version=None, initiative="%"):
        self.refresh_data()
        if not logical_app_version:
            v = self.get_logical_app_version(logical_app)
            if v:
                logical_app_version = v
            else:
                logging.error(f"Failed to get version for {logical_app}")
                return None, None
        if not self.validate_dataset(self.scribe_policy_dataset):
            return None, None

        url = f"{self.base_url}/dataset/data"
        body = {
            "superset_token": self.superset_token,
            "validate": False,
            "query": {
                "datasource": {
                    "id": self.dataset_ids[self.scribe_policy_dataset]["id"],
                    "type": "table"
                },
                "force": "false",
                "queries": [
                    {
                        "columns": [
                            "logical_app",
                            "logical_app_version",
                            "status",
                            "time_evaluated",
                            "initiative_id",
                            "gen_rule_name",
                            "status_string",
                        ],
                        "filters": [
                            {
                                "col": "initiative_id",
                                "op": "like",
                                "val": initiative
                            },
                            {
                                "col": "logical_app",
                                "op": "==",
                                "val": logical_app
                            },
                            {
                                "col": "logical_app_version",
                                "op": "==",
                                "val": logical_app_version
                            },
                            {
                                "col": "status",
                                "op": "!=",
                                "val": 'notApplicable'
                            }
                        ],
                        "metrics": [],
                        "orderby": [["time_evaluated", False], ["status", True]],
                        "row_limit": 10
                    }
                ],
                "result_format": "json",
                "result_type": "results"
            }
        }

        r = self.send_post_request(url=url, token=self.jwt_token, body=body)
        if r:
            try:
                r = r.json()
                r = convert_timestamps(r, "time_evaluated")
                return r, logical_app_version
            except Exception as e:
                logging.error(f"Error decoding JSON: {e}")
                return {}, logical_app_version
        return {}, logical_app_version

    def get_policy_results_str(self, logical_app="scribe-platform", logical_app_version=None, initiative="%", with_link=True):
        r, logical_app_version = self.get_policy_results(logical_app, logical_app_version, initiative)
        if not r:
            return "Failed getting policy results"

        try:
            policy_list = r["result"][0]["data"]
            if not policy_list:
                return f"No policy results found for product {logical_app}: {logical_app_version} and initiative {initiative}"

            # Prepare headers and rows for the table
            headers = ["Rule", "Status", "Time Evaluated", "Type", "Details"]
            rows = [
                [
                    result['gen_rule_name'],
                    result['status'],
                    result['time_evaluated'],
                    result['initiative_id'],
                    result['status_string'].replace('\n', ' ')
                ]
                for result in policy_list
            ]

            # Format the table
            table = self.format_table(headers, rows)

            if with_link:
                table += self.get_link(
                    use="product_policy_results",
                    text="Policy results",
                    params={"product": logical_app, "product_version": logical_app_version, "show_file_components": "false"}
                )

        except Exception as e:
            logging.error(f"Error decoding JSON: {e}")
            table = "Error getting policy results"

        return table
    
     
    def get_product_lineage(self, logical_app, logical_app_version=None):
        self.refresh_data()
        if not logical_app_version:
            v = self.get_logical_app_version(logical_app)
            if v:
                logical_app_version = v
            else:
                logging.error(f"Failed to get version for {logical_app}")
                return None, None
        if not self.validate_dataset(self.scribe_policy_dataset):
            return None, None
        # left out columns:
        # "product_id",
        # "version_id",
        # "child_id",
        # "properties",
        query = {
            "columns": [
                "timestamp",
                "logical_app",
                "logical_app_version",
                "platform_name",
                "platform_type",
                "asset_type",
                "asset_name",
                "external_id",
                "uri",
                "owner",
                "path",
                "parent_id",
                "parent_type",
                "parent_name",
                "parent_external_id",
                # "properties"
            ],
            "filters": [
                {
                    "col": "logical_app",
                    "op": "==",
                    "val": logical_app
                },
                {
                    "col": "logical_app_version",
                    "op": "==",
                    "val": logical_app_version
                }
            ],
            "metrics": [],
            "orderby": [["timestamp", False]],
            "annotation_layers": [],
            "row_limit": 100,
            "post_processing": []
        }
        r = self.query_superset(self.scribe_lineage_dataset, query, time_tokens = ["timestamp"])
        # TODO: check in superset prod for more columns
        if r:
            try:
                data = r["result"][0]["data"]
            except Exception as e:
                logging.error(f"Error decoding JSON: {e}")
                return [], logical_app_version
            if not data:
                return [], logical_app_version
            for row in data:
                if row.get("properties"):
                    try:
                        row["properties"] = ast.literal_eval(row["properties"])
                    except Exception as e:
                        logging.error(f"Error decoding properties: {e}")
                        row["properties"] = {}
            return data, logical_app_version
        else:
            return [], logical_app_version

    types_to_position = {
            "organization": 1,
            "repo": 2,
            "branch": 3,
            "workflow": 4,
            "workflow_run": 5,
            "image": 6,
            "pod": 7,
            "namespace": 8

    }

    def create_lineage_graph(self, lineage_data):
            # Determine allowed asset types from the data.
        # all_types = {record.get("asset_type") for record in lineage_data if record.get("asset_type")}
        # # Exclude unwanted types.
        # exclude_types = {"user", "secret", "org_secret", "commit", "actor", "build_machine"}
        # include_types = all_types - exclude_types
        
        # # Define the mapping for layering.
         
        # # Generate and display the network visualization.
        # fig = lineage_graph.visualize_network(lineage_data, include_types, self.types_to_position)
        logging.error("create_lineage_graph is not supported in the python package.")
        return None
    
    include_fields = [
        "platform_name", "platform_type",
        "asset_name", "asset_type","parent_name", "parent_type"
   ]

    def filter_lineage_data(self, data, include_types=types_to_position, include_fields=include_fields):
        """
        Filter the data to only include records of the specified types
        and remove specified fields.

        Parameters:
            data (list): List of JSON records.
            include_types (set): Asset types to keep.
            include_fields (set): Fields to remove from records.

        Returns:
            list: Filtered data.
        """
        filtered_data = []
        
        for record in data:
            if record.get("asset_type") in include_types:
                # Create a copy to avoid modifying original data
                filtered_record = {key: value for key, value in record.items() if key in include_fields}
                filtered_data.append(filtered_record)
        
        return filtered_data
    
    def list_attestations(self, criteria={}):
        self.refresh_data()
        url = f"{self.base_url}/evidence/list"
        body = criteria
        r = self.send_post_request(url=url, token=self.jwt_token, body=body)
        if r:
            try:
                return r.json()
            except Exception as e:
                logging.error(f"Error decoding JSON: {e}")
        return {}

    def get_attestation(self, attestation_id):
        url = f"{self.base_url}/evidence/{attestation_id}"
        r = self.send_get_request(url=url, token=self.jwt_token)
        if not r:
            return {}
        try:
            o = r.json()
            url = o.get("presigned_url")
            if url:
                response = urllib.request.urlopen(url)
                content = response.read()
                o = json.loads(content)
            
                if 'payload' in o:
                    o = self.att2statement(o)
            else:
                logging.error(f"Presigned URL not found in response")
                return {}
        except Exception as e:
            logging.error(f"Error decoding JSON: {e}")
            return {}
        return o

    def get_latest_attestation(self, criteria={}):
        atts = self.list_attestations(criteria=criteria)
        if not atts:
            return {}
        evidence_list = atts.get("evidences", [])
        if not evidence_list:
            return {}

        evidence_list.sort(key=lambda x: x['context']["timestamp"], reverse=True)
        if not evidence_list:
            return {}
        evidence = evidence_list[0]
        att = self.get_attestation(evidence["id"])
        return att
    
    def query_vulnerabilities(self, querystr, title="") -> str:
        logging.debug(f"Query vulnerabilities with: {querystr}")
        query = self.querystr_to_json(querystr)
        if query:
            r = self.query_superset(self.scribe_vulnerabilities_dataset, query, time_tokens=["timestamp"])
            if r:
                return f"{title}\n{self.format_query_result_table(r)}"
        return "Error running query"

    def query_products(self, querystr, title="") -> str:
        logging.debug(f"Query products with: {querystr}")
        query = self.querystr_to_json(querystr)
        if query:
            r = self.query_superset(self.scribe_products_dataset, query, time_tokens=["timestamp"])
            if r:
                return f"{title}\n{self.format_query_result_table(r)}"
        return "Error running query"

    def query_lineage(self, querystr, title="") -> str:
        logging.debug(f"Query lineage with: {querystr}")
        query = self.querystr_to_json(querystr)
        if query:
            r = self.query_superset(self.scribe_lineage_dataset, query, time_tokens=["timestamp"])
            if r:
                return f"{title}\n{self.format_query_result_table(r)}"
        return "Error running query"
    
    def query_policy_results(self, querystr, title="") -> str:
        logging.debug(f"Query policy results with: {querystr}")
        query = self.querystr_to_json(querystr)
        if query:
            r = self.query_superset(self.scribe_policy_dataset, query, time_tokens=["time_evaluated"])
            if r:
                return f"{title}\n{self.format_query_result_table(r)}"
        return "Error running query"