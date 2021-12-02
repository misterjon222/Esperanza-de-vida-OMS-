from base import Base, engine, Session
from article import Article
import pandas as pd
import argparse
import logging
logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__name__)

def main(filename):
    Base.metadata.create_all(engine)
    session = Session()
    articles = pd.read_csv(filename, encoding='utf-8')

    logger.info('Iniciando el proceso de carga de artículos a la Base de Datos')
    for index, row in articles.iterrows():
        logger.info(
            'Cargando el artículo con uid: {} en la BD'.format(row['uid']))
        article = Article(row['uid'],
                          row['body'],
                          row['host'],
                          row['newspaper_uid'],
                          row['n_tokens_title'],
                          row['title'],
                          row['url'],)
        session.add(article)

    session.commit()
    session.close()
    logger.info('Terminó el proceso de carga de artícuos a la Base de Datos')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                        help='El archivo que deseas cargar hacia la Base de Datos',
                        type=str)

    args = parser.parse_args()

    main(args.filename)
