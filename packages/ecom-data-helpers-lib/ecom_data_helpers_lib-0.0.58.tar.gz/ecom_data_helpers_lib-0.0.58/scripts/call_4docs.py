from ecom_data_helpers.energy_account_extraction import auth_4docs, enrich_energy_account_with_4docs, format_response

if __name__ == "__main__":
    
    s3_path : str = "staging/ba493e0a-dbce-4177-832e-9d3e4d259dae-teste-novo-postman.pdf"
    bucket_name : str = "ecom-energy-account-data-extraction"

    result : dict = enrich_energy_account_with_4docs(bucket_name, s3_path)

    print(result)
