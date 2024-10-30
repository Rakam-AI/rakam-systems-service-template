from rakam_systems.system_manager import SystemManager

from rakam_systems.components.data_processing.data_processor import DataProcessor
from rakam_systems.components.vector_search.vector_store import VectorStore
from rakam_systems.components.vector_search.vs_manager import VSManager
from rakam_systems.components.generation.generation import Generator
from rakam_systems.components.rag_connectors.generation_feeder import GenerationFeeder

base_index_path="data/vector_stores_for_test/example_baseIDXpath"
system_manager = SystemManager(system_config='system_config.yaml')

data_processor = DataProcessor()
vsManager = VSManager(base_index_path=base_index_path,embedding_model= "sentence-transformers/all-MiniLM-L6-v2", system_manager=system_manager)
VS = VectorStore(base_index_path=base_index_path, embedding_model="sentence-transformers/all-MiniLM-L6-v2")
generator = Generator(model="gpt-4o-mini")
ragGen = GenerationFeeder(generator_model=generator, vs_manager=vsManager)

