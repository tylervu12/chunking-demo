# SOP Markdown Chunking & Pinecone Uploader

This system processes markdown files containing Standard Operating Procedures (SOPs), chunks them appropriately, and uploads them to Pinecone for semantic search capabilities.

## Prerequisites

- Python 3.8+
- A Pinecone account
- An OpenAI API key

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory with the following variables:
```
OPENAI_API_KEY=your_openai_api_key
OPENAI_EMBEDDING_MODEL=your_embedding_model
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=your_index_name
```

3. Place your markdown SOP files in the `KBdocs/` directory.

## Usage

Run the script:
```bash
python sop_uploader.py
```

The script will:
1. Parse all markdown files in the `KBdocs/` directory
2. Split content by level 2 headers (`##`)
3. Chunk sections longer than 1500 words
4. Generate embeddings using OpenAI
5. Upload chunks to Pinecone with metadata

## Features

- Automatic chunking of long sections
- Preservation of section headers
- Metadata tracking (source, section title, tags)
- Error handling and logging
- Deterministic ID generation for chunks

## Notes

- The system uses Pinecone's latest API 
- Chunks are stored in a namespace called "sop-namespace"
- Each chunk includes its section header for context
- The system uses the text-embedding-3-small for embeddings 