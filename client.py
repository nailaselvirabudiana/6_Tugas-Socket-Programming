import tkinter as tk
from tkinter import messagebox
import socket
import threading

# Placeholder untuk menyimpan password dan username
user_password = None
user_username = None
client_socket = None
server_address = None

# Fungsi untuk menerima pesan dari server dan memperbarui tampilan chat
def receive_mess():
    while True:
        try:
            mess, address = client_socket.recvfrom(1024)
            chat_display.insert(tk.END, f"{mess.decode()}\n")
            chat_display.see(tk.END)  # Scroll otomatis ke bawah
        except:
            chat_display.insert(tk.END, "Disconnected.\n")
            chat_display.see(tk.END)
            break

# Fungsi untuk mengirim pesan ke server dan menampilkannya di chat display
def send_message(event=None):
    message = message_entry.get()
    if message.lower() == "exit":
        client_socket.sendto("exit".encode(), server_address)
        client_socket.close()
        chat_window.quit()
    else:
        # Tambahkan pesan ke tampilan chat client
        chat_display.insert(tk.END, f"You: {message}\n")
        chat_display.see(tk.END)  # Scroll otomatis ke bawah
        
        # Kirim pesan ke server
        client_socket.sendto(message.encode(), server_address)
        message_entry.delete(0, tk.END)  # Kosongkan entry pesan setelah dikirim

# Jendela pengaturan password
def open_password_window():
    password_window = tk.Toplevel(root)
    password_window.title("Set Password")
    password_window.geometry("300x200")
    
    tk.Label(password_window, text="Enter New Password:", font=("Arial", 12)).pack(pady=10)
    password_entry = tk.Entry(password_window, show="*", font=("Arial", 10))
    password_entry.pack(pady=10)
    tk.Button(password_window, text="OK", font=("Arial", 10), command=lambda: set_password(password_entry.get())).pack(pady=10)

# Fungsi untuk menyimpan password
def set_password(password):
    global user_password
    user_password = password
    messagebox.showinfo("Info", "Password has been set.")
    login_window()

# Jendela login
def login_window():
    login_win = tk.Toplevel(root)
    login_win.title("Login")
    login_win.geometry("300x250")
    
    tk.Label(login_win, text="Username:", font=("Arial", 12)).pack(pady=10)
    username_entry = tk.Entry(login_win, font=("Arial", 10))
    username_entry.pack(pady=5)

    tk.Label(login_win, text="Password:", font=("Arial", 12)).pack(pady=10)
    password_entry = tk.Entry(login_win, show="*", font=("Arial", 10))
    password_entry.pack(pady=5)

    tk.Button(login_win, text="Login", font=("Arial", 10), command=lambda: login(username_entry.get(), password_entry.get())).pack(pady=20)

# Fungsi login untuk memverifikasi username dan password
def login(username, password):
    if password == user_password:
        global user_username
        user_username = username
        connect_to_server()
    else:
        messagebox.showerror("Error", "The password you inputted is wrong!")

# Fungsi utama untuk menghubungkan client ke server
def connect_to_server():
    global client_socket, server_address

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_ip = server_ip_entry.get()
    port = int(port_entry.get())
    client_socket.bind(('', 0))
    server_address = (server_ip, port)

    # Mengirim username untuk validasi ke server
    client_socket.sendto(f"connect:{user_username}:".encode(), server_address)
    response, _ = client_socket.recvfrom(1024)
    
    if response.decode() == "Username taken":
        messagebox.showerror("Error", "Username has been used, please use the other username.")
        login_window()
    else:
        messagebox.showinfo("Info", "Login succeeded!")
        open_chat_client_window()
        threading.Thread(target=receive_mess, daemon=True).start()

# Jendela utama chat client
def open_chat_client_window():
    global chat_window, message_entry, chat_display

    chat_window = tk.Toplevel(root)
    chat_window.title("Chat Client")
    chat_window.geometry("400x400")

    chat_display = tk.Text(chat_window, height=15, width=50, state="normal", font=("Arial", 10))
    chat_display.pack(pady=10)

    message_frame = tk.Frame(chat_window)
    message_frame.pack(pady=5)
    message_entry = tk.Entry(message_frame, width=35, font=("Arial", 10))
    message_entry.grid(row=0, column=0, padx=5)
    message_entry.bind("<Return>", send_message)

    send_button = tk.Button(message_frame, text="Send", command=send_message, font=("Arial", 10))
    send_button.grid(row=0, column=1, padx=5)

# Setup GUI awal untuk pengaturan IP dan Port server
root = tk.Tk()
root.title("Chat Client Setup")
root.geometry("300x300")

tk.Label(root, text="Chat Client Setup", font=("Arial Bold", 14)).pack(pady=10)
tk.Label(root, text="Server IP:", font=("Arial", 12)).pack(pady=5)
server_ip_entry = tk.Entry(root, font=("Arial", 10))
server_ip_entry.pack(pady=5)

tk.Label(root, text="Port:", font=("Arial", 12)).pack(pady=5)
port_entry = tk.Entry(root, font=("Arial", 10))
port_entry.pack(pady=5)

tk.Button(root, text="Next", font=("Arial", 12), command=open_password_window).pack(pady=20)

root.mainloop()