def fixed_point_iteration(g, x_0, tol, max_iter):
    x_n = x_0
    iterations = 0
    data = []

    while iterations < max_iter:
        x_next = g(x_n)
        data.append((x_n, g(x_n)))

        if abs(x_next - x_n) < tol:
            break

        x_n = x_next
        iterations += 1

    return {
        "root": x_n,
        "iterations": iterations,
        "data": data
    }