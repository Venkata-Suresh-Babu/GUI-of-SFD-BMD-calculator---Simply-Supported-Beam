import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog, messagebox

# --- GUI Setup ---
ctk.set_appearance_mode("Dark") # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("dark-blue") # Themes: "blue" (default), "green", "dark-blue"

calc = ctk.CTk()
calc.title("SFD & BMD Calculator: Simply Supported Beam")
screen_width = calc.winfo_screenwidth()
screen_height = calc.winfo_screenheight()
calc.geometry(f"{int(screen_width * 0.6)}x{int(screen_height * 0.7)}")
calc.grid_rowconfigure(6, weight=1)
calc.grid_columnconfigure((0, 1), weight=1)

# --- Styling ---
PAD_X = 20
PAD_Y = 10
ENTRY_WIDTH = 200

font_label = ("Arial", 16, "bold")
font_entry = ("Arial", 14)
font_button = ("Arial", 16, "bold")

# --- Widgets ---

# Title Label
title_label = ctk.CTkLabel(
    calc,
    text="Simply Supported Beam SFD & BMD Calculator",
    font=("Arial", 24, "bold"),
    text_color="#228B22",
)
title_label.grid(row=0, column=0, columnspan=2, pady=20)

# Beam Length
beam_length_label = ctk.CTkLabel(calc, text="Beam Length (m):", font=font_label)
beam_length_label.grid(row=1, column=0, padx=PAD_X, pady=PAD_Y, sticky="e")
beam_length_entry = ctk.CTkEntry(calc, width=ENTRY_WIDTH, font=font_entry)
beam_length_entry.grid(row=1, column=1, padx=PAD_X, pady=PAD_Y, sticky="w")

# Load Magnitude
point_load_label = ctk.CTkLabel(calc, text="Load (N):", font=font_label)
point_load_label.grid(row=2, column=0, padx=PAD_X, pady=PAD_Y, sticky="e")
load_entry = ctk.CTkEntry(calc, width=ENTRY_WIDTH, font=font_entry)
load_entry.grid(row=2, column=1, padx=PAD_X, pady=PAD_Y, sticky="w")

# Load Distance
point_load_distance_label = ctk.CTkLabel(calc, text="Load Distance (m):", font=font_label)
point_load_distance_label.grid(row=3, column=0, padx=PAD_X, pady=PAD_Y, sticky="e")
distance_entry = ctk.CTkEntry(calc, width=ENTRY_WIDTH, font=font_entry)
distance_entry.grid(row=3, column=1, padx=PAD_X, pady=PAD_Y, sticky="w")

# Matplotlib Figure
fig = plt.Figure(figsize=(10, 6), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=calc)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)

# Variables to store inputs globally
beam_inputs = {}

# Function to Calculate and Plot SFD & BMD
def sfd_bmd():
    global beam_inputs
    try:
        L = float(beam_length_entry.get())
        P = float(load_entry.get())
        a = float(distance_entry.get())

        if not (0 <= a <= L):
            raise ValueError("Load position must be within beam length.")

        beam_inputs = {"Beam Length (m)": L, "Load (N)": P, "Load Distance (m)": a}

        RA = P * (L - a) / L
        RB = P * a / L

        x_vals = np.linspace(0, L, 500)
        SF = []
        BM = []

        for x in x_vals:
            if x < a:
                sf = RA
                bm = RA * x
            else:
                sf = RA - P
                bm = RA * x - P * (x - a)

            SF.append(sf)
            BM.append(bm)

        # Clear previous plots
        fig.clear()

        # Shear Force Diagram
        ax1 = fig.add_subplot(2, 1, 1)
        ax1.plot(x_vals, SF, color='royalblue', linewidth=2, label="Shear Force")
        ax1.fill_between(x_vals, SF, color='skyblue', alpha=0.3)
        ax1.axhline(0, color='black', linewidth=0.8)
        ax1.set_xlim(0, L)
        ax1.set_title("Shear Force Diagram (SFD)", fontsize=16, fontweight="bold")
        ax1.set_ylabel("Shear Force (N)", fontsize=12)
        ax1.grid(True)

        # Mark key points on SFD
        ax1.plot([0, a, L], [RA, RA - P, RA - P], 'o', color='darkblue')

        # Bending Moment Diagram
        ax2 = fig.add_subplot(2, 1, 2)
        ax2.plot(x_vals, BM, color='seagreen', linewidth=2, label="Bending Moment")
        ax2.fill_between(x_vals, BM, color='lightgreen', alpha=0.3)
        ax2.axhline(0, color='black', linewidth=0.8)
        ax2.set_xlim(0, L)
        ax2.set_title("Bending Moment Diagram (BMD)", fontsize=16, fontweight="bold")
        ax2.set_xlabel("Beam Length (m)", fontsize=12)
        ax2.set_ylabel("Bending Moment (Nm)", fontsize=12)
        ax2.grid(True)

        fig.tight_layout(pad=3.0)
        canvas.draw()

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

# Save Function
def save_image():
    if not beam_inputs:
        messagebox.showwarning("Warning", "Please calculate SFD & BMD first!")
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"),
                                                        ("All files", "*.*")],
                                             title="Save SFD & BMD Diagram")

    if save_path:
        # Before saving, add input text to the figure
        fig_text = (f"Inputs:\n"
                    f"Beam Length: {beam_inputs['Beam Length (m)']} m\n"
                    f"Load: {beam_inputs['Load (N)']} N\n"
                    f"Load Distance: {beam_inputs['Load Distance (m)']} m")
        fig.text(0.75, 0.02, fig_text, fontsize=10, bbox=dict(facecolor='white', alpha=0.7))

        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        messagebox.showinfo("Success", f"Diagram saved successfully at:\n{save_path}")

# Calculate Button
calc_button = ctk.CTkButton(
    calc,
    text="Calculate SFD & BMD",
    font=font_button,
    corner_radius=8,
    fg_color="#228B22",
    hover_color="#1E7B1E",
    command=sfd_bmd,
)
calc_button.grid(row=4, column=0, pady=20)

# Save Button
save_button = ctk.CTkButton(
    calc,
    text="Save Image",
    font=font_button,
    corner_radius=8,
    fg_color="#1E90FF",
    hover_color="#1C86EE",
    command=save_image,
)
save_button.grid(row=4, column=1, pady=20)

# Run App
calc.mainloop()
