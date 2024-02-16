import tkinter as tk
from PIL import Image, ImageTk

class VendingMachine:
    def __init__(self, master):
        self.master = master
        self.master.title("Vending Machine")

        # Items and their prices
        self.items = {
            "Coke": {"price": 42.00, "image_path": "./assets/coke.png"},
            "Pepsi": {"price": 42.00, "image_path": "./assets/pepsi.png"},
            "Water": {"price": 15.00, "image_path": "./assets/water.png"},
            "Chips": {"price": 36.0, "image_path": "./assets/chips.png"},
            "Chocolate": {"price": 30.00, "image_path": "./assets/chocolate.png"},
            "Candy": {"price": 1.00, "image_path": "./assets/candy.png"},
            "Juice": {"price": 20.00, "image_path": "./assets/juice.png"},
            "Gum": {"price": 2.75, "image_path": "./assets/gum.png"},
            "Cookies": {"price": 10.50, "image_path": "./assets/cookies.png"}
        }

        self.selected_item = tk.StringVar()
        self.selected_item.set("")

        self.coin_inserted = tk.DoubleVar()
        self.coin_inserted.set(0)

        # GUI Elements
        self.selected_item_label = tk.Label(master, textvariable=self.selected_item, font=("Helvetica", 16))
        self.selected_item_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.item_buttons = {}
        button_counter = 0
        for i, (item, data) in enumerate(self.items.items()):
            row_num = i // 3 + 1
            col_num = i % 3
            image = Image.open(data["image_path"]).resize((100, 100), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            button_id = f"A{button_counter + 1}"
            button_counter += 1
            self.item_buttons[item] = tk.Button(master, text=f"{button_id}\nP{data['price']:.2f}",
                                                 command=lambda item=item: self.select_item(item),
                                                 font=("Helvetica", 16), image=photo, compound=tk.TOP)
            self.item_buttons[item].image = photo
            self.item_buttons[item].grid(row=row_num, column=col_num, padx=10, pady=10)

        self.coin_label = tk.Label(master, text="Insert Coin (P):", font=("Helvetica", 16))
        self.coin_label.grid(row=4, column=0, padx=10, pady=10)

        self.coin_entry = tk.Entry(master, textvariable=self.coin_inserted, font=("Helvetica", 16))
        self.coin_entry.grid(row=4, column=1, padx=10, pady=10)

        self.insert_coin_button = tk.Button(master, text="Push", command=self.insert_coin, font=("Helvetica", 16))
        self.insert_coin_button.grid(row=5, columnspan=3, padx=10, pady=10)

        self.retry_button = tk.Button(master, text="Retry", command=self.retry, font=("Helvetica", 16))
        self.retry_button.grid(row=6, column=0, padx=10, pady=10)

        self.cancel_button = tk.Button(master, text="Cancel", command=self.cancel, font=("Helvetica", 16))
        self.cancel_button.grid(row=6, column=1, padx=10, pady=10)

        self.result_label = tk.Label(master, text="", font=("Helvetica", 16))
        self.result_label.grid(row=7, columnspan=3, padx=10, pady=10)

    def select_item(self, item):
        if not self.selected_item.get():
            self.selected_item.set(item)
            self.item_buttons[item].config(state='disabled')
        else:
            self.result_label.config(text="Only one item per purchase.")

    def insert_coin(self):
        coins_inserted = self.coin_inserted.get()
        item = self.selected_item.get()
        if item and item in self.items:
            price = self.items[item]["price"]
            if coins_inserted >= price:
                change = coins_inserted - price
                self.result_label.config(text=f"Purchased {item} for P{price:.2f}. Change: P{change:.2f}")
                self.coin_inserted.set(0)
                self.selected_item.set("")
                for item_button in self.item_buttons.values():
                    item_button.config(state='normal')
            else:
                self.result_label.config(text="Insufficient funds. Please insert more coins.")
        else:
            self.result_label.config(text="Please select an item first.")

    def retry(self):
        self.result_label.config(text="")
        self.selected_item.set("")
        for item_button in self.item_buttons.values():
            item_button.config(state='normal')

    def cancel(self):
        self.master.destroy()

def main():
    root = tk.Tk()
    vending_machine = VendingMachine(root)
    root.mainloop()

if __name__ == "__main__":
    main()
