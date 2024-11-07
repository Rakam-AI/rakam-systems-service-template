import yaml
import sys
from pathlib import Path
import argparse

def parse_parameters(parameters):
    """Generate parameter strings for Django path() arguments."""
    param_strings = []
    for param, details in parameters.items():
        param_string = f"{param}=" + (
            f"str(request.query_params.get('{param}', '{details.get('default', '')}'))" 
            if not details['required'] else f"request.query_params['{param}']"
        )
        param_strings.append(param_string)
    return ', '.join(param_strings)

def generate_urls(components):
    """Generate urls.py content based on component configuration."""
    urls_content = "from django.urls import path\nfrom . import views\n\n\nurlpatterns = [\n"

    for component in components:
        for comp_name, methods in component.items():
            for method_name, method_details in methods.items():
                path_str = f"    path('{method_details['path']}', views.{method_name}, name='{method_name}'),\n"
                urls_content += path_str

    urls_content += "]\n"
    return urls_content

def generate_views(components):
    """Generate views.py content based on component configuration."""
    views_content = "from rest_framework.decorators import api_view\nfrom rest_framework.response import Response\nfrom .serializers import *\n\n"

    for component in components:
        for comp_name, methods in component.items():
            for method_name, method_details in methods.items():
                parameters = parse_parameters(method_details['parameters'])
                view_str = (
                    f"@api_view(['GET'])\n"
                    f"def {method_name}(request):\n"
                    f"    serializer = {comp_name}{method_name.replace('_', '').capitalize()}Serializer(data=request.query_params)\n"
                    f"    serializer.is_valid(raise_exception=True)\n"
                    f"    {parameters}\n"
                    f"    return Response({{'status': 'success', 'data': 'Your data here'}})\n\n"
                )
                views_content += view_str
    return views_content

def generate_serializers(components):
    """Generate serializers.py content based on component configuration."""
    serializers_content = "from rest_framework import serializers\n\n"

    for component in components:
        for comp_name, methods in component.items():
            for method_name, details in methods.items():
                # Serializer class name based on component and method
                class_name = f"{comp_name}{method_name.replace('_', '').capitalize()}Serializer"
                
                # Write the class definition
                serializers_content += f"class {class_name}(serializers.Serializer):\n"
                
                # Parameters for the serializer
                parameters = details.get("parameters", {})
                for param_name, param_details in parameters.items():
                    required = param_details.get("required", False)
                    max_length = param_details.get("max_length", 128)
                    default = param_details.get("default", None)
                    
                    # Write the field definition
                    if default is not None:
                        serializers_content += f"    {param_name} = serializers.CharField(required={required}, max_length={max_length}, default={default!r})\n"
                    else:
                        serializers_content += f"    {param_name} = serializers.CharField(required={required}, max_length={max_length})\n"
                
                # Add a newline after each class
                serializers_content += "\n"
    return serializers_content

def generate_files_for_group(server_group):
    # Load the YAML file
    with open("system_config.yaml", "r") as file:
        config = yaml.safe_load(file)

    server_groups = config.get("ServerGroups", [])
    
    # Find the specified server group
    group_config = next((group for group in server_groups if group['name'] == server_group), None)

    if group_config is None:
        print(f"Server group '{server_group}' not found in system_config.yaml.")
        sys.exit(1)

    components = group_config.get("components", [])

    # Generate and save urls.py content
    urls_content = generate_urls(components)
    Path("urls.py").write_text(urls_content)
    print(f"urls.py generated successfully for {server_group}.")

    # Generate and save views.py content
    views_content = generate_views(components)
    Path("views.py").write_text(views_content)
    print(f"views.py generated successfully for {server_group}.")

    # Generate and save serializers.py content
    serializers_content = generate_serializers(components)
    Path("serializers.py").write_text(serializers_content)
    print(f"serializers.py generated successfully for {server_group}.")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Generate urls, views, and serializers for a specified server group.")
    parser.add_argument("server_group", type=str, help="The name of the server group to generate files for.")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Run the function with the provided server group name
    generate_files_for_group(args.server_group)
