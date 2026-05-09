# Requisitos
Python 3.10
\
pip

# Instalar dependencias:
pip install chromadb
\
pip install sentence-transformers

# Cómo ejecutar
python script.py --input-folder datos_ejemplo/
\
\
\
En caso de agregar archivos de prueba se necesita borrar ChromaDB existente para no tener resultados erroneos 
\
Remove-Item -Recurse -Force chroma_db 
