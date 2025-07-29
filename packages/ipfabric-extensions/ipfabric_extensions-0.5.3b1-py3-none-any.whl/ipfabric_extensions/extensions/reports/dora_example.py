from ipfabric_extensions.extensions.base_extension import IPFExtension
from ipfabric.tools import Vulnerabilities
from ipfabric.tools import DeviceConfigs
from ipfabric.diagrams import Unicast
import pandas as pd

try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib


DEFAULT_TOML = """
    applications = [
        {"name" = "Internal-app", "source" = "172.16.12.60/31", "destination" = "172.16.31.60", "protocol" = "tcp", "port" = "443", "URL" = "https://app.internal/", "Comments" = "Internal app for use by users inside network"},
        {"name" = "External-app", "source" = "172.16.21.0/24", "destination" = "172.16.32.60", "protocol" = "tcp", "port" = "443", "URL" = "https://app.external.com/", "Comments" = "External-facing app for use by users coming in over VPN"}
    ]
    # Define the checks from ipfabric to preform and the requirements to fetch the data
    # Python SDK Accepts both API and Frontend endpoints
    intent_checks =[
        {'unmanged_neighbors' = {'table_endpoint' = 'technology/cdp-lldp/unmanaged-neighbors', 'filter' = ''}},
        {'hardware_eol' = {'table_endpoint' = 'tables/reports/eof/summary', 'filter' = '{"endSupport": ["color", "eq", "30"]}'}},
        {'aaa'= {'table_endpoint' = 'tables/security/aaa/authorization', 'filter' = '{"primaryMethod": ["color", "eq", "20"]}'}},
        {'ntp' = {'table_endpoint' = '/tables/management/ntp/summary', 'filter' = '{"confSources": ["color", "eq", "20"], "reachableSources": ["color", "eq", "20"]}'}},
        {'snmp_summary' = {'table_endpoint' = '/technology/management/snmp/summary', 'filter' = '{"or": [{"communitiesCount": ["color", "eq", "20"]}, {"communitiesCount": ["color", "eq", "10"]}]}'}},
        {'snmp_communities' = {'table_endpoint' = '/tables/management/snmp/communities', 'filter' = '{"name": ["color", "eq", "20"]}'}},
        {'management_access' = {'table_endpoint' = 'tables/security/aaa/lines', 'filter' = '{"inTransports": ["any", "like", "telnet"]}'}},
        {'cve' = true},
        {'backups' = true}
    ]

    ipf_snapshot = '40e3426f-877e-46ee-a48d-18868b51262d'
"""


class IPFDoraExample(IPFExtension):
    """ """

    name: str = "IPF Dora Example"
    version: str = "0.0.0a"
    icon = "💶"
    ipf_columns_to_fetch: list = ["sn", "version", "hostname", "model", "vendor", "siteName"]
    toml_data = tomllib.loads(DEFAULT_TOML)
    nist_api_key = None

    def __init__(self):
        super().__init__()

    def input_form(self):
        ipf_client = self.get_ipf_client()
        if not ipf_client:
            self.st.write("IP Fabric Client not initialized. Please initialize in side panel.")
            return
        self.st.write(
            "Upload a valid toml file. The Toml represents the configuration of the Dora Application path and the intent checks to be performed."
        )
        self.st.write(f"```{DEFAULT_TOML}```")
        with self.st.form(key="Dora Form"):
            toml_file = self.st.file_uploader(label="inputs.toml", help="Upload the inputs.toml file")
            nist_api_key = self.st.text_input(label="NIST API Key", help="Enter your NIST API Key", type="password")
            submit = self.st.form_submit_button("Generate Report")
            if submit:
                self.nist_api_key = nist_api_key
        if not self.nist_api_key:
            self.st.write("Please enter your NIST API Key")
            return
        all_intent_violations_list_df = self.fetch_intent_checks_data()
        vuls, device_backup = self.fetch_other_check_data()
        list_app_tuple = self.fetch_app_data()
        try:
            self.build_report(all_intent_violations_list_df, vuls, device_backup, list_app_tuple)
        except Exception as e:
            self.st.write(f"error building report")
            self.st.write(f"{type(e)}: {e}")

    def fetch_intent_checks_data(self):
        ipf_client = self.get_ipf_client()
        list_of_intent_dfs = list()
        for get_intent_conf in self.toml_data["intent_checks"]:
            for intent_name, table_config in get_intent_conf.items():
                if isinstance(table_config, dict):
                    df = ipf_client.fetch_all(
                        url=table_config["table_endpoint"],
                        filters=table_config["filter"],
                        reports=True,
                        export="df",
                    )
                    list_of_intent_dfs.append({intent_name: df})
        return list_of_intent_dfs

    def fetch_other_check_data(self):
        ipf_client = self.get_ipf_client()
        for get_intent_conf in self.toml_data["intent_checks"]:
            for intent_name, table_config in get_intent_conf.items():
                if isinstance(table_config, bool):
                    if intent_name == "cve":
                        vuln = Vulnerabilities(ipf_client, nvd_api_key=self.nist_api_key)
                        vulns = vuln.check_versions()
                    if intent_name == "backups":
                        device_config = DeviceConfigs(client=ipf_client)
                        device_configs = device_config.get_all_configurations()
        return vulns, device_configs

    def fetch_app_data(self):
        ipf_client = self.get_ipf_client()
        return_data = list()
        for idx, application_config in enumerate(self.toml_data["applications"], start=1):
            app_unicast_lookup = Unicast(
                startingPoint=application_config["source"],
                destinationPoint=application_config["destination"],
                dstPorts=application_config["port"],
                protocol=application_config["protocol"],
            )
            app_graph_png = ipf_client.diagram.png(app_unicast_lookup)
            app_name = application_config["name"]
            self.st.write(f"# Application Data {idx}: {app_name}")
            self.st.image(app_graph_png)
            app_graph_json = ipf_client.diagram.json(app_unicast_lookup)
            app_graph_nodes = app_graph_json["graphResult"]["graphData"]["nodes"]
            device_sn_to_fetch = [
                node_value["sn"]
                for node_value in app_graph_nodes.values()
                if node_value["type"] in ["l3switch", "fw", "switch", "router", "lb"]
            ]
            filters = {"or": [{"sn": ["like", sn]} for sn in device_sn_to_fetch]}
            device_inventory_df = ipf_client.fetch_all(
                url="inventory/devices",
                filters=filters,
                reports=True,
                export="df",
                columns=self.ipf_columns_to_fetch,
            )
            return_data.append((device_inventory_df, app_graph_png))
        return return_data

    def build_report(self, all_intent_violations_list_df, vuls, device_backup, list_app_tuple):
        ipf_client = self.get_ipf_client()
        final_report_df = list()
        all_devices = ipf_client.fetch_all(url="inventory/devices", export="df", columns=self.ipf_columns_to_fetch)
        # process intent checks
        all_merged_df = list()
        for intent_response in all_intent_violations_list_df:
            for intent_name, intent_df in intent_response.items():
                if intent_name == "unmanged_neighbors" or intent_df.empty:
                    merged_df = None
                    all_merged_df.append({intent_name: merged_df})
                    all_devices[intent_name] = False
                    continue
                all_devices[intent_name] = True
                merged_df = pd.merge(all_devices, intent_df[["sn"]], on="sn")
                all_merged_df.append({intent_name: merged_df})
                all_devices.loc[all_devices["sn"].isin(merged_df["sn"]), intent_name] = False

        # process app data
        for app_tuple in list_app_tuple:
            app_df, app_png = app_tuple
            for merged_df_dict in all_merged_df:
                for intent_name, intent_df in merged_df_dict.items():
                    if intent_df is None:
                        app_df[intent_name] = False
                        continue
                    app_df[intent_name] = True
                    merged_df = pd.merge(app_df, intent_df[["sn"]], on="sn")
                    app_df.loc[app_df["sn"].isin(merged_df["sn"]), intent_name] = False
            final_report_df.append(app_df)

        # process cves
        cve_dataframes = list()
        all_devices["cve"] = False
        for vul in vuls:
            dict_for_df = {"version": [vul.version], "cves": [vul.cves[0].total_results]}
            cve_totals_df = pd.DataFrame.from_dict(dict_for_df)
            cve_dataframes.append(cve_totals_df)
            self.st.write(f"Total CVEs for Vendor: {vul.vendor}")
            self.st.write(cve_totals_df)
            self.st.write(vul.cves)

        for cve_dataframe in cve_dataframes:
            version_value = cve_dataframe["version"].values[0]
            cves_value = cve_dataframe["cves"].values[0]

            all_devices.loc[all_devices["version"] == version_value, "cve"] = cves_value

            for df in final_report_df:
                df.loc[df["version"] == version_value, "cve"] = cves_value

        # process device backup
        all_devices["backups"] = False
        flattened_configs = [config for configs in device_backup.values() for config in configs]
        backup_configs_df = pd.DataFrame([config.dict() for config in flattened_configs])
        all_devices["backups"] = all_devices["sn"].isin(backup_configs_df["sn"])
        for df in final_report_df:
            df["backups"] = df["sn"].isin(backup_configs_df["sn"])
        for idx, report in enumerate(final_report_df, start=1):
            self.st.write(f"# App Data {idx}")
            self.st.write(report)

        self.st.write("# All Devices")
        self.st.write(all_devices)
