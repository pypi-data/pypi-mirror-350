import os
import shutil

def copy_recursive(src_dir, dest_dir, extension, pretty_src_base=None, pretty_dst_base=None):
    if not os.path.exists(src_dir):
        print(f"❌ Error: La carpeta {src_dir} no existe.")
        return

    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if any(file.endswith(ext) for ext in extension):
                src_file = os.path.join(root, file)

                # Calcular ruta relativa para mantener la estructura
                relative_path = os.path.relpath(src_file, src_dir)
                dst_file = os.path.join(dest_dir, relative_path)
                        
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                shutil.copy2(src_file, dst_file)

                # Formato bonito para logs
                pretty_src = os.path.relpath(src_file, pretty_src_base or src_dir)
                pretty_dst = os.path.relpath(dst_file, pretty_dst_base or dest_dir)

                print(f"✅ Copiado: {pretty_src} → {pretty_dst}")

def copy_content(dest_path, content, filename='archivo'):
    if not os.path.exists(dest_path):
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Archivo {filename} creado en {dest_path}")
    else:
        print(f"⚠️ Archivo {filename} ya existe en {dest_path}")
