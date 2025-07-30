#!/usr/bin/env python3
import argparse
import sys
import asyncio
import json
from svo_chunker.svo_chunker import SVOChunker

async def chunk_text(input_text, host, port, output_stream, show_vectors, use_gpu):
    chunker = SVOChunker(use_gpu=use_gpu)
    print(f"[CLI] SVOChunker use_gpu={use_gpu}")
    chunk_pairs = await chunker.chunk_by_sv_semantics(input_text, base_url=host, port=port)
    for chunk, chunk_vector in chunk_pairs:
        out = {'chunk': chunk}
        if show_vectors:
            out['chunk_vector'] = chunk_vector
        print(json.dumps(out, ensure_ascii=False, indent=2), file=output_stream)

async def main():
    parser = argparse.ArgumentParser(
        description="SVO Semantic Chunker CLI: splits text into semantic chunks using SVO and vector proximity. Output: JSONL (chunk per line, optionally with chunk_vector)."
    )
    parser.add_argument('-i', '--input', type=str, default=None, help='Input file (default: stdin)')
    parser.add_argument('-o', '--output', type=str, default=None, help='Output file (default: stdout)')
    parser.add_argument('--host', type=str, default='http://localhost', help='Embedding service host')
    parser.add_argument('--port', type=int, default=8001, help='Embedding service port')
    parser.add_argument('-v', '--show-vectors', action='store_true', help='Show chunk vectors in output')
    parser.add_argument('--gpu', '--use-gpu', action='store_true', dest='use_gpu', help='Use GPU for Stanza (if available)')
    args = parser.parse_args()

    if args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            input_text = f.read()
    else:
        input_text = sys.stdin.read()

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as out:
            await chunk_text(input_text, args.host, args.port, out, args.show_vectors, args.use_gpu)
    else:
        await chunk_text(input_text, args.host, args.port, sys.stdout, args.show_vectors, args.use_gpu)

def reconstruct_with_separators(text, chunks):
    """
    Reconstructs the original text from chunk list, preserving all separators between chunks.
    Args:
        text (str): The original text.
        chunks (list): List of (chunk, vector) tuples, where chunk['text'] is the chunk text.
    Returns:
        str: The reconstructed text.
    """
    pos = 0
    result = []
    for i, (chunk, _) in enumerate(chunks):
        idx = text.find(chunk['text'], pos)
        if idx == -1:
            raise ValueError(f"Chunk text not found in original text: {chunk['text'][:30]}")
        # Всё, что между pos и idx — это разделитель
        if i > 0:
            result[-1] += text[pos:idx]
        result.append(chunk['text'])
        pos = idx + len(chunk['text'])
    # Если что-то осталось в конце — добавляем к последнему чанку
    if pos < len(text):
        result[-1] += text[pos:]
    return ''.join(result)

if __name__ == "__main__":
    asyncio.run(main()) 