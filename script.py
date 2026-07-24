import os
import glob
from PIL import Image

def detect_encoding(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read()
        return 'utf-8'
    except UnicodeDecodeError:
        return 'utf-16'

def process():
    print("Iniciando compresión a WebP...")
    img_dir = "img"
    files = glob.glob(os.path.join(img_dir, '*.*'))
    
    total_before = 0
    total_after = 0
    
    for filepath in files:
        if filepath.endswith('.webp') or 'temporal.txt' in filepath or filepath.endswith('.txt'):
            continue
            
        try:
            total_before += os.path.getsize(filepath)
            img = Image.open(filepath)
            
            # Convertir a WebP
            new_filepath = filepath.rsplit('.', 1)[0] + '.webp'
            img.save(new_filepath, 'WEBP', quality=80, method=6)
            total_after += os.path.getsize(new_filepath)
            
            # Borrar original
            img.close()
            os.remove(filepath)
            print(f"Convertido: {os.path.basename(filepath)} -> {os.path.basename(new_filepath)}")
        except Exception as e:
            print(f"Error procesando {filepath}: {e}")
            
    print(f"\nTamaño original: {total_before/1024/1024:.2f} MB")
    print(f"Tamaño nuevo: {total_after/1024/1024:.2f} MB")
    print(f"Ahorro: {100 - (total_after/total_before)*100:.1f}%\n")
    
    # Actualizar código
    files_to_update = ['app.js', 'index.html', 'sw.js', 'manifest.json']
    for file in files_to_update:
        if os.path.exists(file):
            enc = detect_encoding(file)
            with open(file, 'r', encoding=enc) as f:
                content = f.read()
                
            content = content.replace('.png', '.webp').replace('.jpg', '.webp')
            
            with open(file, 'w', encoding=enc) as f:
                f.write(content)
            print(f"Actualizado {file} ({enc})")

if __name__ == '__main__':
    process()
