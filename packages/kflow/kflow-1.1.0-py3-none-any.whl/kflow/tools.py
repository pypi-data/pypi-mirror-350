
import logging
import pendulum
import pandas as pd
from kflow import extract,load,authn
from botocore.exceptions import ClientError

def FindDuplicateforSimilarity(df1:pd.DataFrame,df2:pd.DataFrame,df1_id:str,df1_field:str,df2_field:str,ratio:float=0.90) -> dict:

    """Find Duplicate values between two DataFrame by similarity ratio

    Parameters
    ----------
    df1:pd.DataFrame
        Origin DataFrame to compare
    df2:pd.DataFrame
        Destine DataFrame to compare      
    df1_id: str
        DataFrames' Field to identify posible duplicate row in the firts df.
    df1_field: str
        Firts DataFrames' Field thant you want compare
    df2_field:
        Second DataFrames' Field thant you want compare
    ratio:float
        Tolerance percentage for similarity
    Returns
    -------
    dict
    Keys will be {df1_id}, the firts value {df1_field} and the second field the duplicate value in {df2}.
    e.g.
    {'15489':["Motor Company S.a","Motor Company SA"]} 

    Note: If dicct it's empty so there aren't duplicate values
    """

    import re    
    import difflib

    list1 = [{row[df1_id]:row[df1_field].upper()} for index, row in df1.iterrows()]
    list2 = [row[df2_field].upper() for index, row in df2.iterrows()]

    duplicate = {}
    
    for value in list1:
        value_string = list(value.values())[0]
        match = difflib.get_close_matches(value_string,list2,cutoff=ratio)
        if len(match) > 0:      
            duplicate[list(value.keys())[0]] = [match[0],value_string]
        else:
            continue   
    
    return duplicate

def ExtractSubString(list_values:list,function:str,pattern:str=None) -> pd.DataFrame:

    """Find Duplicate values between two DataFrame by similarity ratio

    Parameters
    ----------
    list_values:list
        List of value that you want extract substring
    function:str
        You can use some default possible: 
                  "fiscal_suffix": S.A, LTDA ect
                  "web_domains": .com, .cl, .org ect
                  "suffix_domains": Fiscal Suffix or Web Domains
    pattern:str=None
        You can get substring with custom regex parttern, default is None.
    Returns
    -------
    pd.DataFrame
    DataFrame with two columns, substring finded and a example in dataset.
    """
    import re
    import pandas as pd

    if function == "fiscal_suffix":
        pattern = "(\ ?)(\.?)([LIMITADASPC]+)(\ ?)(\.?)([LIMITADASPC]?)(\.?)( ?)$"  # Fiscal Suffix (S.A, LTDA ect)
    if function == "web_domains":
        pattern = "(\.)[A-Z]{2,5}(\.[A-Z]{2,5})?"  # Web Domains (.com, .cl, .org ect)  

    if function == "suffix_domains":
        pattern = "(\ ?)(\.?)([LIMITADASPC]+)(\ ?)(\.?)([LIMITADASPC]?)(\.?)( ?)$|(\.)[A-Z]{2,5}(\.[A-Z]{2,5})?" # Fiscal Suffix or Web Domains
    else:
        pattern = pattern

    SubString = {}

    for value in list_values:
        X = re.search(pattern,value)  

        if type(X) == re.Match:        
                SubString[str(X.group())] = value
        else:   
            continue

    df = pd.DataFrame(SubString.items(), columns=['substring','example'])
    
    return df

def DeleteCompaniesHubspot(delete_companies:list,hubspot_env:str,):

    """Delete Companies on Hubspot 

    Parameters
    ----------
    delete_companies:list
        List must contain id_hubspot that companies you want delete   
    hubspot_env:str        
        HubspotProd - ambiente productivo
        HubspotTest - ambiente de pruebas
     
    """
    from kflow import authn  
    from hubspot.crm.companies import BatchInputSimplePublicObjectId, ApiException

    client = authn.getHubspotClient(hubspot_env)  
        
    delete_list = [{"id":str(x)} for x in delete_companies]        
    batch_input_simple_public_object_id = BatchInputSimplePublicObjectId(inputs=delete_list)

    try:
        api_response = client.crm.companies.batch_api.archive(batch_input_simple_public_object_id=batch_input_simple_public_object_id)                
    except ApiException:
        raise

def delete_queue_message(queue_url, receipt_handle):
    """
    Deletes the specified message from the specified queue.
    """
    sqs_client = authn.awsClient(service='sqs')

    try:
        response = sqs_client.delete_message(QueueUrl=queue_url,
                                             ReceiptHandle=receipt_handle)
    except ClientError:
        logging.exception(
            f'Could not delete the meessage from the - {queue_url}.')
        raise
    else:        
        return response

def slack_notification_fail(context):

    """
    Send messege notification to Slack group when your dag execute FAILED
    
    Nota: esta función solo recibe parametros de contexto del DAG, estudiar la posibilidad que reciba parametros personalizado como el grupo al cual
    enviar el mensaje y que tipo de mensaje enviar así contener en una sola función ambos casos (fail/success)

    """ 

    from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator

    slack_msg = """
        :red_circle: Task Failed, I'm sorry... :sweat:
        *Task*: {task}  
        *Dag*: {dag} 
        *Execution Time*: {exec_date}  
        *Log Url*: {log_url}            
        """.format(
        task=context.get('task_instance').task_id,
        dag=context.get('task_instance').dag_id,
        ti=context.get('task_instance'),
        exec_date=context.get('execution_date'),
        log_url=context.get('task_instance').log_url)

    failed_alert = SlackWebhookOperator(
        task_id="slack_notification",
        slack_webhook_conn_id ="slack_team",
        message=slack_msg
    )

    return failed_alert.execute(context=context)

def slack_notification_success(context):

    """
    Send messege notification to Slack group when your dag execute SUCCESS
    
    Nota: esta función solo recibe parametros de contexto del DAG, estudiar la posibilidad que reciba parametros personalizado como el grupo al cual
    enviar el mensaje y que tipo de mensaje enviar así contener en una sola función ambos casos (fail/success)

    """             

    from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator
        
    slack_msg = """
        :large_green_circle: Task Success, Good Job!! :muscle: 
        *Task*: {task}  
        *Dag*: {dag} 
        *Execution Time*: {exec_date}                           
        """.format(
        task=context.get('task_instance').task_id,
        dag=context.get('task_instance').dag_id,
        ti=context.get('task_instance'),
        exec_date=context.get('execution_date'))

    success_alert = SlackWebhookOperator(
        task_id="slack_notification",
        slack_webhook_conn_id ="slack_team",
        message=slack_msg
    )

    return success_alert.execute(context=context)

def read_hubspot_properties(object:str,hubspot_env:str="api_hubspot"):

    import hubspot
    from pprint import pprint
    from hubspot.crm.properties import ApiException

    client = client = authn.getHubspotClient(hubspot_env)

    try:
        api_response = client.crm.properties.core_api.get_all(object_type=object, archived=False)
        
    except ApiException as e:
        print("Exception when calling core_api->get_all: %s\n" % e)

    dict_response = api_response.to_dict()['results']
    list_properties = {property['name']:property['label'] for property in dict_response}
    
    return list_properties

def deploy_table(**context):

    from time import sleep

    warehouse_engine = authn.getConnectionDB('WarehouseProd')    
    name_tables = context["table"]

    if "source_object" in context.keys():
        source_object= context["source_object"]
    else:
        source_object = "table"
    
    if "source_shema" in context.keys():
        source_shema= context["source_shema"]
    else:
        source_shema = "staging"

    if "target_shema" in context.keys():
        target_shema = context["target_shema"]
    else:
        target_shema = "public"


    logging.info(f"source_object: {source_object} source_shema: {source_shema}")   
    
    if source_object == 'table':

        for table in  name_tables: 
            try:
                logging.info(f"Deploying {table} {source_shema} to {target_shema}")
                logging.info(f"Verifying...")                    
                warehouse_engine.execute(f"select * from {source_shema}.{table} limit 1")                
                sleep(1)
                logging.info(f"Deleting...")
                warehouse_engine.execute(f"drop table if exists {target_shema}.{table} cascade")                
                sleep(2)
                logging.info(f"Creating...")
                warehouse_engine.execute(f"create table {target_shema}.{table} (LIKE {source_shema}.{table} INCLUDING DEFAULTS)")                
                sleep(3)
                logging.info(f"Inserting...")            
                warehouse_engine.execute(f"insert into {target_shema}.{table} (select * from {source_shema}.{table})")                
                sleep(5)
                logging.info(f"Donee baby!!")                            
            except:                
                raise ValueError(f"{table} not deploy")
    
    elif source_object == 'view':

        for table in  name_tables: 

            try:
                logging.info(f"Deploying {table} {source_shema} to {target_shema}") 
                logging.info(f"Verifying...")                   
                warehouse_engine.execute(f"select * from {source_shema}.{table} limit 1")                
                sleep(1)
                logging.info(f"Dropping...")
                warehouse_engine.execute(f"drop table if exists {target_shema}.{table} cascade")                
                sleep(2)
                logging.info(f"Creating...")
                warehouse_engine.execute(f"CREATE TABLE {target_shema}.{table} as SELECT * FROM {source_shema}.{table}")
                sleep(6)
                warehouse_engine.execute(f"select * from {target_shema}.{table} limit 1")
                logging.info(f"Donee baby!!")                            
            except:                
                raise ValueError(f"{table} not deploy")                
    sleep(2)
    
def excel_to_date(excel_date):
    
    import datetime

    base_date = datetime.datetime(1900, 1, 1,0,0,0)
    date = base_date + datetime.timedelta(days=excel_date - 1)

    return date #.strftime("%d/%m/%Y %H:%M")

def date_to_excel(date):
    
    import datetime

    base_date = datetime.datetime(1900, 1, 1)
    delta = date - base_date
    excel_date = delta.days + 1

    return excel_date    
