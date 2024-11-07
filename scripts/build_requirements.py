import os
import yaml

# Load the configuration from a YAML file
with open("components_config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Create a folder for requirements if it doesn't exist
os.makedirs("requirements", exist_ok=True)

# Create a requirements file for each server group
for group in config["ServerGroups"]:
    group_name = group["name"]
    components = group["components"]
    libraries = set()

    # Collect unique libraries from each component in the server group
    for component in components:
        component_libs = config.get(component, {}).get("libraries", [])
        libraries.update(component_libs)

    # Write the libraries to a requirements file
    file_path = os.path.join("requirements", f"{group_name}_requirements.txt")
    with open(file_path, "w") as f:
        f.write("\n".join(sorted(libraries)))

    print(f"Created {file_path} with {len(libraries)} libraries.")
