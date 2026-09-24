# 📐 Regras de Engenharia do Formato 10s Text-to-Video

Este documento define as regras inegociáveis para a criação de roteiros de alta performance para modelos gerativos Text-to-Video (Nano Banana, Veo, Runway).

---

## ⏱️ 1. A Regra dos 10 Segundos ($2 \times 5\text{s}$)

* **Duração Total:** Exatamente 10 segundos.
* **Divisão:** 2 Cenas de 5 segundos cada.
  - **Cena 1 (0 a 5s):** Gancho visual de alta retenção + On-Screen Text Hook.
  - **Cena 2 (5 a 10s):** Demonstração do benefício resolvido + Call to Action.

---

## 🎙️ 2. Regra de Ouro da Locução (Anti-Corte de Áudio)

* **Limite por Cena:** Máximo de **8 a 11 palavras**.
* **Total por Vídeo:** Máximo de **18 a 22 palavras**.
* **Tempo de Fechamento:** A locução deve terminar naturalmente entre **8.5s e 9.0s**, deixando 1.0s a 1.5s de respiro para que o áudio **NUNCA termine cortado no meio**.

---

## 🎨 3. Padrão Visual Cinematográfico de Alta Fidelidade

Cada `visual_prompt` deve conter:
1. **Lente & Enquadramento:** `8k photorealistic, 85mm macro lens, shallow depth of field f/1.8, smooth dolly-in, 60fps slow-motion`.
2. **Iluminação de Estúdio:** `Soft rim light, volumetric steam/glow, high contrast reflections, warm golden tones`.
3. **Física de Materiais Realista:** Texturas fiéis ao produto real, comida deslizando sem óleo, cerdas anti-queimadura, luzes LED ativas.
4. **100% Faceless:** Apenas mãos, ombros para baixo, bancadas de mármore e fundos estéticos.

---

## 🛑 4. Protocolo de Aprovação Humana para a Knowledge Base

1. A cada nova leva de roteiros manuais gerada, analisar o que aprendemos com o produto e com os vídeos.
2. Identificar:
   - *Novos modelos de vídeo emergentes*.
   - *Padrões visuais ou ganchos inovadores*.
   - *Detalhes técnicos que precisam ser cobrados em futuros roteiros da categoria*.
3. **OBRIGATÓRIO:** Apresentar a proposta de aprendizado de forma clara ao usuário.
4. Somente após a aprovação explícita do usuário, atualizar o `banco_de_dados/knowledge_base.json`.
