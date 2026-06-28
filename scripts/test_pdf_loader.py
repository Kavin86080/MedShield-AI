from backend.rag.ingestion.pdf_loader import PDFLoader

loader = PDFLoader()

result = loader.load(
    "datasets/medical_knowledge/pneumonia.pdf"
)

print("\n==============================")
print("STATUS")
print("==============================")
print(result["status"])

print("\n==============================")
print("METADATA")
print("==============================")
print(result["metadata"])

print("\n==============================")
print("STATISTICS")
print("==============================")
print(result["statistics"])

print("\n==============================")
print("TEXT (FIRST 1000 CHARACTERS)")
print("==============================")
print(result["text"][:1000])