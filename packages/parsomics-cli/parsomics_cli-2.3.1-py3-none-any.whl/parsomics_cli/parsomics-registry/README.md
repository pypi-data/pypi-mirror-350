# parsomics-registry

A plugin registry for parsomics.

## The plugins.json spec

The `plugins.json` lists all known parsomics plugins. The information for each plugin follows spec below:

- `name`: The name of the plugin
- `pypi_package`: The name of the plugin package in PyPI. Needs to start with "parsomics-plugin"
- `date_added`: ISO 8601 date string in UTC timezone. You can find it on [this website](https://www.utctime.net/)
- `official`: A boolean value indicating whether the plugin was developed by the parsomics team (`true`) or by a third party (`false`)
- `description`: A short description of what the plugin does
- `url`: A link to the plugin's repository or website
- `tool_url`: A link to the targeted tool's repository or website
- `license`: An [SPDX License String](https://spdx.org/licenses/) indicating the license of the plugin

Here's a complete example:

```json
{
    "name": "interpro",
    "pypi_package": "parsomics-plugin-interpro",
    "date_added": "2024-11-18T17:03:01Z",
    "official": true,
    "description": "Adds support for general protein annotations by InterPro",
    "url": "https://gitlab.com/parsomics/parsomics-plugin-interpro",
    "tool_url": "https://www.ebi.ac.uk/interpro/",
    "license": "GPL-3.0"
}
```

## How to update this repository

### Versioning

The `plugins.json` file uses semantic versioning. The major version should be increased when breaking changes are introduced, the minor version should be increased when new features are implemented, and the patch version should be increased when issues are fixed. Here is a rundown of each of those mean for this project:

Breaking changes:

- Adding fields in the plugin metadata
- Removing fields in the plugin metadata
- Renaming fields in the plugin metadata

Features:

- Adding new plugins to `plugins.json`

Fixes:

- Fixing typos in `plugins.json`

### Hashing

After making changes to the `plugins.json` file, run:

```bash
python hash.py
```

This will update the `plugins.json.hash` file, which contains a hash of the `plugins.json` file. The changes to both files should be included in the same commit.

### Signing

Every commit to this repository must be signed with a GPG key.

## License

Each plugin is licensed under their own terms. Check out their packages at the Python Package Index (PyPI) for more information on each of them. This repository itself is licensed under the terms of the GPLv3.
