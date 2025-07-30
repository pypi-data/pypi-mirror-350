import os
import platform
import shutil
from .utils import _load_library



# Obtém o caminho absoluto do diretório deste pacote
#pkg_dir = os.path.dirname(os.path.abspath(__file__))

# Define o caminho para a pasta ".libs" (dentro do pacote)
#libs_dir = os.path.join(pkg_dir, ".libs")

# Se estivermos no Windows e a pasta ".libs" existir, move os arquivos para o diretório do pacote
#if platform.system() == "Windows" and os.path.exists(libs_dir):
#    for filename in os.listdir(libs_dir):
#        src = os.path.join(libs_dir, filename)
#        dst = os.path.join(pkg_dir, filename)
#        shutil.move(src, dst)

# Agora, importe os módulos desejados para expor suas funções
from .manage_os import occluded_surface
from .respak import osp
from .set_parameters import get_radii
from .set_parameters import set_radii
from .set_parameters import reset_radii
