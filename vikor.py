from report_generator import generate_report


def vikor_method(criteria_matrix, weights, v=0.5):
    """
    Метод VIKOR для анализа многокритериального принятия решений.

    :param criteria_matrix: Матрица альтернатив с оценками (список списков).
    :param weights: Веса критериев (список).
    :param v: Вес компромисса (по умолчанию 0.5).
    :return: Лучшая альтернатива и подробные результаты.
    """
    # Найти идеальное (f*) и анти-идеальное (f-) решения
    f_star = [max(criteria) for criteria in zip(*criteria_matrix)]
    f_minus = [min(criteria) for criteria in zip(*criteria_matrix)]

    # Рассчитать S_i и R_i для каждой альтернативы
    s_values = []
    r_values = []
    for alternative in criteria_matrix:
        s_i = 0
        r_i = 0
        for j in range(len(alternative)):
            normalized_diff = (f_star[j] - alternative[j]) / (f_star[j] - f_minus[j])
            weighted_diff = weights[j] * normalized_diff
            s_i += weighted_diff
            r_i = max(r_i, weighted_diff)
        s_values.append(s_i)
        r_values.append(r_i)

    # Найти минимальные и максимальные значения S и R
    s_star = min(s_values)
    s_minus = max(s_values)
    r_star = min(r_values)
    r_minus = max(r_values)

    # Рассчитать Q_i для каждой альтернативы
    q_values = [
        v * (s_i - s_star) / (s_minus - s_star) + (1 - v) * (r_i - r_star) / (r_minus - r_star)
        for s_i, r_i in zip(s_values, r_values)
    ]

    # Найти лучшую альтернативу
    best_alternative_index = q_values.index(min(q_values))

    # Возвратить результаты
    return {
        "best_alternative": best_alternative_index + 1,
        "s_values": s_values,
        "r_values": r_values,
        "q_values": q_values,
        "ranked_alternatives": sorted(
            enumerate(q_values, start=1), key=lambda x: x[1]
        )
    }

# Пример использования
if __name__ == "__main__":
    # Ввод данных
    criteria_matrix = [
        [0.8, 0.7, 0.6, 0.9, 0.85],  # Альтернатива 1
        [0.9, 0.6, 0.8, 0.7, 0.9],  # Альтернатива 2
        [0.7, 0.8, 0.7, 0.8, 0.75]   # Альтернатива 3
    ]
    weights = [0.25, 0.20, 0.20, 0.20, 0.15]  # Веса критериев
    compromise_weight = 0.5  # Вес компромисса

    # Расчет
    result = vikor_method(criteria_matrix, weights, compromise_weight)

    # Генерация отчета
    generate_report(result, criteria_matrix, weights, compromise_weight)

    # Печать результатов
    print("Лучшая альтернатива:", result["best_alternative"])
    print("Значения S:", result["s_values"])
    print("Значения R:", result["r_values"])
    print("Значения Q:", result["q_values"])
    print("Ранжирование альтернатив:", result["ranked_alternatives"])
