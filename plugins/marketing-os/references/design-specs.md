# Design Specs - Especificacoes Tecnicas por Plataforma

Referencia rapida de dimensoes, formatos e safe zones para todas as plataformas.

---

## Instagram

### Dimensoes

| Formato | Tamanho | Ratio | Max File |
|---------|---------|-------|----------|
| Feed Quadrado | 1080x1080 | 1:1 | 30MB |
| Feed Retrato | 1080x1350 | 4:5 | 30MB |
| Feed Paisagem | 1080x566 | 1.91:1 | 30MB |
| Stories | 1080x1920 | 9:16 | 30MB |
| Reels | 1080x1920 | 9:16 | 4GB |
| Carrossel | 1080x1350 | 4:5 | 30MB/slide |
| Foto Perfil | 320x320 | 1:1 | - |
| Destaque | 161x161 | 1:1 | - |

### Safe Zones Stories/Reels
```
Top: 250px (username, hora)
Bottom: 250px (CTA, responder, icones)
Right: 100px (icones de interacao)
```

### Formatos de Video
- MP4 ou MOV
- H.264 codec
- 30fps recomendado
- AAC audio, 128kbps+
- Duracao: Stories 15s, Reels ate 90s

---

## TikTok

### Dimensoes

| Formato | Tamanho | Ratio |
|---------|---------|-------|
| Video | 1080x1920 | 9:16 |
| Foto Perfil | 200x200 | 1:1 |

### Safe Zones
```
Top: 150px (header)
Bottom: 150px (caption, CTA)
Right: 150px (icones de interacao)
Left: Safe
```

### Formatos de Video
- MP4 ou MOV
- Duracao: 15s a 10min
- Tamanho max: 287.6MB (mobile), 500MB (web)

---

## YouTube

### Dimensoes

| Formato | Tamanho | Ratio |
|---------|---------|-------|
| Thumbnail | 1280x720 | 16:9 |
| Shorts | 1080x1920 | 9:16 |
| Banner Canal | 2560x1440 | - |
| Foto Perfil | 800x800 | 1:1 |
| Watermark | 150x150 | 1:1 |

### Safe Zone Banner
```
Area segura (todos dispositivos): 1546x423 (centro)
TV: 2560x1440 (completo)
Desktop: 2560x423 (cortado)
Mobile: 1546x423 (muito cortado)
```

### Thumbnail Best Practices
- Texto maximo 5 palavras
- Rosto ocupa 40-60%
- Contraste alto
- Evitar texto no canto inferior direito (duracao)

---

## LinkedIn

### Dimensoes

| Formato | Tamanho | Ratio |
|---------|---------|-------|
| Post Imagem | 1200x1200 | 1:1 |
| Post Retrato | 1080x1350 | 4:5 |
| Artigo Cover | 1280x720 | 16:9 |
| Banner Perfil | 1584x396 | 4:1 |
| Banner Company | 1128x191 | - |
| Foto Perfil | 400x400 | 1:1 |
| Carrossel PDF | 1080x1080 | 1:1 |

### Limites
- Imagem: max 5MB
- PDF Carrossel: max 100MB, 300 paginas
- Video: max 5GB, 10min

---

## Twitter/X

### Dimensoes

| Formato | Tamanho | Ratio |
|---------|---------|-------|
| Post 1 Imagem | 1200x675 | 16:9 |
| Post 2 Imagens | 700x800 | 7:8 |
| Post 3-4 Imagens | 700x800 | 7:8 |
| Header | 1500x500 | 3:1 |
| Foto Perfil | 400x400 | 1:1 |

### Limites
- Imagem: max 5MB (JPG/PNG), 15MB (GIF)
- Video: max 512MB, 2:20min

---

## Pinterest

### Dimensoes

| Formato | Tamanho | Ratio |
|---------|---------|-------|
| Pin Padrao | 1000x1500 | 2:3 |
| Pin Longo | 1000x2100 | 1:2.1 |
| Pin Quadrado | 1000x1000 | 1:1 |
| Board Cover | 222x150 | - |
| Foto Perfil | 165x165 | 1:1 |

### Best Practices
- Ratio 2:3 tem melhor performance
- Pins muito longos (>2100px) sao cortados
- Texto grande e legivel
- Cores vibrantes performam melhor

---

## Facebook

### Dimensoes

| Formato | Tamanho | Ratio |
|---------|---------|-------|
| Post Feed | 1200x630 | 1.91:1 |
| Post Quadrado | 1200x1200 | 1:1 |
| Stories | 1080x1920 | 9:16 |
| Cover Pagina | 820x312 | - |
| Cover Evento | 1920x1080 | 16:9 |
| Foto Perfil | 180x180 | 1:1 |

---

## Formatos de Exportacao

### Para Web/Social
```
Imagens estaticas: JPG (fotos), PNG (graficos/texto)
Qualidade: 80-90% JPG
Resolucao: 72dpi
Cor: sRGB
```

### Para Impressao
```
Formato: PDF, TIFF, PNG
Resolucao: 300dpi
Cor: CMYK
Sangria: +3mm
```

### Nomenclatura de Arquivos
```
[plataforma]_[tipo]_[data]_[versao].[ext]

Exemplos:
instagram_feed_20260128_v1.jpg
youtube_thumb_20260128_v2.png
linkedin_carrossel_20260128_v1.pdf
```
