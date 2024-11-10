import argparse
import os

from tqdm import tqdm

from smol_tools.summarizer import SmolSummarizer
from smol_tools.rewriter import SmolRewriter
from smol_tools.agent import SmolToolAgent


def run_smol_tool(command, input_reader):
    if command == "summarize":
        summarizer = SmolSummarizer()
        while True:
            input_text = input_reader()
            for summary in tqdm(summarizer.process(input_text)):
                pass
            print(summary)
    elif command == "rewrite":
        rewriter = SmolRewriter()
        while True:
            input_text = input_reader()
            for revision in tqdm(rewriter.process([input_text])):
                pass
            print(revision)
    elif command == "agent":
        agent = SmolToolAgent()
        while True:
            input_text = input_reader()
            for response in tqdm(agent.process(input_text)):
                pass
            print(response)


def get_parser():
    parser = argparse.ArgumentParser(
        description="Run SmolTools commands."
    )
    parser.add_argument(
        "--input-path",
        help="Path to input file with one input per line."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("summarize")
    subparsers.add_parser("rewrite")
    subparsers.add_parser("agent")
    return parser


def has_controlling_terminal():
    try:
        return os.ttyname(0) is not None
    except OSError:
        return False


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    if args.input_path:
        with open(args.input_path, "fh") as fh:
            lines = [line.strip() for line in fh.readlines()]
            input_reader = lambda: lines.pop()
    else:
        # Read from stdin
        prompt = "Enter text: " if has_controlling_terminal() else ""
        input_reader = lambda: input(prompt)

    run_smol_tool(args.command, input_reader)
