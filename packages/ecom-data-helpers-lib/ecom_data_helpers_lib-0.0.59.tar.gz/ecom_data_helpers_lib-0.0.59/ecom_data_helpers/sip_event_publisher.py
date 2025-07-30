from azure.eventhub import EventHubProducerClient, EventData
import json

def validar_payload(payload):
    """
    Valida se um dicionário tem exatamente a estrutura esperada para o payload.
    
    Args:
        payload (dict): O dicionário a ser validado
        
    Returns:
        bool: True se o payload é válido, False caso contrário
        str: Mensagem de erro (vazio se válido)
    """
    # Verifica se é um dicionário
    if not isinstance(payload, dict):
        return False, "O payload deve ser um dicionário"
    
    # Define a estrutura esperada com os tipos esperados
    estrutura_esperada = {
        "nome": str,
        "nome_arquivo": str,
        "sucesso": int,
        "tipo": str,
        "mensagem": str,
        "iniciar_dispara_processo": int,
        "processo": str,
        "notificar": int
    }
    
    # Verifica se todas as chaves esperadas estão presentes
    chaves_esperadas = set(estrutura_esperada.keys())
    chaves_recebidas = set(payload.keys())
    
    # Verifica se há chaves faltando
    if chaves_esperadas - chaves_recebidas:
        chaves_faltantes = chaves_esperadas - chaves_recebidas
        return False, f"Chaves faltantes: {', '.join(chaves_faltantes)}"
    
    # Verifica se há chaves extras
    if chaves_recebidas - chaves_esperadas:
        chaves_extras = chaves_recebidas - chaves_esperadas
        return False, f"Chaves não esperadas: {', '.join(chaves_extras)}"
    
    # Verifica os tipos de cada valor
    for chave, tipo_esperado in estrutura_esperada.items():
        if not isinstance(payload[chave], tipo_esperado):
            return False, f"Valor de '{chave}' deve ser do tipo {tipo_esperado.__name__}"
    
    # # Verifica valores específicos (caso necessário)
    # if payload["tipo"] != "execucao_processo":
    #     return False, "O valor de 'tipo' deve ser 'execucao_processo'"
    
    if payload["sucesso"] not in [0, 1]:
        return False, "O valor de 'sucesso' deve ser 0 ou 1"
        
    if payload["iniciar_dispara_processo"] not in [0, 1]:
        return False, "O valor de 'iniciar_dispara_processo' deve ser 0 ou 1"
        
    if payload["notificar"] not in [0, 1]:
        return False, "O valor de 'notificar' deve ser 0 ou 1"
    
    return True, ""

def publish_to_eventhouse(payload : dict) -> None:

    # # TODO : Proteger essas chaves
    AZURE_CONNECTION_STRING : str = "Endpoint=sb://esehblut6w0z8kj9zafhqm.servicebus.windows.net/;SharedAccessKeyName=key_284df3d5-2a4b-462d-a0fc-f7bb7ad6617a;SharedAccessKey=WA/1C0aitkS0VXb/7GnIkz0AaXHYq36Lf+AEhHL0IJI=;EntityPath=es_2aae92b4-4aad-4a6f-9755-33b934000ac5"
    AZURE_EVENT_HUB_NAME : str = "es_2aae92b4-4aad-4a6f-9755-33b934000ac5"

    producer = EventHubProducerClient.from_connection_string(
        conn_str=AZURE_CONNECTION_STRING,
        eventhub_name=AZURE_EVENT_HUB_NAME
    )

    event_data_batch = producer.create_batch()

    # Validando payload
    valido, mensagem = validar_payload(payload)

    if not valido:
        raise Exception(mensagem)

    event_data_batch.add(EventData(json.dumps(payload)))

    producer.send_batch(event_data_batch)