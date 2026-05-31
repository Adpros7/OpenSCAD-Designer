import asyncio
import subprocess

from agents import Agent, Runner, WebSearchTool, function_tool
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
def search_docs(search_term: str="How to make a cube" ):

    results = client.vector_stores.search(
        vector_store_id=vector_store.id,
        query=search_term,
    )
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
    
@function_tool
def make_stl(output_file_with_extension: str, input_file_with_extension: str):
    subprocess.Popen(f"openscad -o {output_file_with_extension} {input_file_with_extension}")


instruction = """ You are a master OpenSCAD designer who uses programming to create stunning 3d models
Use web search to find anything not in docs
Use search_docs to find things in the docs. It is Semantic Search
use write_file to make the file with all of your .scad code
and use make_stl to output a stl
"""
agent = Agent("OpenSCAD-Designer",
              tools=[search_docs, WebSearchTool(), write_file , make_stl],
              instructions=instruction
              )

async def main():
    result = await Runner.run(agent, "output a stl of a simple cube")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())