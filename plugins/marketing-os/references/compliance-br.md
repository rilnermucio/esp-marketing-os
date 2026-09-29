# Compliance de publicidade no Brasil

> **Verificado em 2026-09-28** no texto integral das normas (Planalto, sites dos conselhos, AnvisaLegis, CVM, CONAR, gov.br). Serve para sinalizar risco numa peça de marketing e **não substitui parecer jurídico**. Normas mudam: revise este arquivo a cada trimestre e sempre que um conselho publicar resolução nova. Esta é a fonte canônica do plugin; em conflito com qualquer knowledge base, vale este arquivo.

## Como usar

1. **Identifique a categoria** da peça: profissão regulamentada (saúde, advocacia, educação física), produto regulado (suplemento, cosmético, medicamento), finanças, infoproduto, influenciador, e-commerce ou uso de dados pessoais. Uma peça pode cair em mais de uma.
2. **Aplique a regra mais restritiva** entre conselho, lei e plataforma. A Meta aceita antes e depois de procedimento estético para maiores de 18 anos, mas o conselho pode proibir.
3. **Confira três coisas**: identificação obrigatória, frases proibidas e aviso exigido. Aviso em letra miúda não salva promessa enganosa, porque o CONAR avalia o anúncio pelo conjunto (art. 17).
4. **Rode o checador**: `python3 scripts/compliance_check.py --input peca.md` lista os trechos de risco com a norma. O command `/checar-compliance` faz a revisão completa.

## Profissões regulamentadas

### Medicina (Res. CFM 2.336/2023, em vigor desde 11/03/2024)

Revogou as Res. 1.974/2011, 2.126/2015 e 2.133/2015.

- **Obrigatório** em toda peça e na página principal do perfil, stories incluídos: nome, CRM seguido da palavra MÉDICO, especialidade e RQE (arts. 4º e 6º). Sem RQE: "MÉDICO com pós-graduação em X" seguido de NÃO ESPECIALISTA (art. 13, §1º). No máximo 2 especialidades.
- **Permitido desde 2024**: selfie sem sensacionalismo (art. 8º, III); preço de consulta e formas de pagamento (art. 9º, VI); desconto em campanha, sem venda casada nem prêmio (art. 9º, VIII); equipamento aprovado pela Anvisa.
- **Antes e depois**: só com finalidade educativa, com texto sobre indicações, fatores que influenciam o resultado e complicações; mostrar evoluções boas, ruins e complicações; sem editar a imagem, sem identificar o paciente e com autorização (art. 14).
- **Proibido**: garantir, prometer ou insinuar bons resultados (art. 11, XII); listas e prêmios como "médico do ano" ou "melhor médico" (art. 11, XIII); sensacionalismo e autopromoção (art. 11, XVI); anunciar serviço gratuito em consultório privado (art. 11, §4º, c); prática "milagrosa" (§5º); procedimento ao vivo (VIII). Quem não é especialista não diz que trata um órgão ou doença (art. 11, I). Repost de depoimento de paciente vale como post do médico e precisa ser sóbrio (art. 8º, §3º).

### Odontologia (Código de Ética, Res. CFO-118/2012, arts. 41 a 46, alterado pela CFO-271/2025; Res. CFO-196/2019)

- **Obrigatório**: nome e número de inscrição; clínica informa também o responsável técnico (art. 43). Toda imagem ou vídeo leva nome e número do CRO (CFO-196, art. 4º).
- **Selfie**: permitida; com paciente, só com TCLE; sem mostrar equipamento, instrumental, material ou tecido (CFO-196, art. 1º).
- **Antes e depois**: só imagens de diagnóstico e de conclusão, feitas pelo dentista que executou, com TCLE, sem sensacionalismo, autopromoção ou promessa de resultado (CFO-196, art. 2º). O "durante" e caso de terceiro são proibidos. A CFO-196 vale para o dentista pessoa física.
- **Proibido**: publicidade com preços, serviços gratuitos ou modalidades de pagamento (art. 44, I); consulta grátis ou "sem compromisso" (art. 20, IX); oferecer serviço como brinde, premiação ou sorteio (art. 20, VIII, redação da CFO-271/2025); a expressão "popular" (art. 44, VII); título que não possui (art. 44, II).
- **O que a CFO-271/2025 mudou**: cumpriu decisão do CADE e liberou só descontos e cartões de desconto. Preço, gratuidade e forma de pagamento no anúncio continuam proibidos, e sorteio segue sendo infração.

### Nutrição (Res. CFN 599/2018, vigente)

A nova Res. CFN 856/2026 só entra em vigor em **23/01/2027** (prorrogação pela Res. CFN 858/2026).

- **Obrigatório**: nome, profissão e número do CRN (art. 21); avisar que o resultado pode não se repetir para todos (art. 55, parágrafo único).
- **Proibido**: mensagem enganosa ou sensacionalista, exclusividade ou garantia de resultado (art. 56); honorários, promoções ou sorteios como publicidade (art. 57); **imagem corporal própria ou de terceiros atribuindo resultado a produto, técnica ou protocolo, mesmo com autorização escrita** (art. 58); associar a própria imagem a marca de alimento, suplemento ou fitoterápico (art. 60) e fazer publicidade dessas marcas (art. 63).
- **A partir de 23/01/2027 (Res. 856)**: divulgar preço passa a ser permitido, mas promoção e sorteio seguem proibidos; mostrar resultado (imagem, composição corporal, exames, gráficos, inclusive gerados por IA) fica proibido mesmo com autorização; declarar uso de IA e patrocínio passa a ser obrigatório. O texto pode mudar até lá.

### Psicologia (Código de Ética, Res. CFP 010/2005, art. 20; Nota Técnica CFP 1/2022)

- **Obrigatório**: nome completo, CRP e número de registro (art. 20, a).
- **Proibido**: título ou qualificação que não possui (b); técnica não reconhecida (c); **preço do serviço como propaganda** (d); previsão taxativa de resultados (e); autopromoção em detrimento de colegas (f); divulgação sensacionalista (h).
- **Nota Técnica 1/2022**: sem "preço social", "desconto", "pacote promocional", "valor acessível", cupom ou sorteio. Pode divulgar convênios. Depoimento e foto de paciente só com consentimento escrito, e mesmo assim a nota desaconselha. Nada que identifique o atendido. A Res. CFP 07/2023 proíbe usar crença religiosa como publicidade.

### Advocacia (Provimento CFOAB 205/2021, vigente; Código de Ética e Disciplina, arts. 39 a 47)

A revisão do provimento está em fase final desde 12/2025, sem texto novo publicado até 2026-09-28.

- **Obrigatório**: nome, ou nome da sociedade, e número da OAB (CED, art. 44).
- **Regra geral**: publicidade informativa e sóbria, sem captação de clientela nem mercantilização (Prov. 205, art. 3º).
- **Proibido**: referência a honorários, forma de pagamento, gratuidade ou desconto como captação (art. 3º, I); especialidade sem título (III); expressões persuasivas, de autoengrandecimento ou comparação (IV); promessa de resultado e uso de casos concretos para oferta (art. 6º); ostentação de bens, veículos e viagens (art. 6º, parágrafo único); mala direta, rádio, TV e outdoor (CED, art. 40).
- **Permitido**: marketing de conteúdo, inclusive impulsionado, desde que a peça não ofereça serviço jurídico (art. 4º e Anexo Único).

### Educação física (Código de Ética CONFEF/CREFs, Res. CONFEF 508/2023)

- **Obrigatório**: nome e número de registro no CREF em qualquer publicidade (art. 4º).
- **Proibido**: conteúdo tecnicamente infundado que possa causar dano (art. 5º, XVII) e divulgação de dados sigilosos (XIII). O código não traz regra específica sobre antes e depois nem sobre preço.

### Qualquer profissional liberal (CONAR, Anexo L)

Nome, título, especialidade, endereço e número de registro no conselho.

## Produtos regulados

### Suplementos e alimentos (RDC 243/2018; IN 28/2018, Anexo V; Decreto-Lei 986/1969)

- Só as alegações do Anexo V da IN 28, **com o texto exato** (RDC 243, art. 16).
- Proibido sugerir finalidade terapêutica, dizer que a alimentação não supre as necessidades ou que o produto é superior a um alimento comum (RDC 243, art. 17).
- As regras de rotulagem valem também para a propaganda, em qualquer veículo (DL 986, art. 23).
- Rótulo traz "Este produto não é um medicamento", "Não exceder a recomendação diária de consumo indicada na embalagem" e "Mantenha fora do alcance de crianças" (RDC 243, art. 14). Nenhum aviso legitima alegação fora da lista.

### Cosméticos (RDC 907/2024, que revogou a RDC 752/2022; Lei 6.360/1976, art. 59)

- Proibido induzir a erro ou fazer alegação terapêutica, como prevenir ou tratar dor, inflamação ou varizes (RDC 907, art. 12).
- A empresa precisa ter dados de eficácia de cada benefício alegado (art. 9º, II).
- A Lei 6.360 proíbe atribuir ao produto finalidade que ele não tem (art. 59).

### Medicamentos (Lei 9.294/1996, art. 7º; Lei 6.360/1976, art. 58; RDC 96/2008)

- Remédio com receita: propaganda só em publicação para profissionais de saúde (Lei 6.360, art. 58, §1º).
- Remédio de venda livre: pode ser anunciado ao público, com advertências, sem afirmação sem comprovação científica e sem depoimento de pessoa não qualificada (Lei 9.294, art. 7º, §§1º e 2º). Frase obrigatória: "A persistirem os sintomas, o médico deverá ser consultado" (§5º).
- A Anvisa ainda lista a RDC 96/2008 como vigente; o STJ (REsp 2.035.645, 1ª Turma, 08/2024) julgou ilegais os dispositivos que vão além da Lei 9.294.

## Finanças e investimentos

Não existe norma da CVM específica para influenciador de finanças até 2026-09-28; o tema está na agenda regulatória.

- **Relatório de análise** inclui vídeo e live com conteúdo típico de análise (Res. CVM 20/2021, art. 1º, §2º) e só pode ser feito por analista credenciado (art. 2º), com declaração de independência e de conflitos (art. 21).
- **Recomendação individualizada** é consultoria (Res. CVM 19/2021, art. 1º).
- Atuar sem registro, mesmo de graça, é **crime**: detenção de 6 meses a 2 anos e multa (Lei 6.385/1976, art. 27-E).
- Frases como "isso não é recomendação" **não afastam** o caráter profissional quando há habitualidade e remuneração, mesmo indireta (Ofício-Circular CVM/SIN 13/2020).
- Usar rede social para manipular preço é infração (Res. CVM 62/2022).
- Material de fundo com rentabilidade passada leva "A rentabilidade obtida no passado não representa garantia de resultados futuros" e o aviso de que o investimento em fundos não tem garantia do administrador, do gestor, de seguro nem do FGC (Res. CVM 175/2022, art. 59).
- Influenciador contratado por instituição aderente à ANBIMA diz que é propaganda e cita a instituição (regras em vigor desde 13/11/2023).

## Publicidade em geral

### CONAR (Código Brasileiro de Autorregulamentação Publicitária, edição 2026)

- Anúncio identificado como tal (arts. 9º e 28), avaliado pelo conjunto (art. 17).
- Dado objetivo precisa ser comprovável (art. 27, §1º); preço total claro e redução de preço comprovável (§3º); "grátis" só se não houver nenhum custo (§4º).
- **Testemunhal** genuíno, comprovável e autorizado por escrito (art. 27, §9º; Anexo Q). Consumidor comum fala só da própria experiência.
- Tratamento (emagrecimento, plástica) sem depoimento de leigo nem promessa de cura (Anexo G).
- Oportunidade de ganho sem exagero de remuneração (Anexo C, item 1). Curso sem ganho irreal nem promessa de emprego, sucesso ou aprovação, salvo se o anunciante assumir a responsabilidade no próprio anúncio (Anexo B, itens 11 e 12). Projeção de ganho explica a base, os impostos e se veio de resultado passado (Anexo E).

### Guia CONAR de Influenciadores 2026 (aprovado em 11/05/2026, efeitos desde 01/06/2026)

- É publicidade toda menção feita dentro de um compromisso recíproco: contrato, comissão de afiliado, embaixador, benefício.
- Identifique com a ferramenta da plataforma ou com #publi ou #publicidade, visível logo de cara, sem precisar clicar em "mais". Nos stories, a marcação fica o tempo todo; no vídeo, no início ou no momento do endosso; na live, mantida ou repetida.
- Só o collab não basta; #ad e #adv exigem cautela. Recebidos e convites também são sinalizados (#recebido, #conviteDeMarca ou agradecimento que nomeie a marca). Vale para IA e avatares.

### Portaria Conjunta SENACON/SEDIGI/SPDIGI nº 3, de 22/09/2026

- O influenciador informa a relação comercial (pagamento, permuta, produto, sociedade, participação em receita) de forma destacada e simples, visível enquanto o conteúdo estiver no ar, inclusive em live, e também no perfil se o vínculo for contínuo (arts. 2º, V, e 9º).
- Anúncio de produto financeiro só depois de a plataforma checar o registro do anunciante (art. 5º).
- Vigência: 30 dias após a publicação (previsão: fim de outubro de 2026); ferramentas das plataformas em 90 dias.

### Código de Defesa do Consumidor (Lei 8.078/1990) e comércio eletrônico (Decreto 7.962/2013)

- Oferta suficientemente precisa obriga o fornecedor e integra o contrato (art. 30).
- Publicidade identificável de imediato; o fornecedor guarda os dados que a sustentam (art. 36).
- Proibida a publicidade enganosa, inclusive por omissão de dado essencial, e a abusiva (art. 37). O ônus da prova é de quem patrocina (art. 38). Publicidade enganosa é crime (art. 67).
- Arrependimento em 7 dias na compra fora do estabelecimento, com devolução imediata e corrigida (art. 49). A loja online explica como exercer esse direito, aceita o pedido pelo mesmo canal (Dec. 7.962, art. 5º) e mostra o preço com despesas extras e restrições da oferta (art. 2º).
- Em crédito, proibido anunciar "sem consulta ao SPC" (art. 54-C).

### Crianças e adolescentes (Lei 15.211/2025, ECA Digital, em vigor desde 17/03/2026)

Proibido usar perfilamento para direcionar publicidade a crianças e adolescentes (art. 22) e criar perfil comportamental de menores para anúncios (art. 26).

### Apostas (Portaria Interministerial MF/SECOM/MJSP nº 73/2026)

Proibido sugerir ganho fácil, apresentar aposta como renda ou investimento, exibir aposta premiada e divulgar operador não autorizado ou link de afiliado para ele. O anunciante mostra o número de autorização. (Fonte: notícia oficial do MJSP; o texto integral da portaria não foi lido nesta verificação.)

## Infoproduto e promessa de ganho

- "Fature R$ X" é oferta que obriga (CDC, art. 30) e, se não for comprovável, é enganosa (art. 37), com o ônus da prova no anunciante (art. 38).
- CONAR: sem exagero de remuneração (Anexo C, 1), sem ganho irreal nem promessa de sucesso (Anexo B), projeção com base explicada (Anexo E).
- Hotmart (Política de Uso Responsável, 20/03/2026): proíbe promessa de enriquecimento irreal, lucro garantido ou ganho rápido sem esforço (item 3.7), ostentação de luxo ou dinheiro que engane sobre a facilidade (3.8) e depoimento sintético feito com IA (4.19).
- Meta: proíbe oferta de retorno financeiro irreal para esforço mínimo e investimento com retorno garantido, sem risco ou rápido.
- Depoimento de resultado precisa de autorização escrita e ser comprovável (CONAR, art. 27, §9º).

## Dados pessoais em marketing (LGPD, Lei 13.709/2018)

- **Bases legais**: consentimento (art. 7º, I) ou legítimo interesse (art. 7º, IX; art. 10, I). Consentimento livre, informado, inequívoco e para finalidade determinada; se escrito, em cláusula destacada; a prova cabe à empresa; autorização genérica é nula; o titular revoga a qualquer momento, de graça (arts. 5º, XII, 8º e 18, IX).
- **Legítimo interesse** (Guia ANPD, fev/2024): só os dados necessários, com transparência. E-mail promocional para base com relação prévia e link de descadastro em cada envio foi aceito como exemplo. Lista de terceiros ou de fonte pública pesa contra. Publicidade para criança por essa base foi rejeitada. O titular pode se opor (art. 18, §2º).
- **WhatsApp**: só contatar quem forneceu o número e fez opt-in; respeitar pedido de parar (Política do WhatsApp Business).
- Link de descadastro em toda mensagem de e-mail marketing.

## Frases de risco

A ligação entre cada frase e a norma é leitura das normas acima: sinaliza risco e não é parecer jurídico. O hook do plugin avisa as que consegue detectar no texto.

| Frase ou prática | Onde é vedada ou arriscada |
|---|---|
| "Resultado garantido", "100% garantido" | CFM art. 11, XII; CFN 599 art. 56; CFP art. 20, e; CFO-196 art. 2º; OAB 205 art. 6º; CDC art. 37 |
| "Veja meu antes e depois" em post promocional | CFM art. 14 (só educativo e com requisitos); CFO art. 44, I, e CFO-196 art. 2º (só diagnóstico e conclusão, com TCLE); CFN 599 art. 58 (vedado) |
| "Consulta ou avaliação grátis" | CFM art. 11, §4º, c; CFO art. 20, IX; OAB 205 art. 3º, I; CFP art. 20, d. "Grátis" com custo escondido: CONAR art. 27, §4º |
| "O melhor médico (dentista, advogado) da cidade", "referência nº 1" | CFM art. 11, XIII e XVI; OAB 205 art. 3º, IV; CFP art. 20, f; CONAR art. 27, §1º |
| "Sorteio de uma harmonização", "concorra a uma consulta" | CFO art. 20, VIII; CFM art. 9º, VIII; CFN 599 art. 57; CFP NT 1/2022 |
| "Preço social", "pacote promocional", "valor acessível" | Psicologia (CFP art. 20, d; NT 1/2022) e advocacia (OAB 205 art. 3º, I) |
| "Limpeza por R$ 150 em 3x" | Dentista: CFO art. 44, I. Nutricionista: vedado até 22/01/2027 (CFN 599 art. 57). Médico: permitido (CFM art. 9º, VI) |
| "Especialista em X" sem título ou RQE | CFM arts. 11, I, e 13, §1º; CFO art. 44, II; OAB 205 art. 3º, III; CFP art. 20, b |
| "Emagreça 10 kg em 30 dias", "cansada dessa barriga?" | CFN 599 art. 56; RDC 243 art. 17 se for suplemento; política de Saúde e Bem-estar da Meta |
| Cosmético ou suplemento que "cura acne", "elimina melasma", "substitui o remédio" | RDC 907/2024 art. 12; Lei 6.360 art. 59; RDC 243 art. 17; DL 986 art. 23 |
| "Fature R$ 10 mil por mês", "renda extra garantida", "dinheiro sem esforço", "aprovação garantida" | CONAR Anexos C (1) e B (11, 12); CDC arts. 30, 37 e 38; Hotmart 3.7; Meta |
| "Rende 5% ao mês sem risco", "compre a ação X agora", "isso não é recomendação" sem registro | Res. CVM 20 arts. 1º e 2º; Lei 6.385 art. 27-E; OC CVM/SIN 13/2020; CONAR Anexo E; Meta |
| Print de faturamento com carro de luxo, aposta premiada | Hotmart 3.8; OAB 205 art. 6º, parágrafo único; Portaria Interministerial 73/2026 |
| Post pago sem identificação, ou só com "#ad" ou collab | CDC art. 36; CONAR art. 28 e Guia 2026; Portaria Conjunta 3/2026 art. 9º |
| "De R$ 997 por R$ 197" sem preço anterior comprovável | CONAR art. 27, §3º; CDC art. 37, §1º |

## Identificações e avisos aceitos

| Tema | O que a peça traz |
|---|---|
| Medicina | "Nome, CRM/UF nº, MÉDICO, Especialidade, RQE nº", na peça e na bio. Sem RQE: "MÉDICO com pós-graduação em X" e "NÃO ESPECIALISTA". Antes e depois: texto educativo com indicações, fatores e complicações |
| Odontologia | "Nome do dentista, CRO-UF nº" em toda imagem ou vídeo; clínica informa o responsável técnico. O TCLE é documento interno e não funciona como aviso ao público |
| Nutrição | "Nome, Nutricionista, CRN-X nº" e aviso de que os resultados podem não ocorrer da mesma forma para todos |
| Psicologia | "Nome completo, Psicóloga(o), CRP XX/nnnnn". Nenhum aviso autoriza preço ou depoimento como propaganda |
| Advocacia | Nome, ou nome da sociedade, e número da OAB |
| Educação física | Nome e número do CREF |
| Suplementos | Avisos de rótulo da RDC 243 e alegação com o texto exato da IN 28, Anexo V |
| Medicamento de venda livre | "A persistirem os sintomas, o médico deverá ser consultado" |
| Investimentos | "A rentabilidade obtida no passado não representa garantia de resultados futuros"; fundos sem garantia do administrador, do gestor, de seguro nem do FGC; analista declara independência e conflitos |
| Influenciador | Ferramenta "parceria paga" da plataforma, #publi ou #publicidade visível logo de cara; relação comercial visível durante todo o conteúdo |
| E-commerce e infoproduto | Como exercer o arrependimento de 7 dias; preço total com despesas extras; depoimento com autorização escrita e comprovável |
| E-mail e WhatsApp | Link de descadastro em toda mensagem; consentimento com finalidade específica; opt-in explícito no WhatsApp |

## Mitos e armadilhas de vigência

- **Lei 15.325/2026** regula só a profissão de multimídia e não cria obrigação de identificar publicidade. Não use como base para exigir #publi (use CDC, CONAR e a Portaria Conjunta 3/2026).
- **CFO-271/2025 não liberou sorteio**: o texto oficial manteve brinde, premiação e sorteio como infração.
- **Nutrição**: a norma válida hoje é a CFN 599/2018. A prorrogação da 856/2026 é a Res. CFN 858/2026 (sites que citam "156/2026" usaram a página do DOU).
- **Cosméticos**: a RDC 752/2022 foi revogada pela RDC 907/2024.
- **Ainda não publicados** até 2026-09-28: o novo provimento da OAB e uma regra da CVM específica para influenciador de finanças.

## Fontes

- CFM 2.336/2023: https://sistemas.cfm.org.br/normas/arquivos/resolucoes/BR/2023/2336_2023.pdf
- Código de Ética Odontológica: https://website.cfo.org.br/wp-content/uploads/2018/03/codigo_etica.pdf
- CFO-271/2025: https://crors.org.br/wp-content/uploads/2025/07/RESOLUCAO-CFO-271-2025.pdf
- CFO-196/2019: https://website.cfo.org.br/resolucao-cfo-196-2019/
- CFN 599/2018: https://cfn.org.br/wp-content/uploads/2018/04/codigo-de-etica.pdf
- CFN 856/2026 e 858/2026: https://sisnormas.cfn.org.br/viewPage.html?id=856 e https://sisnormas.cfn.org.br/viewPage.html?id=858
- Código de Ética do Psicólogo: https://site.cfp.org.br/wp-content/uploads/2012/07/codigo-de-etica-psicologia.pdf
- Nota Técnica CFP 1/2022: https://site.cfp.org.br/wp-content/uploads/2022/06/SEI_CFP-0612475-Nota-Tecnica.pdf
- Provimento OAB 205/2021: https://www.oab.org.br/leisnormas/legislacao/provimentos/205-2021
- Código de Ética e Disciplina da OAB: https://www.oab.org.br/arquivos/resolucao-n-022015-ced-2030601765.pdf
- Código de Ética CONFEF/CREFs: https://cref22.org.br/codigo-de-etica/
- RDC 243/2018 e RDC 907/2024: https://anvisalegis.datalegis.net
- Lei 6.360/1976: https://www.planalto.gov.br/ccivil_03/leis/l6360.htm
- Lei 9.294/1996: https://www.planalto.gov.br/ccivil_03/leis/l9294.htm
- Decreto-Lei 986/1969: https://www.planalto.gov.br/ccivil_03/decreto-lei/del0986.htm
- Res. CVM 20/2021: https://conteudo.cvm.gov.br/export/sites/cvm/legislacao/resolucoes/anexos/001/resol020consolid.pdf
- Res. CVM 19/2021: https://conteudo.cvm.gov.br/export/sites/cvm/legislacao/resolucoes/anexos/001/resol019consolid.pdf
- Res. CVM 175/2022: https://conteudo.cvm.gov.br/export/sites/cvm/legislacao/resolucoes/anexos/100/resol175consolid.pdf
- Lei 6.385/1976: https://www.planalto.gov.br/ccivil_03/leis/l6385.htm
- Código CONAR 2026: https://conar.wpenginepowered.com/wp-content/uploads/2026/08/Codigo_CONAR_2026.pdf
- Guia CONAR de Influenciadores 2026: https://conar.wpenginepowered.com/wp-content/uploads/2026/05/260525_GUIA_INFLUENCIADORES_CONAR_v6.pdf
- CDC: https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm
- Decreto 7.962/2013: https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/decreto/d7962.htm
- LGPD: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm
- Guia ANPD de Legítimo Interesse: https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia_legitimo_interesse.pdf
- ECA Digital (Lei 15.211/2025): https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/L15211.htm
- Portaria Conjunta 3/2026 (notícia oficial): https://www.gov.br/mj/pt-br/assuntos/noticias-1/novas-regras-para-publicidade-digital-visam-conter-fraudes-e-golpes
- Portaria Interministerial 73/2026 (notícia oficial): https://www.gov.br/mj/pt-br/assuntos/noticias-1/portaria-interministerial-estabelece-regras-para-proteger-o-consumidor-na-publicidade-de-apostas-de-quota-fixa
- Política de Uso Responsável da Hotmart: https://hotmart.com/en/legal/responsible-use-policy
- Práticas comerciais proibidas (Meta): https://transparency.meta.com/policies/ad-standards/deceptive-content/prohibited-commercial-practices/
