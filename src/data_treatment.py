import pandas as pd
import numpy as np
import random

# 1. Lê o seu arquivo original completo (as 1303 linhas)
df = pd.read_csv("data/arquivo_base.csv")

# Listas de "sujeiras"
termos_no_usage = ["NoUsage", "no usage", "none", "NO", "NULL", "N/A", "   ", "-", "zero"]
termos_no_ability = ["No_ability", "None", "no-ability", "N/A", "sem_habilidade", "   ", "NULL", "none"]

# 2. Bagunçando as colunas de torneios
colunas_torneio = [c for c in df.columns if 'Usage' in c]
for col in colunas_torneio:
    df[col] = df[col].astype(str)
    # Apenas 35% de chance de trocar um valor vazio/zero por uma string suja (para não ficar artificial)
    df[col] = df[col].apply(lambda x: random.choice(termos_no_usage) if (x in ['NoUsage', '0.0', '0', 'nan']) and (random.random() < 0.35) else x)

# 3. Injetando caos nas strings (Nomes, Tipos, Habilidades)
colunas_texto = ['name', 'type1', 'type2', 'ability1', 'ability2', 'hidden_ability']
for col in colunas_texto:
    df[col] = df[col].astype(str)
    
    # Sujando os nulos de habilidade
    if col == 'ability2':
        df[col] = df[col].apply(lambda x: random.choice(termos_no_ability) if x in ['No_ability', 'None', 'nan'] else x)
        
    # 15% de chance de colocar tudo maiúsculo com espaços, 15% de chance de tudo minúsculo com espaços
    df[col] = df[col].apply(lambda x: 
        f"  {x.upper()} " if random.random() < 0.15 else 
        f"{x.lower()}   " if random.random() < 0.15 else 
        x
    )

# 4. Bagunçando a coluna de Geração (30% de chance total de erro de formatação)
df['generation'] = df['generation'].astype(str).apply(lambda x:
    x.replace("generation-", "generation -   ") if random.random() < 0.1 else
    x.replace("generation-", "GEN_") if random.random() < 0.1 else
    x.replace("generation-", "Geraçao-").upper() if random.random() < 0.1 else
    x
)

# 5. Exporta o arquivo final sujo para você usar no trabalho!
df.to_csv("data/pokemon_competitive_analysis.csv", index=False)
print("✓ Arquivo 'data/pokemon_competitive_analysis.csv' com 1300 linhas corrompidas gerado com sucesso!")