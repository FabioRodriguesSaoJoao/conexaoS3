from datetime import datetime
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
import boto3
from botocore.exceptions import NoCredentialsError
import tempfile
import os
import io
from fastapi.responses import StreamingResponse
app = FastAPI()


s3 = boto3.client('s3',
                  aws_access_key_id='',
                  aws_secret_access_key='P')
bucket_name = ''


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/upload/image")
async def upload_file1(file: UploadFile = File(...), file_type: str = Form(...)):
    
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            file_content = await file.read()  
            tmp_file.write(file_content)
            tmp_file_path = tmp_file.name

        timestamp = str(datetime.now().timestamp())
        
        folder_path = 'infratores/'
        # Faz o upload do arquivo temporário para o S3
        s3.upload_file(tmp_file_path, bucket_name, folder_path+timestamp+"."+file_type)
        
        # Remove o arquivo temporário
        os.unlink(tmp_file_path)
        
        return timestamp+"."+file_type
    
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available")
    
@app.get("/image/ocorrencia/{filename}")
async def get_image(filename: str):
    try:
        # Faça o download da imagem do S3
        pathFilename = '/' + filename
        response = s3.get_object(Bucket=bucket_name, Key=pathFilename)
        image_data = response['Body'].read()
        # Retorne uma resposta de streaming com os dados da imagem 
        return StreamingResponse(io.BytesIO(image_data), media_type="image/png")
    
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available")
    except s3.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="File not found")
    
@app.post("/upload/comprovante")
async def upload_file1(file: UploadFile = File(...), file_type: str = Form(...)):
    
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            file_content = await file.read()  # Lê o conteúdo do arquivo
            tmp_file.write(file_content)
            tmp_file_path = tmp_file.name

        timestamp = str(datetime.now().timestamp())
        
        folder_path = 'comprovante/'
        # Faz o upload do arquivo temporário para o S3
        s3.upload_file(tmp_file_path, bucket_name, folder_path+timestamp+"."+file_type)
        
        # Remove o arquivo temporário
        os.unlink(tmp_file_path)
        
        return timestamp+"."+file_type
    
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available")