def calcular_d(F_A, Posicao, U_max, P1, P2):
    """
    Calculate the value of d_t based on the given parameters.

    Args:
        F_A (float): The force applied.
        Posicao (float): The position value.
        U_max (float): The maximum velocity.
        P1 (float): The first parameter.
        P2 (float): The second parameter.

    Returns:
        float: The calculated value of d_t.
    """
    # Simplificando a fórmula para evitar crescimento descontrolado
    d_t = F_A * Posicao * 1.01398 + 0.5 * (U_max * P1 + U_max * P2)
    return d_t
