import re
import streamlit as st
from importlib import import_module
from ipfabric_extensions.app_index.index import APP_STORE_INDEX
from ipfabric_extensions.extensions.base_extension import IPFExtension
from ipfabric_extensions.utils.ipf_client import initialize_from_session_cookie, manual_ipf_client_form

st.set_page_config(page_title="IP Fabric Extensions", page_icon=":electric_plug:", layout="centered")

initialize_from_session_cookie()
manual_ipf_client_form()

def is_remote_extension_installed(ipf, name: str) -> bool:
    if ipf is not None:
        try:
            ipf.extensions.extension_by_name(name)
            return True
        except ValueError:
            return False
        except Exception as e:
            st.error(f"Failed to check extension '{name}': {e}")
            return False

ipf = st.session_state.get("ipf_client")
if not ipf:
    st.warning("Please initialize the IP Fabric Client using the sidebar to install extensions.")

# Sidebar navigation config
pages_dict = {
    "Extensions Home": [
        st.Page(lambda: build_home_page(), title="Home - View Available Extensions", icon="🏠"),
    ],
    "Installed Extensions": [],
    "Base Extension": [
        st.Page(IPFExtension, title="Base Extension", icon="⚙️"),
    ],
}

for ext_id, ext_meta in APP_STORE_INDEX.items():
    if "class_path" in ext_meta:
        try:
            mod_path, class_name = ext_meta["class_path"].split(":")
            module = import_module(mod_path)
            extension_class = getattr(module, class_name)
            page_obj = st.Page(
                extension_class,
                title=ext_meta["name"],
                icon=ext_meta.get("icon", "🧩"),
            )
            pages_dict["Installed Extensions"].append(page_obj)
        except Exception as e:
            st.warning(f"Failed to load local extension {ext_meta['name']}: {e}")

def build_home_page():
    st.markdown("# IP Fabric Plugin Home Page")
    st.markdown("Browse available extensions. Local extensions are preinstalled; remote extensions can be installed below. "
                "The IP Fabric Client must be initialized to install extensions."
                )

    st.markdown("### 📦 Installed Extensions")
    for ext_id, ext_meta in APP_STORE_INDEX.items():
        if "class_path" in ext_meta:
            col1, col2 = st.columns([0.05, 0.9])
            with col1:
                st.markdown(ext_meta["icon"])
            with col2:
                st.markdown(f"**{ext_meta['name']}**")
                st.caption(ext_meta["description"])
                st.success("🧩 This extension is ready in the sidebar.")

    st.divider()

    st.markdown("### 🌐 Available Remote Extensions")
    for ext_id, ext_meta in APP_STORE_INDEX.items():
        if "git_url" not in ext_meta:
            continue  # Skip non-remote extensions

        col1, col2 = st.columns([0.05, 0.9])
        with col1:
            st.markdown(ext_meta["icon"])
        with col2:
            st.markdown(f"**{ext_meta['name']}**")
            st.caption(ext_meta["description"])

            already_installed = is_remote_extension_installed(ipf, ext_meta["name"])
            if ipf is None:
                st.warning("Please initialize the IP Fabric Client using the sidebar to install  or view this extension.")
                continue
            ipf_url = re.sub(r"/api/v\d+\.\d+/?$", "/", str(ipf.base_url))
            extension_url = f"{ipf_url}extensions-apps/{ext_meta['slug']}"

            if already_installed:
                st.success("✅ Already installed")
                st.page_link(extension_url, label="Launch Extension")
            else:
                if st.button(f"Install {ext_meta['name']}", key=f"install-{ext_id}"):
                    with st.spinner("Installing... Please do not close the page."):
                        try:
                            ipf.extensions.register_from_git_url(
                                git_url=ext_meta["git_url"],
                                name=ext_meta["name"],
                                slug=ext_meta["slug"],
                                description=ext_meta["description"],
                                cpu=ext_meta.get("cpu", 1),
                                memory=ext_meta.get("memory", 512),
                            )
                            st.success("✅ Installed successfully")
                            st.page_link(extension_url, label="Launch Extension")
                        except Exception as e:
                            st.error(f"Install failed: {e}")
# Run navigation
pages = st.navigation(pages_dict)
pages.run()