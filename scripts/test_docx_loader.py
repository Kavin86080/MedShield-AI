from backend.rag.ingestion.docx_loader import DOCXLoader

loader = DOCXLoader()

result = loader.load(
    "datasets/uploads/docx/patient_report.docx"
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
print("TEXT")
print("==============================")
print(result["text"][:1000])