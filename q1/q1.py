

# Tentei de tudo não consegui


# Aluno: Rafael Fiel Cruz Miranda
# RM: 94654
# Turma: 3SIR

import cv2
import numpy as np
import matplotlib.pyplot as plt

def identifica_bandeira(img):
    lista_bandeiras = []

    # Converter a imagem para HSV para melhor análise de cores
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Converter para escala de cinza para encontrar contornos
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar um limiar para binarizar a imagem (melhora a detecção de contornos)
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    # Encontrar contornos das possíveis bandeiras
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Filtrar objetos muito pequenos
        if w < 50 or h < 30:
            continue

        # Extrair a região de interesse (ROI)
        roi_hsv = hsv[y:y+h, x:x+w]

        # Dividir a bandeira em três partes verticais
        left = roi_hsv[:, :w//3]      # Faixa esquerda
        center = roi_hsv[:, w//3:2*w//3]  # Faixa central
        right = roi_hsv[:, 2*w//3:]   # Faixa direita

        # Calcular a cor média para cada faixa
        mean_left = np.mean(left, axis=(0, 1))  # Cor da parte esquerda
        mean_center = np.mean(center, axis=(0, 1))  # Cor da parte central
        mean_right = np.mean(right, axis=(0, 1))  # Cor da parte direita

        # Definir a cor predominante das faixas
        # Faixa esquerda: Vermelho (HSV)
        if (0 <= mean_left[0] <= 10 or 170 <= mean_left[0] <= 180) and mean_left[1] > 50 and mean_left[2] > 100:
            color_left = 'vermelho'
        else:
            color_left = 'outro'

        # Faixa central: Branco (HSV)
        if 0 <= mean_center[0] <= 10 and mean_center[1] < 50 and mean_center[2] > 200:
            color_center = 'branco'
        else:
            color_center = 'outro'

        # Faixa direita: Vermelho (HSV)
        if (0 <= mean_right[0] <= 10 or 170 <= mean_right[0] <= 180) and mean_right[1] > 50 and mean_right[2] > 100:
            color_right = 'vermelho'
        else:
            color_right = 'outro'

        # Identificar as bandeiras conforme as cores:
        
        # 1. **Peru**: Vermelho (esquerda), Branco (centro), Vermelho (direita)
        if color_left == 'vermelho' and color_center == 'branco' and color_right == 'vermelho':
            pais = "peru"

        # 2. **Irlanda**: Verde (esquerda), Branco (centro), Laranja (direita)
        elif color_left == 'verde' and color_center == 'branco' and color_right == 'laranja':
            pais = "irlanda"

        # 3. **Singapura**: Faixa superior vermelha, inferior branca, com símbolo
        elif color_left == 'vermelho' and color_center == 'branco' and color_right == 'branco':
            pais = "singapura"

        # 4. **Mônaco**: Faixa superior vermelha, inferior branca (sem símbolo)
        elif color_left == 'vermelho' and color_center == 'branco' and color_right == 'branco':
            pais = "monaco"
        
        else:
            pais = "desconhecido"

        # Adicionar à lista de bandeiras
        lista_bandeiras.append((pais, (x, y), (x+w, y+h)))

    return lista_bandeiras


def draw_bandeiras(lista_bandeiras, img):
    for bandeira in lista_bandeiras:
        cv2.rectangle(img, bandeira[1], bandeira[2], (255, 0, 0), 5)
        cv2.putText(img, bandeira[0], bandeira[1], cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    return img


# Para testar a função identifica_bandeira
img = cv2.imread('D:/pdi-atividade2-rm94654/q1/img/teste4.png')

# Chamar a função identifica_bandeira
resultado = identifica_bandeira(img)

# Imprimir o resultado da função identifica_bandeira 
print(resultado)

# Desenhar as bandeiras na imagem
img_com_bandeiras = draw_bandeiras(resultado, img)

# Exibir a imagem com as bandeiras usando matplotlib
plt.figure(figsize=(10, 10))
plt.imshow(cv2.cvtColor(img_com_bandeiras, cv2.COLOR_BGR2RGB))
plt.axis('off')  # Desativa o eixo para visualização mais limpa
plt.show()
