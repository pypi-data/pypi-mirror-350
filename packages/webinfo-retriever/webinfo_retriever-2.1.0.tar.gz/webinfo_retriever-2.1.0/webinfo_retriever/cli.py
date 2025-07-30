"""
Command-line interface for WebInfo Retriever.
"""

import argparse
import json
import sys
import asyncio
import time
import uuid
from typing import Dict, Any
from datetime import datetime

from .api.client import WebInfoRetriever
from .utils.exceptions import WebInfoRetrieverError
from .core.analytics_engine import analytics_engine
from .core.smart_cache import smart_cache


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
    search_parser.add_argument("--comprehensive", action="store_true", help="Comprehensive search with multi-source analysis (Tavily-like)")
    search_parser.add_argument("--ultra-fast", action="store_true", help="Ultra-fast comprehensive search with parallel processing")
    search_parser.add_argument("--answer-type", choices=["comprehensive", "factual", "comparative", "instructional"],
                              default="comprehensive", help="Type of answer to generate")
    search_parser.add_argument("--output-file", help="Save markdown report to file")

    compare_parser = subparsers.add_parser("compare", help="Compare specific sources for a query")
    compare_parser.add_argument("query", help="Search query")
    compare_parser.add_argument("--domains", nargs="+", required=True, help="Domains to compare")
    compare_parser.add_argument("--criteria", nargs="+", default=["Relevance", "Quality", "Category"],
                               help="Comparison criteria")

    # Analytics commands
    analytics_parser = subparsers.add_parser("analytics", help="View analytics and performance metrics")
    analytics_parser.add_argument("--export", help="Export analytics to JSON file")
    analytics_parser.add_argument("--clear", action="store_true", help="Clear analytics data")

    # Cache commands
    cache_parser = subparsers.add_parser("cache", help="Manage cache")
    cache_parser.add_argument("--stats", action="store_true", help="Show cache statistics")
    cache_parser.add_argument("--clear", action="store_true", help="Clear cache")

    # Interactive mode
    interactive_parser = subparsers.add_parser("interactive", help="Start interactive mode")
    interactive_parser.add_argument("--analytics", action="store_true", help="Show analytics in interactive mode")

    # Dashboard mode
    dashboard_parser = subparsers.add_parser("dashboard", help="Start web dashboard")
    dashboard_parser.add_argument("--host", default="localhost", help="Dashboard host (default: localhost)")
    dashboard_parser.add_argument("--port", type=int, default=5000, help="Dashboard port (default: 5000)")
    dashboard_parser.add_argument("--debug", action="store_true", help="Enable debug mode")

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

        elif args.command == "analytics":
            # Analytics command
            if args.clear:
                analytics_engine.search_history.clear()
                analytics_engine.error_log.clear()
                print("✅ Analytics data cleared")
                return

            if args.export:
                analytics_engine.export_analytics(args.export)
                print(f"📊 Analytics exported to: {args.export}")
                return

            # Show analytics
            stats = analytics_engine.get_performance_stats()
            trends = analytics_engine.get_search_trends()
            errors = analytics_engine.get_error_analysis()

            print("\n📊 WEBINFO RETRIEVER ANALYTICS")
            print("=" * 50)
            print(f"Total Searches: {stats.total_searches}")
            print(f"Average Response Time: {stats.avg_response_time:.2f}s")
            print(f"Success Rate: {stats.success_rate:.1f}%")
            print(f"Average Confidence: {stats.avg_confidence:.1f}%")
            print(f"Sources Processed: {stats.total_sources_processed}")
            print(f"Cache Hit Rate: {stats.cache_hit_rate:.1f}%")
            print(f"Error Rate: {stats.error_rate:.1f}%")
            print(f"Uptime: {stats.uptime/3600:.1f} hours")

            if trends['total'] > 0:
                print(f"\n📈 RECENT TRENDS (24h)")
                print("-" * 30)
                print(f"Recent Searches: {trends['total']}")
                print(f"Peak Hour: {trends['peak_hour']}:00")

                search_types = trends['search_type_distribution']
                for search_type, count in search_types.items():
                    print(f"{search_type.title()}: {count}")

            if errors['total_errors'] > 0:
                print(f"\n❌ ERROR ANALYSIS")
                print("-" * 20)
                print(f"Total Errors: {errors['total_errors']}")
                print(f"Error Rate: {errors['error_rate']:.1f}%")

                for error_type, count in errors['error_types'].items():
                    print(f"{error_type}: {count}")

            return

        elif args.command == "cache":
            # Cache command
            if args.clear:
                smart_cache.clear()
                print("✅ Cache cleared")
                return

            if args.stats:
                stats = smart_cache.get_stats()
                print("\n💾 CACHE STATISTICS")
                print("=" * 30)
                print(f"Memory Entries: {stats['memory_entries']}")
                print(f"Memory Size: {stats['memory_size_mb']:.2f} MB")
                print(f"Max Size: {stats['max_size_mb']:.2f} MB")
                print(f"Hit Rate: {stats['hit_rate']:.1f}%")
                print(f"Total Hits: {stats['total_hits']}")
                print(f"Total Misses: {stats['total_misses']}")
                print(f"Evictions: {stats['total_evictions']}")
                return

            # Default: show stats
            stats = smart_cache.get_stats()
            print(f"Cache: {stats['memory_entries']} entries, {stats['hit_rate']:.1f}% hit rate")
            return

        elif args.command == "interactive":
            # Interactive mode
            print("🚀 WebInfo Retriever Interactive Mode")
            print("Type 'help' for commands, 'quit' to exit")

            if args.analytics:
                stats = analytics_engine.get_performance_stats()
                print(f"\n📊 Quick Stats: {stats.total_searches} searches, {stats.avg_response_time:.1f}s avg")

            while True:
                try:
                    command = input("\nwebinfo> ").strip()

                    if command.lower() in ['quit', 'exit', 'q']:
                        print("👋 Goodbye!")
                        break

                    elif command.lower() == 'help':
                        print("\n📚 Available Commands:")
                        print("  search <query>     - Perform ultra-fast search")
                        print("  fast <query>       - Perform fast search")
                        print("  analyze <url>      - Analyze single URL")
                        print("  stats              - Show analytics")
                        print("  cache              - Show cache stats")
                        print("  clear cache        - Clear cache")
                        print("  help               - Show this help")
                        print("  quit/exit/q        - Exit interactive mode")

                    elif command.lower() == 'stats':
                        stats = analytics_engine.get_performance_stats()
                        print(f"📊 {stats.total_searches} searches, {stats.avg_response_time:.1f}s avg, {stats.success_rate:.1f}% success")

                    elif command.lower() == 'cache':
                        stats = smart_cache.get_stats()
                        print(f"💾 {stats['memory_entries']} entries, {stats['hit_rate']:.1f}% hit rate")

                    elif command.lower() == 'clear cache':
                        smart_cache.clear()
                        print("✅ Cache cleared")

                    elif command.startswith('search '):
                        query = command[7:].strip()
                        if query:
                            search_id = str(uuid.uuid4())
                            analytics_engine.start_search(search_id, query, "ultra-fast")

                            print(f"🚀 Searching: {query}")
                            start_time = time.time()

                            try:
                                response = asyncio.run(client.fast_comprehensive_search(
                                    query=query,
                                    num_sources=5,
                                    answer_type="comprehensive"
                                ))

                                duration = time.time() - start_time
                                analytics_engine.complete_search(search_id, True, 0.8)

                                print(f"✅ Completed in {duration:.1f}s")
                                if isinstance(response, str):
                                    print(response[:500] + "..." if len(response) > 500 else response)

                            except Exception as e:
                                analytics_engine.record_error(search_id, e)
                                analytics_engine.complete_search(search_id, False)
                                print(f"❌ Error: {e}")

                    elif command.startswith('fast '):
                        query = command[5:].strip()
                        if query:
                            print(f"⚡ Fast search: {query}")
                            try:
                                response = asyncio.run(client.fast_search(
                                    user_query=query,
                                    num_results=3
                                ))
                                print(response[:300] + "..." if len(response) > 300 else response)
                            except Exception as e:
                                print(f"❌ Error: {e}")

                    elif command.startswith('analyze '):
                        url = command[8:].strip()
                        if url:
                            print(f"🔍 Analyzing: {url}")
                            try:
                                response = client.retrieve_and_summarize(url)
                                print(f"📄 {response.get('summary', 'No summary available')[:200]}...")
                            except Exception as e:
                                print(f"❌ Error: {e}")

                    elif command.strip():
                        print("❓ Unknown command. Type 'help' for available commands.")

                except KeyboardInterrupt:
                    print("\n👋 Goodbye!")
                    break
                except Exception as e:
                    print(f"❌ Error: {e}")

            return

        elif args.command == "dashboard":
            # Dashboard mode
            try:
                from .dashboard import start_dashboard
                print(f"🚀 Starting WebInfo Retriever Dashboard")
                print(f"📊 URL: http://{args.host}:{args.port}")
                print(f"📈 Real-time analytics and monitoring")
                print(f"🔄 Press Ctrl+C to stop")

                start_dashboard(host=args.host, port=args.port, debug=args.debug)

            except ImportError:
                print("❌ Dashboard requires Flask. Install with:")
                print("   pip install flask flask-socketio")
                return
            except KeyboardInterrupt:
                print("\n👋 Dashboard stopped")
                return
            except Exception as e:
                print(f"❌ Dashboard error: {e}")
                return

        elif args.command == "search":
            # Join query words into natural language query
            user_query = " ".join(args.query)

            # Start analytics tracking
            search_id = str(uuid.uuid4())
            search_type = "ultra-fast" if args.ultra_fast else "comprehensive" if args.comprehensive else "fast" if args.fast else "intelligent"
            analytics_engine.start_search(search_id, user_query, search_type)

            if args.ultra_fast:
                # Ultra-fast comprehensive search mode
                print(f"🚀 Starting ULTRA-FAST comprehensive search for: {user_query}")
                print("⚡ Parallel processing with streaming results...")

                try:
                    start_time = time.time()
                    analytics_engine.update_search_progress(search_id, sources_found=args.num_results)

                    response = asyncio.run(client.fast_comprehensive_search(
                        query=user_query,
                        num_sources=args.num_results,
                        output_format="both" if args.output_file else ("json" if args.json else "markdown"),
                        answer_type=args.answer_type,
                        stream_results=True
                    ))

                    duration = time.time() - start_time
                    analytics_engine.complete_search(search_id, True, 0.85)

                    if isinstance(response, dict) and "terminal_output" in response:
                        # Display clean terminal output
                        print(response["terminal_output"])

                        if args.output_file:
                            # Save beautiful HTML/markdown report to file
                            with open(args.output_file, 'w', encoding='utf-8') as f:
                                f.write(response["markdown_report"])
                            print(f"\n📄 Ultra-fast comprehensive report saved to: {args.output_file}")
                    elif isinstance(response, str):
                        print(response)
                        if args.output_file:
                            with open(args.output_file, 'w', encoding='utf-8') as f:
                                f.write(response)
                            print(f"\n📄 Report saved to: {args.output_file}")

                    print(f"\n⚡ Completed in {duration:.1f}s")

                except Exception as e:
                    analytics_engine.record_error(search_id, e, "ultra-fast search")
                    analytics_engine.complete_search(search_id, False)
                    raise

                return

            elif args.comprehensive:
                # Comprehensive search mode (Tavily-like)
                print(f"🔍 Starting comprehensive search for: {user_query}")
                print("⚡ Analyzing query, discovering sources, and synthesizing answer...")

                response = asyncio.run(client.comprehensive_search(
                    query=user_query,
                    num_sources=args.num_results,
                    output_format="both" if args.output_file else ("json" if args.json else "markdown"),
                    answer_type=args.answer_type
                ))

                if isinstance(response, dict) and "terminal_output" in response:
                    # Display clean terminal output
                    print(response["terminal_output"])

                    if args.output_file:
                        # Save beautiful HTML/markdown report to file
                        with open(args.output_file, 'w', encoding='utf-8') as f:
                            f.write(response["markdown_report"])
                        print(f"\n📄 Comprehensive report saved to: {args.output_file}")
                elif isinstance(response, str):
                    print(response)
                    if args.output_file:
                        with open(args.output_file, 'w', encoding='utf-8') as f:
                            f.write(response)
                        print(f"\n📄 Report saved to: {args.output_file}")
                return

            elif args.fast:
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
