import csv
import os
from io import StringIO
import json
import yaml

from ipfabric_infoblox.cli import validate_and_sync_infoblox

try:
    import streamlit as st
except ImportError:
    raise ImportError("Please install streamlit with `pip install ipfabric-infoblox[streamlit]`")

CSV_MIME = "text/csv"
JSON_MIME = "application/json"

st.set_page_config(page_title="Infoblox Sync Tool", layout="wide")
st.title("Infoblox Sync Tool")
st.write(
    """
    This tool helps validate and synchronize your IP Fabric and Infoblox network configurations.

    **Instructions:**
    - Upload a **YAML configuration file**.
    - Enter your **IP Fabric** and **Infoblox credentials**.
    - Use the **Enable Sync** option to push changes from IP Fabric to Infoblox.
    - Use the **Download Logs** option to retrieve a JSON log of all sync actions.

    **Note:**  
    - The **Enable Sync** option is **unchecked by default** to allow a dry run (no changes made).  
    - To perform an actual sync, **check the box** before running the process.
    """
)



EXAMPLE_YAML = """\
---
networkViews:
  - name: VPN
    create_containerless_nets: true
    split_networks: true
    smallest_v4_subnet: 32
    include:
      vrfs:
        - value: "VPN-.*"
          regex: true
  - name: Private
    split_networks: true
    include:
      networks:
        - RFC1918
    exclude:
      sites: &cloud
        - value: "(AWS|GCP|AZURE).*"
          regex: true
  - name: Private Cloud
    split_networks: true
    smallest_v4_subnet: 31
    include:
      sites: *cloud
      networks:
        - RFC1918
  - name: Public Cloud
    create_containerless_nets: true
    split_networks: true
    smallest_v4_subnet: 32
    include:
      sites: *cloud
    exclude:
      networks:
        - RFC1918
  - name: Public
    default: true
    create_containerless_nets: true
    split_networks: true
    smallest_v4_subnet: 32
    exclude:
      sites: *cloud
      networks:
        - RFC1918

ipfabric:
  vrf_mapping:
    'default':
      names:
        - ''
infoblox:
  import_timeout: 10
  import_retry: 20
  discovery_timeout: 10
  discovery_retry: 20
"""

input_method = st.radio("Choose input method:", ("Upload valid yaml config file", "Enter yaml manually"))

yaml_file = None
yaml_text = None
parsed_yaml = None
st.write(input_method)

if input_method == "Upload valid yaml config file":
    yaml_file = st.file_uploader("Upload Configuration yaml File", type=["yaml", "yml"])
    if yaml_file:
        parsed_yaml = yaml.safe_load(yaml_file)
else:
    with st.expander("Example yaml"):
        st.code(EXAMPLE_YAML, language="yaml")
    yaml_text = st.text_area("Enter yaml configuration manually", height=400, placeholder=EXAMPLE_YAML)
    if yaml_text:
        try:
            parsed_yaml = yaml.safe_load(yaml_text)
        except yaml.YAMLError as e:
            st.error(f"Invalid yaml: {e}")


ipfabric_url = st.text_input("IP Fabric URL", value="")
ipfabric_token = st.text_input("IP Fabric Token", value="", type="password")
ipfabric_snapshot = st.text_input("IP Fabric Snapshot", value="$last")
ipfabric_verify_ssl = st.checkbox("Verify IP Fabric SSL")
infoblox_host = st.text_input("Infoblox Host", value="")
infoblox_username = st.text_input("Infoblox Username", value="", type="default")
infoblox_password = st.text_input("Infoblox Password", value="", type="password")
infoblox_verify_ssl = st.checkbox("Verify Infoblox SSL")

os.environ["IPF_URL"] = ipfabric_url
os.environ["IPF_TOKEN"] = ipfabric_token
os.environ["IPF_VERIFY"] = str(ipfabric_verify_ssl)
os.environ["IPF_SNAPSHOT"] = ipfabric_snapshot
os.environ["IB_HOST"] = infoblox_host
os.environ["IB_USERNAME"] = infoblox_username
os.environ["IB_PASSWORD"] = infoblox_password
os.environ["IB_VERIFY_SSL"] = str(infoblox_verify_ssl)

logging = st.checkbox("Download Logs")
sync = st.checkbox("Enable Sync - **(Uncheck for Dry Run)**")


def generate_csv(data, fieldnames):
    """Generates a CSV string from data."""
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()

net_validation, managed_ip_validation = None, None
if st.button("Start Process"):
    if not yaml_file:
        st.error("Please upload a configuration YAML file.")
    elif not ipfabric_url or not infoblox_host or not infoblox_username or not infoblox_password:
        st.error("Please provide all required credentials.")
    elif (not logging and not sync) or (not logging and sync):
        net_validation, managed_ip_validation = validate_and_sync_infoblox(yaml_file, logging=logging, sync=sync)
        st.success("Process completed successfully!")
    elif logging and sync:
        net_validation, managed_ip_validation, sync_log = validate_and_sync_infoblox(yaml_file, logging=logging, sync=sync)
        with st.expander("Sync Log"):
            st.download_button(
                label="Download Sync Log as JSON",
                data=json.dumps(sync_log),
                file_name="sync_log.json",
                mime=JSON_MIME,
            )
        st.success("Process completed successfully!")

    st.subheader("Network Validation")
    if net_validation is None or managed_ip_validation is None:
        st.error("No network validation data available.")
        st.stop()
    if net_validation.create_networks:
        with st.expander("Networks to Create"):
            create_networks_data = [
                {
                    "Network": log.network,
                    "View": log.network_view,
                    "Status": log.status,
                }
                for log in net_validation.create_networks
            ]
            st.table(create_networks_data)
            csv_data = generate_csv(create_networks_data, fieldnames=["Network", "View", "Status"])
            st.download_button(
                label="Download Networks to Create as CSV",
                data=csv_data,
                file_name="networks_to_create.csv",
                mime=CSV_MIME,
            )
    else:
        st.write("No networks to create.")
    if net_validation.matched_networks:
        with st.expander("Matched Networks"):
            matched_networks_data = [
                {
                    "Network": log.network,
                    "View": log.network_view,
                    "Status": log.status,
                }
                for log in net_validation.matched_networks
            ]
            st.table(matched_networks_data)
            csv_data = generate_csv(matched_networks_data, fieldnames=["Network", "View", "Status"])
            st.download_button(
                label="Download Matched Networks as CSV",
                data=csv_data,
                file_name="matched_networks.csv",
                mime=CSV_MIME,
            )
    else:
        st.write("No matched networks.")
    if net_validation.logs:
        with st.expander("All Logs"):
            all_logs_data = [
                {
                    "Network": log.network,
                    "View": log.network_view,
                    "Status": log.status,
                    "Skip Reason": log.skip_reason,
                    "Failure": log.failure,
                }
                for log in net_validation.logs
            ]
            st.table(all_logs_data)
            csv_data = generate_csv(
                all_logs_data,
                fieldnames=["Network", "View", "Status", "Skip Reason", "Failure"],
            )
            st.download_button(
                label="Download All Logs as CSV",
                data=csv_data,
                file_name="all_logs.csv",
                mime=CSV_MIME,
            )

    st.subheader("Managed IP Validation")
    if managed_ip_validation.validated_ips:
        with st.expander("Validated IPs"):
            for view, ips in managed_ip_validation.validated_ips.items():
                st.write(f"View: {view}")
                validated_ips_data = [
                    {
                        "IP": str(ip.ip_address),
                        "VRF": ip.vrf_name,
                        "Device": ip.network_component_name,
                        "Interface": ip.network_component_port_name,
                    }
                    for ip in ips
                ]
                st.table(validated_ips_data)
                csv_data = generate_csv(
                    validated_ips_data,
                    fieldnames=["IP", "VRF", "Device", "Interface"],
                )
                st.download_button(
                    label=f"Download Validated IPs for {view} as CSV",
                    data=csv_data,
                    file_name=f"validated_ips_{view}.csv",
                    mime=CSV_MIME,
                )
    else:
        st.write("No validated IPs found.")
