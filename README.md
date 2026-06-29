# Pipeline de Dados e Análise Multidimensional do Metagame VGC (2022-2024)

Este projeto implementa um pipeline completo de Engenharia de Dados (ETL) e análise de grafos utilizando **Python (Pandas)** e **Neo4j**. O objetivo é mapear, integrar e auditar a evolução do cenário competitivo de Pokémon (VGC) entre os anos de 2022 e 2024, comparando o desempenho de monstrinhos em torneios da Smogon e no circuito oficial do Worlds.

---

## 🏗️ Arquitetura do Projeto

O pipeline foi desenhado seguindo as melhores práticas de engenharia de software e divisão de camadas de dados:

1. **Camada Bronze (Raw Data):** Leitura de arquivos brutos (`pokemon_sujo_para_etl.csv`) contendo strings inconsistentes, abreviações incorretas de gerações e dados faltantes de taxas de uso.
2. **Camada Silver (Staging Area / Parquet):** Processo de limpeza, normalização de texto (trimming e casing), tratamento de valores nulos/N/A e mapeamento por dicionário de numerais romanos para inteiros. Os dados limpos são persistidos localmente no formato binário **Parquet** utilizando a engine `fastparquet` para garantir compatibilidade e eficiência de IO no ambiente Python 3.14.
3. **Camada Gold (Graph Ingestion / Neo4j):** Carga de dados otimizada em lote (*batch processing*) utilizando a cláusula `UNWIND` no Cypher. O modelo em grafo elimina a necessidade de JOINS complexos e centraliza a análise em relacionamentos de alta performance.

---

## 📊 Modelo de Dados (Grafo)

O ecossistema foi modelado de forma a expressar a teia de conexões anatômicas e de performance dos Pokémon:

* **Nós:** `(:Pokemon)`, `(:Tipo)`, `(:Habilidade)`, `(:Torneio)`
* **Relacionamentos:**
  * `(:Pokemon)-[:POSSUI_TIPO {ordem: "principal"|"secundario"}]->(:Tipo)`
  * `(:Pokemon)-[:POSSUI_HABILIDADE {tipo: "comum"|"oculta"}]->(:Habilidade)`
  * `(:Pokemon)-[:COMPETIU_EM {taxa_uso: Float}]->(:Torneio {nome: String, ano: Integer})`

---

## 🔍 Painel de Consultas Analíticas (Cypher)

O ecossistema de consultas foi rigorosamente dividido em três níveis estratégicos para demonstrar a versatilidade do modelo:

### 1. Consultas Normais (Mapeamento de Estrutura Básica)
Focadas em validar a integridade anatômica do banco após a ingestão.
* **Consulta 1:** Top 10 Pokémon com maior velocidade base (uso de ordenação composta e paginação).
* **Consulta 2:** Distribuição de volume absoluto de Pokémon por tipo primário.
* **Consulta 3:** As 10 habilidades mais comuns integradas à Pokédex.

### 2. Consultas Complexas (Interconexão Multidimensional de Caminhos)
Explotam o verdadeiro poder de um banco de grafos, realizando múltiplos saltos por setas e nós vizinhos sem depender de tabelas engessadas.
* **Consulta 4:** Rastreamento do caminho da dominância de habilidades ocultas raras em torneios com corte crítico de uso de 15% em 2024 (`Torneio -> Seta de Uso -> Pokemon -> Habilidade Oculta`).
* **Consulta 5 (Sinergia Elemental):** Consulta puramente em formato de "V" que localiza interseções conceituais opostas. Descobre quais Pokémon de elementos conflitantes (`Fire` e `Water`) compartilham a exata mesma habilidade.
* **Consulta 6 (A Teia Completa):** Mapeamento hierárquico máximo que cruza simultaneamente 4 nós (`Torneio -> Competicao -> Pokemon -> Tipo -> Habilidade`) para trazer a foto instantânea dos líderes de 2024.

### 3. Consultas Sérias (Análise Estratégica e Data Analytics)
Extração de inteligência competitiva e análise de tendências temporais agregadas.
* **Consulta 7 (Centralização de Mercado):** Monitora a saúde e a diversidade do meta de cada ano do Worlds, listando detalhadamente quem quebrou a barreira de dominância de 30% de uso.
* **Consulta 8 (Hiperconsistência Histórica):** Identifica e calcula a média de uso dos monstrinhos imutáveis que registraram presença ativa em todos os 6 torneios presentes no banco simultaneamente.
* **Consulta 9 (Efeito das Habilidades Ocultas):** Consolida a média de uso de cada Pokémon em 2024 sob o espectro de suas habilidades ocultas, agrupando torneios duplicados em métricas limpas e legíveis.
* **Consulta 10 (Análise de Variância e Evolução Temporal):** Realiza um `MATCH` duplo e paralelo no grafo para calcular quais Pokémon veteranos ativos desde 2022 obtiveram o maior crescimento absoluto de taxa de uso em 2024, isolando e blindando a análise contra os dados zerados das estreias da Geração 9.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.14**
* **Pandas & NumPy**
* **Fastparquet** (Persistência e Staging)
* **Neo4j Graph Database** (Driver Oficial `neo4j`)
* **Jupyter Notebook**

---

## 🚀 Como Executar

1. Certifique-se de ter as credenciais do Neo4j configuradas em seu arquivo `.env`:
   ```env
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=sua_senha
