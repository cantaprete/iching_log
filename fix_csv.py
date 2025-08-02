import pandas as pd
import datetime

# Carica il file CSV con ; come separatore
def load_csv(file_path):
    try:
        data = pd.read_csv(file_path, sep=';')
        return data
    except Exception as e:
        print(f"Errore nel caricamento del file: {e}")
        return None

# Trasforma la data in Unix epoch
def date_to_unix_epoch(date_str):
    try:
        # Il formato della data sembra essere "dd/mm/yy, hh:mm:ss"
        date_obj = datetime.datetime.strptime(date_str, "%d/%m/%y, %H:%M:%S")
        unix_epoch = int(date_obj.timestamp())
        return unix_epoch
    except Exception as e:
        print(f"Errore nella conversione della data: {e}")
        return None

# Applica la trasformazione alla prima colonna
def transform_date_to_epoch(data, column_name):
    try:
        data['time'] = data[column_name].apply(date_to_unix_epoch)
        # Se vuoi eliminare la colonna originale, uncomment la linea sotto
        # data.drop(column_name, axis=1, inplace=True)
        return data
    except Exception as e:
        print(f"Errore nell'applicazione della trasformazione: {e}")
        return None

# Main
if __name__ == "__main__":
    file_path = 'sig.csv'  # Sostituisci con il percorso del tuo file CSV
    output_file_path = 'output.csv'  # Percorso del file di output
    
    data = load_csv(file_path)
    if data is not None:
        column_name = data.columns[0]  # La prima colonna
        transformed_data = transform_date_to_epoch(data, column_name)
        if transformed_data is not None:
            transformed_data.to_csv(output_file_path, sep=';', index=False)
            print(f"Risultato scritto in {output_file_path}")
