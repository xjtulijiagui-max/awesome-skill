#!/usr/bin/env python3
"""
Build vector index for feishu-lightweight-kb
"""

import os
import argparse
import json
import re
from pathlib import Path
import numpy as np

SUPPORTED_EXTENSIONS = {'.md', '.txt', '.pdf', '.docx'}

def extract_text_from_file(file_path: Path) -> str:
    """Extract text from supported file formats"""
    ext = file_path.suffix.lower()
    
    if ext in ('.md', '.txt'):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    
    elif ext == '.pdf':
        try:
            import pypdf
            text = ''
            with open(file_path, 'rb') as f:
                reader = pypdf.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + '\n'
            return text
        except ImportError:
            print(f"Warning: pypdf not installed, skipping PDF {file_path}")
            return ''
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
            return ''
    
    elif ext == '.docx':
        try:
            from docx import Document
            doc = Document(file_path)
            return '\n'.join([para.text for para in doc.paragraphs])
        except ImportError:
            print(f"Warning: python-docx not installed, skipping DOCX {file_path}")
            return ''
        except Exception as e:
            print(f"Error reading DOCX {file_path}: {e}")
            return ''
    
    else:
        return ''

def split_text(text: str, chunk_size: int = 512, chunk_overlap: int = 50) -> list[str]:
    """Split text into chunks with overlap"""
    chunks = []
    start = 0
    
    # Split by paragraphs first to preserve structure
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    current_chunk = []
    current_length = 0
    
    for para in paragraphs:
        para_len = len(para)
        if current_length + para_len <= chunk_size:
            current_chunk.append(para)
            current_length += para_len
        else:
            if current_chunk:
                chunks.append('\n'.join(current_chunk))
            # Start new chunk with overlap
            overlap_start = max(0, len(current_chunk) - int(chunk_overlap / 50))
            current_chunk = current_chunk[overlap_start:] + [para]
            current_length = sum(len(p) for p in current_chunk)
    
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
    
    # If any chunk is still too big, split it further
    final_chunks = []
    for chunk in chunks:
        if len(chunk) <= chunk_size:
            final_chunks.append(chunk)
        else:
            # Split by sentence
            sentences = re.split(r'(?<=[。！？!?])\s+', chunk)
            current = []
            current_len = 0
            for sent in sentences:
                if current_len + len(sent) <= chunk_size:
                    current.append(sent)
                    current_len += len(sent)
                else:
                    if current:
                        final_chunks.append(' '.join(current))
                    current = [sent]
                    current_len = len(sent)
            if current:
                final_chunks.append(' '.join(current))
    
    return final_chunks

def get_embedder(model_type: str):
    """Get embedding model based on type"""
    if model_type == 'local':
        try:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer('all-MiniLM-L6-v2')
            class LocalEmbedder:
                def encode(self, texts):
                    return model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
            return LocalEmbedder()
        except ImportError:
            raise ImportError("sentence-transformers not installed. Run: pip install sentence-transformers")
    
    elif model_type == 'openai':
        try:
            import openai
            from openai import OpenAI
            client = OpenAI()
            class OpenAIEmbedder:
                def encode(self, texts):
                    embeddings = []
                    batch_size = 100
                    for i in range(0, len(texts), batch_size):
                        batch = texts[i:i+batch_size]
                        response = client.embeddings.create(
                            model="text-embedding-3-small",
                            input=batch
                        )
                        embeddings.extend([np.array(d.embedding) for d in response.data])
                    return np.array(embeddings)
            return OpenAIEmbedder()
        except ImportError:
            raise ImportError("openai not installed. Run: pip install openai")
    
    else:
        raise ValueError(f"Unknown model type: {model_type}")

def main():
    parser = argparse.ArgumentParser(description='Build vector index for lightweight KB')
    parser.add_argument('--kb-dir', required=True, help='Knowledge base root directory')
    parser.add_argument('--chunk-size', type=int, default=512, help='Chunk size in characters')
    parser.add_argument('--chunk-overlap', type=int, default=50, help='Chunk overlap in characters')
    parser.add_argument('--model', choices=['local', 'openai'], default='local', help='Embedding model type')
    args = parser.parse_args()
    
    kb_dir = Path(args.kb_dir).expanduser()
    index_dir = kb_dir / '.index'
    index_dir.mkdir(exist_ok=True)
    
    # Collect all supported files
    chunks = []
    chunk_metadata = []
    
    print(f"Scanning files in {kb_dir}...")
    for root, _, files in os.walk(kb_dir):
        root_path = Path(root)
        # Skip index directory
        if '.index' in str(root_path):
            continue
        
        for file in files:
            file_path = root_path / file
            ext = file_path.suffix.lower()
            if ext not in SUPPORTED_EXTENSIONS:
                continue
            
            print(f"Processing {file_path}...")
            text = extract_text_from_file(file_path)
            if not text.strip():
                continue
            
            file_chunks = split_text(text, args.chunk_size, args.chunk_overlap)
            rel_path = file_path.relative_to(kb_dir)
            
            for i, chunk in enumerate(file_chunks):
                chunks.append(chunk)
                # Extract nearest heading for context
                lines = chunk.split('\n')
                heading = None
                for line in lines:
                    if line.startswith('#'):
                        heading = line.lstrip('#').strip()
                        break
                
                chunk_metadata.append({
                    'file_path': str(rel_path),
                    'chunk_index': i,
                    'heading': heading,
                    'text': chunk
                })
    
    print(f"Total chunks: {len(chunks)}")
    
    if not chunks:
        print("No text chunks found. Exiting.")
        return
    
    print(f"Generating embeddings with {args.model} model...")
    embedder = get_embedder(args.model)
    embeddings = embedder.encode(chunks)
    
    # Save chunks metadata
    chunks_file = index_dir / 'chunks.jsonl'
    with open(chunks_file, 'w', encoding='utf-8') as f:
        for meta in chunk_metadata:
            f.write(json.dumps(meta, ensure_ascii=False) + '\n')
    
    # Save embeddings
    embeddings_file = index_dir / 'embeddings.npz'
    np.savez_compressed(embeddings_file, embeddings=embeddings, model_type=args.model)
    
    print(f"\nIndex built successfully!")
    print(f"Chunks saved: {len(chunks)}")
    print(f"Index directory: {index_dir}")
    print(f"Metadata: {chunks_file}")
    print(f"Embeddings: {embeddings_file}")

if __name__ == '__main__':
    main()
