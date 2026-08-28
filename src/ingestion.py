from pathlib import Path

VAULT_PATH = Path("data/vault")

def load_markdown_files(vault_path:Path):
  documents=[]
  
  for file_path in vault_path.rglob("*.md"):
    try:
      content = file_path.read_text(encoding="utf-8")
      
      documents.append({
        "source":str(file_path),
        "content":content
      })
      
    except Exception as error:
      print(f"Could not read {file_path}: {error}")
      
  return documents


if __name__ == "__main__":
  documents = load_markdown_files(VAULT_PATH)
  
  print(f"\nLoaded {len(documents)} Markdown files.\n")
  
  for document in documents:
    print("-"*60)
    print(f"source: {document['source']}")
    print(f"characters: {len(document['content'])}")
    print(document["content"][:200])
    
    