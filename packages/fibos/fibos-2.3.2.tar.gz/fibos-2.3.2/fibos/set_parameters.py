import pandas as pd
import re
import pkgutil
import os
import io
import shutil

def get_radii():
    name_pack = "fibos"
    path_pack = pkgutil.get_loader(name_pack).get_filename()
    path_pack = os.path.dirname(path_pack)
    path_abs = os.path.abspath(path_pack)
    path_abs = path_abs+"/radii"
    larguras_colunas = [11, 4] # Largura do campo 1, Largura do campo 2
    nomes_colunas = ['ATOM', 'RAY']
    try:
        radii_value = pd.read_fwf(path_abs, widths=larguras_colunas, header=None, names=nomes_colunas)

    except FileNotFoundError:
        print(f"Err: radii file not found.")
        exit()
    except Exception as e:
        print(f"Err to read file: {e}")
        exit()
    return(radii_value)

def set_radii(radii_value):
        name_pack = "fibos"
        path_pack = pkgutil.get_loader(name_pack).get_filename()
        path_pack = os.path.dirname(path_pack)
        path_abs = os.path.abspath(path_pack)
        path_radii = path_abs+"/radii"
        try:
            with open(path_radii, 'w') as f:
                for index, row in radii_value.iterrows():
                    linha_formatada = f"{str(row['ATOM']):<11s}{row['RAY']:.2f}\n"
                    f.write(linha_formatada)#

        except Exception as e:
            print(e)
   
def reset_radii():
    name_pack = "fibos"
    path_pack = pkgutil.get_loader(name_pack).get_filename()
    path_pack = os.path.dirname(path_pack)
    path_abs = os.path.abspath(path_pack)
    path_radii = path_abs+"/radii"
    path_pattern = path_abs+"/pattern"
    os.remove(path_radii)
    shutil.copy(path_pattern,path_radii)
