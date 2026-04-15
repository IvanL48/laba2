import matplotlib.pyplot as plt
import numpy as np


def results_from_py():
    with open('data_antenna.txt', 'r', encoding='utf-8') as file:
        file.readline()
        file.readline()

        axis = [[], [], []]

        for line in file:
            theta_rad, theta_deg, f_val, d_times, d_db = map(float, line.split())
            axis[0].append(theta_rad)
            axis[1].append(d_db)
            axis[2].append(d_times)

        return axis


def results_from_CST(file_name):
    axis = [[], [], []]

    with open(file_name, 'r', encoding='utf-8') as file:
        file.readline()
        file.readline()

        for line in file:
            parts = line.split()
            if len(parts) >= 8:
                try:
                    theta_deg = float(parts[0])
                    phi = float(parts[1])

                    if phi == 90.0 or theta_deg > 180:
                        continue

                    if 'dB' in file_name or 'db' in file_name:
                        d_db = float(parts[3])
                        d_lin = 10 ** (d_db / 10) if d_db > -100 else 0
                    else:
                        d_lin = float(parts[3])
                        d_db = 10 * np.log10(d_lin) if d_lin > 0 else -100

                    axis[0].append(np.deg2rad(theta_deg))
                    axis[1].append(d_db)
                    axis[2].append(d_lin)
                except:
                    continue

    return axis


def creating_plot(cst_pol_db, cst_pol_lin, cst_dec_db, cst_dec_lin, python):
    fig = plt.figure(figsize=(14, 12))

    ax1 = fig.add_subplot(2, 2, 1)
    ax1.plot(cst_dec_db[0], cst_dec_db[1], 'b-', label='CST', linewidth=2)
    ax1.plot(python[0], python[1], 'r--', label='Python', linewidth=2)
    ax1.set_title('ДН (декартова, дБ)')
    ax1.set_xlabel('θ (рад)')
    ax1.set_ylabel('D(θ), дБ')
    ax1.grid(True)
    ax1.legend()

    ax2 = fig.add_subplot(2, 2, 2)
    ax2.plot(cst_dec_lin[0], cst_dec_lin[2], 'b-', label='CST', linewidth=2)
    ax2.plot(python[0], python[2], 'r--', label='Python', linewidth=2)
    ax2.set_title('ДН (декартова, разы)')
    ax2.set_xlabel('θ (рад)')
    ax2.set_ylabel('D(θ)')
    ax2.grid(True)
    ax2.legend()

    ax3 = fig.add_subplot(2, 2, 3, polar=True)
    ax3.plot(cst_pol_db[0], cst_pol_db[1], 'b-', label='CST', linewidth=2)
    ax3.plot(python[0], python[1], 'r--', label='Python', linewidth=2)
    ax3.set_title('ДН (полярная, дБ)')
    ax3.legend()
    ax3.grid(True)

    ax4 = fig.add_subplot(2, 2, 4, polar=True)
    ax4.plot(cst_pol_lin[0], cst_pol_lin[2], 'b-', label='CST', linewidth=2)
    ax4.plot(python[0], python[2], 'r--', label='Python', linewidth=2)
    ax4.set_title('ДН (полярная, разы)')
    ax4.legend()
    ax4.grid(True)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('comparison_plot.png')
    plt.show()


def main():
    python_data = results_from_py()
    cst_pol_db = results_from_CST('Pol_db.txt')
    cst_pol_lin = results_from_CST('Pol_lin.txt')
    cst_dec_db = results_from_CST('Dec_db.txt')
    cst_dec_lin = results_from_CST('Dec_lin.txt')

    creating_plot(cst_pol_db, cst_pol_lin, cst_dec_db, cst_dec_lin, python_data)


if __name__ == '__main__':
    main()
