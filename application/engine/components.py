from rakam_systems.system_manager import SystemManager

from rakam_systems.components.data_processing.data_processor import DataProcessor
from rakam_systems.components.vector_search.vector_store import VectorStore
from rakam_systems.components.vector_search.vs_manager import VSManager
from rakam_systems.components.rag.rag_generator import RAGGenerator

base_index_path="data/vector_stores_for_test/example_baseIDXpath"
embedding_model="sentence-transformers/all-MiniLM-L6-v2"

system_manager = SystemManager(system_config_path='system_config.yaml')

data_processor = DataProcessor(system_manager=system_manager)

vsManager = VSManager(base_index_path=base_index_path,embedding_model= embedding_model, system_manager=system_manager)
VS = VectorStore(base_index_path=base_index_path, embedding_model=embedding_model, system_manager=system_manager)

ragGenerator = RAGGenerator(model="gpt-4o-mini", system_manager=system_manager)