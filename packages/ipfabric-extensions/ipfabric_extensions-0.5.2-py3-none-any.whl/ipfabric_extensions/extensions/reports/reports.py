import os
from os import listdir
from os.path import isfile, join

import pandas as pd
from ipfabric_extensions.extensions.base_extension import IPFExtension
from ipfabric_reports import IPFabricReportGenerator
from ipfabric_reports.report_registry import ReportRegistry


class IPFReport(IPFExtension):
    name: str = "IPF Report"
    version: str = "0.0.0a"
    report_generator: IPFabricReportGenerator = IPFabricReportGenerator
    icon = "📤"

    def __init__(self):
        super().__init__()

    def input_form(self):
        self.ensure_export_dir()
        ipf_client = self.get_ipf_client()
        if ipf_client:
            self.st.write(
                """
                # IP Fabric Report
                This extension allows you to generate reports from the IP Fabric API.
                You can customize the report by providing a custom css file.
                \n
                The following reports are available: \n
                """
            )

            report_options = ReportRegistry.list_reports()
            for report, report_info in report_options.items():
                self.st.write(f"##### {report.upper()}\n" f"{report_info}")
            report_type = self.st.selectbox("Select Report", report_options)
            snapshot = self.st.text_input("Snapshot ID", value=ipf_client.snapshot_id)
            os.environ["REPORT_TYPE"] = report_type
            self.st.write(f"{report_type} selected")
            self.st.write("Please provide the following information to generate the report.")
            if not ipf_client:
                self.st.write("IP Fabric Client not initialized. Please initialize in the sidebar.")
                return
            with self.st.form(key="Report Form"):
                nvd_api_key = os.environ.get("NVD_API_KEY")
                site_filter = self.st.text_input("Site Filter", value="")
                report_style = self.st.text_input("Report Style", value="default_style.css")
                if report_type == "cve" and not nvd_api_key:
                    nvd_api_key = self.st.text_input("NVD API Key", value="")
                    self.st.warning("NVD API Key is required for CVE report.")
                elif report_style == "cve" and not site_filter:
                    self.st.warning("Site Filter is required for CVE report.")

                submit = self.st.form_submit_button("Generate Report")
                if submit:
                    if ipf_client:
                        if snapshot != ipf_client.snapshot_id:
                            ipf_client.snapshot_id = snapshot
                        self.get_report(
                            ipf_client,
                            snapshot_id=snapshot,
                            site_filter=site_filter,
                            report_style=report_style,
                            nvd_api_key=nvd_api_key,
                        )
                    else:
                        self.st.write("IP Fabric Client not initialized. Please initialize in the sidebar.")
            self.display_file()

    @staticmethod
    def get_report(ipf_client, snapshot_id="$last", site_filter=None, report_style=None, nvd_api_key=None):
        os.environ["IPF_SNAPSHOT_ID"] = snapshot_id
        os.environ["REPORT_SITE"] = site_filter
        os.environ["REPORT_STYLE"] = report_style
        if nvd_api_key:
            os.environ["NVD_API_KEY"] = nvd_api_key

        report_generator = IPFabricReportGenerator(
            ipf_client=ipf_client,
            snapshot_id=snapshot_id,
            site_filter=site_filter,
            report_type=os.environ["REPORT_TYPE"],
            report_style=report_style,
            nvd_api_key=nvd_api_key,
        )

        report_generator.generate_report()

    def display_file(self):
        mypath = os.path.join(os.getcwd(), "export")
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        self.st.write("Please select the report file to download. or view")
        report_file = self.st.selectbox("Select Report File", onlyfiles)
        if onlyfiles:
            # if self.st.button("View Report"):
            if report_file.endswith(".html"):
                with open(os.path.join(mypath, report_file), "r") as f:
                    self.st.html(f.read())
            elif report_file.endswith(".xlsx"):
                df = pd.read_excel(os.path.join(mypath, report_file))
                self.st.dataframe(df)
            elif report_file.endswith(".csv"):
                df = pd.read_csv(os.path.join(mypath, report_file))
                self.st.dataframe(df)
            else:
                self.st.write("Only HTML, XLSX*, CSV files can be viewed.\n\n")
            with open(os.path.join(mypath, report_file), "rb") as f:
                # self.st.download_button(label="Download Report", data=f, file_name=report_file, )
                col1, col2 = self.st.columns(2)
                with col1:
                    self.st.download_button(label="Download Report", data=f, file_name=report_file)
                with col2:
                    if self.st.button(
                        "DELETE REPORT",
                    ):
                        try:
                            os.remove(os.path.join(mypath, report_file))
                            self.st.success("Report deleted successfully!")
                        except FileNotFoundError:
                            self.st.error("Report not found!")
                        except Exception as e:
                            self.st.error(f"Error deleting report: {str(e)}")

        else:
            self.st.write("No files to display.")

    @staticmethod
    def ensure_export_dir():
        if not os.path.exists("export"):
            os.makedirs("export")
