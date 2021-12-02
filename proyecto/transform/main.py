from nltk.corpus import stopwords
import nltk
import pandas as pd
from urllib.parse import urlparse
import hashlib
import argparse
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(file_name):
    logger.info('Iniciando Proceso de limpieza de Datos...')

    df = _read_data(file_name)
    newspaper_uid = _extract_newspaper_uid(file_name)
    df = _add_newspaper_uid_column(df, newspaper_uid)
    df = _extract_host(df)
    df = _fill_missing_titles(df)
    df = _generate_uids_for_rows(df)
    df = _remove_scape_characters_from_body(df)
    df = _data_enrichment(df)
    df = _remove_duplicate_entries(df, 'title')
    df = drop_rows_with_missing_values(df)
    _save_data_to_csv(df, file_name)

    return df

def _read_data(file_name):
    logger.info('Leyendo el archivo {}'.format(file_name))
    return pd.read_csv(file_name, encoding='utf-8')

def _extract_newspaper_uid(file_name):
    logger.info('Extrayendo el newspaper uid')
    newspaper_uid = file_name.split('_')[0]

    logger.info('Newspaper udi Detectado: {}'.format(newspaper_uid))
    return newspaper_uid

def _add_newspaper_uid_column(df, newspaper_uid):
    logger.info('Llenando la columna newspaper_uid con {}'.format(newspaper_uid))
    df['newspaper_uid'] = newspaper_uid

    return df

def _extract_host(df):
    logger.info('Extrayendo el host de la url')

    df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)

    return df

def _fill_missing_titles(df):
    logger.info('Rellenando los títulos faltantes')
    missing_titles_mask = df['title'].isna()

    missing_titles = (df[missing_titles_mask]['url']
                      .str.extract(r'(?P<missing_titles>[^/]+)$')
                      .applymap(lambda title: title.split('-'))
                      .applymap(lambda title_word_list: ' '.join(title_word_list).capitalize())
                      )

    df.loc[missing_titles_mask, 'title'] = missing_titles.loc[:, 'missing_titles']

    return df

def _generate_uids_for_rows(df):
    logger.info('Generando los uids para cada fila')
    uids = (df
            .apply(lambda row: hashlib.md5(bytes(row['url'].encode())), axis=1)
            .apply(lambda hash_object: hash_object.hexdigest())
            )
    df['uid'] = uids
    return df.set_index('uid')

def _remove_scape_characters_from_body(df):
    logger.info('Eliminando los caracteres de escape del body')

    stripped_body = df.apply(lambda row: row['body'].replace(
        '\n', '').replace('\r', ''), axis=1)

    df['body'] = stripped_body

    return df

def _data_enrichment(df):
    logger.info('Enriqueciendo el df contando los tokens')

    df['n_tokens_title'] = tokenize_column(df, 'title')
    df['n_tokens_body'] = tokenize_column(df, 'body')

    return df

def tokenize_column(df, column_name):
    stop_words = set(stopwords.words('spanish'))

    return (df
            .dropna()  
            .apply(lambda row: nltk.word_tokenize(row[column_name]), axis=1)
            .apply(lambda tokens: list(filter(lambda token: token.isalpha(), tokens)))
            .apply(lambda tokens: list(map(lambda token: token.lower(), tokens)))
            .apply(lambda word_list: list(filter(lambda word: word not in stop_words, word_list)))
            .apply(lambda valid_word_list: len(valid_word_list))
            )
def _remove_duplicate_entries(df, column_name):
    logger.info('Eliminando entradas duplicadas')
    df.drop_duplicates(subset=[column_name], keep='first', inplace=True)

    return df
def drop_rows_with_missing_values(df):
    logger.info('Eliminando entradas con valores faltantes')
    return df.dropna()

def _save_data_to_csv(df, filename):
    clean_filename = 'clean_{}'.format(filename)
    logger.info(
        'Guardando los datos limpios en el archivo: {}'.format(clean_filename))
    df.to_csv(clean_filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name',
                        help='La ruta al dataset sucio',
                        type=str)
    args = parser.parse_args()
    df = main(args.file_name)

    print(df)
