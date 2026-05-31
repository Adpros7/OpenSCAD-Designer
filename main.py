import asyncio
import subprocess

from agents import (
    Agent,
    Runner,
    WebSearchTool,
    enable_verbose_stdout_logging,
    function_tool,
)
from openai import OpenAI

client = OpenAI()

vector_store = client.vector_stores.create(  # Create vector store
    name="OpenSCAD Docs",
)

client.vector_stores.files.upload_and_poll(  # Upload file
    vector_store_id=vector_store.id, file=open("docs.md", "rb")
)


@function_tool
def search_docs(search_term: str = "How to make a cube"):

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


@function_tool
def make_stl(output_file_with_extension: str, input_file_with_extension: str):
    r = subprocess.run(
        ["openscad", "-o", output_file_with_extension, input_file_with_extension],
        stdout=subprocess.PIPE,
    )
    print(r.stdout)
    return r.stdout


generate_parts = Agent(
    "Generate-parts",
    "Use this when u want to generate a new high detail part",
    [search_docs, WebSearchTool()],
    instructions="You are a expert detailer who specializes in making OpenScad parts. you are a part of a whole. use the docs and the web to help you. make no no misakes. be very detailed. be very realistic. o genric rounded corner, i want every detail to amaze the user. return OpenSCAD code",
)


instruction = """ You are a master OpenSCAD designer who uses programming to create stunning 3d models
Use web search to find anything not in docs
Use search_docs to find things in the docs. It is Semantic Search
use write_file to make the file with all of your .scad code
and use make_stl to output a stl
Work until the model works
Output a stl unless the user specifies otherwise
Unless otherwise specified, create the most high-detailed, amzing, superb model the world has ever seen, it should haave insasenley good detailing, down to the little nooks and crannies
It should also be really big so you can put details on it unless otherwise specified
"""

enable_verbose_stdout_logging()
agent = Agent(
    "OpenSCAD-Designer",
    tools=[
        search_docs,
        WebSearchTool(),
        write_file,
        make_stl,
        generate_parts.as_tool(
            "GenerateParts",
            "Use when u want to generate highly realistic or detailed parts",
        ),
    ],
    instructions=instruction,
)


async def main():
    result = await Runner.run(
        agent,
        input(),
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
