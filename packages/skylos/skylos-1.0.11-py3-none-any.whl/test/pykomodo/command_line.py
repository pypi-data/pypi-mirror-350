import sys
import argparse
import os

KOMODO_VERSION = "0.2.5"

def launch_dashboard():
    """Launch the dashboard interface."""
    try:
        from pykomodo.dashboard import launch_dashboard
        print("Starting Komodo Dashboard...")
        demo = launch_dashboard()
        demo.launch(
            server_name="0.0.0.0", 
            server_port=7860,
            share=False,
            debug=False
        )
    except ImportError as e:
        print(f"[Error] Dashboard dependencies not available: {e}", file=sys.stderr)
        print("Please install gradio: pip install gradio", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[Error] Failed to launch dashboard: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """Main entry point for the komodo CLI."""
    parser = argparse.ArgumentParser(
        description="Process and chunk codebase content with advanced chunking strategies."
    )

    parser.add_argument("--version", action="version", version=f"komodo {KOMODO_VERSION}")
    
    parser.add_argument("--dashboard", action="store_true",
                        help="Launch the web-based dashboard interface")

    parser.add_argument("dirs", nargs="*", default=["."],
                        help="Directories to process (default: current directory)")
    
    chunk_group = parser.add_mutually_exclusive_group(required=False)
    chunk_group.add_argument("--equal-chunks", type=int, 
                            help="Split into N equal chunks")
    chunk_group.add_argument("--max-chunk-size", type=int, 
                            help="Maximum tokens/lines per chunk")
    chunk_group.add_argument("--max-tokens", type=int,
                            help="Maximum tokens per chunk (token-based chunking)")
    
    parser.add_argument("--output-dir", default="chunks",
                        help="Output directory for chunks (default: chunks)")
    
    parser.add_argument("--ignore", action="append", default=[],
                        help="Repeatable. Each usage adds one ignore pattern. Example: --ignore '**/node_modules/**' --ignore 'venv'")
    parser.add_argument("--unignore", action="append", default=[],
                        help="Repeatable. Each usage adds one unignore pattern. Example: --unignore '*.md'")
    
    parser.add_argument("--dry-run", action="store_true",
                        help="Show which files would be processed, but do not generate any chunks.")

    parser.add_argument("--priority", action="append", default=[],
                        help="Priority rules in format 'pattern,score' (repeatable). Example: --priority '*.py,10' --priority 'file2.txt,20'")
    
    parser.add_argument("--num-threads", type=int, default=4,
                        help="Number of processing threads (default: 4)")

    parser.add_argument("--enhanced", action="store_true",
                        help="Enable LLM optimizations")
    
    parser.add_argument("--semantic-chunks", action="store_true",
                        help="Use AST-based chunking for .py files (splits by top-level functions/classes)")

    parser.add_argument("--context-window", type=int, default=4096,
                        help="Target LLM context window size (default: 4096)")
    parser.add_argument("--min-relevance", type=float, default=0.3,
                        help="Minimum relevance score 0.0-1.0 (default: 0.3)")
    parser.add_argument("--no-metadata", action="store_true",
                        help="Disable metadata extraction")
    parser.add_argument("--keep-redundant", action="store_true",
                        help="Keep redundant content")
    parser.add_argument("--no-summaries", action="store_true",
                        help="Disable summary generation")

    parser.add_argument("--file-type", type=str, 
                        help="Only chunk files of this type (e.g., 'pdf', 'py')")
                        
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose output")

    args = parser.parse_args()

    if args.dashboard:
        launch_dashboard()
        return

    if not any([args.equal_chunks, args.max_chunk_size, args.max_tokens]):
        parser.error("One of --equal-chunks, --max-chunk-size, or --max-tokens is required (unless using --dashboard)")

    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)

    priority_rules = []
    for rule in args.priority:
        if not rule:
            continue
        try:
            pattern, score = rule.split(",", 1)
            priority_rules.append((pattern.strip(), int(score.strip())))
        except ValueError:
            print(f"[Error] Priority rule must be 'pattern,score': {rule}", 
                  file=sys.stderr)
            sys.exit(1)

    chunker = None
    try:
        if args.max_tokens:
            try:
                from pykomodo.token_chunker import TokenBasedChunker as ChunkerClass
                if args.verbose:
                    print("Using TokenBasedChunker for token-based chunking")
            except ImportError:
                print("[Error] TokenBasedChunker not available. Please install tiktoken or update pykomodo.", 
                      file=sys.stderr)
                sys.exit(1)
                
            chunker_args = {
                "max_tokens_per_chunk": args.max_tokens,
                "output_dir": args.output_dir,
                "user_ignore": args.ignore,
                "user_unignore": args.unignore,
                "priority_rules": priority_rules,
                "num_threads": args.num_threads,
                "dry_run": args.dry_run,
                "semantic_chunking": args.semantic_chunks,
                "file_type": args.file_type,
                "verbose": args.verbose
            }
        else:
            if args.enhanced:
                from pykomodo.enhanced_chunker import EnhancedParallelChunker as ChunkerClass
            else:
                from pykomodo.multi_dirs_chunker import ParallelChunker as ChunkerClass
                
            chunker_args = {
                "equal_chunks": args.equal_chunks,
                "max_chunk_size": args.max_chunk_size,
                "output_dir": args.output_dir,
                "user_ignore": args.ignore,
                "user_unignore": args.unignore,
                "priority_rules": priority_rules,
                "num_threads": args.num_threads,
                "dry_run": args.dry_run,
                "semantic_chunking": args.semantic_chunks,
                "file_type": args.file_type
            }
            
            if args.enhanced:
                chunker_args.update({
                    "extract_metadata": not args.no_metadata,
                    "add_summaries": not args.no_summaries,
                    "remove_redundancy": not args.keep_redundant,
                    "context_window": args.context_window,
                    "min_relevance_score": args.min_relevance
                })
    
        chunker = ChunkerClass(**chunker_args)
        chunker.process_directories(args.dirs)
        
    except Exception as e:
        print(f"[Error] Processing failed: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if chunker and hasattr(chunker, 'close'):
            chunker.close()

if __name__ == "__main__":
    main()