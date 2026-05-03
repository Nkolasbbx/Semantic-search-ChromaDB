import os
import argparse
import chromadb
from chromadb.utils import embedding_functions

# Crear cliente persistente
client = chromadb.PersistentClient(path="./chroma_db")

# Embeddings
embedding_function = embedding_functions.DefaultEmbeddingFunction()

# Crear colección
collection = client.get_or_create_collection(
    name="logitrans_docs",
    embedding_function=embedding_function
)


def parse_filename(filename):
    name = filename.replace(".txt", "")
    parts = name.split("-")

    source = parts[0]
    doc_number = parts[-1]
    id_doc = "-".join(parts[1:-1])

    return {
        "source": source,
        "id_doc": id_doc,
        "doc_number": doc_number
    }


def process_files(folder):
    doc_id = 0

    for file in os.listdir(folder):
        if file.endswith(".txt"):
            metadata = parse_filename(file)
            path = os.path.join(folder, file)

            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        collection.add(
                            documents=[line],
                            metadatas=[metadata],
                            ids=[str(doc_id)]
                        )
                        doc_id += 1


def search():
    print("\nModo búsqueda (escribe 'exit' para salir)\n")

    while True:
        query = input("Consulta: ")

        if query.lower() == "exit":
            break

        results = collection.query(
            query_texts=[query],
            n_results=3
        )

        for i in range(len(results["documents"][0])):
            print("\nResultado", i + 1)
            print("Texto:", results["documents"][0][i])
            print("Metadata:", results["metadatas"][0][i])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-folder", required=True)
    args = parser.parse_args()

    print("Procesando archivos...")
    process_files(args.input_folder)
    print("Listo.")

    search()


if __name__ == "__main__":
    main()