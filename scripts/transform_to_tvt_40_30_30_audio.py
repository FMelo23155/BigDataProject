import pandas as pd
import os

def transform_to_tvt_40_30_30_audio():
    """
    Transforma os 6 ficheiros CSV individuais num único ficheiro consolidado
    com a estrutura: Song_id,Quadrant,in_balanced_train,in_balanced_validate,in_balanced_test,in_complete_train,in_complete_validate,in_complete_test
    """
    
    # Caminhos dos ficheiros de origem
    base_path = r"c:\Users\aluno23155\Desktop\ProjetoBigData23155\metadata\last\lastsplits"
    output_path = r"c:\Users\aluno23155\Desktop\ProjetoBigData23155\metadata\splits\audio\tvt_40_30_30.csv"
    
    # Definir os ficheiros CSV de origem
    csv_files = {
        'balanced_test': 'tvt_40_30_30_test_audio_balanced.csv',
        'balanced_train': 'tvt_40_30_30_train_audio_balanced.csv', 
        'balanced_validate': 'tvt_40_30_30_validate_audio_balanced.csv',
        'complete_test': 'tvt_40_30_30_test_audio_complete.csv',
        'complete_train': 'tvt_40_30_30_train_audio_complete.csv',
        'complete_validate': 'tvt_40_30_30_validate_audio_complete.csv'
    }
    
    # Verificar se todos os ficheiros existem
    for split_type, filename in csv_files.items():
        file_path = os.path.join(base_path, filename)
        if not os.path.exists(file_path):
            print(f"ERRO: Ficheiro não encontrado: {file_path}")
            return
    
    print("Iniciando transformação...")
    
    # Coletar todas as combinações únicas de Song_id e Quadrant
    all_songs = set()
    
    # Primeiro, vamos coletar todas as músicas únicas
    for split_type, filename in csv_files.items():
        file_path = os.path.join(base_path, filename)
        df = pd.read_csv(file_path)
        print(f"Processando {filename}: {len(df)} entradas")
        
        for _, row in df.iterrows():
            song_id = row['Song']
            quadrant = row['Quadrant']
            all_songs.add((song_id, quadrant))
    
    print(f"Total de músicas únicas encontradas: {len(all_songs)}")
    
    # Criar o DataFrame final
    final_data = []
    
    for song_id, quadrant in sorted(all_songs):
        # Inicializar todas as colunas como False
        row = {
            'Song_id': song_id,
            'Quadrant': quadrant,
            'in_balanced_train': False,
            'in_balanced_validate': False,
            'in_balanced_test': False,
            'in_complete_train': False,
            'in_complete_validate': False,
            'in_complete_test': False
        }
        
        # Verificar em que splits esta música aparece
        for split_type, filename in csv_files.items():
            file_path = os.path.join(base_path, filename)
            df = pd.read_csv(file_path)
            
            # Verificar se esta música está neste split
            song_in_split = df[(df['Song'] == song_id) & (df['Quadrant'] == quadrant)]
            
            if not song_in_split.empty:
                if split_type == 'balanced_train':
                    row['in_balanced_train'] = True
                elif split_type == 'balanced_validate':
                    row['in_balanced_validate'] = True
                elif split_type == 'balanced_test':
                    row['in_balanced_test'] = True
                elif split_type == 'complete_train':
                    row['in_complete_train'] = True
                elif split_type == 'complete_validate':
                    row['in_complete_validate'] = True
                elif split_type == 'complete_test':
                    row['in_complete_test'] = True
        
        final_data.append(row)
    
    # Criar DataFrame final
    final_df = pd.DataFrame(final_data)
    
    # Criar diretório de destino se não existir
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # Guardar o ficheiro
    final_df.to_csv(output_path, index=False)
    
    print(f"\n✅ Transformação concluída!")
    print(f"Ficheiro criado: {output_path}")
    print(f"Total de entradas: {len(final_df)}")
    
    # Estatísticas finais
    print("\n=== Estatísticas Finais ===")
    print(f"Balanced train: {final_df['in_balanced_train'].sum()}")
    print(f"Balanced validate: {final_df['in_balanced_validate'].sum()}")
    print(f"Balanced test: {final_df['in_balanced_test'].sum()}")
    print(f"Complete train: {final_df['in_complete_train'].sum()}")
    print(f"Complete validate: {final_df['in_complete_validate'].sum()}")
    print(f"Complete test: {final_df['in_complete_test'].sum()}")
    
    print("\n=== Distribuição por Quadrante ===")
    print(final_df['Quadrant'].value_counts().sort_index())
    
    return final_df

if __name__ == "__main__":
    transform_to_tvt_40_30_30_audio()
