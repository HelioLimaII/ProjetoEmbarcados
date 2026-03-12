import qrcode

# Lista com os códigos que queremos transformar em imagem
codigos = [
    ("PROD-001-SOLDA", "qr_solda.png"),
    ("PROD-002-MULTIMETRO", "qr_multimetro.png"),
    ("PROD-003-OSCILOSCOPIO", "qr_osciloscopio.png"),
    ("QR-FANTASMA-999", "qr_desconhecido.png")
]

for texto, nome_arquivo in codigos:
    # Cria o QR Code
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(texto)
    qr.make(fit=True)
    
    # Salva como imagem
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(nome_arquivo)
    print(f"✅ Arquivo {nome_arquivo} gerado com o texto: {texto}")