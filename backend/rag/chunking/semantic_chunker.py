"""
===========================================================
MedShield-X

Semantic Chunker
===========================================================
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.rag.chunking.chunk_utils import ChunkUtils


class SemanticChunker:

    def __init__(

        self,

        chunk_size=800,

        chunk_overlap=150

    ):

        self.splitter = RecursiveCharacterTextSplitter(

            chunk_size=chunk_size,

            chunk_overlap=chunk_overlap,

            separators=[

                "\n\n",

                "\n",

                ". ",

                " ",

                ""

            ]

        )

    def chunk(

        self,

        document: dict

    ):

        text = document["clean_text"]

        chunks = self.splitter.split_text(text)

        output = []

        for index, chunk in enumerate(chunks):

            output.append(

                {

                    "chunk_id": ChunkUtils.generate_chunk_id(

                        chunk

                    ),

                    "chunk_index": index,

                    "text": chunk,

                    "statistics": ChunkUtils.calculate_chunk_length(

                        chunk

                    )

                }

            )

        document["chunks"] = output

        return document