from gemini_application.application_abstract import ApplicationAbstract
from gemini_model.chatassistant.rag import RAG, State
import os
import time
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import hub
from langchain_ollama.llms import OllamaLLM
from langchain_ollama import OllamaEmbeddings
import chromadb
from langgraph.graph import START, StateGraph
import ollama


class ChatPopup(ApplicationAbstract):
    def __init__(self):
        super().__init__()

        # Classes
        self.rag_model = RAG()
        self.llm_model = None
        self.docs = None
        self.embeddings_model = None
        self.graph = None
        self.retriever = None
        self.local_embeddings = None
        self.chroma_client = None
        self.chroma_collection = None

        # Variables
        self.langchain_api_key = None
        self.llm_model_verion = None
        self.prompt_type = None
        self.chunks = None
        self.docs_dir = None
        self.chroma_dir = None
        self.text_splitter = None
        self.graph_builder = None
        self.prompt = None
        self.chunk_size = None
        self.chunk_overlap = None
        self.add_start_index = None
        self.collection_name = None

    def init_parameters(self, **kwargs):
        """Function to initialize parameters"""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def initialize_model(self):
        # API key for accessing langchain model
        os.environ["LANGCHAIN_API_KEY"] = (
            self.langchain_api_key
        )

        # Http chromaDB storage, on Docker container
        self.chroma_client = chromadb.HttpClient(host="chromadb", port=8000)

        # Now create or retrieve the collection
        self.chroma_collection = self.chroma_client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

        self.llm_model = OllamaLLM(model=self.llm_model_verion)

        self.local_embeddings = OllamaEmbeddings(model=self.embeddings_model)

        self.prompt = hub.pull(self.prompt_type)

        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size,
                                                            chunk_overlap=self.chunk_overlap,
                                                            add_start_index=self.add_start_index)

    def retrieve(self, state: State):
        retrieved_docs = self.chroma_collection.query(query_texts=[state["question"]],
                                                      n_results=3)
        return {"context": retrieved_docs}

    def generate(self, state: State):
        docs_content = "\n\n".join(doc.page_content for doc in state["context"])

        results = self.prompt.invoke({"question": state["question"], "context": docs_content})

        response = self.llm_model.invoke(results)

        return {"answer": response}

    def update_data(self):
        # Load documents
        tic = time.time()
        # self.docs = self.rag_model.load_files(self.docs_dir)
        docs_data = self.rag_model.readfiles(self.docs_dir)
        toc = time.time()
        elapsed_time = toc - tic
        print(f"Model: Documents are loaded ({elapsed_time:.5f} s)")

        # Split documents
        tic = time.time()
        for filename, text in docs_data.items():
            chunks = self.rag_model.chunksplitter(text, self.chunk_size)
            embeds = self.rag_model.getembedding(chunks)
            chunknumber = list(range(len(chunks)))
            ids = [filename + str(index) for index in chunknumber]
            metadatas = [{"source": filename} for index in chunknumber]

            print(f"DEBUG: Using collection: {self.chroma_collection}")
            self.chroma_collection.add(
                ids=ids,
                documents=chunks,
                embeddings=embeds,
                metadatas=metadatas
            )
        toc = time.time()
        elapsed_time = toc - tic
        print(f"Model: Documents are split ({elapsed_time:.5f} s)")

        # Create graph
        tic = time.time()
        self.graph_builder = StateGraph(State).add_sequence([self.retrieve, self.generate])
        self.graph_builder.add_edge(START, "retrieve")

        self.graph = self.graph_builder.compile()
        toc = time.time()
        elapsed_time = toc - tic
        print(f"Model: Graph created ({elapsed_time:.5f} s)")

    def update_data2(self):
        # Step 1: Fetch existing metadata from the collection
        tic = time.time()
        existing_sources = set()
        all_metadata = self.chroma_collection.get(include=["metadatas"])

        if "metadatas" in all_metadata:
            for meta in all_metadata["metadatas"]:
                if meta and "source" in meta:
                    existing_sources.add(meta["source"])
        toc = time.time()
        elapsed_time = toc - tic
        print(f"Model: Fetched existing metadata from collection ({elapsed_time:.5f} s)")

        # Step 2: List all files and filter out existing ones
        all_files = [
            f for f in os.listdir(self.docs_dir)
            if os.path.isfile(os.path.join(self.docs_dir, f))
        ]
        new_files = [f for f in all_files if f not in existing_sources]
        print(f"Model: Found {len(new_files)} new files to process")

        # Step 3: Read only new files
        tic = time.time()
        docs_data = self.rag_model.readfiles(self.docs_dir, filenames=new_files)
        toc = time.time()
        elapsed_time = toc - tic
        print(f"Model: Documents read ({elapsed_time:.5f} s)")

        # Step 4: Process and add new files to ChromaDB
        tic = time.time()
        for filename, text in docs_data.items():
            chunks = self.rag_model.chunksplitter(text, self.chunk_size)
            embeds = self.rag_model.getembedding(chunks)
            ids = [f"{filename}_{i}" for i in range(len(chunks))]
            metadatas = [{"source": filename} for _ in range(len(chunks))]

            self.chroma_collection.add(
                ids=ids,
                documents=chunks,
                embeddings=embeds,
                metadatas=metadatas
            )
        toc = time.time()
        elapsed_time = toc - tic
        print(f"Model: New files processed ({elapsed_time:.5f} s)")

        # Step 5: Create graph
        tic = time.time()
        self.graph_builder = StateGraph(State).add_sequence([self.retrieve, self.generate])
        self.graph_builder.add_edge(START, "retrieve")

        self.graph = self.graph_builder.compile()
        toc = time.time()
        elapsed_time = toc - tic
        print(f"Model: Graph created ({elapsed_time:.5f} s)")

    def process_prompt(self, user_message):
        user_text = user_message.strip()

        response = self.graph.invoke({"question": user_text})

        # Process response to get sources and citations
        sources = [doc.metadata["source"] for doc in response["context"]]
        citations = [doc.page_content for doc in response["context"]]

        answer = (f'{response["answer"]}\n\nThis answer was generated'
                  f' from the following citations and sources:\n')
        counter = 1
        for so, ci in zip(sources, citations):
            answer += f"Citation {counter}: {ci} (taken from source: {so})\n"
            counter += 1
        return answer

    def process_prompt2(self, user_message):
        queryembed = ollama.embed(model="nomic-embed-text:latest", input=user_message)['embeddings']

        relateddocs = '\n\n'.join(self.chroma_collection.query(
            query_embeddings=queryembed,
            n_results=10)['documents'][0])
        prompt = (f"{user_message} - Answer that question"
                  f" using the following text as a resource: {relateddocs}")

        ragoutput = ollama.generate(model=self.llm_model_verion, prompt=prompt, stream=False)

        return ragoutput

    def process_prompt3(self, user_message):
        print("processing prompt...")

        # Get embedding of the user query
        tic = time.time()
        query_embed = ollama.embed(
            model="nomic-embed-text:latest",
            input=user_message)['embeddings']
        toc = time.time()
        print(f"Model: Embeddings retrieved from user query ({toc - tic:.5f} s)")

        # Retrieve relevant documents
        result = self.chroma_collection.query(
            query_embeddings=query_embed,
            n_results=5,
            include=["documents", "metadatas"]
        )

        documents = result["documents"][0]
        metadatas = result["metadatas"][0]

        # Build prompt
        related_text = "\n\n".join(documents)
        prompt = (f"{user_message}\n\nUse the following information to help"
                  f" answer the question:\n{related_text}")

        # Generate response
        tic = time.time()
        response = ollama.generate(model=self.llm_model_verion, prompt=prompt, stream=False)
        toc = time.time()
        print(f"Model: Ollama generated response ({toc - tic:.5f} s)")

        # Extract text from response
        response_text = response.model_dump().get("response", "")

        # Format shortened citations
        short_citations = []
        short_sources = []

        for i, meta in enumerate(metadatas):
            filename = meta.get("source", "unknown.txt")
            title = os.path.basename(filename)
            location = f"chunk {i + 1}"  # or use metadata['id'] if available
            short_citations.append(f"{title}, {location}")
            short_sources.append(filename)

        return {
            "answer": response_text,
            "citations": short_citations,
            "sources": short_sources
        }

    def calculate(self):
        return "Output calculated"
