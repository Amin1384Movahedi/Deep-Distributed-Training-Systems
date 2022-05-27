# This module will normalize the data in 3 different ways
#   Simple Feature Scaling: The simple feature scaling will normalize a value between -1 and 1 by dividing by 
#                           the max value in the dataset.

#   Min-Max: The min-max method will scale the feature to a fixed range between 0 and 1.
#   
#   Z_score: The Z-Score is the measure of standard deviations between the actual value and a predicted value. 
#            In order to calculate this value, 
#            we must first know the mean value and the standard deviation. 

def Simple_feature_scaling(Input):
    return Input / Input.max()

def Min_Max(Input):
    return (Input - Input.min()) / (Input.max() - Input.min())

def Z_Score(Input):
    return (Input - Input.mean()) / (Input.std())