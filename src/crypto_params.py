import json
import concrete_ml_extensions as fhext


def get_crypto_params():
    params_dict = json.loads(fhext.default_params())
    return fhext.MatmulCryptoParameters.deserialize(json.dumps(params_dict))

def print_crypto_params(crypto_params):
    params_dict = json.loads(crypto_params.serialize())
    print("Parameters:")
    for key, value in params_dict.items():
        print(f"  {key}: {value}")