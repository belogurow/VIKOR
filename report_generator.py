import os


def generate_report(result, criteria_matrix, weights, compromise_weight, filename="vikor_report.md"):
    """
    Генерация отчета в формате Markdown.

    :param result: Результаты метода VIKOR.
    :param criteria_matrix: Матрица альтернатив с оценками.
    :param weights: Веса критериев.
    :param compromise_weight: Вес компромисса.
    :param filename: Имя файла для сохранения отчета.
    """
    transposed_matrix = list(zip(*criteria_matrix))

    with open(filename, "w", encoding="utf-8") as file:
        file.write("# VIKOR\n\n")
        generate_description(file)

        file.write("## Входные данные\n\n")
        generate_criteria_table(file, criteria_matrix)
        generate_weights(file, weights)

        file.write("\n## Вычисление\n\n")
        max_f, min_f = generate_ideal_and_antiideal_solutions(file, transposed_matrix)
        generate_s_and_r(file, result, criteria_matrix, weights, max_f, min_f)
        max_s, min_s, max_r, min_r = generate_max_min_s_r(file, result)
        generate_q(file, criteria_matrix, result, max_s, min_s, max_r, min_r, compromise_weight)

        file.write("\n## Результаты расчетов\n\n")
        generate_results(file, result)

    print(f"Отчет сохранен в файл: {os.path.abspath(filename)}")


def generate_description(file):
    file.write(
        "Метод VIKOR (VIsekriterijumska Optimizacija i Kompromisno Resenje) – это метод многокритериального анализа "
        "принятия решений (MCDA). Он предназначен для нахождения компромиссного решения в задачах, "
        "где нужно учитывать несколько критериев, которые могут быть как конфликтующими, так и несравнимыми.\n")

    file.write("## Основные особенности: \n")
    file.write(
        "1. **Компромиссное решение**: Метод использует концепцию компромисса, что подразумевает выбор решения, которое максимально близко к идеальному по всем критериям, но с учетом допустимых отклонений.\n")
    file.write("\n")

    file.write("2. **Идеальное и анти-идеальное решения**:\n")
    file.write(
        "    - Идеальное решение $f^*$— это гипотетическое решение, которое максимально удовлетворяет всем критериям.\n")
    file.write("    - Анти-идеальное решение $f^-$ — противоположность идеального.\n")
    file.write("\n")

    file.write("3. **Расчет индексов**:\n")
    file.write(
        "   - Вычисляются два индекса:  $S$ (мера соответствия идеальному решению) и $R$ (мера согласованности с наиболее критическим критерием).\n")
    file.write("    - Индекс $Q$ (мера компромисса) вычисляется как взвешенная сумма индексов $S$ и $R$.\n")
    file.write("\n")

    file.write("4. **Ранжирование альтернатив**:\n")
    file.write(
        "    - Альтернативы ранжируются по значению индекса $Q$. Наименьшее значение $Q$ соответствует наилучшему компромиссному решению\n")
    file.write("\n")

    file.write("5. **Гибкость**:\n")
    file.write("   - Метод позволяет учитывать вес критериев, что делает его адаптивным для различных задач.\n")
    file.write("\n")


def generate_criteria_table(file, table):
    file.write("### Матрица критериев\n")
    file.write("- $i$ - альтернатива\n")
    file.write("- $j$ - критерий\n\n")

    file.write("$$\n")
    file.write("f_{ij} = ")
    file.write(f"\\begin{{array}}  {{|r|r|}}\n")

    # Заголовок таблицы
    file.write(" ")
    for i, _ in enumerate(table, start=1):
        file.write(f"& Альтернатива_{i}")
    file.write("\\\\ \n")

    # Значения таблицы
    transposed_table = list(zip(*table))
    for i in range(len(transposed_table)):
        file.write(f"Критерий_{i} ")
        for criteria in transposed_table[i]:
            file.write(f"& {criteria:.2f} ")
        file.write("\\\\ \n")

    file.write("\end{array}\n")
    file.write("$$\n")


def generate_weights(file, weights):
    file.write("\n### Веса критериев\n")
    file.write(f"$$ w_j = {weights} $$\n\n")


def generate_ideal_and_antiideal_solutions(file, transposed_matrix):
    # Найти идеальное (f*) и анти-идеальное (f-) решения
    max_f = [max(criteria) for criteria in transposed_matrix]
    min_f = [min(criteria) for criteria in transposed_matrix]

    file.write("\n### Идеальное и анти-идеальное решения\n")
    file.write(f"- Максимальное значение критериев: $f^* = {max_f}$\n")
    file.write(f"- Минимальное значение критериев: $f^- = {min_f}$\n")

    return max_f, min_f


def generate_s_and_r(file, result, criteria_matrix, weights, max_f, min_f):
    file.write("### Вычисление S и R\n")
    file.write("Формула для $S_i$:\n\n")
    file.write("$$ S_i = \sum_{j=1}^m w_j \cdot \\frac{f_j^* - f_{ij}}{f_j^* - f^-_j} $$\n\n")

    # Вычисление S
    for i, alternative in enumerate(criteria_matrix, start=1):
        file.write(f"* $S_{i} = ")
        elements = []
        for j, criteria in enumerate(alternative, start=0):
            elements.append(
                f"{weights[j]:.2f} \cdot \\frac{{ {max_f[j]} - {criteria} }}{{ {max_f[j]} - {min_f[j]} }}")
        file.write(" + ".join(elements))

        file.write(f" = ")
        elements.clear()
        for j, criteria in enumerate(alternative, start=0):
            elements.append(f"{weights[j] * (max_f[j] - criteria) / (max_f[j] - min_f[j]):.4f}")
        file.write(" + ".join(elements))

        file.write(f" = {result['s_values'][i - 1]:.4f}")
        file.write("$\n")
    file.write("\n")

    # Вычисление R
    file.write("Формула для $R_i$:\n\n$$ R_i = \max_j \left(w_j \cdot \\frac{f_j^* - f_{ij}}{f_j^* - f^-_j}\\right) $$\n\n")
    for i, alternative in enumerate(criteria_matrix, start=1):
        file.write(f"* $R_{i} = \max(")
        elements = []
        for j, criteria in enumerate(alternative, start=0):
            elements.append(
                f"{weights[j]:.2f} \cdot \\frac{{ {max_f[j]} - {criteria} }}{{ {max_f[j]} - {min_f[j]} }}")
        file.write(", ".join(elements))
        file.write(")")

        file.write(" = \max(")
        elements.clear()
        for j, criteria in enumerate(alternative, start=0):
            elements.append(f"{weights[j] * (max_f[j] - criteria) / (max_f[j] - min_f[j]):.4f}")
        file.write(", ".join(elements))
        file.write(")")

        file.write(f" = {result['r_values'][i - 1]:.4f}")
        file.write("$\n")
    file.write("\n")


def generate_max_min_s_r(file, result):
    # Найти минимальные и максимальные значения S и R
    max_s = max(result['s_values'])
    min_s = min(result['s_values'])
    max_r = max(result['r_values'])
    min_r = min(result['r_values'])

    file.write("### Максимальное и минимальное значения S и R\n")
    file.write(f"- Максимальное значение S: $S^- = {max_s}$\n")
    file.write(f"- Минимальное значение S: $S^* = {min_s}$\n")
    file.write(f"- Максимальное значение R: $R^- = {max_r}$\n")
    file.write(f"- Минимальное значение R: $R^* = {min_r}$\n")

    return max_s, min_s, max_r, min_r


def generate_q(file, criteria_matrix, result, max_s, min_s, max_r, min_r, compromise_weight):
    file.write("\n### Вычисление Q\n")
    file.write(
        "Формула для $Q_i$:\n\n$$ Q_i = v \cdot \\frac{S_i - S^*}{S^- - S^*} + (1-v) \cdot \\frac{R_i - R^*}{R^- - R^*} $$\n\n")
    file.write(f"Вес компромисса: $v = {compromise_weight}$\n")

    for i, alternative in enumerate(criteria_matrix, start=1):
        file.write(f"* $Q_{i} = ")

        file.write(
            f"{compromise_weight} \cdot \\frac {{ {result['s_values'][i - 1]} - {min_s} }} {{ {max_s} - {min_s} }}")
        file.write(" + ")
        file.write(
            f"(1-{compromise_weight}) \cdot \\frac {{ {result['r_values'][i - 1]} - {min_r} }} {{ {max_r} - {min_r} }}")

        file.write(f"= {result['q_values'][i - 1]:.4f}")
        file.write("$\n")


def generate_results(file, result):
    file.write(
        "Упорядочьте альтернативы по возрастанию значений $Q_i$. "
        "Наименьшее значение $Q$ соответствует наилучшему компромиссному решению\n")

    file.write("### Ранжирование альтернатив\n")
    for rank, (alt, q) in enumerate(result["ranked_alternatives"], start=1):
        file.write(f"- {rank}-е место: Альтернатива {alt} ($Q_{alt} = {q:.4f}$)")
        file.write("\n")
