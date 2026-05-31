from agents import Agent, WebSearchTool, function_tool
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
def search_docs(search_term: str="How to download from the cli" ):

    results = client.vector_stores.search(
        vector_store_id=vector_store.id,
        query=search_term,
    )
    print(results)
    return results

@function_tool
def write_file(filenameWithExtension: str, content: str):
    try:
        with open(filenameWithExtension, "r"):
            pass

        return "File Already Exists"
    
    except FileNotFoundError:
        with open(filenameWithExtension, "w", encoding="utf-8") as f:
            f.write(content)
        
        return f"Wrote {content} to {filenameWithExtension}"
    


agent = Agent("OpenSCAD-Designer",
              tools=[search_docs, WebSearchTool(), write_file]) 