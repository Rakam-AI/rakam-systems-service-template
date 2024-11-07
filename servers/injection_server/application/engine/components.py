from rakam_systems.system_manager import SystemManager
system_manager = SystemManager(system_config_path='system_config.yaml')

base_index_path = "data/vector_stores_for_test/example_baseIDXpath"
embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
from rakam_systems.components.data_processing.data_processor import DataProcessor
dataProcessor = DataProcessor(system_manager=system_manager)

from rakam_systems.components.vector_search.vs_manager import VSManager
vSManager = VSManager(system_manager=system_manager, base_index_path=base_index_path, embedding_model=embedding_model)

from rakam_systems.components.connectors.file_storage import S3FileManager
s3FileManager = S3FileManager(system_manager=system_manager, bucket_name='rakam-test-rs')
