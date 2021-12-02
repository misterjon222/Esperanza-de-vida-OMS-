import subprocess
import logging
from extract.GestionArchivos import GestionArchivos

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def main():
    _extract()
    _transform()
    _load()
    logger.info('Proceso a termino satisfactoria mente')



def _extract():
    logger.info('#####Iniciando el proceso de extracción#####')

    subprocess.run(['python', 'main.py'], cwd='./extract')

    subprocess.run(['move', r'extract\*.csv', r'transform'], shell=True)
    subprocess.run(['del', r'extract\*.rar'], shell=True)

def _transform():
    logger.info('#####Iniciando el proceso de Transformación#####')

    gestionArchivos = GestionArchivos()

    ficheros_csv = gestionArchivos.getFilesCSVFromOrigin('./transform')

    for fichero in ficheros_csv:

        subprocess.run(
            ['python', 'main.py', fichero["FICHERO"]], cwd='./transform')
        subprocess.run(['del', fichero["FICHERO"]],
                       shell=True, cwd='./transform')

    subprocess.run(['move', r'transform\*.csv', r'load'], shell=True)

def _load():
    logger.info('#####Iniciando el proceso de Carga#####')

    gestionArchivos = GestionArchivos()

    ficheros_csv = gestionArchivos.getFilesCSVFromOrigin('./load')

    for fichero in ficheros_csv:

        subprocess.run(
            ['python', 'main.py', fichero["FICHERO"]], cwd='./load')
        subprocess.run(['del', fichero["FICHERO"]],
                       shell=True, cwd='./load')

if __name__ == '__main__':
    main()
