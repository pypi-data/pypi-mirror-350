import asyncio

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio

from playwright_server_custom.tools import browser_click, browser_click_text, browser_evaluate, browser_fill, browser_hover, browser_hover_text, browser_navigate, browser_screenshot, browser_select, browser_select_text, get_dom, tools, tool_names



# Store notes as a simple key-value dict to demonstrate state management
notes: dict[str, str] = {}

server = Server("playwright-server")

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """
    List available note resources.
    Each note is exposed as a resource with a custom note:// URI scheme.
    """
    return [
        types.Resource(
            uri=AnyUrl(f"note://internal/{name}"),
            name=f"Note: {name}",
            description=f"A simple note named {name}",
            mimeType="text/plain",
        )
        for name in notes
    ]

@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """
    Read a specific note's content by its URI.
    The note name is extracted from the URI host component.
    """
    if uri.scheme != "note":
        raise ValueError(f"Unsupported URI scheme: {uri.scheme}")

    name = uri.path
    if name is not None:
        name = name.lstrip("/")
        return notes[name]
    raise ValueError(f"Note not found: {name}")

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """
    List available prompts.
    Each prompt can have optional arguments to customize its behavior.
    """
    return [
        types.Prompt(
            name="summarize-notes",
            description="Creates a summary of all notes",
            arguments=[
                types.PromptArgument(
                    name="style",
                    description="Style of the summary (brief/detailed)",
                    required=False,
                )
            ],
        )
    ]

@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    """
    Generate a prompt by combining arguments with server state.
    The prompt includes all current notes and can be customized via arguments.
    """
    if name != "summarize-notes":
        raise ValueError(f"Unknown prompt: {name}")

    style = (arguments or {}).get("style", "brief")
    detail_prompt = " Give extensive details." if style == "detailed" else ""

    return types.GetPromptResult(
        description="Summarize the current notes",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=f"Here are the current notes to summarize:{detail_prompt}\n\n"
                    + "\n".join(
                        f"- {name}: {content}"
                        for name, content in notes.items()
                    ),
                ),
            )
        ],
    )

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    print(f'tools: {tools}')
    return tools

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    Tools can modify server state and notify clients of changes.
    """
    if name not in tool_names:
        raise ValueError(f"Unknown tool: {name}")
        
    if not arguments:
        raise ValueError("Missing arguments")

    if name == "get-dom":
        url = arguments.get("url")
        dom = await get_dom(url)
        return [
            types.TextContent(
                type="text",
                text=f"DOM : {dom}",
            )
        ]
    
    elif name == "browser_navigate":
        url = arguments.get("url")
        result = await browser_navigate(url)
        return [
            types.TextContent(
                type="text",
                text=f"Navigated to: {url}",
            )
        ]
    
    elif name == "browser_screenshot":
        name = arguments.get("name")
        selector = arguments.get("selector")
        fullPage = arguments.get("fullPage", False)
        result = await browser_screenshot(name, selector, fullPage)
        return [
            types.ImageContent(
                type="image",
                image_url=result["screenshot"],
                description=f"Screenshot: {name}",
            )
        ]
    
    elif name == "browser_click":
        selector = arguments.get("selector")
        result = await browser_click(selector)
        return [
            types.TextContent(
                type="text",
                text=f"Clicked element with selector: {selector}",
            )
        ]
    
    elif name == "browser_click_text":
        text = arguments.get("text")
        result = await browser_click_text(text)
        return [
            types.TextContent(
                type="text",
                text=f"Clicked element with text: {text}",
            )
        ]
    
    elif name == "browser_hover":
        selector = arguments.get("selector")
        result = await browser_hover(selector)
        return [
            types.TextContent(
                type="text",
                text=f"Hovered over element with selector: {selector}",
            )
        ]
    
    elif name == "browser_hover_text":
        text = arguments.get("text")
        result = await browser_hover_text(text)
        return [
            types.TextContent(
                type="text",
                text=f"Hovered over element with text: {text}",
            )
        ]
    
    elif name == "browser_fill":
        selector = arguments.get("selector")
        value = arguments.get("value")
        result = await browser_fill(selector, value)
        return [
            types.TextContent(
                type="text",
                text=f"Filled {selector} with value: {value}",
            )
        ]
    
    elif name == "browser_select":
        selector = arguments.get("selector")
        value = arguments.get("value")
        result = await browser_select(selector, value)
        return [
            types.TextContent(
                type="text",
                text=f"Selected option {value} in selector: {selector}",
            )
        ]
    
    elif name == "browser_select_text":
        text = arguments.get("text")
        value = arguments.get("value")
        result = await browser_select_text(text, value)
        return [
            types.TextContent(
                type="text",
                text=f"Selected option {value} in element with text: {text}",
            )
        ]
    
    elif name == "browser_evaluate":
        script = arguments.get("script")
        result = await browser_evaluate(script)
        return [
            types.TextContent(
                type="text",
                text=f"JavaScript evaluation result: {result['result']}",
            )
        ]
    
    else:
        raise ValueError(f"Tool {name} not implemented")

async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="playwright-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )