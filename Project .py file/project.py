
from functools import partial
import tkinter
from tkinter import END, Frame, Menu, Menubutton
from tkinter import PhotoImage, Toplevel, messagebox
from tkinter import filedialog
import customtkinter
from PIL import Image, ImageTk
import pandas as pd
from pandastable import Table
# ML modules
import matplotlib.pyplot as plt
import seaborn as sns
from apyori import apriori
from mlxtend.preprocessing import TransactionEncoder
import os

sns.set_style("dark")
# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("dark")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")


loginroot = customtkinter.CTk()
loginroot.geometry('900x600+200+80')
loginroot.resizable(False, False)
loginroot.grab_set()
loginroot.title("Sign up")
loginroot.wm_iconbitmap("E:\\VS Code files\\Project\\basket.ico")

frame_2 = customtkinter.CTkFrame(
    master=loginroot, corner_radius=15, fg_color="#424242")
frame_2.pack(pady=10, padx=20, fill="both", expand=True)

global username_verify
global password_verify

username_verify = tkinter.StringVar()
password_verify = tkinter.StringVar()

global username_login_entry
global password_login_entry


def signin():

    username1 = username_verify.get()
    password1 = password_verify.get()

    entry1.delete(0, END)
    entry2.delete(0, END)

    list_of_files = os.listdir()
    if username1 in list_of_files:
        file1 = open(username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            loginroot.withdraw()
            root_tk = customtkinter.CTkToplevel()

            # Geometry
            width = root_tk.winfo_screenwidth()
            height = root_tk.winfo_screenheight()
            root_tk.geometry("%dx%d" % (width, height))
            root_tk.state('zoomed')
            root_tk.wm_iconbitmap("E:\\VS Code files\\Project\\basket.ico")
            root_tk.title("PREDICTIFY")
            # *************** Functions ****************
            df = ""

            def import_file():
                global df
                filename = filedialog.askopenfilename(
                    initialdir="C:/gui/",
                    title="Open A File",
                    filetype=(("csv files", "*.csv"), ("All Files", "*.*"))
                )
                if filename:

                    try:
                        filename = r"{}".format(filename)
                        df = pd.read_csv(filename, header=None,
                                         encoding="ISO-8859-1")
                    except ValueError:
                        label_file_explorer.config(
                            text="File Couldn't Be Opened...try again!")
                    except FileNotFoundError:
                        label_file_explorer.config(
                            text="File Couldn't Be Found...try again!")

                label_file_explorer.configure(text="File Opened: "+filename)

            def predict():
                global df
                global DataFrame_intelligence
                trasnsactions = []
                num1 = len(df)
                num2 = len(df.columns)

                if num1 == 0 and num2 == 0:
                    messagebox.showinfo(
                        'Notification', 'dataset is empty!!!', parent=frame_1)
                else:
                    for i in range(0, num1):
                        trasnsactions.append([str(df.values[i, j])
                                              for j in range(0, num2)])

                    # Encoding.
                    temp = trasnsactions
                    t = TransactionEncoder()
                    temp = t.fit_transform(trasnsactions)
                    temp = pd.DataFrame(temp, columns=t.columns_, dtype=int)

                    # Dropping NaN values.
                    temp.drop('nan', axis=1, inplace=True)
                    r = temp.sum(axis=0).sort_values(ascending=False)[:20]

                    plt.figure(figsize=(20, 20))
                    plt.title('Top 20 items that are frequently purchased ')
                    plt.text(2, 2000, 'So we may advice that this 20 items must be always in the stock', fontsize=16,
                             bbox=dict(facecolor='#e6ee9c'))
                    plt.bar(r.index, r.values, color=[
                            '#ec407a', '#ab47bc', '#ef5350', '#7e57c2', '#5c6bc0', '#42a5f5', '#29b6f6', '#26c6da', '#26a69a', '#66bb6a', '#9ccc65', '#d4e157', '#ffee58', '#ffca28', '#ffa726', '#ff7043', '#8d6e63', '#bdbdbd', '#78909c'])
                    plt.show()

                    basket = apriori(trasnsactions, min_support=0.003,
                                     min_confidance=0.2, min_lift=2, min_length=2, max_length=2, use_columns=True)
                    results = list(basket)

                    def inspect(results):
                        product1 = [tuple(result[2][0][0])[0]
                                    for result in results]
                        product2 = [tuple(result[2][0][1])[0]
                                    for result in results]
                        supports = [result[1] for result in results]
                        confidences = [result[2][0][2] for result in results]
                        lifts = [result[2][0][3] for result in results]
                        return list(zip(product1, product2, supports, confidences, lifts))

                    DataFrame_intelligence = pd.DataFrame(inspect(results), columns=[
                        'Product-1', 'Product-2', 'Support', 'Confidence', 'Lift'])
                    DataFrame_intelligence = DataFrame_intelligence.nlargest(
                        n=500, columns='Lift')
                    DataFrame_intelligence.drop_duplicates(
                        inplace=True)
                    table = Table(
                        showdataframe, dataframe=DataFrame_intelligence, read_only=True, setRowHeight=800, show_progress_window=True,
                        showtoolbar=True, showstatusbar=True)

                    mask_1 = table.model.df['Lift'] > 3
                    table.setColorByMask('Lift', mask_1, '#66bb6a')
                    mask_1 = table.model.df['Lift'] < 3
                    table.setColorByMask('Lift', mask_1, '#ef5350')
                    table.show()

            def export():
                global DataFrame_intelligence
                DataFrame_intelligence.to_excel(
                    r'C:\\Users\\USER\\Desktop\\name.xlsx', index=False)

                messagebox.showinfo('Notification',
                                    '''
                                    File Exported sucessfully 
                                    Path = C:\\Users\\USER\\Desktop\\name.xlsx
                                    ''')

            def preview():
                global df
                previewroot = Toplevel()
                width = root_tk.winfo_screenwidth()
                height = root_tk.winfo_screenheight()
                previewroot.geometry("%dx%d" % (width, height))
                previewroot.state('zoomed')
                previewroot.title('Preview')
                p1 = PhotoImage(file="E:\VS Code files\Project\\preview.png")
                previewroot.iconphoto(False, p1)
                previewroot.config(bg='#616161')

                inside_frame = Frame(master=previewroot, bg="#cfd8dc")
                inside_frame.place(width=1340, height=710)
                table = Table(inside_frame, dataframe=df, read_only=False,
                              showtoolbar=True, showstatusbar=True)
                table.show()

                previewroot.mainloop()

            def help():
                helproot = Toplevel()
                width = root_tk.winfo_screenwidth()
                height = root_tk.winfo_screenheight()
                helproot.geometry("%dx%d" % (width, height))
                helproot.state('zoomed')
                helproot.title('Help')
                p1 = PhotoImage(file="E:\VS Code files\Project\\help.png")
                helproot.iconphoto(False, p1)
                helproot.resizable(False, False)
                helproot.config(bg='#616161')
                image = ImageTk.PhotoImage(Image.open(
                    "E:\VS Code files\Project\capture.jpg").resize((600, 500), Image.ANTIALIAS))
                help_img_2 = customtkinter.CTkLabel(helproot, image=image)
                help_img_2.place(x=10, y=20)

                image_112 = ImageTk.PhotoImage(Image.open(
                    "E:\VS Code files\Project\SCL.png").resize((650, 500), Image.ANTIALIAS))
                help_img_2 = customtkinter.CTkLabel(helproot, image=image_112)
                help_img_2.place(x=620, y=20)

                image_113 = ImageTk.PhotoImage(Image.open(
                    "E:\\VS Code files\\Project\\relation.png").resize((1000, 200), Image.ANTIALIAS))
                help_img_3 = customtkinter.CTkLabel(helproot, image=image_113)
                help_img_3.place(x=10, y=540)

                helproot.mainloop()

            def about():
                messagebox.showinfo('Notification',
                                    '''
                1. PRDECTIFY version 1.0.0.0 \n
                2. Made by Shounak, Ashish, Prasad \n
                3. As a Final year project which gives you a most purchasable items by customers\n
                4. Guide : prof. Charhre sir\n
                5. collage : DIEMS\n
                6. Date : 29th April 2022''', parent=frame_1)

            def exit():
                res = messagebox.askyesnocancel(
                    "Notification", "Are you want to exit?")
                if (res == True):
                    root_tk.destroy()

            # ****************** Frames/Labels *******************

            frame_1 = customtkinter.CTkFrame(
                master=root_tk, corner_radius=15, fg_color="#424242")
            frame_1.pack(pady=10, padx=20, fill="both", expand=True)

            showdataframe = Frame(
                master=frame_1, bg="#cfd8dc")
            showdataframe.place(x=300, y=200, width=975, height=480)

            label_file_explorer = customtkinter.CTkLabel(
                frame_1, corner_radius=15, text="File Path:                                                                               ", width=400, height=8, text_color='yellow')
            label_file_explorer.place(x=-20, y=175)

            # **************** Heading, 2-images *****************

            def color_config(widget, color, event):
                widget.configure(foreground=color)

            name_label = customtkinter.CTkLabel(master=frame_1, text_font=(
                " 3ds ", 50, 'bold', 'underline'), text_color='#673ab7', text='P R E D I C T I F Y', corner_radius=20)
            name_label.bind("<Enter>", partial(
                color_config, name_label, "#fff176"))
            name_label.bind("<Leave>", partial(
                color_config, name_label, "#673ab7"))
            name_label.pack(pady=10, padx=10)

            load1 = Image.open("E:\VS Code files\Project\header_image.png")
            resized_image1 = load1.resize((90, 90), Image.ANTIALIAS)
            render1 = ImageTk.PhotoImage(resized_image1)
            img1 = customtkinter.CTkLabel(frame_1, image=render1)
            img1.place(x=250, y=5)

            load2 = Image.open("E:\VS Code files\Project\header_image.png")
            resized_image2 = load2.resize((90, 85), Image.ANTIALIAS)
            render2 = ImageTk.PhotoImage(resized_image2)
            img2 = customtkinter.CTkLabel(frame_1, image=render2)
            img2.place(x=950, y=5)

            # ***************** Buttons *****************************
            # 1
            import_bt = ImageTk.PhotoImage(Image.open(
                "E:\VS Code files\Project\import.png").resize((40, 40), Image.ANTIALIAS))
            import_data = customtkinter.CTkButton(master=frame_1, text='           Import data', text_color='black', width=300, height=50, text_font=(
                " Times ", 25, 'bold'), corner_radius=20, hover_color='#7e57c2', image=import_bt, compound="right", command=import_file)
            import_data.place(x=-110, y=200)

            # 2
            export_bt = ImageTk.PhotoImage(Image.open(
                "E:\VS Code files\Project\export.png").resize((40, 40), Image.ANTIALIAS))
            export_data = customtkinter.CTkButton(master=frame_1, text='           Export data', text_color='black', width=300, height=50, text_font=(
                " Times ", 25, 'bold'), corner_radius=20, hover_color='#7e57c2', image=export_bt, compound="right", command=export)
            export_data.place(x=-110, y=300)

            # 3
            help_ig = ImageTk.PhotoImage(Image.open(
                "E:\VS Code files\Project\help.png").resize((40, 40), Image.ANTIALIAS))
            help = customtkinter.CTkButton(master=frame_1, text='           Help', text_color='black', width=370, height=50, text_font=(
                " Times ", 25, 'bold'), corner_radius=20, hover_color='#7e57c2', image=help_ig, compound="right", command=help)
            help.place(x=-110, y=400)

            # 4
            about_ig = ImageTk.PhotoImage(Image.open(
                "E:\VS Code files\Project\\about.png").resize((40, 40), Image.ANTIALIAS))
            about = customtkinter.CTkButton(master=frame_1, text='           About', text_color='black', width=370, height=50, text_font=(
                " Times ", 25, 'bold'), corner_radius=20, hover_color='#7e57c2', image=about_ig, compound="right", command=about)
            about.place(x=-110, y=500)

            # 5
            exit_ig = ImageTk.PhotoImage(Image.open(
                "E:\VS Code files\Project\\exit.png").resize((40, 40), Image.ANTIALIAS))
            exit = customtkinter.CTkButton(master=frame_1, text='           Exit', text_color='black', width=370, height=50, text_font=(
                " Times ", 25, 'bold'), corner_radius=20, hover_color='#7e57c2', image=exit_ig, compound="right", command=exit)
            exit.place(x=-110, y=600)

            # 6

            def change_mode():
                if switch_2.get() != 1:
                    customtkinter.set_appearance_mode("dark")
                    width = root_tk.winfo_screenwidth()
                    height = root_tk.winfo_screenheight()
                    root_tk.geometry("%dx%d" % (width, height))
                    root_tk.state('zoomed')
                else:
                    customtkinter.set_appearance_mode("light")
                    width = root_tk.winfo_screenwidth()
                    height = root_tk.winfo_screenheight()
                    root_tk.geometry("%dx%d" % (width, height))
                    root_tk.state('zoomed')

            switch_2 = customtkinter.CTkSwitch(master=frame_1, text="Light Mode",
                                               command=change_mode, text_color='yellow', text_font=('3ds', 10, "bold"))
            switch_2.place(x=20, y=20)

            # 7
            predict_ig = ImageTk.PhotoImage(Image.open(
                "E:\VS Code files\Project\\predict.png").resize((50, 50), Image.ANTIALIAS))
            predict = customtkinter.CTkButton(master=frame_1, text='Predict', text_color='black', width=50, height=50, text_font=(
                " Times ", 25, 'bold'), corner_radius=40, hover_color='#7e57c2', image=predict_ig, compound="right", command=predict)
            predict.place(x=550, y=115)
            # 8
            preview_ig = ImageTk.PhotoImage(Image.open(
                "E:\VS Code files\Project\\preview.png").resize((50, 50), Image.ANTIALIAS))
            preview = customtkinter.CTkButton(master=frame_1, text='           Preview', text_color='black', width=370, height=50, text_font=(
                " Times ", 25, 'bold'), corner_radius=20, hover_color='#7e57c2', image=preview_ig, compound="right", command=preview)
            preview.place(x=-110, y=115)

            # Other
            text = customtkinter.CTkLabel(
                frame_1, corner_radius=15, text="Made with 💖 by Shounak", width=50, height=5, text_color='yellow')
            text.place(x=10, y=675)

            rights = customtkinter.CTkLabel(
                frame_1, corner_radius=10, text="Copyright © 2022. All Rights Reserved", width=50, height=3, text_color='yellow')
            rights.place(x=600, y=680)

            w = customtkinter.CTkCanvas(
                frame_1, width=150, height=90, bg="#424242", bd=0, relief='solid', highlightthickness=0)
            w.place(x=850, y=95)
            w.create_rectangle(40, 43, 10, 17, fill="#66bb6a")
            w.create_text(100, 31, text="LIFT > 3", font=(
                '3ds', 16, 'bold'), fill='White')

            w.create_rectangle(40, 83, 10, 57, fill="#ef5350")
            w.create_text(100, 71, text="LIFT < 3", font=(
                '3ds', 16, 'bold'), fill='White')

            def sign_out():
                root_tk.destroy()

            user_ig = ImageTk.PhotoImage(Image.open(
                "E:\VS Code files\Project\\user.png").resize((30, 30), Image.ANTIALIAS))
            user = Menubutton(master=frame_1, text=username1, fg='white', font=(" 3ds ", 10, 'bold'),  bg="#424242",
                              image=user_ig, compound="right", relief='solid', bd=0, activebackground="#424242", activeforeground='#7e57c2')
            user.place(x=1165, y=20, width=150, height=35)

            user.menu = Menu(user, tearoff=0)
            user["menu"] = user.menu

            user.menu.add_command(label="Sign Out", command=sign_out)

            root_tk.mainloop()
        else:
            messagebox.showinfo(
                'Notification', 'Password not recognized', parent=loginroot)

    else:
        messagebox.showinfo('Notification', 'User not found', parent=loginroot)


login_ig = Image.open("E:\VS Code files\Project\login.JPG")
resized_image11 = login_ig.resize((440, 568), Image.ANTIALIAS)
render2 = ImageTk.PhotoImage(resized_image11)
img11 = customtkinter.CTkLabel(frame_2, image=render2)
img11.place(x=5, y=5)

enterence = customtkinter.CTkLabel(master=loginroot, text_font=(" 3ds ", 25, 'bold'), text_color='#cddc39', text='P R E D I C T I F Y', corner_radius=8, bg_color="#424242"
                                   )
enterence.place(x=525, y=100)


entry1 = customtkinter.CTkEntry(master=frame_2, width=250, height=30, corner_radius=10,
                                text_color='#7e57c2', text_font=(" Times ", 16), textvariable=username_verify)
entry1.place(x=650, y=250, anchor=tkinter.CENTER)

label1 = customtkinter.CTkLabel(frame_2, text='Enter Username',
                                text_color='yellow', text_font=("times", 16), corner_radius=10)
label1.place(x=520, y=205)

entry2 = customtkinter.CTkEntry(master=frame_2, width=250, height=30, corner_radius=10,
                                text_color='#7e57c2', text_font=(" Times ", 16), textvariable=password_verify)
entry2.place(x=650, y=335, anchor=tkinter.CENTER)

label1 = customtkinter.CTkLabel(frame_2, text='Enter Password',
                                text_color='yellow', text_font=("times", 16), corner_radius=10)
label1.place(x=520, y=290)


login_bt = ImageTk.PhotoImage(Image.open(
    "E:\VS Code files\Project\login_bt1.png").resize((40, 40), Image.ANTIALIAS))
login_1 = customtkinter.CTkButton(master=frame_2, text='Sign In', text_color='yellow', width=10, height=10, text_font=(
    " 3ds ", 14, 'bold'), corner_radius=20, hover_color='#7e57c2', image=login_bt, compound="right", command=signin)
login_1.place(x=570, y=375)


def signup():
    signuproot = customtkinter.CTkToplevel()
    signuproot.geometry('500x500+400+150')
    signuproot.resizable(False, False)
    signuproot.grab_set()
    signuproot.title("Create account")
    p1 = tkinter.PhotoImage(file='E:\VS Code files\Project\create.png')
    signuproot.iconphoto(False, p1)

    global name_signup
    global username_signup
    global password_signup

    name_signup = tkinter.StringVar()
    username_signup = tkinter.StringVar()
    password_signup = tkinter.StringVar()

    def register():
        name_info = name_signup.get()
        username_info = username_signup.get()
        password_info = password_signup.get()

        if len(username_info) == 0 and len(password_info) == 0 and len(name_info) == 0:
            messagebox.showinfo(
                'Notification', "Fields can't be empty", parent=frame_2)
        else:
            file = open(username_info, "w")
            file.write(name_info + "\n")
            file.write(username_info + "\n")
            file.write(password_info)
            file.close()

            name.delete(0, END)
            username.delete(0, END)
            password.delete(0, END)

            messagebox.showinfo(
                'Notification', 'Registration Successfully', parent=loginroot)
            signuproot.destroy()

    label21 = customtkinter.CTkLabel(
        signuproot, text='Name', text_color='yellow', text_font=("times", 16), corner_radius=10)
    label21.place(x=100, y=60)
    name = customtkinter.CTkEntry(master=signuproot, width=250, height=30, corner_radius=10,
                                  text_color='#7e57c2', text_font=(" Times ", 16), textvariable=name_signup)
    name.place(x=250, y=100, anchor=tkinter.CENTER)

    label22 = customtkinter.CTkLabel(
        signuproot, text='Enter Username', text_color='yellow', text_font=("times", 16), corner_radius=10)
    label22.place(x=120, y=160)
    username = customtkinter.CTkEntry(master=signuproot, width=250, height=30, corner_radius=10,
                                      text_color='#7e57c2', text_font=(" Times ", 16), textvariable=username_signup)
    username.place(x=250, y=200, anchor=tkinter.CENTER)

    label23 = customtkinter.CTkLabel(
        signuproot, text='Password', text_color='yellow', text_font=("times", 16), corner_radius=10)
    label23.place(x=110, y=260)
    password = customtkinter.CTkEntry(master=signuproot, width=250, height=30, corner_radius=10,
                                      text_color='#7e57c2', text_font=(" Times ", 16), textvariable=password_signup)
    password.place(x=250, y=300, anchor=tkinter.CENTER)

    sign_bt = ImageTk.PhotoImage(
        Image.open("E:\VS Code files\Project\login_bt1.png").resize((40, 40), Image.ANTIALIAS))
    signup_1 = customtkinter.CTkButton(master=signuproot, text='Sign Up', text_color='yellow', width=10, height=10, text_font=(
        " 3ds ", 14, 'bold'), corner_radius=20, hover_color='#7e57c2', image=sign_bt, compound="right", command=register)
    signup_1.place(x=150, y=350)

    signuproot.mainloop()


create = tkinter.Button(frame_2, text="Don't have account? Sign Up here", font=('times', 12, 'bold'),
                        fg='Yellow', bg="#424242", relief='solid', bd=0, activebackground="#424242", activeforeground='#7e57c2', command=signup)
create.place(x=535, y=435)

loginroot.mainloop()
