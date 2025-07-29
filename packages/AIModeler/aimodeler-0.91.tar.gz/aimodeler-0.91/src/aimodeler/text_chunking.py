import tiktoken

MAX_TOKENS = 512
OVERLAP = 64
TOKENIZER = tiktoken.encoding_for_model("text-embedding-ada-002")

def chunk_text(filenames, documents, max_tokens=MAX_TOKENS, overlap=OVERLAP):

    chunks = []
    sources = []
    
    for idx, document in enumerate(documents):

        tokens = TOKENIZER.encode(document)
        
        source = filenames[idx] if filenames else f"document_{idx}"
        
        i = 0
        while i < len(tokens):
            chunk = tokens[i:i + max_tokens]
            chunks.append(TOKENIZER.decode(chunk))
            sources.append(filenames[idx])
            i += max_tokens - overlap
    
    return chunks, sources
