#!/usr/bin/env python3

import asyncio
import os
import argparse
import traceback
import uuid
from enum import Enum
from webEvalAgent.src.utils import stop_log_server
from webEvalAgent.src.log_server import send_log

# Only require NIA API key for public distribution
# The NIA backend will handle LLM calls internally
os.environ["ANONYMIZED_TELEMETRY"] = 'false'

# MCP imports
from mcp.server.fastmcp import FastMCP, Context
from mcp.types import TextContent

# Import our modules
from webEvalAgent.src.api_utils import validate_api_key
from webEvalAgent.src.tool_handlers import handle_web_evaluation, handle_setup_browser_state

# Stop any existing log server to avoid conflicts
stop_log_server()

# Create the MCP server
mcp = FastMCP("NIA Web Evaluator")

# Define the browser tools
class BrowserTools(str, Enum):
    WEB_EVAL_AGENT = "web_eval_agent"
    SETUP_BROWSER_STATE = "setup_browser_state"

def get_api_key():
    """Get and validate the NIA API key from environment."""
    api_key = os.environ.get('NIA_API_KEY')
    if not api_key:
        print("Error: No NIA API key provided. Please set the NIA_API_KEY environment variable.")
        print("Get your API key at: https://trynia.ai")
        return None
    return api_key

# Validate API key on startup
api_key = get_api_key()
if api_key:
    # Only validate if we have a key - validation will happen again at runtime
    try:
        is_valid = asyncio.run(validate_api_key(api_key))
        if not is_valid:
            print("Warning: API key validation failed. Please check your NIA_API_KEY.")
    except Exception as e:
        print(f"Warning: Could not validate API key during startup: {e}")

@mcp.tool(name=BrowserTools.WEB_EVAL_AGENT)
async def web_eval_agent(url: str, task: str, ctx: Context, headless_browser: bool = False) -> list[TextContent]:
    """Evaluate the user experience / interface of a web application.

    This tool allows the AI to assess the quality of user experience and interface design
    of a web application by performing specific tasks and analyzing the interaction flow.

    Before this tool is used, the web application should already be running locally on a port.

    Args:
        url: Required. The localhost URL of the web application to evaluate, including the port number.
            Example: http://localhost:3000, http://localhost:8080, http://localhost:4200, http://localhost:5173, etc.
            Try to avoid using the path segments of the URL, and instead use the root URL.
        task: Required. The specific UX/UI aspect to test (e.g., "test the checkout flow",
             "evaluate the navigation menu usability", "check form validation feedback")
             Be as detailed as possible in your task description. It could be anywhere from 2 sentences to 2 paragraphs.
        headless_browser: Optional. Whether to hide the browser window popup during evaluation.
        If headless_browser is True, only the NIA control center browser will show, and no popup browser will be shown.

    Returns:
        list[list[TextContent, ImageContent]]: A detailed evaluation of the web application's UX/UI, including
                         observations, issues found, and recommendations for improvement
                         and screenshots of the web application during the evaluation
    """
    # Get fresh API key for each request
    current_api_key = get_api_key()
    if not current_api_key:
        return [TextContent(type="text", text="❌ Error: No NIA API key provided. Please set the NIA_API_KEY environment variable.")]
    
    is_valid = await validate_api_key(current_api_key)
    if not is_valid:
        error_message_str = "❌ Error: API Key validation failed when running the tool.\n"
        error_message_str += "   Reason: Free tier limit reached or invalid key.\n"
        error_message_str += "   👉 Please subscribe at https://trynia.ai to continue."
        return [TextContent(type="text", text=error_message_str)]
    
    try:
        # Generate a new tool_call_id for this specific tool call
        tool_call_id = str(uuid.uuid4())
        return await handle_web_evaluation(
            {"url": url, "task": task, "headless": headless_browser, "tool_call_id": tool_call_id},
            ctx,
            current_api_key
        )
    except Exception as e:
        tb = traceback.format_exc()
        return [TextContent(
            type="text",
            text=f"Error executing web_eval_agent: {str(e)}\n\nTraceback:\n{tb}"
        )]

@mcp.tool(name=BrowserTools.SETUP_BROWSER_STATE)
async def setup_browser_state(url: str = None, ctx: Context = None) -> list[TextContent]:
    """Sets up and saves browser state for future use.

    This tool should only be called in one scenario:
    1. The user explicitly requests to set up browser state/authentication

    Launches a non-headless browser for user interaction, allows login/authentication,
    and saves the browser state (cookies, local storage, etc.) to a local file.

    Args:
        url: Optional URL to navigate to upon opening the browser.
        ctx: The MCP context (used for progress reporting, not directly here).

    Returns:
        list[TextContent]: Confirmation of state saving or error messages.
    """
    # Get fresh API key for each request
    current_api_key = get_api_key()
    if not current_api_key:
        return [TextContent(type="text", text="❌ Error: No NIA API key provided. Please set the NIA_API_KEY environment variable.")]
    
    is_valid = await validate_api_key(current_api_key)
    if not is_valid:
        error_message_str = "❌ Error: API Key validation failed when running the tool.\n"
        error_message_str += "   Reason: Free tier limit reached or invalid key.\n"
        error_message_str += "   👉 Please subscribe at https://trynia.ai to continue."
        return [TextContent(type="text", text=error_message_str)]
    
    try:
        # Generate a new tool_call_id for this specific tool call
        tool_call_id = str(uuid.uuid4())
        send_log(f"Generated new tool_call_id for setup_browser_state: {tool_call_id}")
        return await handle_setup_browser_state(
            {"url": url, "tool_call_id": tool_call_id},
            ctx,
            current_api_key
        )
    except Exception as e:
        tb = traceback.format_exc()
        return [TextContent(
            type="text",
            text=f"Error executing setup_browser_state: {str(e)}\n\nTraceback:\n{tb}"
        )]

def main():
    """Main entry point for the MCP server."""
    try:
        # Run the FastMCP server
        mcp.run(transport='stdio')
    finally:
        # Ensure resources are cleaned up when server terminates
        pass

# This entry point is used when running directly
if __name__ == "__main__":
    main()
