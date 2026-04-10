#!/usr/bin/env python3
"""
Vector search for feishu-lightweight-kb
"""

import os
import json
import re
import numpy as np
from pathlib import Path
from collections import defaultdict

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors"""
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def keyword_score(text: str, keywords: list[str]) -> float:
    """Calculate keyword matching score"""
    score = 0.0
    text_lower = text.lower()
    for kw in keywords:
        if kw.lower() in text_lower:
            # Count occurrences
            count = len(re.findall(re.escape(kw.lower()), text_lower))
            score += count * (1 + 0.1 * count)  # Bonus for multiple occurrences
    return score

def expand_keywords(query: str) -> list[str]:
    """Basic keyword expansion - can be extended with synonyms"""
    query = query.lower()
    keywords = [query]
    
    # Split into individual words
    words = re.findall(r'[\w]+', query)
    if len(words) > 1:
        keywords.extend(words)
    
    # Add common synonyms for typical business terms
    synonyms = {
        '报销': ['费用报销', '差旅报销', '报账', 'reimbursement'],
        '入职': ['新员工', 'onboarding', '报到'],
        '离职': ['辞职', 'offboarding', '离开'],
        '请假': ['休假', '请假申请', '缺勤'],
        '审批': ['审核', '批准', '审批流程', 'approval'],
        '培训': ['课程', '学习', 'training'],
        '预算': ['预算申请', '费用预算', 'finance'],
        '项目': ['project', '项目管理'],
        '政策': ['制度', '规定', 'policy'],
    }
    
    for word in words:
        if word in synonyms:
            keywords.extend(synonyms[word])
    
    # Remove duplicates while preserving order
    seen = set()
    result = []
    for kw in keywords:
        if kw not in seen:
            seen.add(kw)
            result.append(kw)
    
    return result

class VectorSearch:
    def __init__(self, kb_dir: str, model_type: str = None):
        self.kb_dir = Path(kb_dir).expanduser()
        self.index_dir = self.kb_dir / '.index'
        self.chunks = []
        self.embeddings = None
        self.model_type = model_type
        self.embedder = None
        self._load_index()
    
    def _load_index(self):
        """Load index from disk"""
        if not self.index_dir.exists():
            print(f"Index directory {self.index_dir} does not exist. Fallback to keyword search only.")
            return False
        
        chunks_file = self.index_dir / 'chunks.jsonl'
        embeddings_file = self.index_dir / 'embeddings.npz'
        
        if not chunks_file.exists() or not embeddings_file.exists():
            print(f"Index files not found. Please build index first.")
            return False
        
        # Load chunks
        self.chunks = []
        with open(chunks_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    self.chunks.append(json.loads(line))
        
        # Load embeddings
        data = np.load(embeddings_file)
        self.embeddings = data['embeddings']
        if self.model_type is None and 'model_type' in data:
            self.model_type = str(data['model_type'])
        
        print(f"Loaded index: {len(self.chunks)} chunks, model_type={self.model_type}")
        return True
    
    def _get_embedder(self):
        """Get embedder lazily"""
        if self.embedder is not None:
            return self.embedder
        
        if self.model_type == 'local':
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer('all-MiniLM-L6-v2')
            class LocalEmbedder:
                def encode(self, text):
                    return model.encode(text, convert_to_numpy=True)
            self.embedder = LocalEmbedder()
        
        elif self.model_type == 'openai':
            from openai import OpenAI
            client = OpenAI()
            class OpenAIEmbedder:
                def encode(self, text):
                    response = client.embeddings.create(
                        model="text-embedding-3-small",
                        input=[text]
                    )
                    return np.array(response.data[0].embedding)
            self.embedder = OpenAIEmbedder()
        
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
        
        return self.embedder
    
    def has_index(self):
        """Check if index exists and is loaded"""
        return self.embeddings is not None and len(self.chunks) > 0
    
    def search(self, query: str, top_k: int = 10, hybrid_alpha: float = 0.7) -> list[dict]:
        """
        Hybrid search: vector similarity + keyword matching
        hybrid_alpha: weight for vector similarity (1-alpha for keyword)
        """
        if not self.has_index():
            return []
        
        # Generate query embedding
        embedder = self._get_embedder()
        query_embedding = embedder.encode(query)
        
        # Compute vector similarities
        similarities = np.array([
            cosine_similarity(query_embedding, doc_emb)
            for doc_emb in self.embeddings
        ])
        
        # Get top-k from vector search
        vector_top_indices = similarities.argsort()[-top_k*2:][::-1]
        
        # Expand keywords for keyword scoring
        keywords = expand_keywords(query)
        
        # Compute hybrid scores for vector candidates
        candidate_scores = []
        for idx in vector_top_indices:
            chunk = self.chunks[idx]
            vec_score = similarities[idx]
            kw_score = keyword_score(chunk['text'], keywords)
            # Normalize keyword score (0 ~ max 5)
            norm_kw_score = min(kw_score / 5.0, 1.0)
            # Hybrid score: weighted combination
            hybrid_score = hybrid_alpha * vec_score + (1 - hybrid_alpha) * norm_kw_score
            candidate_scores.append((hybrid_score, idx, vec_score, kw_score))
        
        # Sort by hybrid score
        candidate_scores.sort(reverse=True, key=lambda x: x[0])
        
        # Take top-k results
        results = []
        seen_files = defaultdict(int)
        for score, idx, vec_score, kw_score in candidate_scores[:top_k]:
            chunk = self.chunks[idx]
            # Limit results per file to avoid domination
            if seen_files[chunk['file_path']] >= 3:
                continue
            seen_files[chunk['file_path']] += 1
            
            results.append({
                'file_path': chunk['file_path'],
                'full_path': str(self.kb_dir / chunk['file_path']),
                'heading': chunk['heading'],
                'text': chunk['text'],
                'score': score,
                'vector_score': vec_score,
                'keyword_score': kw_score,
                'chunk_index': chunk['chunk_index']
            })
        
        return results

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Vector search in lightweight KB')
    parser.add_argument('--kb-dir', required=True, help='Knowledge base root directory')
    parser.add_argument('--query', required=True, help='Search query')
    parser.add_argument('--top-k', type=int, default=10, help='Number of results to return')
    parser.add_argument('--alpha', type=float, default=0.7, help='Weight for vector similarity (0-1)')
    parser.add_argument('--model', help='Model type (local/openai), inferred from index if not given')
    args = parser.parse_args()
    
    vs = VectorSearch(args.kb_dir, model_type=args.model)
    if not vs.has_index():
        print("No index available. Please build index first.")
        return
    
    results = vs.search(args.query, args.top_k, args.alpha)
    
    print(f"\nSearch results for: {args.query}")
    print("-" * 80)
    
    for i, r in enumerate(results, 1):
        print(f"\n{i}. Score: {r['score']:.4f} (vector: {r['vector_score']:.4f}, keyword: {r['keyword_score']:.2f})")
        print(f"   File: {r['file_path']}")
        if r['heading']:
            print(f"   Heading: {r['heading']}")
        print(f"   Preview: {r['text'][:200]}...")
    
    print()

if __name__ == '__main__':
    main()
