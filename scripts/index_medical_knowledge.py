import os

from rag.pipelines.pdf_rag_pipeline import (
    PDFRAGPipeline
)

KNOWLEDGE_DIR = (
    "datasets/medical_knowledge"
)


def main():

    pipeline = PDFRAGPipeline()

    pdf_files = [

        os.path.join(
            KNOWLEDGE_DIR,
            file
        )

        for file in os.listdir(
            KNOWLEDGE_DIR
        )

        if file.lower().endswith(
            ".pdf"
        )
    ]

    print(
        f"\nFound {len(pdf_files)} PDFs\n"
    )

    total_chunks = 0

    for pdf_path in pdf_files:

        try:

            print(
                f"Indexing: {pdf_path}"
            )

            chunks = (
                pipeline.index_pdf(
                    pdf_path
                )
            )

            total_chunks += (
                chunks
            )

            print(
                f"Chunks: {chunks}"
            )

        except Exception as e:

            print(
                f"Failed: {pdf_path}"
            )

            print(e)

    print(
        "\n=================================="
    )

    print(
        f"Total Chunks: {total_chunks}"
    )

    print(
        "Medical Knowledge Indexed Successfully"
    )


if __name__ == "__main__":

    main()