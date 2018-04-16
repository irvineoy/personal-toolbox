import numpy as np


def de(n=4, m_size=20, f=0.5, cr=0.7, iterate_times=1000, x_l=np.array([-5, -5, -5, -5]), x_u=np.array([5, 5, 5, 5])):
    x_all = np.zeros((iterate_times, m_size, n))
    for i in range(m_size):
        x_all[0][i] = x_l + np.random.random() * (x_u - x_l)
    for g in range(iterate_times - 1):
        print('number ', g, ' generation')
        for i in range(m_size):
            x_g_without_i = np.delete(x_all[g], i, 0)
            np.random.shuffle(x_g_without_i)
            h_i = x_g_without_i[1] + f * (x_g_without_i[2] - x_g_without_i[3])
            h_i = [h_i[item] if h_i[item] < x_u[item] else x_u[item] for item in range(n)]
            h_i = [h_i[item] if h_i[item] > x_l[item] else x_l[item] for item in range(n)]
            print(h_i)
            v_i = np.array([x_all[g][i][j] if (np.random.random() > cr) else h_i[j] for j in range(n)])
            if evaluate_func(x_all[g][i] > evaluate_func(v_i)):
                x_all[g + 1][i] = v_i
            else:
                x_all[g + 1][i] = x_all[g][i]
    evaluate_result = [evaluate_func(x_all[iterate_times - 1][i]) for i in range(m_size)]
    best_x_i = x_all[iterate_times-1][np.argmin(evaluate_result)]
    print(evaluate_result)
    print(best_x_i)


def evaluate_func(x):
    a = x[0]
    b = x[1]
    c = x[2]
    d = x[3]
    return 4 * a ** 2 - 3 * b + 5 * c ** 3 - 6 * d
    return a**2 + b**2 + c**2 + d**2


if __name__ == '__main__':
    de()
