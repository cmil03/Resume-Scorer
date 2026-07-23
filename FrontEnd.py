# Simple frontend UI primarily for testing
import tkinter as tk
root = tk.Tk()
root.title("Resume Scorer")
root.geometry("660x460")
root.resizable(True, True)



form_frame = tk.Frame(root, pady=5)
form_frame.pack(fill="x", padx=20)
# JD = Job Description
label1 = tk.Label(form_frame, text="Paste Job Description:", anchor="w", width=20)
label1.grid(row=0, column=0, sticky="w", padx=(0, 8), pady=6)
jd = tk.Entry(form_frame, width=28)
jd.grid(row=0, column=1, sticky="w", pady=6)



# Enter button
button_frame = tk.Frame(root, pady=10)
button_frame.pack()


def get_data():

    job_descr = jd.get()
    print(job_descr)

enter_btn = tk.Button(button_frame, text="Enter", command=get_data, width=16)
enter_btn.grid(row=0, column=0, padx=8)


root.mainloop()