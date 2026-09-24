"""
schemas/creative_report.py — Contratos Pydantic para dna_*.json e
BEEMIDIA_CREATIVE_REPORT.json (Fase 1 e Fase 2 do Pipeline).

Suporta:
- Métricas de referência e taxas de engajamento (likes/views, comments/views, shares/views)
- Análise de ganchos com enum carregado e transcrições 0-3s
- Estrutura de cenas com timestamps
- Decomposição de produto (dores, transformação, provas)
- Público-alvo e contexto de uso
- Análise de áudio, texto e CTA
- Checagem cruzada de claims contra product_profile.json
- Gerabilidade de IA (nota 1 a 5 + justificativa física)
- Classificação de nível (produto vs transferível)
- Extração de comentários reais de clientes
"""
from __future__ import annotations
from typing import List, Optional, Dict, Any, Literal
from enum import Enum
from pydantic import BaseModel, Field, model_validator


class TipoGanchoEnum(str, Enum):
    DOR = "dor"
    CURIOSIDADE = "curiosidade"
    DEMONSTRACAO_VISUAL = "demonstracao_visual"
    PROVA_SOCIAL = "prova_social"
    PRECO_OFERTA = "preco_oferta"
    CHOQUE_VISUAL = "choque_visual"
    OUTRO = "outro"


class FuncaoCenaEnum(str, Enum):
    GANCHO = "gancho"
    PROBLEMA = "problema"
    DEMONSTRACAO = "demonstracao"
    PROVA = "prova"
    OFERTA = "oferta"
    CTA = "cta"
    OUTRO = "outro"


class TipoClaimEnum(str, Enum):
    NUMERICA = "numerica"
    COMPARATIVA = "comparativa"
    ABSOLUTA = "absoluta"


class NivelPadraoEnum(str, Enum):
    PRODUTO = "produto"
    TRANSFERIVEL = "transferivel"


# -------------------------------------------------------------
# SUB-MODELOS DO DNA DE VÍDEO (FASE 1)
# -------------------------------------------------------------

class MetricasReferencia(BaseModel):
    """Métricas brutas e taxas de engajamento calculadas do vídeo de referência."""
    views: Optional[int] = None
    likes: Optional[int] = None
    comentarios: Optional[int] = None
    compartilhamentos: Optional[int] = None
    vendas_pedidos: Optional[int] = None
    data_postagem: Optional[str] = None
    
    # Taxas calculadas
    taxa_likes: Optional[float] = Field(default=None, description="likes / views")
    taxa_comentarios: Optional[float] = Field(default=None, description="comentarios / views")
    taxa_compartilhamentos: Optional[float] = Field(default=None, description="compartilhamentos / views")
    score_tracao_referencia: Optional[float] = Field(default=None, description="Score ponderado de tração de referência")

    @model_validator(mode="after")
    def calcular_taxas(self) -> "MetricasReferencia":
        if self.views and self.views > 0:
            if self.likes is not None:
                self.taxa_likes = round(self.likes / self.views, 6)
            if self.comentarios is not None:
                self.taxa_comentarios = round(self.comentarios / self.views, 6)
            if self.compartilhamentos is not None:
                self.taxa_compartilhamentos = round(self.compartilhamentos / self.views, 6)
            
            # Score de tração composto: likes (1x) + comentarios (2x) + shares (3x)
            l = self.taxa_likes or 0.0
            c = self.taxa_comentarios or 0.0
            s = self.taxa_compartilhamentos or 0.0
            self.score_tracao_referencia = round((l * 1.0) + (c * 2.0) + (s * 3.0), 6)
        return self


class GanchoDNA(BaseModel):
    """Análise aprofundada dos primeiros 3 segundos do vídeo."""
    tipo: TipoGanchoEnum = Field(..., description="Tipo do gancho principal")
    descricao: str = Field(..., description="Descrição detalhada de como o gancho atua")
    fala_0_3s: Optional[str] = Field(default=None, description="Transcrição exata do que foi falado nos primeiros 3s")
    texto_tela_0_3s: Optional[str] = Field(default=None, description="Texto exibido na tela nos primeiros 3s")
    evidencia_timestamp: Optional[str] = Field(default="0:00-0:03", description="Timestamp do gancho")


class CenaDNA(BaseModel):
    """Segmentação cena a cena com função narrativa e timestamps."""
    inicio_s: float = Field(ge=0.0)
    fim_s: float = Field(ge=0.0)
    funcao: FuncaoCenaEnum = Field(..., description="Papel funcional da cena")
    descricao: str = Field(..., description="O que a câmera e o áudio mostram nessa cena")


class ProdutoDNA(BaseModel):
    """Decomposição dos atributos de produto e promessas exploradas no vídeo."""
    dor_principal: Optional[str] = None
    dores_secundarias: List[str] = Field(default_factory=list)
    transformacao: Optional[str] = Field(default=None, description="O contraste antes/depois demonstrado")
    gatilho_de_compra: Optional[str] = Field(default=None, description="Principal razão que induz à compra")
    objecoes_tratadas: List[str] = Field(default_factory=list)
    prova_usada: Optional[str] = Field(default=None, description="Tipo de prova demonstrada (teste, visual, depoimento)")


class PublicoDNA(BaseModel):
    """Identificação do público e contexto de uso evidenciados no vídeo."""
    quem_compra: Optional[str] = None
    quem_usa: Optional[str] = None
    contexto_de_uso: Optional[str] = None


class AudioTextoDNA(BaseModel):
    """Padrão sonoro e emocional do vídeo."""
    tipo_de_voz: Optional[str] = Field(default=None, description="Tom, ritmo e estilo da voz (ex: enérgico, calmo, ASMR)")
    musica: Optional[str] = Field(default=None, description="Estilo de música ou trilha sonora de fundo")
    emocao_dominante: Optional[str] = Field(default=None, description="Sentimento transmitido (desejo, alívio, urgência)")


class CtaDNA(BaseModel):
    """Chamada para ação do vídeo."""
    tipo: Optional[str] = Field(default=None, description="Tipo de CTA (link na bio, carrinho amarelo, clique)")
    momento: Optional[str] = Field(default=None, description="Quando o CTA ocorre (ex: final 3s, constante)")


class ClaimCheck(BaseModel):
    """Verificação cruzada de afirmações feitas no vídeo contra o product_profile.json."""
    afirmacao: str = Field(..., description="Afirmação/promessa feita no vídeo")
    tipo: TipoClaimEnum = Field(..., description="Tipo de alegação")
    no_product_profile: Literal["sim", "parcial", "nao"] = Field(
        ...,
        description="Se a claim foi confirmada pelo product_profile.json. Claim 'nao' nunca vira regra."
    )
    observacao: Optional[str] = None


class GerabilidadeIA(BaseModel):
    """Avaliação de viabilidade de reprodução sintética em modelos Text-to-Video de 5s/10s."""
    nota: int = Field(ge=1, le=5, description="Nota de 1 (muito difícil) a 5 (perfeitamente gerável)")
    motivo: str = Field(..., description="Justificativa técnica (física de fluidos/cabelos, mãos, consistência)")
    desafios_identificados: List[str] = Field(default_factory=list)


class ComentariosAnalise(BaseModel):
    """Dores e objeções extraídas diretamente dos comentários reais de clientes."""
    dores_citadas: List[str] = Field(default_factory=list)
    objecoes_citadas: List[str] = Field(default_factory=list)
    duvidas_frequentes: List[str] = Field(default_factory=list)


class PadraoItem(BaseModel):
    """Padrão identificado no vídeo com classificação de nível (produto vs transferível)."""
    nome_padrao: str
    descricao: str
    nivel: NivelPadraoEnum = Field(
        ...,
        description="produto (depende de característica específica) ou transferivel (aplicável à categoria)"
    )
    justificativa_nivel: str = Field(..., description="Por que é produto ou transferível")
    evidencia: str = Field(..., description="Trecho ou timestamp de evidência no vídeo")


# -------------------------------------------------------------
# CONTRATO PRINCIPAL DO DNA POR VÍDEO (FASE 1)
# -------------------------------------------------------------

class VideoDNA(BaseModel):
    """DNA criativo completo e estruturado extraído de um único vídeo de referência."""

    video_filename: str
    model_classification: str = Field(
        ...,
        description="Modelo narrativo identificado (ex: HAND_DEMO_VOICEOVER, PROBLEM_SOLUTION, STRESS_TEST_DEMO, etc.)"
    )
    metricas: Optional[MetricasReferencia] = Field(default=None)
    gancho: Optional[GanchoDNA] = Field(default=None, description="Análise estruturada do gancho nos primeiros 3 segundos")
    estrutura_cenas: List[CenaDNA] = Field(default_factory=list, description="Cenas identificadas com timestamps")
    arco_narrativo: Optional[str] = Field(default=None, description="Resumo do fluxo narrativo do vídeo")
    produto_analise: ProdutoDNA = Field(default_factory=ProdutoDNA)
    publico_analise: PublicoDNA = Field(default_factory=PublicoDNA)
    audio_texto: AudioTextoDNA = Field(default_factory=AudioTextoDNA)
    cta: CtaDNA = Field(default_factory=CtaDNA)
    claims: List[ClaimCheck] = Field(default_factory=list, description="Verificação de claims contra product_profile")
    gerabilidade_ia: Optional[GerabilidadeIA] = Field(default=None, description="Score e viabilidade de geração por IA")
    padroes_identificados: List[PadraoItem] = Field(default_factory=list, description="Padrões classificados em produto ou transferível")
    padroes_novos: List[str] = Field(default_factory=list, description="Lista aberta do que não coube nos enums")
    comentarios_analise: Optional[ComentariosAnalise] = Field(default=None)
    
    # Campos legados preservados para compatibilidade reversa
    hook_mechanism: Optional[str] = None
    visual_structure: Optional[str] = None
    audio_pattern: Optional[str] = None
    cta_type: Optional[str] = None
    faceless_score: int = Field(default=5, ge=0, le=10)
    faceless_analysis: Optional[str] = None

    model_config = {"extra": "allow"}


# -------------------------------------------------------------
# CONTRATOS DO CREATIVE REPORT CONSOLIDADO (FASE 2)
# -------------------------------------------------------------

class ReceitaVideo(BaseModel):
    """Receita criativa consolidada: dor x público x gancho x estrutura x prova."""
    receita_id: str
    dor_chave: str
    publico_chave: str
    gancho_tipo: str
    estrutura_resumo: str
    prova_usada: str
    cta_tipo: str
    video_count: int = Field(ge=1, description="Quantos vídeos usaram essa receita")
    evidencias: List[str] = Field(default_factory=list)
    score_tracao_medio: Optional[float] = None
    destaque_multiplo: bool = Field(default=False, description="True se aparece em 2 ou mais vídeos")


class AtributoPrevalencia(BaseModel):
    """Prevalência estatística ponderada por métricas de referência."""
    atributo: str
    categoria_atributo: str = Field(..., description="gancho, dor, prova, cta, etc.")
    ocorrencias: int = 0
    total_videos: int = 0
    prevalencia_percentual: float = 0.0
    tracao_ponderada_media: Optional[float] = None
    evidencias: List[str] = Field(default_factory=list)


class ModelUsageStats(BaseModel):
    model: str
    video_count: int = 0
    percentage: float = 0.0
    avg_faceless_score: float = 0.0
    avg_gerabilidade_ia: float = 0.0
    tracao_referencia_media: Optional[float] = None
    confidence: float = 0.0


class StrongestModel(BaseModel):
    model: str
    reason: str
    evidence: List[str] = Field(default_factory=list)
    tracao_score: Optional[float] = None


class NewModelCandidate(BaseModel):
    model_id: str
    name: str
    description: Optional[str] = None
    visual_structure: Optional[str] = None
    audio_pattern: Optional[str] = None
    nivel: NivelPadraoEnum = NivelPadraoEnum.TRANSFERIVEL


class DatasetInfo(BaseModel):
    video_count: int = 0
    product_count: int = 1
    videos_com_metricas: int = 0


class CreativeReport(BaseModel):
    """Relatório criativo consolidado com prevalência e receitas observadas (BEEMIDIA_CREATIVE_REPORT.json)."""

    report_id: str
    niche: str
    dataset: DatasetInfo = Field(default_factory=DatasetInfo)
    model_usage: List[ModelUsageStats] = Field(default_factory=list)
    strongest_models: List[StrongestModel] = Field(default_factory=list)
    receitas_observadas: List[ReceitaVideo] = Field(default_factory=list, description="Receitas dor x publico x gancho x estrutura x prova")
    receitas_destaque: List[ReceitaVideo] = Field(default_factory=list, description="Receitas que aparecem em >= 2 vídeos")
    prevalencia_atributos: List[AtributoPrevalencia] = Field(default_factory=list)
    
    # Listas agregadas e compatibilidade reversa
    recurring_hooks: List[str] = Field(default_factory=list)
    recurring_visual_patterns: List[str] = Field(default_factory=list)
    recurring_audio_patterns: List[str] = Field(default_factory=list)
    faceless_patterns: List[str] = Field(default_factory=list)
    new_model_candidates: List[NewModelCandidate] = Field(default_factory=list)

    model_config = {"extra": "allow"}
