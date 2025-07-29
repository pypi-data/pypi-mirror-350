import httpx
import streamlit as st
from ipfabric import IPFClient

DEFAULT_TIMEOUT = 60


def build_ipf_client(host: str, token: str, snapshot_id: str = None, timeout: int = DEFAULT_TIMEOUT):
    if not token:
        return None
    snapshot_id = snapshot_id or "$last"
    try:
        return IPFClient(base_url=host, auth=token, snapshot_id=snapshot_id, timeout=timeout, http2=False)
    except httpx.ConnectError as ssl_error:
        if "certificate verify failed" in str(ssl_error):
            return IPFClient(base_url=host, auth=token, snapshot_id=snapshot_id, verify=False, timeout=timeout, http2=False)
    except Exception as e:
        st.warning(f"Unable to initialize IP Fabric SDK Client: {e}")
    return None


def initialize_from_session_cookie():
    token = st.context.cookies.get("accessToken")
    host = st.context.headers.get("Origin")

    if not st.session_state.get("ipf_client"):
        st.warning(
            "To initialize the IP Fabric SDK Client, please log in to the IP Fabric platform. "
            "Authentication will be handled automatically using your session cookie."
        )

    client = build_ipf_client(host, token)
    if not client:
        return

    snapshots = [
        {
            "display_name": f"{snap.name} - {snap.snapshot_id}"
            if snap.name
            else snap.snapshot_id,
            "snapshot_id": snap.snapshot_id,
        }
        for snap in client.snapshots.values()
    ]

    seen = set()
    unique_snapshots = []
    for snap in snapshots:
        if snap["snapshot_id"] not in seen:
            seen.add(snap["snapshot_id"])
            unique_snapshots.append(snap)

    unique_snapshots = sorted(unique_snapshots, key=lambda x: x["display_name"])
    selected_display = st.sidebar.selectbox(
        "Select Snapshot",
        [s["display_name"] for s in unique_snapshots],
        index=0,
        key="snapshot_id",
    )
    selected_id = next(
        s["snapshot_id"]
        for s in unique_snapshots
        if s["display_name"] == selected_display
    )
    client.snapshot_id = selected_id
    st.session_state["ipf_client"] = client


def manual_ipf_client_form(default_timeout: int = DEFAULT_TIMEOUT):
    if "ipf_client" in st.session_state:
        st.sidebar.success("IP Fabric Client Initialized")
        if st.sidebar.button("Reinitialize IP Fabric Client"):
            del st.session_state["ipf_client"]
            st.sidebar.info("Client removed from session. Please refresh to reinitialize.")
            st.rerun()
        return

    st.sidebar.write("Fill out the form to initialize the IP Fabric Client")
    url = st.sidebar.text_input("IPF URL")
    token = st.sidebar.text_input("IPF Token", type="password")
    snapshot = st.sidebar.text_input("Snapshot", value="$last")
    timeout = st.sidebar.number_input("Timeout", value=default_timeout, min_value=1)
    verify = st.sidebar.checkbox("Verify SSL", value=True)

    if st.sidebar.button("Submit"):
        client = IPFClient(base_url=url, auth=token, snapshot_id=snapshot, timeout=timeout, verify=verify, http2=False)
        st.session_state["ipf_client"] = client
        st.sidebar.success("Client Initialized")
        st.rerun()


def get_ipf_client():
    return st.session_state.get("ipf_client")