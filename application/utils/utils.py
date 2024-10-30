import yaml

CONFIG_PATH = 'system_config.yaml'

def get_component_url(component_name, config_path = CONFIG_PATH):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config["components"].get(component_name, {}).get("url")

if __name__ == "__main__":
    import requests
    from utils import get_component_url

    def call_vector_store(query, collection_name="base"):
        vector_store_url = get_component_url("VectorStore")
        response = requests.post(
            vector_store_url,
            json={"query": query, "collection_name": collection_name}
        )
        return response.json()

    print(call_vector_store("What is attention?"))
    