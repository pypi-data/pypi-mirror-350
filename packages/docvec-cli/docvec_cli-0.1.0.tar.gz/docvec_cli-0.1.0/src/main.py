import argparse
import os
import sys # Import sys for clean exit

from .document_parser import parse_document
from .text_processor import clean_text, chunk_text
from .embedding_generator import load_embedding_model, generate_embeddings, DEFAULT_EMBEDDING_MODEL
from .output_formatter import save_to_json_chroma_compatible

def main():

    parser = argparse.ArgumentParser(
        description="DocVec CLI: A console-based tool for generating vector embeddings from documents."
    )

    parser.add_argument(
        "--input-path",
        type=str,
        required=True,
        help="Path to the document file or directory to be processed (e.g., 'my_docs/' or 'my_docs/report.pdf')."
    )

    parser.add_argument(
        "--output-path",
        type=str,
        required=True,
        help="Path to the directory where generated vector and metadata files will be saved."
    )

    parser.add_argument(
        "--chunk-size",
        type=int,
        default=1000,
        help="Maximum size of each text chunk in characters (default: 1000)."
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=200,
        help="Number of characters to overlap between consecutive chunks (default: 200)."
    )
    parser.add_argument(
        "--model-name",
        type=str,
        default=DEFAULT_EMBEDDING_MODEL,
        help=f"Name of the SentenceTransformer model to use for embeddings (default: '{DEFAULT_EMBEDDING_MODEL}')."
    )
    parser.add_argument(
        "--output-format",
        type=str,
        default="json",
        choices=["json"], # For now, only 'json' is supported
        help="Output format for the generated vectors and metadata (default: 'json')."
    )

    args = parser.parse_args()

    print("-" * 30)
    print("DocVec CLI Starting...")
    print(f"Input Path     : {args.input_path}")
    print(f"Output Path    : {args.output_path}")
    print(f"Chunk Size     : {args.chunk_size}")
    print(f"Chunk Overlap  : {args.chunk_overlap}")
    print(f"Embedding Model: {args.model_name}")
    print(f"Output Format  : {args.output_format}")
    print("-" * 30)

    if not os.path.exists(args.input_path):
        print(f"Error: The specified input path '{args.input_path}' does not exist.")
        sys.exit(1)

    try:
        os.makedirs(args.output_path, exist_ok=True)
    except OSError as e:
        print(f"Error: Could not create output directory '{args.output_path}'. Reason: {e}")
        sys.exit(1)

    embedding_model = None # Initialize to None
    try:
        embedding_model = load_embedding_model(args.model_name)
    except RuntimeError as e:
        print(f"Initialization error: Failed to load embedding model. {e}")
        sys.exit(1)


    if os.path.isfile(args.input_path):
        try:
            print(f"Processing single file: {args.input_path}")
            raw_content = parse_document(args.input_path)
            print(f"Successfully read {len(raw_content)} characters from {args.input_path}.")

            cleaned_content = clean_text(raw_content)
            print(f"Cleaned content has {len(cleaned_content)} characters.")

            chunks = chunk_text(cleaned_content, args.chunk_size, args.chunk_overlap)
            print(f"Text split into {len(chunks)} chunks.")

            if not chunks:
                print("Warning: No chunks generated from the document. Skipping embedding generation and output.")
                sys.exit(0)

            embeddings = generate_embeddings(chunks, embedding_model)
            print(f"Generated {embeddings.shape[0]} embeddings with dimension {embeddings.shape[1]}.")

            processed_data = []
            file_name_base = os.path.basename(args.input_path).rsplit('.', 1)[0]

            for i, chunk in enumerate(chunks):
                chunk_id = f"{file_name_base}-{i}"
                metadata = {
                    "source_file": os.path.basename(args.input_path),
                    "chunk_index": i,
                    "chunk_size": len(chunk),
                }
                processed_data.append({
                    "id": chunk_id,
                    "document": chunk,
                    "embedding": embeddings[i],
                    "metadata": metadata
                })

            if args.output_format == "json":
                output_filename = f"{file_name_base}_vectors.json"
                output_filepath = os.path.join(args.output_path, output_filename)
                save_to_json_chroma_compatible(processed_data, output_filepath)
                print(f"Output saved successfully to: {output_filepath}")
            else:
                print(f"Error: Unsupported output format '{args.output_format}'. Currently only 'json' is supported.")
                sys.exit(1)

        except FileNotFoundError as e:
            print(f"Error: Document file not found. {e}")
            sys.exit(1)
        except ValueError as e:
            print(f"Error: Document parsing failed due to unsupported format or content. {e}")
            sys.exit(1)
        except IOError as e:
            print(f"Error: An I/O issue occurred during file processing. {e}")
            sys.exit(1)
        except RuntimeError as e:
            print(f"Error: An issue occurred during embedding model operation. {e}")
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Please ensure your input file is valid and dependencies are installed.")
            sys.exit(1)
    else:
        print(f"Input path '{args.input_path}' is a directory. Directory processing logic will be added in future updates.")

        sys.exit(1)

if __name__ == "__main__":
    main()