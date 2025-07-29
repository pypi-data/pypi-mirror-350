# IP Fabric Extensions 

## IP Fabric

[IP Fabric](https://ipfabric.io) is a vendor-neutral network assurance platform that automates the 
holistic discovery, verification, visualization, and documentation of 
large-scale enterprise networks, reducing the associated costs and required 
resources whilst improving security and efficiency.

It supports your engineering and operations teams, underpinning migration and 
transformation projects. IP Fabric will revolutionize how you approach network 
visibility and assurance, security assurance, automation, multi-cloud 
networking, and trouble resolution.

**Integrations or scripts should not be installed directly on the IP Fabric VM unless directly communicated from the
IP Fabric Support or Solution Architect teams.  Any action on the Command-Line Interface (CLI) using the root, osadmin,
or autoboss account may cause irreversible, detrimental changes to the product and can render the system unusable.**

## Project Description

This project is a collection of officially supported IP Fabric extensions.  These extensions are designed to provide 
features and functionality that are not available in the core IP Fabric product. Or Functionality that may not be suited
for the core IP Fabric product. These extensions are supported by the IP Fabric team and are designed to be installed 
using the IP Fabric Extension Endpoints.

## Installation

Pull the docker image from this repository. The docker image will contain the extension and all necessary dependencies.


## Configuration

<Configuration Information>

## Usage

```bash
docker run -d -p 8501:8501 --name ipf-extensions ipfabric/ipf-extensions:latest`
```

## Support

TODO: How to open issue in Gitlab, some base information around it, etc.

## Contributing

To contribute to this project, please see the [CONTRIBUTING.md](docs/CONTRIBUTING.md) file.
