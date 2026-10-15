# Modelo LaTeX — Relatório PIBIT (eFlesh)

Modelo que espelha o formato do relatório PIBIC/UnB usado como referência (A4, ABNT, Arial 12, espaçamento 1,5, margens 3/2/3/2 cm, seções numeradas em maiúsculas, legendas "Figura 1 – …" com "Fonte:" abaixo) e a estrutura das *Instruções para escrita de trabalhos científicos* (Profª Simone Borges Simão Monteiro).

## Como subir no Overleaf

1. No Overleaf: **New Project → Upload Project** e escolha o arquivo `.zip`.
2. Em **Menu → Compiler**, deixe **pdfLaTeX**.
3. Clique em **Recompile**. As referências aparecem a partir da segunda compilação.

## Onde escrever

| Arquivo | Seção | Pergunta-guia das instruções |
| --- | --- | --- |
| `main.tex` | Título, autor, orientador, programa | — |
| `secoes/00-resumo.tex` | Resumo e Abstract (escrever por último) | O que eu fiz em poucas palavras? |
| `secoes/01-introducao.tex` | 1 Introdução | Qual é o problema da pesquisa? |
| `secoes/02-estado-da-arte.tex` | 2 Levantamento do Estado da Arte (TEMAC) | O que já foi falado sobre isso? |
| `secoes/03-referencial-teorico.tex` | 3 Referencial Teórico | Quais conceitos subsidiam o trabalho? |
| `secoes/04-metodo.tex` | 4 Método de Pesquisa (com a Figura das etapas) | Como resolvi o problema? |
| `secoes/05-resultados.tex` | 5 Resultados e Discussão (mesmas etapas do Método) | O que descobri? O que significa? |
| `secoes/06-consideracoes-finais.tex` | 6 Considerações Finais | O objetivo foi atendido? |
| `secoes/07-agradecimentos.tex` | Agradecimentos | Quem me ajudou? |
| `secoes/08-apendices.tex` | Apêndices | Tenho informações extras? |
| `siglas.tex` | Lista de siglas | — |
| `referencias.bib` | Referências (já com as fontes verificadas da revisão) | — |
| `figuras/` | Coloque aqui as imagens | — |

## Comandos úteis

| Para | Escreva | Resultado |
| --- | --- | --- |
| Citação no texto | `\citeonline{pattabiraman2025eflesh}` | Pattabiraman et al. (2025) |
| Citação entre parênteses | `\cite{pattabiraman2025eflesh}` | (PATTABIRAMAN et al., 2025) |
| Sigla | `\ac{MLP}` | 1.ª vez: Perceptron Multicamadas (MLP); depois: MLP |
| Fonte de figura/tabela | `\fonte{Elaborado pelo autor (2026).}` | Fonte: Elaborado pelo autor (2026). |
| Referir a uma figura | `Figura~\ref{fig:estrutura}` | Figura 1 |
| Quadro (texto) ou Gráfico | ambientes `quadro` e `grafico` | Quadro 1 / Gráfico 1 |
| Unidades | `\SI{0,27}{\newton}` | 0,27 N |

## Orientações em vermelho

Os trechos `\escrever{...}` e `\dica{...}` aparecem em vermelho no PDF como lembrete do que escrever. Para entregar, troque em `main.tex`:

```latex
\setboolean{rascunho}{true}   % -> false
```

e todas as orientações somem.

## Dicas das instruções que o modelo já ajuda a cumprir

- **Dica 1** — texto impessoal ("propõe-se", "foi realizado"), nunca 1.ª pessoa.
- **Dica 3** — sempre "conforme a Figura 1", nunca "a figura abaixo"; use `\ref`.
- **Dica 4** — siglas por extenso na 1.ª vez: o comando `\ac{}` faz isso sozinho.
- **Dica 5** — a estruturação do Método já está numa Figura (TikZ, editável).
- **Dica 6** — as subseções de Resultados repetem as etapas do Método.
- **Dica 7** — o objetivo da Introdução deve ser copiado igual no Resumo.
- Referências atualizadas: priorize os últimos 4 anos.

## Pendências a preencher

- Nome do orientador e departamento em `main.tex`.
- Confirmar volume/páginas das referências marcadas como *preprint* no `referencias.bib`.
