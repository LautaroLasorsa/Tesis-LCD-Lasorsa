import os

# Directorio actual
dir_actual = os.getcwd()

# Recorrer directorios y subdirectorios
for root, dirs, files in os.walk(dir_actual):
    for file in files:
        if file.endswith('.ini'):
            # Construir la ruta completa del archivo
            file_path = os.path.join(root, file)
            try:
                # Borrar el archivo
                os.remove(file_path)
                print(f'Archivo borrado: {file_path}')
            except Exception as e:
                print(f'No se pudo borrar el archivo {file_path}: {e}')
