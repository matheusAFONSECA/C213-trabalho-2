def calcular_d(F_A, Posicao, U_max, P1, P2):
    # Simplificando a fórmula para evitar crescimento descontrolado
    d_t =   (F_A * Posicao * 1.01398 + 0.5 * (U_max * P1 + U_max*P2))
    return d_t