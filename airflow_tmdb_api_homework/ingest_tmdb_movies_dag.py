from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import Variable
from datetime import datetime, timedelta
import requests
import logging


DAG_ID = 'tmdb_movie_ingest'
POSTGRES_CONN_ID = 'postgresql_conn'
TABLE_NAME = 'tmdb_movie_discover'
TMDB_TOKEN_VAR = 'tmdb_api_token' 
MIN_RECORDS = 500

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def fetch_and_load_movies(**kwargs):

    try:
        api_token = Variable.get(TMDB_TOKEN_VAR)
    except KeyError:
        raise ValueError(f"Variable {TMDB_TOKEN_VAR} not found. Please set it in Admin -> Variables.")

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_token}"
    }

    movies_to_insert = []
    page = 1
    total_fetched = 0
    

    while total_fetched < MIN_RECORDS:
        url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={page}&sort_by=popularity.desc"
        
        logging.info(f"Fetching page {page}...")
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            logging.error(f"Failed to fetch page {page}: {response.text}")
            raise Exception(f"API Error: {response.status_code}")

        data = response.json()
        results = data.get('results', [])
        
        if not results:
            logging.warning("No more results found.")
            break

        for movie in results:
           
            row = (
                movie.get('adult'),
                movie.get('backdrop_path'),
                movie.get('genre_ids'),
                movie.get('id'),
                movie.get('original_language'),
                movie.get('original_title'),
                movie.get('overview'),
                movie.get('popularity'),
                movie.get('poster_path'),
                movie.get('release_date'),
                movie.get('title'),
                movie.get('video'),
                movie.get('vote_average'),
                movie.get('vote_count')
            )
            movies_to_insert.append(row)
        
        total_fetched += len(results)
        page += 1

    logging.info(f"Total movies fetched: {len(movies_to_insert)}")

    pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
    
    target_fields = [
        'adult', 'backdrop_path', 'genre_ids', 'id', 'original_language',
        'original_title', 'overview', 'popularity', 'poster_path', 
        'release_date', 'title', 'video', 'vote_average', 'vote_count'
    ]

    logging.info(f"Inserting {len(movies_to_insert)} rows into {TABLE_NAME}...")
    
    pg_hook.insert_rows(
        table=TABLE_NAME,
        rows=movies_to_insert,
        target_fields=target_fields,
        commit_every=1000
    )

with DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    description='Ingest 500+ movies from TMDB to Postgres',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@once',
    catchup=False,
    tags=['tmdb', 'postgres', 'ingest']
) as dag:

    create_table_task = PostgresOperator(
        task_id='create_table',
        postgres_conn_id=POSTGRES_CONN_ID,
        sql=f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                adult boolean,
                backdrop_path text,
                genre_ids integer[],
                id bigint,
                original_language text,
                original_title text,
                overview text,
                popularity double precision,
                poster_path text,
                release_date text,
                title text,
                video boolean,
                vote_average double precision,
                vote_count integer
            );
        """
    )

    ingest_task = PythonOperator(
        task_id='fetch_and_load_movies',
        python_callable=fetch_and_load_movies
    )

    create_table_task >> ingest_task