import os
import json
from pathlib import Path
from typing import List, Dict, Any
import hashlib
from dotenv import load_dotenv
from markdown_it import MarkdownIt
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize clients
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def parse_markdown_file(file_path: Path) -> List[Dict[str, Any]]:
    """Parse markdown file into sections based on level 2 headers."""
    md = MarkdownIt()
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse markdown
    tokens = md.parse(content)
    
    sections = []
    current_section = None
    current_content = []
    
    for i, token in enumerate(tokens):
        if token.type == 'heading_open' and token.tag == 'h2':
            # Save previous section if exists
            if current_section:
                sections.append({
                    'title': current_section,
                    'content': '\n'.join(current_content).strip()
                })
            # Start new section - get the title from the next inline token
            if i + 1 < len(tokens) and tokens[i + 1].type == 'inline':
                current_section = tokens[i + 1].content
            else:
                current_section = "Untitled Section"
            current_content = []
        elif token.type == 'inline' and current_section:
            current_content.append(token.content)
    
    # Add last section
    if current_section:
        sections.append({
            'title': current_section,
            'content': '\n'.join(current_content).strip()
        })
    
    return sections

def chunk_section(section: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Split section into chunks if it's too long."""
    text = section['content']  # Remove title from text
    word_count = len(text.split())
    
    if word_count < 1500:
        return [section]
    
    # Use RecursiveCharacterTextSplitter for longer sections
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
    )
    
    chunks = splitter.split_text(text)
    return [{'title': section['title'], 'content': chunk} for chunk in chunks]

def generate_embedding(text: str) -> List[float]:
    """Generate embedding using OpenAI's API."""
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def generate_id(text: str, source: str) -> str:
    """Generate deterministic ID for a chunk."""
    return hashlib.sha256(f"{source}-{text}".encode()).hexdigest()

def process_files():
    """Main function to process all markdown files and upload to Pinecone."""
    kb_dir = Path('KBdocs')
    if not kb_dir.exists():
        print("KBdocs directory not found!")
        return
    
    # Get or create index
    index_name = os.getenv('PINECONE_INDEX_NAME')
    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            spec={
                "serverless": {
                    "cloud": "aws",
                    "region": "us-east-1"
                }
            },
            dimension=1536,  # dimension for text-embedding-3-small
            metric="cosine"
        )
    
    index = pc.Index(index_name)
    
    # Process each markdown file
    for md_file in kb_dir.glob('*.md'):
        print(f"Processing {md_file.name}...")
        
        # Parse sections
        sections = parse_markdown_file(md_file)
        
        # Process each section
        for section in sections:
            # Chunk if necessary
            chunks = chunk_section(section)
            
            # Prepare records for Pinecone
            records = []
            for chunk in chunks:
                chunk_text = chunk['content']  # Just use the content without title
                
                # Generate embedding
                try:
                    embedding = generate_embedding(chunk_text)
                except Exception as e:
                    print(f"Error generating embedding: {e}")
                    continue
                
                # Create record with full path in section_title
                record = {
                    "id": generate_id(chunk_text, str(md_file)),
                    "values": embedding,
                    "metadata": {
                        "text": chunk_text,
                        "source": f"KBdocs/{md_file.name}",
                        "section_title": f"{md_file.stem}/{section['title']}"  # Include both file name and section title
                    }
                }
                records.append(record)
            
            # Upload to Pinecone
            if records:
                try:
                    index.upsert(vectors=records)
                    print(f"Uploaded {len(records)} chunks from {md_file.name}")
                except Exception as e:
                    print(f"Error uploading to Pinecone: {e}")

if __name__ == "__main__":
    process_files() 