import time
import concrete_ml_extensions as fhext
import numpy as np
import pytest
import json
from timing import Timing

from crypto_params import get_crypto_params, print_crypto_params
from test_profiles import get_user_profile, get_ad_target_profile_matrix


def main_benchmark():
    # Parameter setup
    params_dict = json.loads(fhext.default_params())
    print("Parameters:")
    for key, value in params_dict.items():
        print(f"  {key}: {value}")
    crypto_params = fhext.MatmulCryptoParameters.deserialize(json.dumps(params_dict))

    feature_count = 128
    ad_count = 32

    # FHE setup
    user_private_key, user_compression_key = fhext.create_private_key(crypto_params)
    serialized_compression_key = user_compression_key.serialize()

    # No idea what this is yet
    num_valid_glwe_values_in_last_ciphertext = ad_count % 2048

    # Get test data
    user_profile = get_user_profile(feature_count)
    ad_target_profile_matrix = get_ad_target_profile_matrix(feature_count, ad_count)

    # Encrypt user profile on user's side

    with Timing("encryption"):
        ciphertext = fhext.encrypt_matrix(user_private_key, crypto_params, user_profile)
    
    # Server side matching computation
    # Just a matrix multiplication to get all the dot products for each ad
    with Timing("matching"):
        encrypted_result = fhext.matrix_multiplication(ciphertext, ad_target_profile_matrix, user_compression_key)
    
    # Decrypt the result on the user's side
    with Timing("decryption"):
        decrypted_result = fhext.decrypt_matrix(
            encrypted_result,
            user_private_key,
            crypto_params,
            num_valid_glwe_values_in_last_ciphertext=num_valid_glwe_values_in_last_ciphertext,
        )

    print(
        f"""
        How the user profile looks like in raw form:
         {user_profile=},

         Example ad targeting profile:
         {ad_target_profile_matrix.transpose()[0]=},

         Decrypted results of all dot products, each representing the matching score for an ad:
         {decrypted_result=},

         Compared to the exact non-FHE dot product:
         {np.dot(user_profile, ad_target_profile_matrix)=},
        """
    )


if __name__ == "__main__":
    main_benchmark()