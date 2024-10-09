from tkinter import Tk, Label, filedialog, messagebox
from PIL import Image
import piexif
import os
import pyodbc

# Função para criar a conexão com o banco de dados no SQL Server
def conectar_bd():
    try:
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS01;DATABASE=ImagensDrones;Trusted_Connection=yes;')
        cursor = conn.cursor()
        
        return conn
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao conectar ao banco de dados: {e}")
        return None

# Função para criar a tabela no banco de dados SQL Server
def criar_tabela():
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS Imagens')  # Remove tabela antiga se existir
        cursor.execute('''
            CREATE TABLE Imagens (
                id INT IDENTITY(1,1) PRIMARY KEY,
                nome NVARCHAR(255),
                caminho_arquivo NVARCHAR(500),
                data_captura NVARCHAR(50),
                cidade NVARCHAR(255),
                pais NVARCHAR(255),
                cep NVARCHAR(20),
                localizacao_gps NVARCHAR(100),
                tamanho_imagem FLOAT,
                tipo_arquivo NVARCHAR(10)
            )
        ''')
        conn.commit()
        conn.close()

# Função para extrair metadados da imagem
def extrair_metadados(caminho_imagem):
    try:
        imagem = Image.open(caminho_imagem)
        metadados = piexif.load(imagem.info['exif'])

        # Extração de informações
        data_captura = metadados['Exif'].get(piexif.ExifIFD.DateTimeOriginal, b'').decode('utf-8') if piexif.ExifIFD.DateTimeOriginal in metadados['Exif'] else 'Data não disponível'
        gpsinfo = metadados.get('GPS', {})
        lat = gpsinfo.get(piexif.GPSIFD.GPSLatitude, None)
        lng = gpsinfo.get(piexif.GPSIFD.GPSLongitude, None)

        # Outros campos personalizados pelo usuário
        cidade = "Desconhecida"
        pais = "Brasil"
        cep = "00000-000"

        return {
            'Nome': os.path.basename(caminho_imagem),
            'Caminho_arquivo': caminho_imagem,
            'Data_captura': data_captura,
            'Cidade': cidade,
            'Pais': pais,
            'CEP': cep,
            'Localizacao_gps': (lat, lng) if lat and lng else None,
            'Tamanho_imagem': os.path.getsize(caminho_imagem) / (1024 * 1024), 
        }
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao extrair metadados: {e}")
        return None

# Função para inserir os metadados no banco de dados
def inserir_metadados(metadados):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Imagens (nome, caminho_arquivo, data_captura, cidade, pais, cep, localizacao_gps, tamanho_imagem, tipo_arquivo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            metadados['Nome'],
            metadados['Caminho_arquivo'],
            metadados['Data_captura'],
            metadados['Cidade'],
            metadados['Pais'],
            metadados['CEP'],
            str(metadados['Localizacao_gps']),
            metadados['Tamanho_imagem'],
            'jpg'  
        ))
        conn.commit()
        conn.close()

# Função para selecionar imagem e extrair metadados automaticamente
def selecionar_imagem():
    caminho_imagem = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if caminho_imagem:
        metadados = extrair_metadados(caminho_imagem)
        if metadados:
            inserir_metadados(metadados)
            messagebox.showinfo("Sucesso", "Metadados extraídos e imagem processada com sucesso!")
        else:
            messagebox.showwarning("Aviso", "Não foi possível extrair os metadados.")

# Função para inicializar a interface gráfica
def iniciar_interface():
    root = Tk()
    root.title("Gerenciador de Imagens de Drones")
    
    Label(root, text="Selecione uma imagem para processar").grid(row=0, column=0, padx=10, pady=10)
    
    # Chamando a função de seleção de imagem diretamente
    selecionar_imagem()

    root.mainloop()

# Criar a tabela ao iniciar o programa
criar_tabela()

# Iniciar a interface gráfica
iniciar_interface()
