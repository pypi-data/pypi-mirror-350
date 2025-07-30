from ecom_data_helpers.sip_event_publisher import publish_to_eventhouse

if __name__ == "__main__":
    payload : dict = {
        "nome": "teste",
        "nome_arquivo": "teste.zip",
        "sucesso": 1,
        "tipo": "teste",
        "mensagem": "teste",
        "iniciar_dispara_processo": 0,
        "processo": "teste",
        "notificar": 0
    }
    publish_to_eventhouse(payload)