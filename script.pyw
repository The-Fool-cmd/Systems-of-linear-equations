import tkinter as tk
from tkinter import ttk
import random
import numpy as np # required for matrix determinant

def matrix_generate(num_vars, allow_negative, coef_range, sol_range):
    while True:
        solutions = [random.randint(-sol_range, sol_range) if allow_negative else random.randint(0, sol_range) for _ in range(num_vars)]
        if solutions.count(0) > 1:
            continue  # At most one zero solution
        matrix = []
        total_coefficients = []
        for _ in range(num_vars):
            coefficients = [random.randint(-coef_range, coef_range) if allow_negative else random.randint(0, coef_range) for _ in range(num_vars)]
            total_coefficients.extend(coefficients)
            result = sum(coef * sol for coef, sol in zip(coefficients, solutions))
            matrix.append((coefficients, result))
        if total_coefficients.count(0) > 1:
            continue  # At most one zero coefficient
        coefficients_matrix = np.array([coefficients for coefficients, _ in matrix])
        if np.linalg.det(coefficients_matrix) != 0:
            break
    return matrix, solutions

def toggle_visibility():
    if solutions_text.winfo_viewable():
        solutions_text.grid_remove()
        toggle_button.config(text="Show Solutions")
    else:
        solutions_text.grid()
        toggle_button.config(text="Hide Solutions")

def submit():
    num_vars = int(num_vars_entry.get())
    allow_negative = allow_negative_var.get()
    coef_range = int(coef_range_entry.get())
    sol_range = int(sol_range_entry.get())
    equations_text.delete(1.0, tk.END)  # Clear previous equations
    solutions_text.delete(1.0, tk.END)  # Clear previous solutions
    matrix, solutions = matrix_generate(num_vars, allow_negative, coef_range, sol_range)
    for i in range(num_vars): # Display the equations
        coefficients, result = matrix[i] # Unpack the coefficients and result
        equation_str = " + ".join([f"{coefficients[j]}*x{j+1}" for j in range(num_vars)]) # Construct the equation string
        equation_str += f" = {result}" # Append the result to the equation string
        equations_text.insert(tk.END, equation_str + "\n") # Insert the equation string into the text widget
    for i, solution in enumerate(solutions): # Display the solutions
        solutions_text.insert(tk.END, f"x{i+1} = {solution}\n") 
    solutions_text.grid_remove()  # Hide the solutions text widget
    toggle_button.config(text="Show Solutions")

# Main Window
root = tk.Tk()
root.title("System of Linear Equations")

# Number of variables entry
num_vars_label = ttk.Label(root, text="Number of variables:")
num_vars_label.grid(column=0, row=0, padx=10, pady=10)
num_vars_entry = ttk.Entry(root)
num_vars_entry.grid(column=1, row=0, padx=10, pady=10)

# Allow negative solutions check
allow_negative_var = tk.BooleanVar()
allow_negative_check = ttk.Checkbutton(root, text="Allow negative solutions", variable=allow_negative_var)
allow_negative_check.grid(column=0, row=1, columnspan=2, padx=10, pady=10)

# Coefficient range entry
coef_range_label = ttk.Label(root, text="Coefficient range:")
coef_range_label.grid(column=0, row=2, padx=10, pady=10)
coef_range_entry = ttk.Entry(root)
coef_range_entry.grid(column=1, row=2, padx=10, pady=10)

# Solution range entry
sol_range_label = ttk.Label(root, text="Solution range:")
sol_range_label.grid(column=0, row=3, padx=10, pady=10)
sol_range_entry = ttk.Entry(root)
sol_range_entry.grid(column=1, row=3, padx=10, pady=10)

# Submit button
submit_button = ttk.Button(root, text="Submit", command=submit)
submit_button.grid(column=0, row=4, columnspan=2, padx=10, pady=10)

# Text widget to display equations
equations_text = tk.Text(root, height=10, width=50, wrap=tk.WORD)
equations_text.grid(column=0, row=5, columnspan=2, padx=10, pady=10)

# Text widget to display solutions
solutions_text = tk.Text(root, height=10, width=50, wrap=tk.WORD)
solutions_text.grid(column=0, row=6, columnspan=2, padx=10, pady=10)

# Toggle button to show/hide solutions
toggle_button = ttk.Button(root, text="Hide Solutions", command=toggle_visibility)
toggle_button.grid(column=0, row=7, columnspan=2, padx=10, pady=10)

# Run the application
root.mainloop()
