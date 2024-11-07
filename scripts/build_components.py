import yaml
import sys

def generate_script_for_server_group(server_group: str, yaml_path: str = "components_config.yaml", output_path: str = "generated_components.py"):
    # Load YAML configuration
    with open(yaml_path, "r") as file:
        config = yaml.safe_load(file)

    # Retrieve components in the specified server group
    server_group_config = next((group for group in config["ServerGroups"] if group["name"] == server_group), None)
    if not server_group_config:
        raise ValueError(f"Server group '{server_group}' not found in configuration.")

    server_group_components = server_group_config["components"]

    # Track components to avoid duplicate imports and instantiations
    added_components = set()
    content = []

    # Ensure SystemManager is added if required by any component
    system_manager_def = config.get("SystemManager")
    if "SystemManager" in server_group_components and system_manager_def:
        content.append(system_manager_def["import_path"])
        content.append("system_manager = SystemManager(system_config_path='system_config.yaml')\n")
        added_components.add("SystemManager")

    # Define base paths and parameters for VSManager and VectorStore if present
    base_index_path = None
    embedding_model = None
    if "VSManager" in server_group_components or "VectorStore" in server_group_components:
        vs_manager_params = config["VSManager"]["parameters"]
        base_index_path = next((param["base_index_path"] for param in vs_manager_params if "base_index_path" in param), None)
        embedding_model = next((param["embedding_model"] for param in vs_manager_params if "embedding_model" in param), None)
        if base_index_path:
            content.append(f'base_index_path = "{base_index_path}"')
        if embedding_model:
            content.append(f'embedding_model = "{embedding_model}"')

    # Generate imports and instances for each component
    for component_name in server_group_components:
        if component_name in added_components:
            continue
        component_config = config.get(component_name)
        if not component_config:
            print(f"Warning: '{component_name}' not defined in YAML.")
            continue

        # Import statement
        content.append(component_config["import_path"])

        # Parameters for instance creation
        parameters = []
        for param in component_config["parameters"]:
            for key, value in param.items():
                if key == "system_manager":
                    parameters.append(f"{key}=system_manager")
                elif key == "base_index_path" and base_index_path:
                    parameters.append(f"{key}=base_index_path")
                elif key == "embedding_model" and embedding_model:
                    parameters.append(f"{key}=embedding_model")
                else:
                    parameters.append(f"{key}='{value}'" if isinstance(value, str) else f"{key}={value}")

        # Instance creation with consistent variable naming
        instance_name = component_name[0].lower() + component_name[1:]
        params_str = ", ".join(parameters)
        content.append(f"{instance_name} = {component_name}({params_str})\n")
        added_components.add(component_name)

    # Join all lines and save to output file
    with open(output_path, "w") as file:
        file.write("\n".join(content))

    print(f"{output_path} file has been created successfully for the '{server_group}' server group.")

# If script is run directly, get the server_group from the command line
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_script.py <server_group>")
        sys.exit(1)
    
    server_group = sys.argv[1]
    generate_script_for_server_group(server_group)
