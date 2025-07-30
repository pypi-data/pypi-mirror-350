# PixFlow: Image Processing Package

## 🖼️ Descrição

Este é um pacote de **processamento de imagens em Python**, desenvolvido para simplificar tarefas comuns como:

- Redimensionamento
- Transferência de histograma entre imagens
- Detecção de diferenças estruturais (SSIM)
- Leitura e salvamento de imagens
- Plotagem de imagens e histogramas

O pacote é construído utilizando bibliotecas como `scikit-image`, `matplotlib` e `numpy`.

---

## 📦 Funcionalidades

- 🔸 **Leitura e salvamento de imagens:** Suporte para formatos como `.jpg`, `.png` e outros.
- 🔸 **Redimensionamento de imagem:** Por proporção relativa.
- 🔸 **Transferência de histograma:** Ajusta os tons de uma imagem para combinar com outra.
- 🔸 **Diferença estrutural (SSIM):** Detecta e visualiza diferenças entre duas imagens.
- 🔸 **Plotagem:**
  - Exibição de imagens
  - Comparação de múltiplas imagens lado a lado
  - Visualização de histogramas dos canais RGB

---

## 🚀 Instalação

Instale diretamente do PyPI:

```bash
pip install my-image-processing
```

Ou instale localmente clonando o repositório:

```bash
git clone https://github.com/A-Chioquetta/pixflow.git
cd seu-repositorio
pip install -e .
```

## Dependências:
- Numpy
- matplotlib
- scikit-image

Instale com:
```bash
pip install -r requirements.txt
```

## Como utilizar
### Exemplo básico (contém na pasta)

```bash
from my_image_processing import (
    read_image, save_image,
    resize_image, transfer_histogram, find_difference,
    plot_image, plot_result, plot_histogram
)

# Leitura
image1 = read_image('flor1.jpg')
image2 = read_image('flor2.jpg')
image3 = read_image('flor1_alterada.jpg')

# Redimensionamento
resized = resize_image(image1, proportion=0.5)
plot_image(resized, title="Imagem Redimensionada")

# Transferência de histograma
matched = transfer_histogram(image1, image2)
plot_result(image1, image2, matched, title="Transferência de Histograma")

# Diferença estrutural
difference = find_difference(image1, image3)
plot_result(image1, image3, difference, title="Diferença Estrutural")

# Histograma
plot_histogram(image1)

# Salvamento
save_image(resized, 'resized_image.jpg')
```

## License
[MIT](LICENSE.txt)