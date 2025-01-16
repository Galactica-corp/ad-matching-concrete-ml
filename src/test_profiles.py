import numpy as np


"""
    Get a user profile vector for testing
    @param feature_count: The number of features in the user profile
    @return: A user profile vector
"""
def get_user_profile(feature_count=128):
    return np.random.randint(0, 2**8, size=(1, feature_count), dtype=np.uint64)

"""
    Get a matrix containing ad target profiles for testing
    @param feature_count: The number of features in the ad target profile
    @param ad_count: The number of ads in the ad target profile matrix
    @return: An ad target profile matrix
"""
def get_ad_target_profile_matrix(feature_count=128, ad_count=32):
    return np.random.randint(0, 2**8, size=(feature_count, ad_count), dtype=np.uint64)