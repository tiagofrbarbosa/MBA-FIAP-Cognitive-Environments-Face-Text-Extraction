# 🧠 Validação de Identidade com AWS Rekognition e Textract

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Este projeto demonstra como utilizar **Amazon Rekognition** e **Amazon Textract** para validar a identidade de uma pessoa com base em:

- Comparação facial entre uma **selfie** e a **foto da CNH (Carteira Nacional de Habilitação)**.
- Extração de **informações textuais** da **CNH** e de uma **conta de consumo** (ex: conta de luz ou água).

---

## 🚀 Tecnologias Utilizadas

### 📷 Amazon Rekognition
Utilizado para comparar duas imagens:
- Uma selfie enviada pelo usuário.
- Uma imagem da CNH com foto.
  
A comparação retorna uma **similaridade facial**, e o projeto considera como **válido** quando o valor for **≥ 95%**.

### 📄 Amazon Textract
Empregado para **extrair textos** de documentos enviados:
- **CNH**: para leitura de nome, CPF, data de nascimento, entre outros campos relevantes.
- **Conta de consumo**: para verificar endereço, titularidade, entre outras informações úteis para validação.

---

## 📜 Licença
Distribuído sob a licença MIT — sinta-se à vontade para usar, modificar e distribuir para fins acadêmicos ou pessoais. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---
