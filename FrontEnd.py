# Simple frontend UI primarily for testing
import tkinter as tk
from tkinter import filedialog, scrolledtext
# from Resume import extract__text
import Resume

root = tk.Tk()
root.title("Resume Scorer")
root.geometry("660x620")
root.resizable(True, True)

form_frame = tk.Frame(root, pady=5)
form_frame.pack(fill="x", padx=20)

# JD = Job Description
label1 = tk.Label(form_frame, text="Paste Job Description:", anchor="w", width=20)
label1.grid(row=0, column=0, sticky="w", padx=(0, 8), pady=6)
jd = tk.Entry(form_frame, width=38)
jd.grid(row=0, column=1, sticky="w", pady=6)

# Resume PDF input
label2 = tk.Label(form_frame, text="Select Resume PDF:", anchor="w", width=20)
label2.grid(row=1, column=0, sticky="w", padx=(0, 8), pady=6)
resume_path = tk.Entry(form_frame, width=38)
resume_path.grid(row=1, column=1, sticky="w", pady=6)

browse_btn = tk.Button(form_frame, text="Browse", command=lambda: browse_pdf(), width=10)
browse_btn.grid(row=1, column=2, sticky="w", padx=(8, 0), pady=6)

# Enter button
button_frame = tk.Frame(root, pady=10)
button_frame.pack()


# Text Preview Frame
output_frame = tk.Frame(root, pady=5)
output_frame.pack(fill="both", expand=True, padx=20)
output_label = tk.Label(output_frame, text="Resume Text Preview:", anchor="w")
output_label.pack(anchor="w")
output_text = scrolledtext.ScrolledText(output_frame, height=5, wrap="word")
output_text.pack(fill="both", expand=False)

# Score Frame
score_frame = tk.Frame(root, pady = 5)
score_frame.pack(fill="both", expand=True, padx=20)
score_text = scrolledtext.ScrolledText(score_frame, height = 10, wrap = "word")
score_text.pack(fill = "both", expand=False)


# Select PDF
def browse_pdf():
    file_path = filedialog.askopenfilename(
        title="Choose a PDF resume",
        filetypes=[("PDF Files", "*.pdf")],
    )

    if file_path:
        resume_path.delete(0, tk.END) #Clears text previously in the entry box
        resume_path.insert(0, file_path) #Adds new file to entry box


def get_data():
    job_descr = jd.get().strip()
    pdf_file = resume_path.get().strip()
    output_text.delete(1.0, tk.END)

    if not pdf_file:
        output_text.insert(tk.END, "Please select a PDF resume file first.\n")
        return

    try:
        resume_text = Resume.extract__text(pdf_file)
        output_text.insert(tk.END, f"Selected PDF: {pdf_file}\n\n")
        output_text.insert(tk.END, resume_text or "(No text extracted from PDF.)")
        score_text.insert(tk.END,
        f"Here are the required skills:\n {Resume.parse_job_description(job_descr)[0]}\n")
    except Exception as error:
        output_text.insert(tk.END, f"Error reading PDF: {error}")

    # Is it necessary to paste the job description preview as well?
    if job_descr:
        output_text.insert(tk.END, f"\n\nJob Description:\n{job_descr}")


enter_btn = tk.Button(button_frame, text="Enter", command=get_data, width=16)
enter_btn.grid(row=0, column=0, padx=8)

root.mainloop()