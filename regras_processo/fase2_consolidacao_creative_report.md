# Fase 2: Consolidação e Relatório Criativo (`BEEMIDIA_CREATIVE_REPORT.json`)

## 1. Visão Geral
A **Fase 2** transforma as observações individuais de cada vídeo do lote (`dna_*.json`) em um relatório consolidado de inteligência criativa (`BEEMIDIA_CREATIVE_REPORT.json`), combinando estatística determinística com análise profunda de IA.

---

## 2. Pilares da Consolidação

### A. Prevalência Ponderada por Tração de Referência
- **Frequência Absoluta e Percentual:** Quantas vezes cada gancho, dor, transformação, tipo de prova e CTA aparece no lote.
- **Tração de Referência Ponderada:** Média das taxas de engajamento dos vídeos de referência que usaram aquele elemento:
  $$\text{Score Tração} = (\text{Taxa Likes} \times 1.0) + (\text{Taxa Comentários} \times 2.0) + (\text{Taxa Compartilhamentos} \times 3.0)$$
- **Não depende de views brutas:** Foco na eficiência proporcional de engajamento do formato.

### B. Extração de "Receitas de Vídeo" (`ReceitaVideo`)
Cada vídeo é decomposto em sua receita estrutural:
$$\text{Receita} = \text{Dor Chave} \times \text{Público Chave} \times \text{Gancho (Tipo)} \times \text{Estrutura} \times \text{Prova} \times \text{CTA}$$

- **Destaque Múltiplo ($\ge 2$ vídeos):** Quando 2 ou mais vídeos no lote compartilham a mesma receita básica, ela é marcada como `destaque_multiplo = True` e promovida para o topo da lista de receitas observadas.
- **Base para Roteirização:** Estas receitas comprovadas alimentam a alocação de 70% de modelos canônicos nos roteiros de 10s.

### C. Estatísticas de Uso de Modelos (`ModelUsageStats`)
- Percentual de adoção de cada modelo narrativo no lote.
- Score médio de formato Faceless ($0 \text{ a } 10$).
- Nota média de Gerabilidade por IA ($1 \text{ a } 5$), avaliando desafios como consistência temporal, mãos e física de cabelos/fluidos.

### D. Candidatos a Novos Modelos (`NewModelCandidate`)
Identificação de modelos narrativos emergentes ou variações não mapeadas na Knowledge Base, categorizados como:
- `transferivel`: Aplicável a toda a categoria ou nicho (geralmente testado em $\ge 2$ produtos).
- `produto`: Depende estritamente de mecanismo físico ou acessório único do produto atual.

---

## 3. Estrutura do Schema JSON Consolidado

```json
{
  "report_id": "report_Beleza_Acessorios_Cabelo",
  "niche": "Beleza/Acessorios_Cabelo",
  "dataset": {
    "video_count": 8,
    "product_count": 1,
    "videos_com_metricas": 8
  },
  "model_usage": [
    {
      "model": "HAND_DEMO_VOICEOVER",
      "video_count": 4,
      "percentage": 50.0,
      "avg_faceless_score": 8.5,
      "avg_gerabilidade_ia": 4.2,
      "tracao_referencia_media": 0.065,
      "confidence": 0.9
    }
  ],
  "strongest_models": [
    {
      "model": "HAND_DEMO_VOICEOVER",
      "reason": "Maior prevalência e facilidade de reprodução sintética em IA",
      "evidence": ["video1.mp4", "video2.mp4"],
      "tracao_score": 0.065
    }
  ],
  "receitas_observadas": [
    {
      "receita_id": "RECEITA_01",
      "dor_chave": "Frizz e demora na secagem",
      "publico_chave": "Mulheres que buscam praticidade",
      "gancho_tipo": "dor",
      "estrutura_resumo": "Demonstração comparativa antes/depois em mechas",
      "prova_usada": "Demonstração visual do bico modelador",
      "cta_tipo": "Carrinho laranja",
      "video_count": 3,
      "evidencias": ["video1.mp4", "video2.mp4", "video5.mp4"],
      "score_tracao_medio": 0.072,
      "destaque_multiplo": true
    }
  ],
  "receitas_destaque": [
    {
      "receita_id": "RECEITA_01",
      "destaque_multiplo": true
    }
  ],
  "prevalencia_atributos": [
    {
      "atributo": "dor",
      "categoria_atributo": "gancho",
      "ocorrencias": 5,
      "total_videos": 8,
      "prevalencia_percentual": 62.5,
      "tracao_ponderada_media": 0.068,
      "evidencias": ["video1.mp4", "video2.mp4"]
    }
  ],
  "recurring_hooks": ["Problema de frizz em 0-3s"],
  "recurring_visual_patterns": ["Close-up em mãos manipulando os bicos"],
  "recurring_audio_patterns": ["Voz amigável e explicativa em tom de resenha"],
  "faceless_patterns": ["Ângulo POV em bancada"],
  "new_model_candidates": []
}
```
