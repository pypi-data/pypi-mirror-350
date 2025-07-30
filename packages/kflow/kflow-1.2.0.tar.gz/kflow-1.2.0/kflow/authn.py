import os
import logging
from functools import lru_cache

# Add a connection pool cache
_connection_pools = {}

@lru_cache(maxsize=5)
def _get_connection_string(base_env: str):
    """Cache connection strings to avoid repeated AWS Secrets Manager calls"""
    rename_secret = {"PrismaProd":"prisma_bd",
                    "WarehouseProd":"secret-redshift-cluster-1",
                    "Vekna":"vekna_cluster",
                    "Data_RDS":"data_rds"
                    }                       
    try:           
        secret_name = rename_secret[base_env]
    except:
        raise ValueError('No se reconoce la BD solicitada')

    secret_value = get_secret(secret_name) 

    if secret_name == 'vekna_cluster':
        sql_connector="postgresql"
        db_name = 'vekna'
    elif secret_name == 'data_rds':
        sql_connector="postgresql"
        db_name = 'postgres'
    elif secret_name == 'secret-redshift-cluster-1':
        sql_connector="redshift+psycopg2"
        db_name = 'warehouse'                
    elif secret_name == 'prisma_bd':
        sql_connector="postgresql"
        db_name = 'prisma'       
    else:
        raise ValueError('Current BD environment not recognized')

    return f"{sql_connector}://{secret_value['username']}:{secret_value['password']}@{secret_value['host']}:{secret_value['port']}/{db_name}"

def getConnectionDB(base_env:str):
    """
    Get a database connection with connection pooling.
    Reuses existing connection pools to avoid connection churning.
    """
    from sqlalchemy import create_engine
    from sqlalchemy.pool import QueuePool
    
    # Check if we already have a connection pool for this environment
    if base_env in _connection_pools:
        return _connection_pools[base_env]
    
    conn_string = _get_connection_string(base_env)
    
    # Create engine with connection pooling
    if base_env == 'WarehouseProd':
        # Redshift-specific pooling settings
        engine = create_engine(
            conn_string,
            poolclass=QueuePool,
            pool_size=5,           # Keep 5 persistent connections
            max_overflow=10,       # Allow up to 10 additional connections
            pool_recycle=3600,     # Recycle connections after 1 hour
            pool_pre_ping=True,    # Validate connections before use
            echo=False,
            connect_args={
                'application_name': 'kflow_etl',
                'options': '-c statement_timeout=1800000'  # 30 minute timeout
            }
        )
    else:
        # PostgreSQL pooling settings
        engine = create_engine(
            conn_string,
            poolclass=QueuePool,
            pool_size=3,
            max_overflow=5,
            pool_recycle=3600,
            pool_pre_ping=True,
            echo=False
        )
    
    # Cache the engine
    _connection_pools[base_env] = engine
    logging.info(f"Created new connection pool for {base_env}")
    
    return engine

def _get_s3_local_env(): 

    aws_key_id  =  os.environ.get('aws_key_id')
    aws_access_key  =  os.environ.get('aws_access_key')

    if aws_key_id == None or aws_access_key == None:
        try:
            from airflow.models import Variable        
            try:
                aws_key_id = Variable.get("aws_key_id")
                aws_access_key = Variable.get("aws_access_key")
                logging.info('Got AWS Airflow values')
                return [aws_key_id,aws_access_key] 
            except KeyError:
                logging.warning("Variable ENV not found, we default to local environment")
        except ModuleNotFoundError as err:
            logging.warning("Airflow not found, we default to local environment")
    else:
        logging.info('Got AWS local values')
        return [aws_key_id,aws_access_key]
    
def getHubspotClient(hubspot_env:str):
    
    import hubspot  

    api_token=get_secret(hubspot_env)
    client = hubspot.Client.create(access_token=api_token)    
    return client

def awsClient(type_auth:str='client',service:str='s3'):  
    """
    Get S3 client
    
    service:str    
        s3: to get acceses Data Lake
        sqs: to get acceses sqs service

    Return
    ----------------
    S3 client
    """
    import boto3

    aws_key = _get_s3_local_env()
    aws_access_key_id=aws_key[0]
    aws_secret_access_key=aws_key[1]

    if type_auth == 'client':

        s3_auth = boto3.client(service,
                                aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key,
                                region_name='us-east-1')
        logging.info('Return S3 credentials to "client"')

    elif type_auth == 'session':

        s3_auth = boto3.Session( aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key)
        logging.info('Return S3 credentials to "session"')

    return s3_auth

def get_secret(secret_name, region_name='us-east-1'):    
    
    from botocore.exceptions import NoCredentialsError, PartialCredentialsError    
    import json 

    # Crea un cliente para interactuar con AWS Secrets Manager
    session = awsClient(type_auth='session')    
    client = session.client(service_name='secretsmanager',region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)

    except NoCredentialsError as e:
        print(f"Error de credenciales: {e}")
        return None
    except PartialCredentialsError as e:
        print(f"Error de credenciales parciales: {e}")
        return None
    except client.exceptions.ResourceNotFoundException:
        print("El recurso no se encontró")
        return None
    except client.exceptions.InvalidRequestException as e:
        print(f"Solicitud no válida: {e}")
        return None
    except client.exceptions.InvalidParameterException as e:
        print(f"Parámetro no válido: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None
    
    # Comprueba si el secreto está en texto plano o en un JSON
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
        secret = json.loads(secret)   
        secret_value = secret    
    else:
        secret = get_secret_value_response['SecretBinary']
        secret_value = secret

    if secret_name == "api_hubspot":
        return secret_value[secret_name]
    
    elif secret_name == "data_arn_role":
        return secret_value
    
    elif secret_name in ["vekna_cluster","data_rds","secret-redshift-cluster-1","prisma_bd"]:
        return secret_value
    
    elif secret_name == "data_iam_role":
        return [secret_value['aws_access_key_id'],secret_value['aws_secret_access_key']]
    
    else:
        return secret_value[secret_name]  

def getConnectionGoogleSheet(auth:str="SERVICE"):   
    
    """
    Devuelve el servicio de Google Sheets
    
    Parameters
    ----------
    auth: str
        Indica tipo de autenticación a usar. Tipos:
        * SERVICE: Autenticación por cuenta de servicio. Esta se basa en una service
        account a la que hay que compartirle el sheet que queramos accesar.
    """
   
    from googleapiclient.discovery import build
    from google.oauth2 import service_account
    from kflow import extract

    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    if auth == "SERVICE":
        service_account_json = extract.LakeFileAsJson("auth/","data-and-bi-342313-9363b0ec39cf.json")
        credentials = service_account.Credentials.from_service_account_info(service_account_json, scopes=scopes)
        return build('sheets', 'v4', credentials=credentials)
    else:
        logging.error("Unidentified auth")
        return None
