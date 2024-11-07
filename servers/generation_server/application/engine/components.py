from rakam_systems.system_manager import SystemManager
system_manager = SystemManager(system_config_path='system_config.yaml')

from rakam_systems.components.connectors.LLMconnector import LLMManager
lLMManager = LLMManager(system_manager=system_manager, model='mistral-large-latest')

from rakam_systems.components.rag.rag_generator import RAGGenerator
rAGGenerator = RAGGenerator(system_manager=system_manager)

from rakam_systems.components.connectors.file_storage import S3FileManager
s3FileManager = S3FileManager(system_manager=system_manager, bucket_name='rakam-test-rs')
