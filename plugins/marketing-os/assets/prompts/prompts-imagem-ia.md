# Biblioteca de Prompts para Geração de Imagem IA

Prompts otimizados para **6 modelos**: Midjourney, DALL-E, Nano Banana Pro, Flux 2 Pro, GPT Image 1.5 e Seedream 4.5.

---

## Modelos Suportados

| Modelo | Fabricante | Pontos Fortes | Resolução |
|--------|------------|---------------|-----------|
| **Midjourney v6** | Midjourney | Estética artística, estilos únicos | Até 2K |
| **DALL-E 3** | OpenAI | Compreensão contextual, criatividade | 1024x1024 |
| **Nano Banana Pro** | Google DeepMind | Texto perfeito, consistência de personagem, 14 objetos | Até 2K |
| **Flux 2 Pro** | Black Forest Labs | Fotorrealismo, tipografia, cores hex | Até 4MP |
| **GPT Image 1.5** | OpenAI | UI mockups, comics, velocidade 4x | Até 4K |
| **Seedream 4.5** | ByteDance | Posters, branding, combina 6 refs | Até 4MP |

---

## Estruturas de Prompt por Modelo

### Midjourney v6
```
[SUJEITO] + [AÇÃO] + [AMBIENTE] + [ESTILO] + [ILUMINAÇÃO] + [CÂMERA] + [QUALIDADE]
+ parâmetros: --ar --v 6 --style raw --s --c --no
```

### DALL-E 3
```
Linguagem natural descritiva. Frases completas explicando contexto,
sujeito, ambiente, estilo e qualidade desejada.
```

### Nano Banana Pro (Google)
```
Linguagem natural + controles de estúdio. Suporta:
- Texto em múltiplos idiomas e fontes
- Consistência de personagem (até 5 pessoas, 14 objetos)
- Edição conversacional (in-painting, restauração, colorização)
- Método collage (mesclar até 13 imagens)
```

### Flux 2 Pro (Black Forest Labs)
```
ESTRUTURA: Subject + Action + Style + Context
- SEM negative prompts (descreva o que QUER, não o que não quer)
- Cores exatas: use hex codes (#F48120)
- Pode usar JSON estruturado para controle preciso
```

### GPT Image 1.5 (OpenAI)
```
ESTRUTURA: background/scene → subject → key details → constraints → intended use
- Texto: use "ASPAS" ou CAPS para garantir renderização
- Especifique fonte, posição e tamanho do texto
- Inclua o uso pretendido (ad, UI mock, infographic)
```

### Seedream 4.5 (ByteDance)
```
ESTRUTURA: subject description → style specification → compositional details →
           lighting/atmosphere → technical parameters
- Forte em tipografia e composição de posters
- Pode combinar até 6 imagens de referência
- Linguagem natural, não precisa ser técnico
```

---

## Prompts por Tipo de Conteúdo

### Feed Post - Lifestyle Profissional

**MIDJOURNEY:**
```
Brazilian professional woman in her 30s, working on laptop
in modern minimalist home office, indoor plants, natural
window light, lifestyle editorial photography, Canon EOS R5,
85mm lens, shallow depth of field, 8k resolution
--ar 4:5 --v 6 --style raw
```

**DALL-E 3:**
```
Create a lifestyle photograph of a Brazilian professional
woman in her 30s working on a MacBook in a modern minimalist
home office. The space has white walls, a wooden desk, and
green indoor plants. Natural light comes through a large
window creating soft shadows. The image should look like
editorial photography with a shallow depth of field.
Professional quality, high resolution.
```

**NANO BANANA PRO:**
```
Create a lifestyle editorial photograph of a confident Brazilian
businesswoman in her early 30s working on a MacBook Pro in a
modern minimalist home office. She wears a cream blazer and has
natural makeup. The space features white walls, a light oak desk,
a monstera plant, and sheer curtains filtering soft natural
daylight. Shoot with Canon EOS R5, 85mm f/1.4 lens creating
beautiful bokeh. The mood is professional yet warm and inviting.
Aspect ratio 4:5 for Instagram feed.
```

**FLUX 2 PRO:**
```
Subject: Brazilian professional woman, early 30s, cream blazer,
natural makeup, working on MacBook Pro
Action: Typing while looking at screen with subtle confident smile
Style: Lifestyle editorial photography, shallow depth of field,
Canon 85mm f/1.4 aesthetic
Context: Modern minimalist home office, white walls, light oak desk,
monstera plant, natural window light creating soft shadows
Color palette: Warm neutrals, cream #F5F5DC, sage green #9CAF88
```

**GPT IMAGE 1.5:**
```
Background: Modern minimalist home office with white walls, light
oak desk, and a large monstera plant near a window with sheer curtains.
Subject: Brazilian professional woman in her early 30s wearing a
cream blazer, natural makeup, working on a MacBook Pro with a subtle
confident smile.
Key details: Soft natural daylight filtering through curtains, shallow
depth of field with bokeh effect, lifestyle editorial photography style.
Constraints: 4:5 aspect ratio, warm neutral tones, professional yet
approachable mood.
Intended use: Instagram feed post for female entrepreneurship brand.
```

**SEEDREAM 4.5:**
```
Subject: A confident Brazilian businesswoman in her early 30s with
natural makeup, wearing an elegant cream blazer, working on a MacBook Pro.
Style: Lifestyle editorial photography with shallow depth of field
and soft bokeh, similar to Vogue Business portraits.
Composition: Woman positioned slightly left of center, laptop visible,
monstera plant in soft focus background, natural leading lines from
desk edge.
Lighting: Soft natural daylight from large window on the right,
creating gentle shadows and warm skin tones. Golden hour quality
without harsh contrasts.
Technical: Shot on 85mm lens, f/1.4 aperture, 4:5 aspect ratio,
high resolution suitable for print.
```

---

### Feed Post - Flat Lay

**MIDJOURNEY:**
```
flat lay photography, workspace essentials on marble surface,
MacBook laptop, coffee cup, notebook, pen, succulent plant,
minimalist aesthetic, soft overhead lighting, product
photography style, 8k resolution, clean organized composition
--ar 1:1 --v 6 --style raw
```

**DALL-E 3:**
```
Create a flat lay photograph shot from directly above showing
a minimalist workspace on a white marble surface. Include a
MacBook laptop, a cup of coffee, a leather notebook, a gold
pen, and a small succulent plant. The items should be
arranged in a balanced, aesthetically pleasing composition.
Soft, even lighting with minimal shadows. Product photography
style, high resolution.
```

**NANO BANANA PRO:**
```
Create a perfectly styled flat lay photograph shot from directly
overhead. On a white Carrara marble surface, arrange: a MacBook Air
(space gray), a ceramic cup of latte with latte art, a tan leather
Moleskine notebook, a gold Parker pen, a small succulent in a white
geometric pot, and scattered gold paper clips. The composition follows
the rule of thirds with intentional negative space. Soft, even studio
lighting eliminates harsh shadows. Product photography aesthetic,
ultra-sharp focus across entire frame. Square 1:1 format.
```

**FLUX 2 PRO:**
```
Subject: Flat lay workspace arrangement on white Carrara marble
Action: Static overhead product shot
Style: Minimalist product photography, soft even lighting,
ultra-sharp focus, Instagram aesthetic
Context: MacBook Air space gray, ceramic latte cup with art,
tan leather notebook, gold pen, white geometric succulent pot,
scattered gold paper clips
Color palette: White marble #FFFFFF, tan leather #D2B48C,
gold accents #D4AF37, sage succulent #9CAF88
```

**GPT IMAGE 1.5:**
```
Background: White Carrara marble surface filling the entire frame,
shot from directly overhead.
Subject: Carefully arranged workspace items - MacBook Air (space gray),
ceramic cup with latte art, tan leather Moleskine notebook, gold
Parker pen, small succulent in white geometric pot, scattered gold
paper clips.
Key details: Rule of thirds composition, intentional negative space,
soft even studio lighting with no harsh shadows, ultra-sharp focus
across entire frame.
Constraints: 1:1 square aspect ratio, product photography style,
Instagram-worthy aesthetic.
Intended use: Social media content for productivity/lifestyle brand.
```

**SEEDREAM 4.5:**
```
Subject: Flat lay workspace arrangement featuring MacBook Air,
ceramic latte cup, leather notebook, gold pen, and succulent plant.
Style: Minimalist product photography, Instagram flat lay aesthetic,
clean and modern.
Composition: Overhead shot on white Carrara marble, items arranged
following rule of thirds, intentional negative space for potential
text overlay, balanced visual weight.
Lighting: Soft diffused studio lighting from above, eliminating
harsh shadows while maintaining subtle depth through gentle gradients.
Technical: Square 1:1 format, ultra-sharp focus throughout,
high resolution for print quality.
```

---

### Stories/Reels - Behind the Scenes

**MIDJOURNEY:**
```
candid photo of content creator woman preparing for video,
ring light visible, camera equipment, messy creative
workspace, authentic documentary style, warm indoor lighting,
natural unposed moment, iPhone quality aesthetic
--ar 9:16 --v 6 --style raw
```

**NANO BANANA PRO:**
```
Create an authentic behind-the-scenes moment of a female content
creator preparing for a video shoot. She's adjusting a ring light
while looking at her phone, hair slightly messy, wearing comfortable
loungewear. Her creative workspace shows camera on tripod, laptop
with editing software, scattered makeup items, and coffee cup.
The image feels candid and unposed, like a friend captured the moment.
Warm tungsten indoor lighting mixed with the ring light glow.
Vertical 9:16 format for Instagram Stories. Documentary photography
style with slight motion blur on her moving hand.
```

**FLUX 2 PRO:**
```
Subject: Female content creator in loungewear, hair slightly messy,
adjusting ring light while checking phone
Action: Candid moment of preparation, unposed and authentic,
slight motion blur on moving hand
Style: Documentary photography, iPhone quality aesthetic,
warm and relatable, not overly produced
Context: Creative home workspace, camera on tripod, laptop showing
editing software, scattered makeup items, half-drunk coffee,
warm tungsten lighting mixed with ring light glow
```

**GPT IMAGE 1.5:**
```
Background: Cozy creative home workspace with visible camera equipment,
laptop showing editing software, and scattered makeup items.
Subject: Female content creator in comfortable loungewear, hair
slightly messy, caught in a candid moment adjusting her ring light
while checking her phone.
Key details: Authentic unposed feeling, slight motion blur on moving
hand, warm tungsten indoor lighting mixed with ring light glow,
half-drunk coffee cup nearby.
Constraints: Vertical 9:16 format, documentary style, iPhone quality
aesthetic rather than overly produced.
Intended use: Instagram Stories behind-the-scenes content.
```

**SEEDREAM 4.5:**
```
Subject: Female content creator in comfortable loungewear adjusting
a ring light while looking at her smartphone, hair naturally messy.
Style: Candid documentary photography, authentic and unposed,
relatable "real life" aesthetic rather than staged perfection.
Composition: Vertical 9:16 Stories format, subject positioned center-left,
ring light creating circular catchlight in eyes, workspace details
visible in background.
Lighting: Warm tungsten indoor ambient light mixed with cool ring
light creating interesting color contrast. Slight overexposure on
ring light for authenticity.
Technical: Slight motion blur on moving hand, iPhone camera quality
aesthetic, vertical format optimized for Stories/Reels.
```

---

### Thumbnail YouTube

**MIDJOURNEY:**
```
surprised young woman pointing at empty text space on right,
bright solid yellow background, exaggerated facial expression
with wide eyes and open mouth, YouTube thumbnail style,
high contrast vibrant colors, clean professional studio
lighting, sharp focus on face, bold dynamic composition
--ar 16:9 --v 6
```

**NANO BANANA PRO:**
```
Create a YouTube thumbnail showing an excited young woman with an
exaggerated surprised expression - wide eyes, raised eyebrows, and
open mouth showing teeth. She's positioned on the left third of the
frame, pointing dramatically toward the right side where there's
empty space for text overlay. Bright solid yellow background (#FFD700).
Her face is the focal point with sharp focus and professional studio
lighting creating slight rim light on hair. High contrast, vibrant
saturated colors, bold and eye-catching composition. The expression
should stop the scroll. 16:9 horizontal format.
```

**FLUX 2 PRO:**
```
Subject: Young woman with exaggerated surprised expression, wide eyes,
raised eyebrows, open mouth showing teeth, pointing toward right
Action: Dynamic pointing gesture toward empty space for text
Style: YouTube thumbnail aesthetic, high contrast, vibrant saturated
colors, scroll-stopping bold composition, professional studio lighting
with rim light on hair
Context: Bright solid yellow background color #FFD700, clean and
uncluttered, woman positioned on left third
```

**GPT IMAGE 1.5:**
```
Background: Solid bright yellow (#FFD700), clean and vibrant,
filling the entire frame.
Subject: Young woman with exaggerated surprised expression - wide
eyes, raised eyebrows, open mouth showing teeth. Positioned on
the left third of the frame, pointing dramatically toward the
empty right side.
Key details: Professional studio lighting with subtle rim light
on hair, sharp focus on face, high contrast vibrant colors,
scroll-stopping energy.
Constraints: 16:9 horizontal aspect ratio, empty space on right
for text overlay, YouTube thumbnail style.
Intended use: YouTube video thumbnail for viral clickability.
```

**SEEDREAM 4.5:**
```
Subject: Energetic young woman with exaggerated surprised expression -
eyes wide open, eyebrows raised high, mouth open showing teeth,
pointing dramatically toward the right.
Style: YouTube thumbnail aesthetic, bold and eye-catching, high
contrast with vibrant saturated colors, professional but energetic.
Composition: Woman positioned on left third of 16:9 frame, pointing
toward empty right side (reserved for text overlay), face is the
dominant focal point.
Lighting: Professional studio setup with main light on face and
subtle rim/hair light for depth. Clean shadows, high contrast to
pop against background.
Technical: Solid yellow background #FFD700, 16:9 horizontal format,
ultra-sharp focus on face, expression designed to stop the scroll.
```

---

### Carrossel - Ilustração Educativa

**MIDJOURNEY:**
```
minimal line art illustration, abstract business concept,
geometric shapes, soft pastel colors, flat design style,
clean white background, vector art aesthetic, modern
minimalist infographic style
--ar 4:5 --v 6 --style raw
```

**NANO BANANA PRO:**
```
Create a minimal vector-style illustration for an educational
carousel slide about business growth. Use simple geometric shapes -
circles, triangles, and abstract graph lines - to represent the
concept. Soft pastel color palette: light coral, mint green, and
soft lavender on a clean white background. Flat design aesthetic
with no gradients or shadows, similar to modern app illustrations.
The composition should be balanced with plenty of white space for
text overlay. 4:5 aspect ratio for Instagram carousel.
```

**FLUX 2 PRO:**
```
Subject: Abstract business growth concept using geometric shapes
Action: Static educational illustration
Style: Minimal flat design, vector art aesthetic, modern app
illustration style, clean lines with no gradients or shadows
Context: Simple geometric shapes (circles, triangles, abstract
graph lines), soft pastel colors, clean white background,
plenty of negative space for text overlay
Color palette: Light coral #FFB5A7, mint green #B5EAD7,
soft lavender #C7CEEA, white background #FFFFFF
```

**GPT IMAGE 1.5:**
```
Background: Clean white (#FFFFFF), minimalist with generous
negative space for text overlay.
Subject: Abstract geometric illustration representing business
growth concept - simple shapes like circles, triangles, upward
graph lines, and connecting dots.
Key details: Flat design style with no gradients or 3D effects,
clean vector aesthetic, balanced composition with visual hierarchy.
Constraints: 4:5 aspect ratio, soft pastel palette (coral #FFB5A7,
mint #B5EAD7, lavender #C7CEEA), modern app illustration style.
Intended use: Educational Instagram carousel slide about business concepts.
```

**SEEDREAM 4.5:**
```
Subject: Abstract geometric illustration representing business
growth - circles, triangles, upward trending lines, and connecting
nodes forming a cohesive visual metaphor.
Style: Minimal flat design, modern vector illustration aesthetic
similar to Notion or Stripe illustrations, clean and professional.
Composition: 4:5 Instagram carousel format, balanced arrangement
with generous white space on top and bottom for text overlay,
visual elements centered.
Lighting: N/A (flat illustration style, no lighting effects,
pure flat colors without gradients or shadows).
Technical: Soft pastel palette (coral, mint, lavender), clean
white background, crisp vector edges, suitable for educational
content and infographics.
```

---

## Prompts por Nicho

### Marketing Digital

**MIDJOURNEY:**
```
digital marketing professional analyzing data on multiple
screens, modern tech office, blue accent lighting, futuristic
corporate aesthetic, cinematic lighting, wide angle shot,
tech startup atmosphere, 8k resolution
--ar 4:5 --v 6 --style raw
```

**FLUX 2 PRO:**
```
Subject: Digital marketing professional analyzing dashboard data
on ultrawide curved monitor
Action: Focused work pose, hand on chin in contemplation,
data visualizations reflecting in glasses
Style: Tech corporate photography, futuristic aesthetic,
cinematic lighting with blue accent tones
Context: Modern open-plan tech office, standing desk, multiple
screens showing analytics dashboards, ambient RGB lighting,
startup atmosphere
Color palette: Deep blue #1E3A5F, electric blue accent #00D4FF,
neutral grays, screen glow
```

**NANO BANANA PRO:**
```
Create a cinematic photograph of a digital marketing professional
in a modern tech office. They're analyzing real-time data on an
ultrawide curved monitor showing marketing dashboards with graphs
and metrics. The office has futuristic blue accent lighting,
standing desks, and floor-to-ceiling windows showing a city skyline
at dusk. The person wears smart casual attire and has a focused,
contemplative expression with data visualizations subtly reflecting
in their glasses. Wide angle shot capturing the tech startup
atmosphere. Cinematic color grading with teal and orange tones.
```

### Empreendedorismo Feminino

**MIDJOURNEY:**
```
confident Brazilian businesswoman in elegant outfit,
modern office with rose gold accents, natural lighting,
empowering portrait, editorial fashion photography,
soft bokeh background, Canon 85mm f/1.4, warm tones
--ar 4:5 --v 6 --style raw
```

**FLUX 2 PRO:**
```
Subject: Confident Brazilian businesswoman in her 30s, elegant
cream pantsuit, gold jewelry, natural makeup, power pose
Action: Standing with arms crossed confidently, subtle warm smile,
direct eye contact with camera
Style: Editorial fashion portrait, empowering feminine aesthetic,
Canon 85mm f/1.4 shallow depth of field
Context: Modern office with rose gold accents, blush pink and
white decor, natural window light, soft bokeh background
Color palette: Cream #FFFDD0, rose gold #B76E79, blush pink #FFB6C1,
warm skin tones
```

**SEEDREAM 4.5:**
```
Subject: Confident Brazilian businesswoman in her mid-30s wearing
an elegant cream pantsuit with delicate gold jewelry. Natural
makeup, warm smile, direct eye contact conveying strength and
approachability.
Style: Editorial fashion portrait meets corporate photography,
empowering feminine aesthetic, magazine-quality lighting.
Composition: 4:5 portrait format, subject positioned using rule
of thirds, shallow depth of field with beautiful bokeh, negative
space above for potential quote overlay.
Lighting: Soft natural window light from the side creating gentle
shadows and warm skin tones, hint of rim light on hair.
Technical: Modern office with rose gold and blush pink accents
in soft focus background, 85mm portrait lens aesthetic, warm
color grading.
```

### Finanças Pessoais

**FLUX 2 PRO:**
```
Subject: Professional financial advisor at organized desk,
approachable expression, smart casual attire
Action: Explaining concept with hands, engaged and trustworthy
body language
Style: Corporate editorial photography, trust-inspiring aesthetic,
neutral professional color palette
Context: Clean organized workspace, laptop showing financial charts,
small plant, natural window light, business casual atmosphere
Color palette: Navy blue #1E3A5F, forest green #228B22 (money/growth),
warm neutrals, white
```

### Desenvolvimento Pessoal

**FLUX 2 PRO:**
```
Subject: Peaceful person in meditation pose at sunrise
Action: Seated meditation, eyes closed, serene expression,
hands in mudra position
Style: Wellness lifestyle photography, ethereal atmospheric quality,
inspirational self-care aesthetic
Context: Peaceful outdoor setting, golden hour sunrise, soft
morning mist, nature elements (grass, distant trees)
Color palette: Golden sunrise #FFD700, soft orange #FFAB40,
pale blue sky #87CEEB, natural greens
```

### Fitness/Saúde

**FLUX 2 PRO:**
```
Subject: Athletic woman mid-workout, dynamic action pose,
showing strength and determination
Action: High-energy movement (box jump, kettlebell swing, or sprint),
sweat visible, muscles engaged
Style: Sports photography, Nike/Adidas campaign aesthetic,
dramatic lighting with motion energy
Context: Modern gym with industrial elements, dramatic directional
lighting, motion blur suggesting speed and power
Color palette: Black, white, neon accent color #FF6B35 or #00FF87
```

### Tech/Programação

**FLUX 2 PRO:**
```
Subject: Software developer focused on code, ambient RGB lighting
reflecting on face
Action: Typing on mechanical keyboard, code visible on ultrawide
monitor, deep concentration
Style: Cyberpunk tech aesthetic, moody atmospheric photography,
cinematic color grading
Context: Dark room with RGB ambient lighting, multiple monitors
showing code, mechanical keyboard, minimalist desk setup
Color palette: Deep purple #2D1B4E, neon cyan #00FFFF,
neon pink #FF00FF, dark background
```

---

## Prompts com Texto Integrado

### Para Nano Banana Pro (melhor renderização de texto):

```
Create an Instagram carousel cover slide with the headline
"5 ERROS QUE ESTÃO MATANDO SEU INSTAGRAM" in bold Impact font,
white text with black outline, positioned at the top third.
Below, show a frustrated content creator looking at phone with
worried expression. Background is gradient from coral to pink.
The text must be perfectly legible and spelled correctly.
4:5 aspect ratio.
```

### Para Flux 2 Pro (usando hex para cores exatas):

```
Subject: Motivational quote poster design
Style: Modern minimalist typography poster, bold sans-serif font,
clean professional design
Context: Quote text "COMECE ANTES DE ESTAR PRONTO" in bold white
Impact font, centered, on solid background color #FF6B35 (vibrant coral)
Text must be: perfectly spelled, centered horizontally, large and bold,
white color #FFFFFF with subtle shadow for depth
```

### Para GPT Image 1.5 (usando CAPS e aspas):

```
Background: Solid deep teal (#008080) filling entire frame.
Subject: Typography-focused motivational poster with the quote
"FEITO É MELHOR QUE PERFEITO" in large bold white Impact font.
Key details: Text must be PERFECTLY SPELLED AND LEGIBLE, centered
both horizontally and vertically, white color with subtle drop shadow.
Constraints: 4:5 portrait aspect ratio, minimalist design with only
text and background, professional typography poster style.
Intended use: Instagram motivational quote post.
```

### Para Seedream 4.5 (forte em posters):

```
Subject: Typographic motivational poster with the phrase
"O SUCESSO É CONSTRUÍDO UM DIA DE CADA VEZ"
Style: Modern minimalist poster design, bold typography as the
hero element, professional graphic design aesthetic.
Composition: Text centered on 4:5 canvas, generous margins,
hierarchy with main quote large and bold, potential for smaller
attribution text below.
Lighting: N/A (graphic design, not photography)
Technical: Deep teal background #008080, white text #FFFFFF,
Impact or Montserrat Extra Bold font style, text must be
perfectly readable and correctly spelled.
```

---

## Negative Prompts

### Geral (Midjourney/Stable Diffusion)
```
cartoon, illustration, 3d render, anime, drawing,
painting, artificial, fake, stock photo feeling,
oversaturated, blurry, low quality, watermark,
text, logo, signature
```

### Para Pessoas
```
deformed, ugly, mutilated, disfigured, extra limbs,
extra fingers, fused fingers, bad anatomy, bad
proportions, gross proportions, malformed limbs,
missing arms, missing legs, extra arms, extra legs
```

### Para Produtos
```
distorted, warped, unnatural colors, unrealistic
shadows, floating objects, impossible physics,
cluttered, messy, unprofessional
```

> ⚠️ **IMPORTANTE**: Flux 2 Pro NÃO suporta negative prompts!
> Descreva apenas o que você QUER ver, não o que não quer.

---

## Parâmetros por Modelo

### Midjourney v6
```
--ar [ratio]     Aspect ratio (1:1, 4:5, 9:16, 16:9)
--v 6            Versão do modelo
--style raw      Menos estilizado, mais fotográfico
--q 2            Qualidade máxima
--s [0-1000]     Stylize (baixo = mais literal)
--c [0-100]      Chaos (variação)
--no [item]      Excluir elemento
--seed [número]  Reproduzir resultado
```

### Flux 2 Pro
```
Sem parâmetros técnicos - usa linguagem natural
Cores: especifique hex codes (#FF6B35)
Estrutura JSON opcional para controle preciso:
{
  "scene": "descrição do ambiente",
  "subjects": "descrição dos sujeitos",
  "style": "estilo fotográfico",
  "lighting": "tipo de iluminação",
  "camera": "configurações de câmera",
  "color_palette": ["#hex1", "#hex2", "#hex3"]
}
```

### GPT Image 1.5
```
Texto: use "ASPAS" ou CAPS para garantir renderização
Especifique: fonte, posição, tamanho, cor do texto
Inclua "intended use" no final do prompt
Quality options: standard, hd
```

### Seedream 4.5
```
Suporta até 6 imagens de referência simultâneas
Resolução máxima: 2048x2048 (4MP)
Linguagem natural, sem parâmetros técnicos
Forte em tipografia e composição de posters
```

### Nano Banana Pro
```
Texto: especifique idioma, fonte e posição
Consistência: pode manter mesmo personagem em várias cenas
Collage: pode mesclar até 13 imagens
Edição: suporta comandos conversacionais de edição
```

---

## Fluxo de Iteração

```
1. PROMPT INICIAL
   └── Gerar 4 variações

2. AVALIAR RESULTADOS
   ├── Composição ok?
   ├── Iluminação ok?
   ├── Sujeito ok?
   ├── Texto legível? (se aplicável)
   └── Estilo ok?

3. REFINAR
   ├── Adicionar detalhes faltantes
   ├── Ajustar cores (use hex codes)
   ├── Especificar melhor o que quer
   └── Tentar modelo diferente se necessário

4. UPSCALE/ENHANCE
   └── Selecionar melhor e aumentar resolução

5. PÓS-PRODUÇÃO
   └── Ajustes finais em editor (se necessário)
```

---

## Qual Modelo Usar?

| Necessidade | Modelo Recomendado |
|-------------|-------------------|
| Texto/Tipografia perfeita | Nano Banana Pro ou Seedream 4.5 |
| Fotorrealismo | Flux 2 Pro |
| Estilo artístico único | Midjourney |
| UI Mockups/Comics | GPT Image 1.5 |
| Posters e Branding | Seedream 4.5 |
| Consistência de personagem | Nano Banana Pro |
| Velocidade | GPT Image 1.5 (4x mais rápido) |
| Edição de imagem | Nano Banana Pro ou Seedream 4.5 |
| Cores exatas (hex) | Flux 2 Pro |

---

## Fontes e Documentação

- [Nano Banana Pro Guide](https://www.imagine.art/blogs/nano-banana-pro-prompt-guide)
- [Flux 2 Pro Official Guide](https://docs.bfl.ml/guides/prompting_guide_flux2)
- [GPT Image 1.5 Cookbook](https://cookbook.openai.com/examples/multimodal/image-gen-1.5-prompting_guide)
- [Seedream 4.5 Guide](https://fal.ai/learn/devs/seedream-v4-5-prompt-guide)
