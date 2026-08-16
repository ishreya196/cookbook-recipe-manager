import mysql.connector
import csv
import pickle
import os
import functions
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

obj = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME)


def dish_add():
    c = obj.cursor()
    f1 = open("dishes.csv", "a", newline="")
    f2 = open("recipes.dat", "ab")
    w = csv.writer(f1)
    n = eval(input("No. Of Dishes To Add: "))
    for i in range(n):
        dish = input("Dish Name: ")
        ing = list(eval(input("Ingredients: ")))
        for k in ing:
            f3 = open("suggestions.txt", "r")
            f4 = open("suggestions1.txt", "w")
            r = f3.readline()
            while r:
                if k.lower() + "\n" != r.lower():
                    f4.write(r)
                r = f3.readline()
            f3.close()
            f4.close()
            os.remove("suggestions.txt")
            os.rename("suggestions1.txt", "suggestions.txt")
        l = [dish, ing]
        w.writerow(l)
        d = {}
        d["name"] = dish
        k = int(input("Enter No. Of Steps"))
        print()
        for j in range(k):
            d[j + 1] = input("Enter Step:")
            print()
        pickle.dump(d, f2)
        c.execute("insert into review(name) values('{}')".format(dish))
        obj.commit()
        print()
    c.close()
    f1.close()
    f2.close()


def dish_del():
    c = obj.cursor()
    f1 = open("dishes.csv", "r", newline="")
    x = input("Enter Name Of Dish To Delete:")
    x = x.lower()
    r = csv.reader(f1)
    flag = "green"
    for i in r:
        if i[0].lower() == x:
            flag = "red"
    f1.close()
    if flag == "red":
        f1 = open("dishes.csv", "r", newline="")
        f2 = open("recipes.dat", "rb")
        f3 = open("ndishes.csv", "w", newline="")
        f4 = open("nrecipes.dat", "wb")
        r = csv.reader(f1)
        w = csv.writer(f3)
        for i in r:
            if i[0].lower() != x:
                w.writerow(i)
        try:
            while True:
                l = pickle.load(f2)
                if x == l["name"].lower():
                    continue
                else:
                    pickle.dump(l, f4)
        except EOFError:
            f1.close()
            f2.close()
            f3.close()
            f4.close()
        os.remove("dishes.csv")
        os.rename("ndishes.csv", "dishes.csv")
        os.remove("recipes.dat")
        os.rename("nrecipes.dat", "recipes.dat")
        c.execute("delete from review where name= %s", (x.title(),))
        c.execute("delete from comment where name= %s", (x.title(),))
        obj.commit()
    else:
        print("**NAME NOT FOUND**")
        f1.close()
    c.close()


def ing_sugg():
    f = open("suggestions.txt", "r")
    print("================ INGREDIENT SUGGESTIONS ================")
    s = f.read()
    print(s.title())


def adisplay_dishes():
    f = open("dishes.csv", "r", newline="\n")
    r = csv.reader(f)
    t = 1
    for i in r:
        print(">", i[0].title())
    print("_________________________________________________")
    print()
    f.close()
