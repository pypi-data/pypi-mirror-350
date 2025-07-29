from playwright.async_api import async_playwright
import mcp.types as types

tool_names = ["get-dom", "browser_navigate", "browser_screenshot", "browser_click", 
              "browser_click_text", "browser_hover", "browser_hover_text", "browser_fill",
              "browser_select", "browser_select_text", "browser_evaluate"]

tools = [
    types.Tool(
        name="get-dom",
        description="Get DOM of a url",
        inputSchema={
            "type": "object",
            "properties": {
                "url": {"type": "string"},
            },
            "required": ["url"],
        },
    ),
    types.Tool(
        name="browser_navigate",
        description="Navigate to any URL in the browser",
        inputSchema={
            "type": "object",
            "properties": {
                "url": {"type": "string"},
            },
            "required": ["url"],
        },
    ),
    types.Tool(
        name="browser_screenshot",
        description="Capture screenshots of the entire page or specific elements",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "selector": {"type": "string"},
                "fullPage": {"type": "boolean"},
            },
            "required": ["name"],
        },
    ),
    types.Tool(
        name="browser_click",
        description="Click elements on the page using CSS selector",
        inputSchema={
            "type": "object",
            "properties": {
                "selector": {"type": "string"},
            },
            "required": ["selector"],
        },
    ),
    types.Tool(
        name="browser_click_text",
        description="Click elements on the page by their text content",
        inputSchema={
            "type": "object",
            "properties": {
                "text": {"type": "string"},
            },
            "required": ["text"],
        },
    ),
    types.Tool(
        name="browser_hover",
        description="Hover over elements on the page using CSS selector",
        inputSchema={
            "type": "object",
            "properties": {
                "selector": {"type": "string"},
            },
            "required": ["selector"],
        },
    ),
    types.Tool(
        name="browser_hover_text",
        description="Hover over elements on the page by their text content",
        inputSchema={
            "type": "object",
            "properties": {
                "text": {"type": "string"},
            },
            "required": ["text"],
        },
    ),
    types.Tool(
        name="browser_fill",
        description="Fill out input fields",
        inputSchema={
            "type": "object",
            "properties": {
                "selector": {"type": "string"},
                "value": {"type": "string"},
            },
            "required": ["selector", "value"],
        },
    ),
    types.Tool(
        name="browser_select",
        description="Select an option in a SELECT element using CSS selector",
        inputSchema={
            "type": "object",
            "properties": {
                "selector": {"type": "string"},
                "value": {"type": "string"},
            },
            "required": ["selector", "value"],
        },
    ),
    types.Tool(
        name="browser_select_text",
        description="Select an option in a SELECT element by its text content",
        inputSchema={
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "value": {"type": "string"},
            },
            "required": ["text", "value"],
        },
    ),
    types.Tool(
        name="browser_evaluate",
        description="Execute JavaScript in the browser console",
        inputSchema={
            "type": "object",
            "properties": {
                "script": {"type": "string"},
            },
            "required": ["script"],
        },
    )
]

async def get_dom(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        dom = await page.content()
        await browser.close()
        return dom

async def browser_navigate(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await browser.close()
        return {"status": "success", "url": url}

async def browser_screenshot(name: str, selector: str = None, fullPage: bool = False):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        if selector:
            element = await page.wait_for_selector(selector)
            screenshot = await element.screenshot(path=f"{name}.png")
        else:
            screenshot = await page.screenshot(path=f"{name}.png", full_page=fullPage)
        
        await browser.close()
        return {"status": "success", "screenshot": name + ".png"}

async def browser_click(selector: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.click(selector)
        await browser.close()
        return {"status": "success", "action": "click", "selector": selector}

async def browser_click_text(text: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.click(f"text={text}")
        await browser.close()
        return {"status": "success", "action": "click", "text": text}

async def browser_hover(selector: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.hover(selector)
        await browser.close()
        return {"status": "success", "action": "hover", "selector": selector}

async def browser_hover_text(text: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.hover(f"text={text}")
        await browser.close()
        return {"status": "success", "action": "hover", "text": text}

async def browser_fill(selector: str, value: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.fill(selector, value)
        await browser.close()
        return {"status": "success", "action": "fill", "selector": selector, "value": value}

async def browser_select(selector: str, value: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.select_option(selector, value)
        await browser.close()
        return {"status": "success", "action": "select", "selector": selector, "value": value}

async def browser_select_text(text: str, value: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.select_option(f"text={text}", value)
        await browser.close()
        return {"status": "success", "action": "select", "text": text, "value": value}

async def browser_evaluate(script: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        result = await page.evaluate(script)
        await browser.close()
        return {"status": "success", "result": result}