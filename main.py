from agents import function_tool
from openai import OpenAI
client = OpenAI()

vector_store = client.vector_stores.create(        # Create vector store
    name="OpenSCAD Docs",
)

client.vector_stores.files.upload_and_poll(        # Upload file
    vector_store_id=vector_store.id,
    file=open("docs.md", "rb")
)

@function_tool
def search_docs(search_term: str="How to make a cube?" ):

    results = client.vector_stores.search(
        vector_store_id=vector_store.id,
        query=search_term,
    )

    return results

