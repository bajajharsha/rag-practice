# src/main.py

from fastapi import FastAPI

from .src.app.routes import upload_routes

app = FastAPI()
app.include_router(upload_routes.router)


# import time

# from fastapi import FastAPI, File, UploadFile

# from .embed_pinecone import embed_pincone
# from .process_text import chunk_text, extract_pdf_text

# app = FastAPI()


# @app.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
#     """Process uploaded file, save it, and extract text."""
#     start_time = time.time()

#     if file.content_type == "application/pdf":
#         text = await extract_pdf_text(file)
#     else:
#         text = await file.read()
#         text = text.decode("utf-8")

#     # chunking
#     chunks = chunk_text(text)
#     print(chunks)
#     # embedding + pinecone

#     # 1. Using models hosted on Pinecone’s infrastructure.
#     embed_pincone()

#     # 2. Using an open source embedding mode then upload to Pinecone.

#     end_time = time.time()
#     print(end_time - start_time)
#     return {"result": chunks}  # Preview of extracted text
