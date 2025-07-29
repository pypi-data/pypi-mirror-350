#!/usr/bin/env python3
import argparse
import asyncio
import os
import sys

from .src.agent import CodeAgent


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="OpenCursor: AI-powered code agent for workspace operations"
    )
    
    parser.add_argument(
        "-w", "--workspace",
        help="Path to the workspace directory",
        default=os.getcwd(),
        type=str
    )
    
    parser.add_argument(
        "-q", "--query",
        help="Query to process",
        required=True,
        type=str
    )
    
    parser.add_argument(
        "-m", "--model",
        help="LLM model to use",
        default="qwen3_14b_q6k:latest",
        type=str
    )
    
    parser.add_argument(
        "-H", "--host",
        help="Ollama API host URL",
        default="http://192.168.170.76:11434",
        type=str
    )
    
    parser.add_argument(
        "-i", "--interactive",
        help="Run in interactive mode (one tool call at a time)",
        action="store_true"
    )
    
    return parser.parse_args()


async def run_agent(args):
    """Run the code agent with the provided arguments."""
    agent = CodeAgent(
        model_name=args.model,
        host=args.host,
        workspace_root=args.workspace
    )
    
    if args.interactive:
        result = await agent.interactive(args.query)
    else:
        result = await agent.autonomous_mode(args.query)
    
    print(result)


def main():
    """Main entry point for the CLI."""
    args = parse_args()
    
    # Ensure workspace path is absolute
    args.workspace = os.path.abspath(args.workspace)
    
    # Check if workspace exists
    if not os.path.isdir(args.workspace):
        print(f"Error: Workspace directory '{args.workspace}' does not exist.")
        sys.exit(1)
    
    # Run the agent
    asyncio.run(run_agent(args))


if __name__ == "__main__":
    main() 