import streamlit as st
import pandas as pd
import plotly.express as px
import os
import numpy as np

# Caminhos dos ficheiros CSV relativos ao diretório deste script
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_files = {
    'Audio 70/15/15': os.path.join(base_dir, '../metadata/splits/audio/tvt_70_15_15.csv'),
    'Audio 40/30/30': os.path.join(base_dir, '../metadata/splits/audio/tvt_40_30_30.csv'),
    'Lyrics 70/15/15': os.path.join(base_dir, '../metadata/splits/lyrics/tvt_70_15_15.csv'),
    'Lyrics 40/30/30': os.path.join(base_dir, '../metadata/splits/lyrics/tvt_40_30_30.csv'),
    'Bimodal 70/15/15': os.path.join(base_dir, '../metadata/splits/bimodal/tvt_70_15_15.csv'),
    'Bimodal 40/30/30': os.path.join(base_dir, '../metadata/splits/bimodal/tvt_40_30_30.csv'),
    'Merge Unified': os.path.join(base_dir, '../metadata/base/merge_unified.csv'),
}

# Define características de cada ficheiro
file_features = {
    'Audio 70/15/15': {'type': 'split', 'modality': 'audio', 'split_ratio': '70/15/15'},
    'Audio 40/30/30': {'type': 'split', 'modality': 'audio', 'split_ratio': '40/30/30'},
    'Lyrics 70/15/15': {'type': 'split', 'modality': 'lyrics', 'split_ratio': '70/15/15'},
    'Lyrics 40/30/30': {'type': 'split', 'modality': 'lyrics', 'split_ratio': '40/30/30'},
    'Bimodal 70/15/15': {'type': 'split', 'modality': 'bimodal', 'split_ratio': '70/15/15'},
    'Bimodal 40/30/30': {'type': 'split', 'modality': 'bimodal', 'split_ratio': '40/30/30'},
    'Merge Unified': {'type': 'unified', 'modality': 'all', 'split_ratio': 'N/A'}
}

st.title('Dashboard Dinâmico de Splits e Quadrantes')

# Seleção do ficheiro (com Merge Unified como padrão)
file_label = st.sidebar.selectbox('Escolha o ficheiro para análise:', 
                                 list(csv_files.keys()),
                                 index=list(csv_files.keys()).index('Merge Unified'))
file_path = csv_files[file_label]
file_type = file_features[file_label]['type']
file_modality = file_features[file_label]['modality']

# Carregar dados
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
else:
    st.error(f'Ficheiro não encontrado: {file_path}')
    st.stop()

# Informações sobre o ficheiro selecionado
st.sidebar.markdown("## Informações do Ficheiro")
st.sidebar.markdown(f"**Tipo:** {file_type.capitalize()}")
st.sidebar.markdown(f"**Modalidade:** {file_modality.capitalize()}")
st.sidebar.markdown(f"**Rácio de Split:** {file_features[file_label]['split_ratio']}")

# Filtros dinâmicos adaptados ao tipo de ficheiro
if "Quadrant" in df.columns:
    quadrants = sorted(df['Quadrant'].unique().tolist())
    selected_quadrants = st.sidebar.multiselect('Filtrar por Quadrante:', quadrants, default=quadrants)
else:
    st.sidebar.warning("Coluna 'Quadrant' não encontrada")
    selected_quadrants = []

# Define as variáveis globais para os tipos de split
split_types = ['balanced', 'complete']
split_names = ['train', 'validate', 'test', 'todos']

# Apenas mostrar filtros de split para ficheiros de tipo 'split'
if file_type == 'split':
    st.sidebar.markdown("## Filtros de Split")
    
    # Iniciar com 'complete' e 'todos' como valores padrão
    selected_split_type = st.sidebar.selectbox('Tipo de split:', split_types, index=split_types.index('complete'))
    selected_split = st.sidebar.selectbox('Split:', split_names, index=split_names.index('todos'))
    
    # Nome da coluna booleana para os ficheiros split
    if selected_split != 'todos':
        col_name = f'in_{selected_split_type}_{selected_split}'
    else:
        # Para "todos", não definimos col_name aqui - será tratado na lógica de filtragem
        pass
else:
    # Para o ficheiro unificado, usamos filtros de tipo (complete/balanced) e modalidade
    st.sidebar.markdown("## Filtros do Merge Unified")
    
    # Primeiro, selecionamos entre complete ou balanced
    filter_type_options = ['Todos', 'Complete', 'Balanced']
    selected_filter_type = st.sidebar.selectbox('Tipo de Filtro:', filter_type_options)
    
    # Verificar quais modalidades estão disponíveis baseado nas colunas de balanced
    modality_options = []
    if 'in_audio_balanced' in df.columns or selected_filter_type == 'Complete':
        modality_options.append('Audio')
    if 'in_lyrics_balanced' in df.columns or selected_filter_type == 'Complete':
        modality_options.append('Lyrics')
    if 'in_bimodal_balanced' in df.columns or selected_filter_type == 'Complete':
        modality_options.append('Bimodal')
    
    # Adicionar opção "Todos" no início
    if modality_options:
        modality_options = ['Todos'] + modality_options
        selected_modality = st.sidebar.selectbox('Modalidade:', modality_options)
    else:
        selected_modality = 'Todos'

# Filtragem inicial por quadrante (comum a todos os tipos)
if "Quadrant" in df.columns and selected_quadrants:
    mask = df['Quadrant'].isin(selected_quadrants)
    df_filtered = df[mask]
else:
    df_filtered = df

# Filtragem adicional baseada no tipo de ficheiro
if file_type == 'split':
    # Filtragem para ficheiros de split
    if selected_split == 'todos':
        # Para "todos", criamos uma máscara que combina train, validate e test
        mask = pd.Series(False, index=df_filtered.index)
        for split in ['train', 'validate', 'test']:
            split_col = f'in_{selected_split_type}_{split}'
            if split_col in df_filtered.columns:
                mask = mask | df_filtered[split_col]
        df_split = df_filtered[mask]
    elif col_name in df_filtered.columns:
        df_split = df_filtered[df_filtered[col_name] == True]
    else:
        st.warning(f'Coluna {col_name} não encontrada no ficheiro.')
        df_split = df_filtered
else:
    # Filtragem para ficheiro unificado
    df_temp = df_filtered.copy()
    
    # Aplicar filtros com base nas seleções do usuário
    if selected_filter_type != 'Todos' and selected_modality != 'Todos':
        # Caso específico: filtrar por tipo e modalidade
        if selected_filter_type == 'Balanced':
            # Aplicar filtro balanced para a modalidade selecionada
            balanced_col = f'in_{selected_modality.lower()}_balanced'
            if balanced_col in df.columns:
                df_temp = df_temp[df_temp[balanced_col] == True]
            else:
                st.warning(f"Coluna {balanced_col} não encontrada no ficheiro.")
        elif selected_filter_type == 'Complete':
            # Para o complete, usamos a lógica de modalidade apenas baseada nas colunas Song_id e Lyric_id
            if selected_modality == 'Audio':
                # Audio Complete: apenas os que têm Song_id (independente de ter ou não Lyric_id)
                if 'Song_id' in df_temp.columns:
                    df_temp = df_temp[df_temp['Song_id'].notna()]
            elif selected_modality == 'Lyrics':
                # Lyrics Complete: apenas os que têm Lyric_id (independente de ter ou não Song_id)
                if 'Lyric_id' in df_temp.columns:
                    df_temp = df_temp[df_temp['Lyric_id'].notna()]
            elif selected_modality == 'Bimodal':
                # Bimodal Complete: apenas os que têm ambos Song_id E Lyric_id
                if 'Song_id' in df_temp.columns and 'Lyric_id' in df_temp.columns:
                    df_temp = df_temp[df_temp['Song_id'].notna() & df_temp['Lyric_id'].notna()]
    elif selected_filter_type != 'Todos':
        # Filtrar apenas por tipo (balanced/complete)
        if selected_filter_type == 'Balanced':
            # União de todas as modalidades balanced
            mask = pd.Series(False, index=df_temp.index)
            for col in ['in_audio_balanced', 'in_lyrics_balanced', 'in_bimodal_balanced']:
                if col in df.columns:
                    mask = mask | df_temp[col]
            df_temp = df_temp[mask]
        elif selected_filter_type == 'Complete':
            # Para 'Complete' sem especificar modalidade, usamos todos os registros:
            # Audio Complete (tem Song_id) OU Lyrics Complete (tem Lyric_id)
            mask = pd.Series(False, index=df_temp.index)
            if 'Song_id' in df_temp.columns:
                mask = mask | df_temp['Song_id'].notna()
            if 'Lyric_id' in df_temp.columns:
                mask = mask | df_temp['Lyric_id'].notna()
            df_temp = df_temp[mask]
    elif selected_modality != 'Todos':
        # Filtrar apenas por modalidade
        if selected_modality == 'Audio':
            # Audio: tem Song_id (independente de ter Lyric_id ou não)
            if 'Song_id' in df_temp.columns:
                df_temp = df_temp[df_temp['Song_id'].notna()]
        elif selected_modality == 'Lyrics':
            # Lyrics: tem Lyric_id (independente de ter Song_id ou não)
            if 'Lyric_id' in df_temp.columns:
                df_temp = df_temp[df_temp['Lyric_id'].notna()]
        elif selected_modality == 'Bimodal':
            # Bimodal: tem ambos Song_id E Lyric_id
            if 'Song_id' in df_temp.columns and 'Lyric_id' in df_temp.columns:
                df_temp = df_temp[df_temp['Song_id'].notna() & df_temp['Lyric_id'].notna()]
            
    df_split = df_temp

# 1. Resumo Geral - adaptado ao tipo de ficheiro
st.header("Resumo Geral")
st.write(f"**Total de músicas no ficheiro:** {len(df)}")
st.write(f"**Total de músicas após filtros:** {len(df_split)}")

# Mostrar informações específicas do ficheiro
if "Quadrant" in df.columns:
    quadrant_counts = df['Quadrant'].value_counts().to_dict()
    st.write("**Distribuição por Quadrante:**")
    
    # Criar um dicionário ordenado por quadrante
    ordered_quadrants = {}
    for q in sorted(quadrant_counts.keys()):
        ordered_quadrants[q] = quadrant_counts[q]
    
    # Exibir como tabela formatada
    col1, col2 = st.columns(2)
    with col1:
        for q, count in list(ordered_quadrants.items())[:len(ordered_quadrants)//2 + len(ordered_quadrants)%2]:
            st.write(f"- {q}: {count} músicas")
    with col2:
        for q, count in list(ordered_quadrants.items())[len(ordered_quadrants)//2 + len(ordered_quadrants)%2:]:
            st.write(f"- {q}: {count} músicas")

# Inicializa a variável modalidades globalmente
modalidades = {}

# 2. Distribuição por Modalidade - apenas mostrar para o ficheiro unificado
if file_type == 'unified':
    st.subheader("Distribuição por Modalidade")
    # Verificar se temos as colunas básicas para determinar modalidade
    if 'Song_id' in df.columns and 'Lyric_id' in df.columns:
        # Criar classificação baseada em Song_id e Lyric_id
        audio_only = df[(df['Song_id'].notna()) & (df['Lyric_id'].isna())]
        lyrics_only = df[(df['Song_id'].isna()) & (df['Lyric_id'].notna())]
        
        # Para bimodal, preferimos a coluna específica se disponível
        if 'bimodal' in df.columns:
            bimodal = df[df['bimodal'] == True]
        else:
            bimodal = df[(df['Song_id'].notna()) & (df['Lyric_id'].notna())]
        
        # Construir o dicionário de modalidades
        modalidades = {
            "Audio Only": audio_only,
            "Lyrics Only": lyrics_only,
            "Bimodal": bimodal
        }
        modalidade_counts = {k: len(v) for k, v in modalidades.items()}
        st.bar_chart(pd.Series(modalidade_counts))
    else:
        st.warning(f"As colunas necessárias (Song_id, Lyric_id) estão ausentes")
        st.info(f"A distribuição por modalidade não pode ser mostrada para o ficheiro {file_label}")

# 3. Distribuição por Quadrante - comum a todos os ficheiros
if "Quadrant" in df.columns:
    st.subheader("Distribuição por Quadrante")
    # Usar o dataframe filtrado para mostrar a distribuição atual
    st.plotly_chart(px.histogram(df_split, x="Quadrant", color="Quadrant", 
                                 title="Distribuição por Quadrante após Filtros"))
    
    # Se estiver usando filtros, mostrar comparação antes/depois
    if len(df_split) != len(df):
        df_quadrant_counts = df['Quadrant'].value_counts().reset_index()
        df_quadrant_counts.columns = ['Quadrant', 'Total']
        
        df_split_quadrant_counts = df_split['Quadrant'].value_counts().reset_index()
        df_split_quadrant_counts.columns = ['Quadrant', 'Após Filtros']
        
        # Mesclar os dois dataframes
        comparison_df = df_quadrant_counts.merge(df_split_quadrant_counts, on='Quadrant', how='left')
        comparison_df['Após Filtros'].fillna(0, inplace=True)
        comparison_df['Após Filtros'] = comparison_df['Após Filtros'].astype(int)
        
        # Calcular a porcentagem de cada quadrante no conjunto filtrado
        comparison_df['% Mantido'] = (comparison_df['Após Filtros'] / comparison_df['Total'] * 100).round(1)
        
        st.write("**Comparação antes/depois dos filtros:**")
        st.dataframe(comparison_df)
else:
    st.warning("A coluna 'Quadrant' não está disponível neste ficheiro")

# 4. Valores Faltantes - útil para todos os ficheiros
st.subheader("Valores Faltantes por Coluna")
missing = df.isna().sum()
missing = missing[missing > 0]
if not missing.empty:
    st.bar_chart(missing)
else:
    st.success("Não há valores faltantes!")

# 5. Arousal e Valence - apenas relevante para o ficheiro unificado
if file_type == 'unified' and all(col in df.columns for col in ["Arousal", "Valence"]):
    st.subheader("Distribuição de Arousal e Valence")
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(px.histogram(df_split, x="Arousal", nbins=30, title="Distribuição de Arousal"))
    
    with col2:
        st.plotly_chart(px.histogram(df_split, x="Valence", nbins=30, title="Distribuição de Valence"))

    # Gráfico de dispersão Arousal vs Valence
    if "Quadrant" in df.columns:
        st.subheader("Arousal vs Valence por Quadrante")
        
        # Verificar se Artist e Title estão disponíveis para hover_data
        hover_cols = []
        if "Artist" in df.columns:
            hover_cols.append("Artist")
        if "Title" in df.columns:
            hover_cols.append("Title")
            
        fig = px.scatter(df_split, x="Arousal", y="Valence", color="Quadrant", 
                        hover_data=hover_cols, title="Distribuição no espaço emocional")
        
        # Adicionar linhas para os quadrantes
        fig.add_hline(y=0.5, line_dash="dash", line_color="gray")
        fig.add_vline(x=0.5, line_dash="dash", line_color="gray")
        
        # Adicionar anotações para os quadrantes
        fig.add_annotation(x=0.25, y=0.75, text="Q2", showarrow=False)
        fig.add_annotation(x=0.75, y=0.75, text="Q1", showarrow=False)
        fig.add_annotation(x=0.25, y=0.25, text="Q3", showarrow=False)
        fig.add_annotation(x=0.75, y=0.25, text="Q4", showarrow=False)
        
        st.plotly_chart(fig)

# 6. Conjuntos Balanceados
st.subheader("Registros em Conjuntos Balanceados")
for col in ["in_audio_balanced", "in_lyrics_balanced", "in_bimodal_balanced"]:
    if col in df.columns:
        st.write(f"**{col}:** {df[col].sum()}")

# 7. Exemplos de Registros
st.subheader("Exemplos de Registros por Modalidade")

# Verificar se as modalidades foram definidas (depende das colunas has_audio, has_lyrics, etc)
if modalidades:
    for name, subset in modalidades.items():
        st.write(f"**{name}:**")
        # Verificar também se todas as colunas esperadas estão disponíveis
        display_cols = ["Song_id", "Artist", "Title", "Quadrant", "Arousal", "Valence"]
        available_cols = [col for col in display_cols if col in subset.columns]
        if not available_cols:
            st.warning(f"Nenhuma das colunas esperadas encontradas para {name}")
        else:
            st.dataframe(subset[available_cols].head(3))
else:
    # Se não temos modalidades, mostrar exemplos genéricos do DataFrame
    st.write("**Exemplos de registros (geral):**")
    st.dataframe(df.head(3))

# Métricas principais
st.subheader('Métricas Gerais')
st.metric('Total de Registos', len(df))
st.metric('Registos Selecionados', len(df_split))

if "Quadrant" in df_split.columns:
    st.write('Distribuição por Quadrante (dados filtrados):')
    st.bar_chart(df_split['Quadrant'].value_counts())
else:
    st.warning("A coluna 'Quadrant' não está disponível para mostrar a distribuição")

# Tabela interativa
st.subheader('Tabela de Dados Filtrados')
st.dataframe(df_split)

# Distribuição dos splits
st.subheader('Distribuição dos Splits (Balanced e Complete)')
for split_type in split_types:
    st.write(f'**{split_type.capitalize()}**')
    counts = {}
    # Contagem para train, validate e test
    for split in ['train', 'validate', 'test']:
        col = f"in_{split_type}_{split}"
        if col in df.columns:
            counts[split] = df[df[col] == True].shape[0]
    
    # Adicionar contagem para "todos" (união de train, validate e test)
    if all(f"in_{split_type}_{split}" in df.columns for split in ['train', 'validate', 'test']):
        mask = pd.Series(False, index=df.index)
        for split in ['train', 'validate', 'test']:
            split_col = f'in_{split_type}_{split}'
            mask = mask | df[split_col]
        counts['todos'] = mask.sum()
    
    if counts:
        st.bar_chart(pd.Series(counts))