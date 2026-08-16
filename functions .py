import mysql.connector
import pickle
import os
import csv
import tkinter as tk
from tkinter import simpledialog
from prettytable import PrettyTable
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

obj = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME)


def display_dish():
    cu = obj.cursor()
    flag = "green"
    cu.execute("select * from review")
    a = cu.fetchall()
    t = ["Name", "avg_stars", "no. of reviews"]
    tab = PrettyTable()
    tab.field_names = t
    for i in a:
        tab.add_row(i)
    print(tab)
    cu.close()
    f = open("dishes.csv", "r", newline="\n")
    r = csv.reader(f)
    global c
    print()
    c = input("Enter Dish Name To View Recipe:")
    print()
    for i in r:
        if i[0].lower() == c.lower():
            print("========================", c.upper(), "========================")
            print()
            print("INGREDIENTS:")
            for j in i[1].split("'"):
                k = j.strip("[]").replace(",", "").strip()
                if k:
                    print("-", k.title())
            print()
            print("PROCEDURE:")
            break
    else:
        print("**RECIPE NOT IN LIST**")
        print()
        print("1.New Search")
        print("2.Check Favourites")
        print("3.Sign Out")
        m = int(input("Enter Your Option:"))
        print("_________________________________________________________")
        print()
        if m == 1:
            print("1.Search By Ingredients")
            print("2.View All Recipes")
            g = int(input("Enter Your Option:"))
            print("________________________________________________________")
            print()
            if g == 1:
                dish_search()
            elif g == 2:
                display_dish()
        elif m == 2:
            display_fav()
        elif m == 3:
            print("                     **LOGGED OUT**")
            print("_________________________________________________________")
            print()
            flag = "red"
    f.close()
    f = open("recipes.dat", "rb")
    try:
        while True:
            x = pickle.load(f)
            if x["name"].lower() == c.lower():
                for i in x:
                    if i != "name":
                        print(i, ".", x[i], sep="")
                        print()
    except EOFError:
        print("_________________________________________________________")
        f.close()
    print()
    print("1.Add To Fav")
    print("2.New Search")
    print("3.Add review")
    print("4.view review")
    print("5.Sign Out")
    z = int(input("Choose An Option From Above:"))
    print("_________________________________________________________")
    print()
    if z == 1:
        fav_add()
    elif z == 2:
        print("1.Search By Ingredients")
        print("2.View All Recipes")
        g = int(input("Enter Your Option:"))
        print("_________________________________________________________")
        print()
        if g == 1:
            dish_search()
        elif g == 2:
            display_dish()
    elif z == 3:
        review()
    elif z == 4:
        cu = obj.cursor()
        cu.execute("select * from comment where name = %s", (c,))
        k = cu.fetchall()
        if k:
            t = ["Name", "stars", "user name", "comment"]
            tab = PrettyTable()
            tab.field_names = t
            for i in k:
                tab.add_row(i)
            print(tab)
        else:
            print("**NO REVIEWS YET**")
        print()
        b = input("Would u like to  add it to favourites?(y/n)")
        print()
        if b == "y":
            fav_add()
    elif z == 5:
        print("                      **LOGGED OUT**")
        print("_________________________________________________________")
        flag = "red"
    cu.close()
    return flag


def checkpass():
    f = open("passwords.dat", "rb")
    flag = "green"
    try:
        while True:
            r = pickle.load(f)
            if r[0] == user:
                flag = "red"
                if r[1] == pwd:
                    x = "successful login"
                else:
                    x = "incorrect password"
    except EOFError:
        f.close()
    if flag == "green":
        x = "**USER NOT FOUND**"
    return x


def signin():
    while True:
        global user
        global pwd
        print("====================== LOGIN PAGE =======================")
        user = input("Enter Username: ")
        pwd = getpwd()
        t = checkpass()
        print()
        print("**" + t.upper() + "**")
        print("_________________________________________________________")
        print()
        if t == "successful login":
            break
        else:
            print("1.Re-enter Details")
            print("2.Create Account")
            c = int(input("Enter Your Option:"))
            print("_________________________________________________________")
            print()
            if c == 1:
                continue
            elif c == 2:
                t = signup()
                if not t:
                    signup()
                break


def signup():
    print()
    user = input("Enter Username: ")
    user_exists = False
    f1 = open("passwords.dat", "rb")
    try:
        while True:
            user_data = pickle.load(f1)
            if user_data[0] == user:
                print("**USERNAME TAKEN**")
                user_exists = True
                break
    except EOFError:
        f1.close()
    if not user_exists:
        pwd = getpwd()
        f2 = open("passwords.dat", "ab")
        user_data = [user, pwd]
        pickle.dump(user_data, f2)
        print()
        print("**Account Created**")
        x = user + ".txt"
        f = open(x, "w")
        f.write("")
        f.close()
        print("**SIGN IN**")
        print()
        f2.close()
        signin()
        return True
    elif user_exists:
        return False


def fav_delete():
    x = user + ".txt"
    f = open(x, "r")
    f1 = open("new.txt", "w")
    a = input("Enter Dish To Be Removed:")
    print()
    r = f.readline()
    while r:
        if r.lower() != a.lower() + "\n":
            f1.write(r)
        r = f.readline()
    f.close()
    f1.close()
    os.remove(x)
    os.rename("new.txt", x)
    f = open(x, "r")
    r = f.read()
    print("======================= FAVOURITES ========================")
    print(r)
    print("**DELETED**")
    print()


def fav_search():
    f = open("dishes.csv", "r", newline="\n")
    r = csv.reader(f)
    c = input("enter dish name to view:")
    for i in r:
        if i[0].lower() == c.lower():
            for j in i[1].split("'"):
                k = j.strip("[]").replace(",", "").strip()
                if k:
                    print("-", k.title())
    f.close()
    f = open("recipes.dat", "rb")
    try:
        while True:
            x = pickle.load(f)
            if x["name"].lower() == c.lower():
                for i in x:
                    if i != "name":
                        print(i, ".", x[i])
                        print()
    except EOFError:
        f.close()


def sugg_add():
    f1 = open("suggestions.txt", "r")
    s = f1.readlines()
    f1.close()
    for p in sug:
        flg = "red"
        l = p + "\n"
        for i in s:
            if i.lower() == l.lower():
                flg = "green"
                break
        if flg == "red":
            f2 = open("suggestions.txt", "a")
            k = p.lower()
            f2.write(k + "\n")
            f2.close()


def dish_search():
    flag = "green"
    n = int(input("No. Of Ingredients:"))
    l = []
    global sug
    sug = []
    if n < 3:
        n = 0
        print("Not Enough Ingredients!!!!")
    for i in range(n):
        ing = input("Ingredient: ")
        l.append(ing.lower())
        f = open("dishes.csv", "r", newline="\n")
        r = csv.reader(f)
        fg = "green"
        for i in r:
            if ing.lower() in i[1]:
                fg = "red"
                break
        if fg == "green":
            sug.append(ing)
        f.close()
    print()
    sugg_add()
    f = open("dishes.csv", "r", newline="\n")
    r = csv.reader(f)
    p = []
    for i in r:
        count = 0
        for j in l:
            if j in i[1]:
                count = count + 1
        if count >= 3:
            p.append(i[0])
    x = []
    cu = obj.cursor()
    for i in p:
        cu.execute("select * from review where name= %s", (i,))
        a = cu.fetchone()
        x.append(a)
    t = ["Name", "avg_stars", "no. of reviews"]
    tab = PrettyTable()
    tab.field_names = t
    for i in x:
        tab.add_row(i)
    print(tab)
    cu.close()
    print()
    if p == []:
        print("**NO RECIPES FOUND**")
        print()
        print("1.New Search")
        print("2.Check Fav")
        print("3.Sign Out")
        m = eval(input("Enter Your Option:"))
        print("_________________________________________________________")
        print()
        if m == 1:
            print("1.Search By Ingredients")
            print("2.View All Recipes")
            g = int(input("Enter Your Option:"))
            print("_________________________________________________________")
            print()
            if g == 1:
                dish_search()
            elif g == 2:
                display_dish()
        elif m == 2:
            display_fav()
        elif m == 3:
            print("                     **LOGGED OUT**")
            print("_________________________________________________________")
            print()
            flag = "red"
    f.close()
    if p != []:
        f = open("dishes.csv", "r", newline="\n")
        r = csv.reader(f)
        global c
        c = input("Enter Dish Name To View Recipe:")
        print()
        for i in r:
            if i[0].lower() == c.lower():
                print("========================", c.upper(), "========================")
                print()
                print("INGREDIENTS:")
                for j in i[1].split("'"):
                    k = j.strip("[]").replace(",", "").strip()
                    if k:
                        print("-", k.title())
                print()
                print("PROCEDURE:")
                break
        else:
            print("**RECIPE NOT IN LIST**")
            print()
            print("1.New Search")
            print("2.Check Favourites")
            print("3.Sign Out")
            m = int(input("Enter Your Option:"))
            print("_________________________________________________________")
            print()
            if m == 1:
                print("1.Search By Ingredients")
                print("2.View All Recipes")
                g = eval(input("Enter Your Option:"))
                print("_________________________________________________________")
                print()
                if g == 1:
                    dish_search()
                elif g == 2:
                    display_dish()
            elif m == 2:
                display_fav()
            elif m == 3:
                print("                     **LOGGED OUT**")
                print("_________________________________________________________")
                print()
                flag = "red"
        print()
        f.close()
        f = open("recipes.dat", "rb")
        try:
            while True:
                x = pickle.load(f)
                if x["name"].lower() == c.lower():
                    for i in x:
                        if i != "name":
                            print(i, ".", x[i])
                            print()
        except EOFError:
            print("_________________________________________________________")
            f.close()
        print()
        print("1.Add To Fav")
        print("2.New Search")
        print("3.Add review")
        print("4.View reviews")
        print("5.Sign Out")
        z = int(input("Choose An Option From Above:"))
        print("_________________________________________________________")
        print()
        if z == 1:
            fav_add()
        elif z == 2:
            print("1.Search By Ingredients")
            print("2.View All Recipes")
            g = int(input("Enter Your Option:"))
            print("_________________________________________________________")
            print()
            if g == 1:
                dish_search()
            elif g == 2:
                display_dish()
        elif z == 3:
            review()
        elif z == 4:
            cu = obj.cursor()
            cu.execute("select * from comment where name = %s", (c,))
            k = cu.fetchall()
            if k:
                t = ["Name", "stars", "user name", "comment"]
                tab = PrettyTable()
                tab.field_names = t
                for i in k:
                    tab.add_row(i)
                print(tab)
            else:
                print("**NO REVIEWS YET**")
            print()
            b = input("Would u like to  add it to favourites?(y/n)")
            print()
            if b == "y":
                fav_add()
        elif z == 5:
            print("                    **LOGGED OUT**")
            print("_________________________________________________________")
            print()
            flag = "red"
    return flag


def fav_add():
    x = user + ".txt"
    f = open(x, "r")
    s = f.readline()
    flg = "red"
    p = c + "\n"
    while s:
        if s.lower() == p.lower():
            flg = "green"
            print("**ALREADY IN FAVOURITES**")
            print("_________________________________________________________")
            print()
            f.close()
            break
        s = f.readline()
    if flg == "red":
        f = open(x, "a")
        k = c.lower()
        f.write(k + "\n")
    f.close()


def display_fav():
    print("======================= FAVOURITES =======================")
    flag = "green"
    x = user + ".txt"
    f2 = open(x, "r")
    f3 = open("nfav.txt", "w")
    s = f2.readlines()
    for i in s:
        f1 = open("dishes.csv", "r")
        r = csv.reader(f1)
        for j in r:
            if j[0].lower() + "\n" == i.lower():
                f3.write(j[0].title() + "\n")
        f1.close()
    f2.close()
    f3.close()
    os.remove(x)
    os.rename("nfav.txt", x)
    x = user + ".txt"
    f = open(x, "r")
    w = f.read()
    print(w)
    if w == "":
        print("**FAVOURITES EMPTY**")
        print()
    f.close()
    print("_________________________________________________________")
    print()
    print("1.Continue Searching")
    print("2.Remove From Fav")
    print("3.Choose From Fav To View Recipe")
    print("4.Sign Out")
    r = int(input("Choose An Option From Above:"))
    print("_________________________________________________________")
    print()
    if r == 1:
        print("1.Search By Ingredients")
        print("2.View All Recipes")
        g = int(input("Enter Your Option:"))
        print("_________________________________________________________")
        print()
        if g == 1:
            dish_search()
        elif g == 2:
            display_dish()
    elif r == 2:
        fav_delete()
    elif r == 3:
        fav_search()
    elif r == 4:
        print("                       **LOGGED OUT**")
        print("_________________________________________________________")
        print()
        flag = "red"
    return flag


def getpwd():
    root = tk.Tk()
    root.withdraw()
    password = simpledialog.askstring("Password", "Enter Your Password:", show='*')
    return password


def review():
    cu = obj.cursor()
    s = int(input("stars:"))
    com = input("comment:")
    q1 = "insert into comment VALUES(%s,%s,%s,%s)"
    cu.execute(q1, (c, s, user, com))
    obj.commit()
    cu.execute("select avg(stars) from comment where name= %s", (c,))
    a1 = cu.fetchone()
    cu.execute("select * from review where name= %s", (c,))
    a2 = cu.fetchone()
    count = a2[2] + 1
    p = a1[0]
    cu.execute("update review set avg_stars= %s, count=%s where name= %s", (p, count, c))
    obj.commit()
    cu.close()
    b = input("Would u like to  add it to favourites?(y/n)")
    print()
    if b == "y":
        fav_add()
