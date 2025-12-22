import tkinter as tk

def main():
    """Main function to create the tkinter GUI and handle post-GUI logic."""
    # Create the tkinter window
    root = tk.Tk()
    root.title("Checkbox Example")

    # Variable to track the state of the checkbox (must be created after root)
    checkbox_var = tk.BooleanVar(value=False) # <---------väärtus

    # Add a label for instructions
    tk.Label(root, text="Check the box if you agree.").pack(pady=10)

    # Add the checkbox
    tk.Checkbutton(root, text="Yes", variable=checkbox_var).pack(pady=5)

    # Add the Close button
    tk.Button(root, text="Close", command=root.destroy).pack(pady=5)

    # Start the tkinter event loop
    root.mainloop()

    # Check the state of the checkbox and print Hello if it was checked
    if checkbox_var.get():
        print("Hello")
        
    print(checkbox_var.get()) # <--------saab .get()-iga väärtuse True/False

if __name__ == "__main__":
    main()


