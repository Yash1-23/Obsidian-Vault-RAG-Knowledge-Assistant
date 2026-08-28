from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

from ingestion import load_markdown_files

VAULT_PATH = Path("data/vault")


def create_chunks(documents):
  splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
    separators=["\n##", "\n###","\n\n","\n"," ", ""]
    
    
  )
  
  chunks = []
  
  for document in documents:
    split_texts = splitter.split_text(document["content"])
    
    for index, text in enumerate(split_texts):
      chunks.append({
        "source":document["source"],
        "chunk_id":index,
        "content":text
      })
      
  return chunks

if __name__ == "__main__":
  documents = load_markdown_files(VAULT_PATH)
  chunks = create_chunks(documents)
  
  print(f"\nDocuments loaded: {len(documents)}")
  print(f"Chunks created: {len(chunks)}\n")
  
  
  for chunk in chunks[:5]:
    print("-"*60)
    print(f"Source: {chunk['source']}")
    print(f"Chunk ID: {chunk['chunk_id']}")
    print(chunk["content"][:500])
    
    