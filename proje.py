import tkinter as tk
from tkinter import ttk
import requests
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FixedPointIterationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Fixed-Point Iteration Method")

        self.function_label = ttk.Label(root, text="f(x) =")
        self.function_entry = ttk.Entry(root, width=30)

        self.initial_guess_label = ttk.Label(root, text="Initial Guess:")
        self.initial_guess_entry = ttk.Entry(root)

        self.tol_label = ttk.Label(root, text="Tolerance:")
        self.tol_entry = ttk.Entry(root)

        self.max_iter_label = ttk.Label(root, text="Max Iterations:")
        self.max_iter_entry = ttk.Entry(root)

        self.calculate_button = ttk.Button(root, text="Calculate", command=self.calculate)

        # Matplotlib figürleri ve canvas oluştur
        self.fig1, self.ax1 = plt.subplots(figsize=(5, 4), tight_layout=True)
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=root)
        self.canvas1.get_tk_widget().grid(row=5, column=0, columnspan=2)

        self.fig2, self.ax2 = plt.subplots(figsize=(5, 4), tight_layout=True)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=root)
        self.canvas2.get_tk_widget().grid(row=5, column=2, columnspan=2)

        self.fig3, self.ax3 = plt.subplots(figsize=(5, 4), tight_layout=True)
        self.canvas3 = FigureCanvasTkAgg(self.fig3, master=root)
        self.canvas3.get_tk_widget().grid(row=5, column=4, columnspan=2)

        # Iterasyonları göstermek için bir Listbox ekleyin
        self.iteration_listbox = tk.Listbox(root, height=10, width=50, relief='solid')  # Relief özelliğini 'solid' olarak ayarlayın
        self.iteration_listbox.grid(row=6, column=0, columnspan=6, pady=10)

        # Layout
        self.function_label.grid(row=0, column=0, sticky="e")
        self.function_entry.grid(row=0, column=1)

        self.initial_guess_label.grid(row=1, column=0, sticky="e")
        self.initial_guess_entry.grid(row=1, column=1)

        self.tol_label.grid(row=2, column=0, sticky="e")
        self.tol_entry.grid(row=2, column=1)

        self.max_iter_label.grid(row=3, column=0, sticky="e")
        self.max_iter_entry.grid(row=3, column=1)

        self.calculate_button.grid(row=4, column=0, columnspan=6)

    def calculate(self):
        function_str = self.function_entry.get()
        initial_guess = float(self.initial_guess_entry.get())
        tol = float(self.tol_entry.get())
        max_iter = int(self.max_iter_entry.get())

        def f(x):
            return eval(function_str)

        api_url = "http://localhost:8008/fixed-point-iteration"
        payload = {
            "function": function_str,
            "initial_guess": initial_guess,
            "tolerance": tol,
            "max_iterations": max_iter
        }

        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            result = response.json()

            # Grafiği temizle
            self.ax1.clear()
            self.ax2.clear()
            self.ax3.clear()

            # Grafiği çiz
            x_values_func = np.linspace(min(result['data'], key=lambda x: x[0])[0] - 1,
                                        max(result['data'], key=lambda x: x[0])[0] + 1, 100)
            y_values_func = f(x_values_func)

            # Grafiği 1: Dönüş Değerleri Grafiği
            self.ax1.plot(range(len(result['data'])), [point[1] for point in result['data']], marker='o', linestyle='-', color='b')
            self.ax1.set_title('Dönüş Değerleri Grafiği')
            self.ax1.set_xlabel('Iterasyon Sayısı')
            self.ax1.set_ylabel('f(x_n)')

            # Grafiği 2: Hata Grafiği
            errors = [abs(point[1] - point[0]) for point in result['data']]
            self.ax2.plot(range(len(result['data'])), errors, marker='o', linestyle='-', color='r')
            self.ax2.set_title('Hata Grafiği')
            self.ax2.set_xlabel('Iterasyon Sayısı')
            self.ax2.set_ylabel('|x_{n+1} - x_n|')

            # Grafiği 3: İterasyon Noktaları Grafiği
            self.ax3.plot(x_values_func, y_values_func, label='f(x) = ' + function_str)
            self.ax3.scatter(*zip(*result['data']), color='red', label='Iterasyon Noktaları')
            self.ax3.axhline(0, color='black', linewidth=0.5, linestyle='--', label='x ekseni')
            self.ax3.axvline(result['root'], color='green', linewidth=2, linestyle='--', label='Bulunan Sabit Nokta')
            self.ax3.set_title('İterasyon Noktaları Grafiği')
            self.ax3.set_xlabel('x')
            self.ax3.set_ylabel('f(x)')
            self.ax3.legend()

            # Iterasyonları Listbox'a ekle
            self.iteration_listbox.delete(0, tk.END)
            for iteration, (x_n, f_x_n) in enumerate(result['data']):
                self.iteration_listbox.insert(tk.END, f"Iteration:{iteration}, x_n: {x_n:.5f}, f(x_n): {f_x_n:.6f}")

            # Canvas'leri güncelle
            self.canvas1.draw()
            self.canvas2.draw()
            self.canvas3.draw()

        else:
            print(f"API request failed with status code: {response.status_code}")

if __name__ == '__main__':
    root = tk.Tk()
    app = FixedPointIterationGUI(root)
    root.mainloop()
