# Conceito Odontológico — site institucional

Site de página única, responsivo e sem dependências, para a **Conceito Odontológico**
(clínica odontológica em Hortolândia/SP, atuando desde 1994).

HTML + CSS + JavaScript puros. Sem build, sem framework, sem node_modules.

---

## Como visualizar localmente

**Opção 1 — abrir direto no navegador**

```bash
# a partir da raiz do repositório
open conceito-odontologico/index.html      # macOS
xdg-open conceito-odontologico/index.html  # Linux
start conceito-odontologico\index.html     # Windows
```

**Opção 2 — servidor local (recomendado)**

Alguns recursos (o iframe do Google Maps, por exemplo) se comportam melhor via `http://`
do que via `file://`:

```bash
cd conceito-odontologico
python3 -m http.server 8000
# depois acesse http://localhost:8000
```

Ou, com Node instalado: `npx serve conceito-odontologico`

---

## Estrutura do projeto

```
conceito-odontologico/
├── index.html                 # a página inteira (todas as 10 seções + JSON-LD)
├── css/
│   └── styles.css             # estilos, mobile-first, com tokens de cor no :root
├── js/
│   └── main.js                # menu, scroll reveal, "aberto agora", depoimentos
├── assets/
│   ├── favicon.svg            # ícone do site
│   ├── og-image.svg           # arte-fonte do preview social (vetor)
│   ├── og-image.png           # preview social 1200×630 usado nas meta tags
│   └── build-og-image.py      # script que regenera o PNG a partir do design
├── DADOS-COLETADOS.md         # o que foi extraído, de onde, e o que falta confirmar
└── README.md
```

---

## Deploy

O site é 100% estático — qualquer hospedagem serve. A pasta a publicar é
`conceito-odontologico/`.

### Netlify (arrastar e soltar)

1. Acesse <https://app.netlify.com/drop>
2. Arraste a pasta `conceito-odontologico/` para a área indicada.
3. Pronto. Em seguida, em *Site settings → Domain management*, aponte o domínio
   `conceitoodontologico.com.br`.

### Netlify (via Git)

- **Base directory:** `conceito-odontologico`
- **Build command:** *(deixe em branco)*
- **Publish directory:** `conceito-odontologico`

### Vercel

```bash
npm i -g vercel
cd conceito-odontologico
vercel            # preview
vercel --prod     # produção
```

No painel da Vercel, ao importar o repositório: **Framework Preset** = `Other`,
**Root Directory** = `conceito-odontologico`, sem comando de build.

### GitHub Pages

Em *Settings → Pages*, selecione a branch e a pasta `/conceito-odontologico`.
Lembre-se de ajustar os caminhos absolutos das meta tags Open Graph para a URL final.

---

## Antes de publicar: o que precisa ser preenchido

Tudo que não pôde ser confirmado em fonte pública está marcado no código com
`[A CONFIRMAR COM O CLIENTE]`. Para listar as ocorrências:

```bash
grep -rn "A CONFIRMAR" conceito-odontologico/
```

### 1. Depoimentos (seção "O que dizem os pacientes")

**Nenhum depoimento foi inventado.** O array `DEPOIMENTOS` em `js/main.js` está vazio
de propósito, e enquanto estiver vazio a seção exibe um bloco honesto convidando a ler
as avaliações no Google.

Para publicar depoimentos reais, copie o texto **integral** das avaliações publicadas
(sem resumir, sem reescrever) para o array:

```js
var DEPOIMENTOS = [
  {
    nome:  'João S.',                       // como aparece publicado, abreviado
    nota:  5,                               // a nota real da avaliação, de 1 a 5
    texto: 'Texto integral da avaliação.',  // sem cortes nem edições
    fonte: 'Google'
  },
  // ... 8 a 12 itens
];
```

A seção passa a renderizar o grid automaticamente. Se quiser exibir também a nota média
e o total de avaliações, acrescente `aggregateRating` ao JSON-LD no fim do `index.html` —
**apenas com os números reais do perfil**, porque o Google penaliza dados estruturados
que não conferem com a realidade.

### 2. Fotos reais (seção "A clínica")

Os cinco blocos da galeria são placeholders com a identidade visual da clínica.
Para trocar por fotos reais:

1. Salve as imagens em `assets/galeria/` (JPG ou WebP, ~1600px no lado maior, otimizadas).
2. No `index.html`, dentro de cada `<li class="tile">`, substitua

   ```html
   <div class="tile-art tile-art-1" aria-hidden="true"></div>
   ```

   por

   ```html
   <img src="assets/galeria/01.jpg" alt="Recepção da Conceito Odontológico"
        loading="lazy" width="1600" height="1200">
   ```

O CSS já trata `.tile img` com `object-fit: cover`, então o enquadramento se resolve sozinho.
Escreva `alt` descritivo de verdade — é o que garante a acessibilidade da seção.

### 3. Outros campos pendentes

Veja a lista completa e as fontes de cada dado em [`DADOS-COLETADOS.md`](DADOS-COLETADOS.md).

---

## Manutenção

### Alterar o horário de funcionamento

Os horários aparecem em **três** lugares que precisam ficar em sincronia:

1. A tabela em `index.html` (seção `#horarios`);
2. O objeto `HORARIOS` em `js/main.js` (alimenta o selo "Aberto agora");
3. O bloco `openingHoursSpecification` do JSON-LD no fim do `index.html`.

O selo "Aberto agora" calcula o estado sempre no fuso `America/Sao_Paulo`, então funciona
corretamente mesmo para quem acessa de outro fuso.

### Alterar cores e tipografia

Todas as cores estão como custom properties no `:root` de `css/styles.css`.
As fontes são Fraunces (títulos) e Inter (texto), carregadas do Google Fonts no `<head>`.

### Regenerar a imagem de preview social

```bash
pip install pillow
python3 assets/build-og-image.py
```

---

## O que já está implementado

- **Responsivo** de 320px a telas largas, mobile-first, sem scroll horizontal em nenhum breakpoint.
- **SEO:** `<title>`, meta description, canonical, Open Graph, Twitter Card e dados estruturados
  JSON-LD do tipo `Dentist` (subtipo de `LocalBusiness`) com nome, endereço, telefone, geo,
  horários e lista de serviços — todos com os dados reais coletados.
- **Acessibilidade:** skip link, marcos semânticos, `aria-expanded` no menu, foco visível,
  tabela de horários com `<th scope>`, contraste conferido nos textos sobre fundo escuro,
  navegação completa por teclado e respeito a `prefers-reduced-motion`.
- **Performance:** sem framework nem bibliotecas; um CSS e um JS enxutos; iframe do mapa com
  `loading="lazy"`; animações via `IntersectionObserver` (nada de listeners de scroll pesados);
  fontes com `display=swap` e `preconnect`.
- **Micro-interações:** reveal no scroll, contadores animados, header que ganha sombra ao rolar,
  link ativo conforme a seção visível, hovers com elevação — todos desativados quando o
  sistema pede menos movimento.
- **Botão flutuante de WhatsApp** visível em todas as seções, com mensagem pré-preenchida.
