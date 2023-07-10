from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# MAIN WINDOW
root = Tk()
root.title("colorsim")
root.geometry("900x600")
root.resizable(width=False, height=False)


# FUNCTIONS
def read_data_from_file():
    try:
        with open("database.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line:
                    color, value = line.split()
                    value = float(value)
                    tree.insert("", "end", text="", values=(color, value))
    except FileNotFoundError:
        messagebox.showerror("Error", "File 'database.txt' not found.")


def save_data_to_file():
    items = tree.get_children()
    data = []
    for item in items:
        values = tree.item(item, "values")
        if values:
            color, value = values
            data.append(f"{color} {value}\n")
    try:
        with open("database.txt", "w") as file:
            file.writelines(data)
        messagebox.showinfo("Success", "Data saved to 'database.txt'.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving data:\n{str(e)}")


def closing():
    save_data_to_file()
    root.destroy()


def add_color():
    # NESTED FUNCTION
    def add_color_to_table():
        color = color_input.get()
        value = value_input.get()

        for item in tree.get_children():
            values = tree.item(item, "values")
            if color.lower() == values[0].lower():
                messagebox.showerror("Error", "Color already exists!")
                return

        tree.insert("", "end", text="", values=(color, value))
        add_window.destroy()

    # CREATE ADD WINDOW
    add_window = Toplevel()
    add_window.title("")
    add_window.geometry("400x210")
    add_window["bg"] = "white"
    add_window.resizable(width=False, height=False)

    # FRAME
    frame = Frame(add_window, bg="white")

    # INPUTS
    color_input = Entry(frame, bg="white")
    value_input = Entry(frame, bg="white")

    btn_ok = Button(
        frame,
        text="Add",
        bg="white",
        width=10,
        command=add_color_to_table,
        cursor="hand2",
    )

    # LABELS
    add_color_label = Label(frame, text="Color", bg="white")
    add_value_label = Label(frame, text="Value", bg="white")
    add_window_label = Label(frame, text="Add a new color", bg="white")
    add_window_label.grid(row=0, column=0, columnspan=2, pady=10)
    add_color_label.grid(row=1, column=0, pady=10, padx=10)
    color_input.grid(row=1, column=1, pady=10)
    add_value_label.grid(row=2, column=0, pady=10, padx=10)
    value_input.grid(row=2, column=1, pady=10)
    btn_ok.grid(row=3, column=0, columnspan=2, pady=10)
    frame.pack()


def search():
    query = search_enter.get().lower()
    for item in tree.get_children():
        values = tree.item(item, "values")
        if query in values:
            tree.selection_set(item)
            tree.focus(item)
            tree.see(item)


def edit_color():
    selected_item = tree.focus()
    if selected_item:
        values = tree.item(selected_item, "values")
        if values:
            color = values[0]
            value = float(values[1])

            # NESTED FUNCTION
            def update_color():
                input_value = value_input.get()
                try:
                    number = float(input_value)
                except ValueError:
                    messagebox.showerror("Error", "Invalid number!")
                    return

                new_value = value + number

                tree.set(selected_item, column="Total", value=new_value)
                edit_window.destroy()

            # CREATE EDIT WINDOW
            edit_window = Toplevel()
            edit_window.title("")
            edit_window.geometry("300x200")
            edit_window["bg"] = "white"
            edit_window.resizable(width=False, height=False)

            frame = Frame(edit_window, bg="white")
            # INPUTS
            value_input = Entry(frame, bg="white")

            button_update = Button(
                frame,
                text="Update",
                bg="white",
                width=10,
                command=update_color,
                cursor="hand2",
            )

            # LABELS
            edit_color_label = Label(frame, text="Color: " + color, bg="white")
            edit_value_label = Label(
                frame, text="Current Total: " + str(value), bg="white"
            )
            edit_color_label.grid(row=0, column=0, pady=10, padx=10)
            edit_value_label.grid(row=1, column=0, pady=10)
            value_input.grid(row=2, column=0, pady=10)
            button_update.grid(row=3, column=0, columnspan=2, pady=10)
            frame.pack()

            edit_window.lift(root)
        else:
            messagebox.showerror("Error", "Please select a valid item.")
    else:
        messagebox.showerror("Error", "Please select an item.")


def remove_color():
    selected_item = tree.focus()
    if selected_item:
        confirmed = messagebox.askyesno(
            "Confirmation", "Are you sure you want to remove this color?"
        )
        if confirmed:
            tree.delete(selected_item)
    else:
        messagebox.showerror("Error", "Please select an item.")


# FRAMES
left_frame = Frame(root)
left_frame.place(relx=-0.001, rely=0.05, relwidth=0.63, relheight=0.7)
right_frame = Frame(root)
right_frame.place(relx=0.67, rely=0.09, relwidth=0.3, relheight=0.6)


# TABLE
tree = ttk.Treeview(left_frame, columns=("Color", "Total"), show="headings")

tree.heading("Color", text="Color")
tree.heading("Total", text="Total")
tree.pack()
tree.place(x=150, y=0)
yscrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=tree.yview)
yscrollbar.pack(side=RIGHT, fill="y")
tree.configure(height=20, yscrollcommand=yscrollbar.set)

# BUTTONS
button_add = Button(
    right_frame, text="Add", bg="white", width=10, command=add_color, cursor="hand2"
)
button_edit = Button(
    right_frame, text="Edit", bg="white", width=10, command=edit_color, cursor="hand2"
)
button_remove = Button(
    right_frame,
    text="Remove",
    bg="white",
    width=10,
    command=remove_color,
    cursor="hand2",
)


# SEARCH SECTION
search_label = Label(right_frame, text="Search")
search_enter = Entry(right_frame)
search_button = Button(
    right_frame, text="Search", command=search, bg="white", width=10, cursor="hand2"
)

button_add.grid(row=0, column=0, columnspan=2, pady=7)
button_edit.grid(row=1, column=0, columnspan=2, pady=7)
button_remove.grid(row=2, column=0, columnspan=2, pady=7)
search_label.grid(row=3, column=0, pady=(100, 0))
search_enter.grid(row=3, column=1, pady=(100, 0), padx=10)
search_button.grid(row=4, column=0, columnspan=2, pady=(15, 0))

read_data_from_file()

#############################
root.protocol("WM_DELETE_WINDOW", closing)
root.mainloop()
