from matplotlib import pyplot as plt


def build_graphics():
    m = 1000  # масса ракеты вначале
    dt = 0.0001  # малый интервал времени
    dM = 500  # масса топлива
    g = 9.81
    u = 3000
    w = 5  # скорость изменения массы ракеты
    h = 0
    v = 0
    M = m  # масса ракеты
    t = 0

    a_a = []
    v_a = []
    h_a = []
    t_a = []

    while m - M <= dM:
        mi = w * dt
        a = (u * w - M * g) / M
        M -= mi
        v += a * dt
        h += v * dt + a * dt * dt / 2
        t += dt
        t_a.append(t)
        h_a.append(h)
        v_a.append(v)
        a_a.append(a)

    plt.subplot(1, 3, 1)
    plt.plot(t_a, a_a)
    plt.title('Ускорение ракеты')
    plt.xlabel('Время (с)')
    plt.ylabel('Ускорение (м/с²)')
    plt.grid()

    plt.subplot(1, 3, 2)
    plt.plot(t_a, v_a)
    plt.title('Скорость ракеты')
    plt.xlabel('Время (с)')
    plt.ylabel('Скорость (м/с)')
    plt.grid()

    plt.subplot(1, 3, 3)
    plt.plot(t_a, h_a)
    plt.title('Высота ракеты на Землёй')
    plt.xlabel('Время (с)')
    plt.ylabel('Высота (м)')
    plt.grid()

    plt.show()

    print(f"3) v = {v_a[-1]:.2f} м / c \n4) {'Да, сможет' if v_a[-1] >= 3070 else 'Нет, не сможет'}")