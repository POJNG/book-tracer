import tkinter as tk
from tkinter import messagebox, font
import json

# Global variables
my_books = []
wishlist = []

# Save data to JSON file
def save_data():
    with open("books.json", "w") as file:
        json.dump({"my_books": my_books, "wishlist": wishlist}, file)

# Load data from JSON file
def load_data():
    global my_books, wishlist
    try:
        with open("books.json", "r") as file:
            data = json.load(file)
            my_books = data.get("my_books", [])
            wishlist = data.get("wishlist", [])
    except FileNotFoundError:
        pass

# Delete book function
def delete_book(collection, index):
    if collection == "my_books":
        book = my_books[index]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{book['title']}' from My Books?"):
            my_books.pop(index)
            save_data()
            view_books_gui("my_books", main_frame)
    else:
        book = wishlist[index]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{book['title']}' from Wishlist?"):
            wishlist.pop(index)
            save_data()
            view_books_gui("wishlist", main_frame)

# Add book function for GUI
def add_book_gui(collection, frame):
    for widget in frame.winfo_children():
        widget.destroy()

    def save_book():
        title = title_entry.get()
        author = author_entry.get()
        if not title or not author:
            messagebox.showerror("Error", "Both title and author are required!")
            return
        
        book = {"title": title, "author": author}
        if collection == "my_books":
            book["status"] = "To Read"
            my_books.append(book)
            messagebox.showinfo("Success", f"Book '{title}' added to My Books!")
        elif collection == "wishlist":
            wishlist.append(book)
            messagebox.showinfo("Success", f"Book '{title}' added to Wishlist!")
        save_data()
        show_home()

    # Create a container frame with padding
    container = tk.Frame(frame, bg="#f0f0f0", padx=20, pady=20)
    container.grid(row=0, column=0, sticky="nsew")
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    # Configure grid weights for container
    container.grid_columnconfigure(0, weight=1)
    for i in range(5):
        container.grid_rowconfigure(i, weight=1)

    # Create and style widgets
    title_label = tk.Label(container, text="Title:", font=("Helvetica", 12), bg="#f0f0f0")
    title_label.grid(row=0, column=0, pady=10, sticky="w")
    
    title_entry = tk.Entry(container, font=("Helvetica", 12))
    title_entry.grid(row=1, column=0, pady=5, sticky="ew")

    author_label = tk.Label(container, text="Author:", font=("Helvetica", 12), bg="#f0f0f0")
    author_label.grid(row=2, column=0, pady=10, sticky="w")
    
    author_entry = tk.Entry(container, font=("Helvetica", 12))
    author_entry.grid(row=3, column=0, pady=5, sticky="ew")

    button_frame = tk.Frame(container, bg="#f0f0f0")
    button_frame.grid(row=4, column=0, pady=20)
    
    save_button = tk.Button(button_frame, text="Save", command=save_book, 
                          font=("Helvetica", 12), bg="#4CAF50", fg="white",
                          padx=20, pady=10)
    save_button.pack(side="left", padx=5)
    
    back_button = tk.Button(button_frame, text="Back", command=show_home,
                          font=("Helvetica", 12), bg="#f44336", fg="white",
                          padx=20, pady=10)
    back_button.pack(side="left", padx=5)

# View books function for GUI
def view_books_gui(collection, frame):
    for widget in frame.winfo_children():
        widget.destroy()

    # Create a container frame with padding
    container = tk.Frame(frame, bg="#f0f0f0", padx=20, pady=20)
    container.grid(row=0, column=0, sticky="nsew")
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    # Create a canvas with scrollbar
    canvas = tk.Canvas(container, bg="#f0f0f0")
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    books = my_books if collection == "my_books" else wishlist
    if not books:
        tk.Label(scrollable_frame, text="No books found.", 
                font=("Helvetica", 12), bg="#f0f0f0").pack(pady=10)
    else:
        for index, book in enumerate(books, start=1):
            status = book.get("status", "N/A")
            book_frame = tk.Frame(scrollable_frame, bg="#f0f0f0", pady=5)
            book_frame.pack(fill="x", padx=5)
            
            # Create a frame for the book info and delete button
            info_frame = tk.Frame(book_frame, bg="#f0f0f0")
            info_frame.pack(fill="x", expand=True)
            
            # Book info label
            tk.Label(info_frame, 
                    text=f"{index}. {book['title']} by {book['author']} (Status: {status})",
                    font=("Helvetica", 12), bg="#f0f0f0").pack(side="left", anchor="w")
            
            # Delete button
            delete_btn = tk.Button(info_frame, text="Delete",
                                 command=lambda idx=index-1: delete_book(collection, idx),
                                 font=("Helvetica", 10), bg="#f44336", fg="white",
                                 padx=10, pady=5)
            delete_btn.pack(side="right", padx=5)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    back_button = tk.Button(container, text="Back", command=show_home,
                          font=("Helvetica", 12), bg="#f44336", fg="white",
                          padx=20, pady=10)
    back_button.pack(pady=10)

# Main GUI
root = tk.Tk()
root.title("Cozy Book Tracker")

# Set minimum window size
root.minsize(600, 400)

# Configure the root window grid
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

load_data()

# Create a Main Content Frame
main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

# Home Screen Function
def show_home():
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Configure grid weights
    main_frame.grid_columnconfigure(0, weight=1)
    for i in range(6):
        main_frame.grid_rowconfigure(i, weight=1)

    # Create and style widgets
    title_label = tk.Label(main_frame, text="Welcome to Cozy Book Tracker",
                          font=("Helvetica", 16, "bold"), bg="#f0f0f0")
    title_label.grid(row=0, column=0, pady=20)

    button_style = {"font": ("Helvetica", 12), "padx": 20, "pady": 10, "width": 20}

    add_my_books_btn = tk.Button(main_frame, text="Add Book to My Books",
                                command=lambda: add_book_gui("my_books", main_frame),
                                bg="#2196F3", fg="white", **button_style)
    add_my_books_btn.grid(row=1, column=0, pady=5)

    add_wishlist_btn = tk.Button(main_frame, text="Add Book to Wishlist",
                                command=lambda: add_book_gui("wishlist", main_frame),
                                bg="#2196F3", fg="white", **button_style)
    add_wishlist_btn.grid(row=2, column=0, pady=5)

    view_my_books_btn = tk.Button(main_frame, text="View My Books",
                                 command=lambda: view_books_gui("my_books", main_frame),
                                 bg="#4CAF50", fg="white", **button_style)
    view_my_books_btn.grid(row=3, column=0, pady=5)

    view_wishlist_btn = tk.Button(main_frame, text="View Wishlist",
                                 command=lambda: view_books_gui("wishlist", main_frame),
                                 bg="#4CAF50", fg="white", **button_style)
    view_wishlist_btn.grid(row=4, column=0, pady=5)

    exit_btn = tk.Button(main_frame, text="Exit", command=root.quit,
                        bg="#f44336", fg="white", **button_style)
    exit_btn.grid(row=5, column=0, pady=5)

# Show the Home Screen Initially
show_home()

# Start the GUI application
root.mainloop()





