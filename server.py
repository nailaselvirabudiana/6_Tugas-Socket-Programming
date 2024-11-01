import tkinter as tk
from tkinter import scrolledtext, messagebox
import socket
import threading

# Dictionary untuk menyimpan alamat setiap client berdasarkan username
clients = {}

# Fungsi untuk menangani pesan dari client dan mengirimkannya ke client lain
def handle_client(address):
    username = clients[address]
    while True:
        try:
            # Menerima pesan dari client
            data, addr = server_socket.recvfrom(1024)
            
            # Memastikan pesan yang datang berasal dari address yang diinginkan
            if addr == address:
                mess = data.decode()
                
                # Log and broadcast the message to other clients
                update_log(f"Message from {username}: {mess}")
                for client_address in clients:
                    if client_address != addr:
                        server_socket.sendto(f"{username}: {mess}".encode(), client_address)
            else:
                print(f"Message received from unexpected address {addr} for user {username}")
                    
        except Exception as e:
            # Jika ada disconnect atau error, client diremove 
            update_log(f"Client {username} in {address} has been disconnected. Error: {e}")
            del clients[address]
            break

# Fungsi untuk menjalankan server
def run_server():
    global server_socket

    server_ip = server_ip_entry.get()
    port = int(port_entry.get())
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((server_ip, port))
    update_log(f"Server active at {server_ip}:{port}")
    status_label.config(text="Status: Server is running", fg="green")

    # Thread untuk menerima data dari client
    threading.Thread(target=receive_messages, daemon=True).start()

def receive_messages():
    while True:
        try:
            data, address = server_socket.recvfrom(1024)
            mess = data.decode()
            
            # Cek apakah terdapat connection request
            if mess.startswith("connect:"):
                # split pesan untuk memisahkan connection dan additional text
                parts = mess.split(":", 2) 
                usn = parts[1] 

                # Cek konten chat tambahan di pesan awal
                initial_message = parts[2] if len(parts) > 2 else None
                
                # Validasi jika username unik
                if usn not in clients.values():
                    clients[address] = usn 
                    server_socket.sendto("Username accepted".encode(), address)
                    print(f"{usn} joined from {address}")
                    update_log(f"{usn} joined in address {address}")

                    # Jika ada pesan awal, ditangani langsung
                    if initial_message:
                        route_message(address, initial_message)
                else:
                    # Jika username telah dipakai, kirim pesan bahwa username telah dipakai
                    server_socket.sendto("Username taken".encode(), address)
            else:
                # Jika ini adalah pesan chat biasa, di-route langsung
                route_message(address, mess)
        
        except Exception as e:
            print(f"Error in receive_messages: {e}")
            break

def route_message(sender_address, message):
    username = clients.get(sender_address)
    
    if username:
        if message.lower() == "exit":
            # Catat dan hapus klien jika mereka mengirimkan 'exit'
            update_log(f"{username} has disconnected.")
            print(f"{username} at {sender_address} has disconnected.")
            del clients[sender_address]
            return
        # Catat dan kirim ulang pesan ke klien lain
        update_log(f"Message from {username}: {message}")
        for client_address in clients:
            if client_address != sender_address:
                try:
                    server_socket.sendto(f"{username}: {message}".encode(), client_address)
                except Exception as e:
                    # Catat pemutusan koneksi jika pengiriman gagal
                    disconnected_user = clients[client_address]
                    print(f"{disconnected_user} at {client_address} has disconnected unexpectedly.")
                    update_log(f"{disconnected_user} has disconnected unexpectedly.")
                    del clients[client_address]

# Fungsi untuk memperbarui log di GUI
def update_log(message):
    log_display.config(state="normal")
    log_display.insert(tk.END, message + "\n")
    log_display.config(state="disabled")
    log_display.see(tk.END)

# Fungsi untuk menutup server dan GUI
def on_closing():
    try:
        server_socket.close()
    except:
        pass
    root.quit()

# Setup GUI
root = tk.Tk()
root.title("Server GUI")
root.geometry("500x500")
root.configure(bg="#f0f0f0")

tk.Label(root, text="Server Setup", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
tk.Label(root, text="Server IP:", font=("Arial", 10), bg="#f0f0f0").pack()
server_ip_entry = tk.Entry(root, font=("Arial", 10))
server_ip_entry.pack(pady=5)

tk.Label(root, text="Port:", font=("Arial", 10), bg="#f0f0f0").pack()
port_entry = tk.Entry(root, font=("Arial", 10))
port_entry.pack(pady=5)

start_button = tk.Button(root, text="Start Server", font=("Arial", 12, "bold"), bg="#4caf50", fg="white", command=run_server)
start_button.pack(pady=10)

status_label = tk.Label(root, text="Status: Server Tidak Berjalan", font=("Arial", 10, "italic"), fg="red", bg="#f0f0f0")
status_label.pack(pady=5)

tk.Label(root, text="Server Log:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=10)
log_display = scrolledtext.ScrolledText(root, width=60, height=20, font=("Courier", 10), bg="#e8e8e8", state="disabled")
log_display.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
