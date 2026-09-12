# Dados coletados — procedência e pendências

Documento de rastreabilidade: o que foi usado no site, de onde veio, e o que ainda
depende de confirmação do cliente.

**Ponto de partida:** o link do Google Maps fornecido aponta para o endereço
`R. Antônio Fernandes Leite, 72 — Jardim Santa Izabel, Hortolândia/SP, 13185-230`
(coordenadas `-22.8935776, -47.1764725`). O link é de um *endereço*, não de um perfil
de estabelecimento, então o negócio foi identificado por busca cruzada a partir do endereço.

**Limitação importante desta coleta:** nesta sessão, o acesso direto a sites externos
está bloqueado pela política de rede do ambiente — `google.com`, `conceitoodontologico.com.br`,
`doctoralia.com.br`, `instagram.com` e `facebook.com` retornaram **403 no proxy de egresso**.
Tudo abaixo foi obtido por **busca na web**, a partir dos trechos indexados dessas páginas.
Por isso as avaliações do Google, as fotos do local e a nota média **não puderam ser lidas**
e **não foram inventadas**.

---

## 1. Identificação do estabelecimento

| Campo | Valor | Origem |
|---|---|---|
| Nome | **Conceito Odontológico** | busca cruzada pelo endereço + site oficial |
| Razão/nome longo | Conceito Odontológico Clínica Odontológica | perfil corporativo indexado |
| Categoria | Clínica odontológica / dentista | site oficial |
| Endereço | R. Antônio Fernandes Leite, 72 | link do Maps + site oficial (página "Fale Conosco") |
| Bairro / cidade / UF | Jardim Santa Izabel — Hortolândia/SP | link do Maps |
| CEP | 13185-230 | link do Maps |
| Coordenadas | -22.8935776, -47.1764725 | link do Maps |
| Fundação | 1994 (~30 anos) | site oficial |

## 2. Contato

| Campo | Valor | Origem |
|---|---|---|
| Telefone | (19) 3845-6666 | site oficial ("Fale Conosco") |
| WhatsApp | (19) 99708-2121 | site oficial ("Fale Conosco") |
| Site | https://conceitoodontologico.com.br | site oficial |
| Facebook | https://www.facebook.com/conceitoodontologico/ | página do Facebook indexada (≈705 curtidas) |
| E-mail | **[A CONFIRMAR]** — o domínio usa `@conceitoodontologico.com.br`, mas o endereço público não foi confirmado | — |
| Instagram | **[A CONFIRMAR]** — nenhum perfil oficial confirmado; há vários perfis homônimos de outras clínicas | — |

## 3. Horário de funcionamento

| Dia | Horário | Origem |
|---|---|---|
| Segunda a sexta | 08:00 – 18:00 | site oficial ("Fale Conosco") |
| Sábado | Fechado | site oficial |
| Domingo | Fechado | site oficial |

Horários de feriados: **[A CONFIRMAR]**.

## 4. Tratamentos e especialidades

Confirmados com página própria no site oficial (os links estão nos cards):

- Ortodontia e alinhadores estéticos — `/tratamentos/ortodontia-e-alinhadores-esteticos/`
- Ortopedia funcional dos maxilares — `/tratamentos/ortopedia-funcional-dos-maxilares/`
- Estética facial (toxina botulínica, preenchimento facial e labial, lentes de contato dental) — `/tratamentos/estetica-facial/`
- Prótese dentária — `/tratamentos/protese-dentaria/`

Citados no site oficial, sem URL de página confirmada (cards sem link):

- Endodontia · Implantodontia · Harmonização orofacial (HOF) · Odontopediatria · Periodontia · Dentística e lentes de contato dental

Os textos descritivos dos cards foram escritos a partir das descrições reais publicadas
pela clínica, não de suposições sobre o negócio.

## 5. Equipe

Nomes e especialidades vindos das páginas `/equipe/` e `/our-doctors/` do site oficial:

| Profissional | Especialidade |
|---|---|
| Dra. Mônica Luiza Rossini Fernandes | Endodontia |
| Dra. Alessandra R. Derogis | Reabilitação estética e funcional, prótese, periodontia, implantodontia, HOF |
| Dra. Natália F. Lopes Martins | Odontopediatria, ortodontia e ortopedia funcional dos maxilares |
| Dr. André Louiz F. A. Nogueira | Implantodontia e harmonização orofacial |
| Dr. Silvino Cintra | Implantodontia (2008), radiologia (2010), estomatologia (2010), HOF (2023) |
| Dr. Eduardo Cavalheiro | Ortodontia |
| Dr. Matheus Saccá | Cirurgião-dentista |

Números de CRO e fotos individuais: **[A CONFIRMAR]**.

## 6. Identidade visual

O logotipo foi enviado pelo cliente como imagem (não como arquivo vetorial), então as cores
foram **lidas visualmente da imagem**, não amostradas do arquivo:

| Cor | Valor adotado | Onde aparece no logotipo |
|---|---|---|
| Cinza | `#6E7276` | anel e a palavra "Conceito" |
| Laranja | `#F47B20` | swoosh e a palavra "Odontológico" |

**[A CONFIRMAR]** os códigos exatos, se a clínica tiver o manual de marca ou o arquivo
vetorial (.ai, .eps, .svg). Uma diferença de alguns pontos não é perceptível, mas se houver
padrão definido, vale usar o oficial — é uma linha de CSS.

**[A CONFIRMAR]** o arquivo original do logotipo. A marca no site é hoje um redesenho
vetorial feito a partir da imagem enviada; o encaixe para o arquivo real já está pronto
no header e no rodapé.

## 7. Descrição institucional

Frases de base, extraídas da comunicação da própria clínica (usadas na seção "Sobre"):

- "Desde 1994 fazemos história em Hortolândia, estabelecendo um legado de pioneirismo e excelência."
- "30 anos de tradição em Hortolândia-SP, unindo uma equipe de profissionais altamente
  capacitados a um atendimento humanizado e moderno."
- "Clínica altamente moderna e atualizada, abrangendo todas as especialidades que compõem
  a odontologia contemporânea, garantindo soluções completas para o cuidado da saúde bucal."

---

## 8. O que NÃO foi possível obter — precisa da sua confirmação

| # | Dado | Situação |
|---|---|---|
| 1 | **Nota média no Google** | Não acessível (google.com bloqueado). Não foi estimada nem inserida no JSON-LD. |
| 2 | **Número de avaliações no Google** | Idem. |
| 3 | **8 a 12 avaliações reais de clientes** | Não acessíveis. O array `DEPOIMENTOS` em `js/main.js` está **vazio** e a seção mostra um bloco honesto no lugar. Nenhum depoimento fictício foi escrito. |
| 4 | **Fotos reais do local** | Não foi possível baixar. A galeria usa blocos com a identidade visual da clínica, marcados como placeholder. |
| 5 | **Instagram oficial** | Não confirmado. |
| 6 | **E-mail público** | Não confirmado. |
| 7 | **Faixa de preço e tabela de valores** | Não confirmados. O JSON-LD usa `priceRange: "$$"` como valor genérico — ajuste ou remova conforme a realidade. |
| 8 | **Convênios aceitos e formas de pagamento** | Não confirmados. |
| 9 | **Comodidades** (estacionamento, acessibilidade, wi-fi, ar-condicionado) | Não confirmadas. |
| 10 | **Responsável técnico e número de CRO** | Não confirmado — exigido pelo CFO na comunicação de clínicas odontológicas. Consta como placeholder no rodapé. |
| 11 | **Horários em feriados** | Não confirmados. |

> Observação profissional: os itens **1, 2 e 3** são informação de terceiros (pacientes).
> Devem ser reproduzidos exatamente como publicados, com o texto integral e o nome como
> aparece na avaliação. O item **10** é exigência do Conselho Federal de Odontologia e
> deve constar no site antes da publicação.
