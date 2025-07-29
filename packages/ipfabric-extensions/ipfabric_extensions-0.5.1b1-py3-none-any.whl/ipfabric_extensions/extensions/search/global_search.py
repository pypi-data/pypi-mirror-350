from ipfabric_extensions.extensions.base_extension import IPFExtension
from ipfabric.models.global_search import GlobalSearch, RANKED
import pandas as pd


class IPFGlobalSearch(IPFExtension):
    name: str = "IPF Global Search"
    version: str = "0.0.0a"
    icon = "🔍"

    def input_form(self):
        ipf_client = self.get_ipf_client()
        if not ipf_client:
            self.st.write("IP Fabric Client not initialized. Please initialize in side panel.")
            return
        results = None
        self.st.title("Global Search")
        with self.st.form(key="Global Search Args"):
            snapshot = self.st.text_input(label="IPF Snapshot UUID", value="$last")
            ipf_client._client.headers["user-agent"] += "; IPF Extensions Global Search"
            gs = GlobalSearch(client=ipf_client)
            address = self.st.text_input(label="IP or MAC Address to search")
            regex = self.st.text_input(label="Regex to use in search")
            if regex:
                search_type = self.st.multiselect(
                    label="Search Type",
                    options=["ipv4", "ipv6", "mac"],
                    default=["ipv4"],
                    max_selections=1,
                )
            full_scan = self.st.checkbox(label="Full Scan")
            break_on_match = self.st.checkbox(label="Break on Match?")
            submitted = self.st.form_submit_button("Run Global Search")
            if submitted:
                if regex:
                    results = gs.search_regex(
                        search_type=search_type[0],
                        address=regex,
                        full_scan=full_scan,
                        first_match=break_on_match,
                    )
                else:
                    results = gs.search(address=address, full_scan=full_scan, first_match=break_on_match)
        if results:
            self.display_global_search(results.values())

    def display_global_search(self, results):
        self.st.write("# Results of Global Search")
        for result in results:
            self.st.write(f"Menu: {result['menu']}")
            self.st.write(f"Path: {result['path']}")
            self.st.write(f"URL: {result['url']}")
            self.st.write(pd.DataFrame.from_records(result["data"]))
