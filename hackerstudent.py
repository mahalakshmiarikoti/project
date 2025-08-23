from PIL import Image,ImageDraw,ImageFont
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog,messagebox

bg_path_var=None
logo_path_var=None

def create_invitation(bg_color,bg_path,logo_path):
    width,height=800,600
    image=Image.new('RGB',(width,height),bg_color)

    if bg_path:
        try:
            bg=Image.open(bg_path).resize((width,height))
            image.paste(bg,(0,0))
        except Exception as e:
            messagebox.showerror("Error",f"could not load background image:\n{e}")
            return
    draw=ImageDraw.Draw(image)
    draw.rectangle([10,10,width-10,height-10],outline=(0,102,204),width=10)
    try:
        title_font=ImageFont.truetype("arial.ttf",40)
        body_font=ImageFont.truetype("arial.ttf",24)
    except:
        title_font=ImageFont.load_default()
        body_font=ImageFont.load_default()


    title="you're invited"
    bbox=draw.textbbox((0,0),title,font=title_font)
    text_width=bbox[2]-bbox[0]
    draw.text(((width-text_width)//2,50),title,fill="cyan",font=title_font)

    details="""

    
    
join us for a special celebration!
Date:22nd and 23rd
time:8:00 AM
venue:K.B.N Collge
Duration:24 Hours
Organisation:K.B.N Management"""
    draw.multiline_text((100, 150), details, fill="red", font=body_font, spacing=10)

    # Add logo
    try:
        logo = Image.open(logo_path).resize((150, 150))

        if logo.mode in ('RGBA', 'LA'):
            if logo.mode == 'LA':
                logo = logo.convert('RGBA')
            r, g, b, alpha = logo.split()
            bg = Image.new('RGBA', logo.size, (255, 255, 255, 0))
            bg.paste(logo, (0, 0), mask=alpha)
            image.paste(bg, (width - 160, 20), mask=alpha)
        else:
            image.paste(logo, (width - 160, 20))
    except Exception as e:
        messagebox.showerror("Error", f"Could not load logo image:\n{e}")
        return

    # Save and show
    image.save('invitation_card.png', quality=95)
    plt.figure(figsize=(10, 7.5))
    plt.imshow(image)
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def select_background_image():
    path = filedialog.askopenfilename(title="Select Background Image",
                                      filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if path:
        bg_path_var.set(path)


def select_logo():
    path = filedialog.askopenfilename(title="Select Logo Image",
                                      filetypes=[("Image Files", "*.png")])
    if path:
        logo_path_var.set(path)


def generate_invitation():
    bg_path = bg_path_var.get() if bg_path_var.get() != "No background selected" else None
    logo_path = logo_path_var.get()

    if not logo_path or logo_path == "No logo selected":
        messagebox.showwarning("Warning", "Please select a logo image.")
        return

    create_invitation((255, 255, 255), bg_path, logo_path)
root=tk.Tk()
root.title("Invitation card Generation")
root.geometry("400x300")

bg_path_var=tk.StringVar(value="No background selected")
logo_path_var=tk.StringVar(value="No logo selected")

tk.Button(root,text="select background image",command=select_background_image).pack(pady=10)
tk.Label(root,textvariable=bg_path_var,wraplength=350).pack(pady=5)

tk.Button(root,text="select logo image",command=select_logo).pack(pady=10)
tk.Label(root,textvariable=logo_path_var,wraplength=350).pack(pady=5)

tk.Button(root,text="Generate Invitation",command=generate_invitation).pack(pady=20)

root.mainloop()
