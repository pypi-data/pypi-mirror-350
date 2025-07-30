def balance_variables(A, B, weight_A):
    weight_B = 100 - weight_A
    return (A * weight_A + B * weight_B) / 100

def exponential_weighting(A, B, weight_A):
    weight_B = 100 - weight_A
    return (A ** (weight_A / 100)) + (B ** (weight_B / 100))
