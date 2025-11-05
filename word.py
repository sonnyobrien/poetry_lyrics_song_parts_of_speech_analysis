import nltk
import csv
import subprocess
import tkinter as tk
from tkinter import messagebox
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# Download required NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Function to extract POS tags and write to CSV
def extract_pos_to_csv(text, output_file='pos_tags.csv'):
    # Tokenize the text into words
    tokens = word_tokenize(text)
    
    # Perform POS tagging
    tagged_tokens = pos_tag(tokens)
    
    # Prepare lists for nouns, verbs, and determiners
    nouns = []
    verbs = []
    determiners = []
    
    # Loop through the tagged tokens and classify them into Nouns, Verbs, and Determiners
    for word, tag in tagged_tokens:
        if tag.startswith('NN'):  # Nouns (singular/plural)
            nouns.append(word)
        elif tag.startswith('VB'):  # Verbs (base, past, present, etc.)
            verbs.append(word)
        elif tag == 'DT':  # Determiners
            determiners.append(word)

    # Write the results to a CSV file
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Nouns', 'Verbs', 'Determiners'])  # Column headers
        
        # Find the max length of lists to ensure equal number of rows
        max_length = max(len(nouns), len(verbs), len(determiners))
        
        # Pad shorter lists with empty strings
        nouns += [''] * (max_length - len(nouns))
        verbs += [''] * (max_length - len(verbs))
        determiners += [''] * (max_length - len(determiners))

        # Write data row by row
        for i in range(max_length):
            writer.writerow([nouns[i], verbs[i], determiners[i]])

    print(f"POS tags have been written to '{output_file}'.")

    # Open the CSV file in LibreOffice Calc
    subprocess.run(['libreoffice', '--calc', output_file])

    # Show a success message
    messagebox.showinfo("Success", f"POS tags have been successfully written to {output_file} and opened in LibreOffice Calc!")

# GUI Function
def on_button_click():
    # Get the text from the text box
    input_text = text_box.get("1.0", "end-1c")
    
    if input_text.strip() == "":
        messagebox.showerror("Error", "Please enter some text to analyze.")
    else:
        # Call the function to analyze the text and open LibreOffice Calc
        extract_pos_to_csv(input_text)

# Create the main window for the GUI
root = tk.Tk()
root.title("POS Tagging and Analysis")

# Create and pack the widgets
label = tk.Label(root, text="Enter Text for POS Analysis (Poem/Song Lyrics):")
label.pack(padx=10, pady=5)

text_box = tk.Text(root, height=10, width=50)
text_box.pack(padx=10, pady=5)

button = tk.Button(root, text="Analyze and Open in LibreOffice Calc", command=on_button_click)
button.pack(padx=10, pady=10)

# Run the GUI loop
root.mainloop()
