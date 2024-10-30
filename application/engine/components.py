from rakam_systems.components.data_processing.data_processor import DataProcessor
from rakam_systems.components.vector_search.vector_store import VectorStore
from rakam_systems.components.vector_search.vs_manager import VSManager
from rakam_systems.components.generation.generation import Generator
from rakam_systems.components.rag_connectors.generation_feeder import GenerationFeeder

data_processor = DataProcessor()
VS = VectorStore(base_index_path="data/vector_stores_for_test/example_baseIDXpath", embedding_model="sentence-transformers/all-MiniLM-L6-v2")
vsManager = VSManager(vector_store=VS,data_processor=data_processor)
generator = Generator(model="gpt-4o-mini")
ragGen = GenerationFeeder(generator_model=generator, vs_manager=vsManager)

