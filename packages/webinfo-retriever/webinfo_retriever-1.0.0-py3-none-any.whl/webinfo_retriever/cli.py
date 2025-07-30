"""
Command-line interface for WebInfo Retriever.
"""

import argparse
import json
import sys
import asyncio
from typing import Dict, Any

from .api.client import WebInfoRetriever
from .utils.exceptions import WebInfoRetrieverError


def print_json_response(response: Dict[str, Any], indent: int = 2) -> None:
    """Print response as formatted JSON."""
    print(json.dumps(response, indent=indent, ensure_ascii=False))


def print_formatted_response(response: Dict[str, Any]) -> None:
    """Print response in a human-readable format."""
    print(f"\n{'='*60}")
    print(f"QUERY: {response.get('query', 'N/A')}")
    print(f"{'='*60}")

    if response.get('response'):
        print("\nRESPONSE:")
        print("-" * 40)
        print(response['response'])

    if response.get('answer'):
        print(f"\nANSWER:")
        print("-" * 40)
        print(response['answer'])
        print(f"\nConfidence: {response.get('confidence', 0):.2f}")

    if response.get('key_points'):
        print(f"\nKEY POINTS:")
        print("-" * 40)
        for i, point in enumerate(response['key_points'], 1):
            print(f"{i}. {point}")

    if response.get('sources'):
        print(f"\nSOURCES ({len(response['sources'])}):")
        print("-" * 40)
        for i, source in enumerate(response['sources'], 1):
            print(f"{i}. {source.get('title', 'Untitled')} - {source.get('url', 'N/A')}")

    if response.get('confidence_score'):
        print(f"\nOverall Confidence: {response['confidence_score']:.2f}")

    print(f"\n{'='*60}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="WebInfo Retriever - Advanced web information retrieval and AI summarization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  webinfo-retriever summarize https://example.com
  webinfo-retriever summarize https://example.com --query "main topics"
  webinfo-retriever question https://example.com "What is the main topic?"
  webinfo-retriever keypoints https://example.com --num-points 3
  webinfo-retriever metadata https://example.com
  webinfo-retriever multiple https://site1.com https://site2.com --query "comparison"
        """
    )

    parser.add_argument(
        "--api-key",
        help="Google Gemini API key (or set GEMINI_API_KEY env var)"
    )

    parser.add_argument(
        "--selenium",
        action="store_true",
        help="Use Selenium for scraping (for dynamic content)"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output response as JSON"
    )

    parser.add_argument(
        "--max-length",
        type=int,
        help="Maximum summary length"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    summarize_parser = subparsers.add_parser("summarize", help="Summarize content from a URL")
    summarize_parser.add_argument("url", help="URL to summarize")
    summarize_parser.add_argument("--query", help="Optional query to focus the summary")

    question_parser = subparsers.add_parser("question", help="Answer a question based on URL content")
    question_parser.add_argument("url", help="URL to analyze")
    question_parser.add_argument("question", help="Question to answer")

    keypoints_parser = subparsers.add_parser("keypoints", help="Extract key points from URL content")
    keypoints_parser.add_argument("url", help="URL to analyze")
    keypoints_parser.add_argument("--num-points", type=int, default=5, help="Number of key points to extract")

    metadata_parser = subparsers.add_parser("metadata", help="Get metadata about a webpage")
    metadata_parser.add_argument("url", help="URL to analyze")

    multiple_parser = subparsers.add_parser("multiple", help="Summarize content from multiple URLs")
    multiple_parser.add_argument("urls", nargs="+", help="URLs to summarize")
    multiple_parser.add_argument("--query", help="Optional query to focus the summary")
    multiple_parser.add_argument("--max-concurrent", type=int, default=5, help="Maximum concurrent requests")

    search_parser = subparsers.add_parser("search", help="Intelligent web search with AI analysis")
    search_parser.add_argument("query", nargs="+", help="Natural language search query (e.g., 'find me python tutorials')")
    search_parser.add_argument("--num-results", type=int, default=8, help="Number of results to process")

    search_parser.add_argument("--no-summary", action="store_true", help="Skip executive summary generation")
    search_parser.add_argument("--quick", action="store_true", help="Quick search mode (faster, less detailed)")
    search_parser.add_argument("--fast", action="store_true", help="Super fast search mode (fastest)")
    search_parser.add_argument("--output-file", help="Save markdown report to file")

    compare_parser = subparsers.add_parser("compare", help="Compare specific sources for a query")
    compare_parser.add_argument("query", help="Search query")
    compare_parser.add_argument("--domains", nargs="+", required=True, help="Domains to compare")
    compare_parser.add_argument("--criteria", nargs="+", default=["Relevance", "Quality", "Category"],
                               help="Comparison criteria")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        client = WebInfoRetriever(api_key=args.api_key)

        if args.command == "summarize":
            response = client.retrieve_and_summarize(
                args.url,
                query=args.query,
                max_summary_length=args.max_length,
                use_selenium=args.selenium
            )

        elif args.command == "question":
            response = client.answer_question(
                args.url,
                args.question,
                use_selenium=args.selenium
            )

        elif args.command == "keypoints":
            response = client.extract_key_points(
                args.url,
                num_points=args.num_points,
                use_selenium=args.selenium
            )

        elif args.command == "metadata":
            response = client.get_page_metadata(
                args.url,
                use_selenium=args.selenium
            )

        elif args.command == "multiple":
            response = client.retrieve_multiple_and_summarize(
                args.urls,
                query=args.query,
                max_summary_length=args.max_length,
                max_concurrent=args.max_concurrent
            )

        elif args.command == "search":
            # Join query words into natural language query
            user_query = " ".join(args.query)

            if args.fast:
                # Super fast search mode
                response = asyncio.run(client.fast_search(
                    user_query=user_query,
                    num_results=args.num_results
                ))

                print(response)
                if args.output_file:
                    with open(args.output_file, 'w', encoding='utf-8') as f:
                        f.write(response)
                    print(f"\nReport saved to: {args.output_file}")
                return

            elif args.quick:
                # Quick search mode
                response = asyncio.run(client.quick_search(
                    query=user_query,
                    num_results=args.num_results,
                    format_output=not args.json
                ))

                if isinstance(response, str) and not args.json:
                    print(response)
                    if args.output_file:
                        with open(args.output_file, 'w', encoding='utf-8') as f:
                            f.write(response)
                        print(f"\nReport saved to: {args.output_file}")
                    return
            else:
                # Full intelligent search
                response = asyncio.run(client.intelligent_search(
                    query=user_query,
                    num_results=args.num_results,
                    include_executive_summary=not args.no_summary,
                    output_format="both" if args.output_file else ("json" if args.json else "markdown")
                ))

                # Handle markdown output
                if not args.json and "markdown_report" in response:
                    print(response["markdown_report"])

                    if args.output_file:
                        with open(args.output_file, 'w', encoding='utf-8') as f:
                            f.write(response["markdown_report"])
                        print(f"\nMarkdown report saved to: {args.output_file}")
                    return

        elif args.command == "compare":
            response = asyncio.run(client.compare_sources(
                query=args.query,
                specific_domains=args.domains,
                comparison_criteria=args.criteria
            ))

            if isinstance(response, str):
                print(response)
                if args.output_file:
                    with open(args.output_file, 'w', encoding='utf-8') as f:
                        f.write(response)
                    print(f"\nComparison report saved to: {args.output_file}")
                return

        else:
            print(f"Unknown command: {args.command}")
            sys.exit(1)

        if args.json:
            print_json_response(response)
        else:
            print_formatted_response(response)

        client.close()

    except WebInfoRetrieverError as e:
        print(f"Error: {e.message}", file=sys.stderr)
        if e.details:
            print(f"Details: {e.details}", file=sys.stderr)
        sys.exit(1)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
