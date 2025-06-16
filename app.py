import streamlit as st
import boto3
import re
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# Função para converter imagem em bytes
def image_to_bytes(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    return buffer.getvalue()

# Interface do Streamlit
st.title("Validação Facial e Textual com AWS Rekognition e Textract")

ACCESS_ID = st.text_input("AWS ACCESS_KEY_ID", type="password")
ACCESS_KEY = st.text_input("AWS SECRET_ACCESS_KEY", type="password")
region = "us-east-1"

source_file = st.file_uploader("Upload da CNH (Fonte)", type=["jpg", "jpeg", "png"])
target_file = st.file_uploader("Upload da Selfie (Destino)", type=["jpg", "jpeg", "png"])
utility_file = st.file_uploader("Upload da Conta de Consumo", type=["jpg", "jpeg", "png"])

if st.button("Autenticar") and ACCESS_ID and ACCESS_KEY and source_file and target_file and utility_file:
    session = boto3.Session(
        aws_access_key_id=ACCESS_ID,
        aws_secret_access_key=ACCESS_KEY,
        region_name=region
    )
    rekognition = session.client("rekognition")
    textract = session.client("textract")

    # Comparação de rostos
    source_bytes = image_to_bytes(source_file)
    target_bytes = image_to_bytes(target_file)
    utility_bytes = image_to_bytes(utility_file)

    rekognition_response = rekognition.compare_faces(
        SourceImage={"Bytes": source_bytes},
        TargetImage={"Bytes": target_bytes},
        SimilarityThreshold=90
    )

    similaridade = 0
    for match in rekognition_response.get("FaceMatches", []):
        similaridade = match["Similarity"]

    # Extração da CNH (nome e CPF)
    textract_response_cnh = textract.detect_document_text(Document={"Bytes": source_bytes})
    all_text_cnh = "\n".join([b["Text"] for b in textract_response_cnh["Blocks"] if b["BlockType"] == "LINE"])
    
    cpf_match = re.search(r"\d{3}\.\d{3}\.\d{3}-\d{2}", all_text_cnh)
    nome_cnh = None
    linhas = all_text_cnh.split("\n")
    for i, linha in enumerate(linhas):
        if "NOME" in linha.upper():
            nome_cnh = linhas[i + 1].strip() if i + 1 < len(linhas) else None
            break
    cpf_cnh = cpf_match.group() if cpf_match else "CPF não encontrado"

    # Extração da conta de consumo (nome e endereço)
    textract_response_utility = textract.detect_document_text(Document={"Bytes": utility_bytes})
    all_text_utility = "\n".join([b["Text"] for b in textract_response_utility["Blocks"] if b["BlockType"] == "LINE"])
    
    nome_match = re.search(r"Nome do Cliente:\s*(.*)", all_text_utility)
    endereco_match = re.search(r"Endereço de Fornenecimento:\s*(.*)", all_text_utility)

    nome_conta = nome_match.group(1).strip() if nome_match else "Nome não encontrado"
    endereco_conta = endereco_match.group(1).strip() if endereco_match else "Endereço não encontrado"

    # Resultado
    st.subheader("Resultados")
    st.write(f"Similaridade: {similaridade:.2f}%")
    st.write(f"Nome na CNH: {nome_cnh}")
    st.write(f"CPF na CNH: {cpf_cnh}")
    st.write(f"Nome na Conta: {nome_conta}")
    st.write(f"Endereço: {endereco_conta}")

    if similaridade > 90 and nome_cnh and nome_conta and nome_cnh.lower() == nome_conta.lower():
        st.success("✅ Cliente autenticado com sucesso!")
    else:
        st.error("❌ Cliente não pôde ser autenticado.")
