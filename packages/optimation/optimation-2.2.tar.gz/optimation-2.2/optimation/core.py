def optimate(A, B, weight_A):
    weight_B = 100 - weight_A
    return (A * (weight_A / 100)) + (B * (weight_B / 100))
