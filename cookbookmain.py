import pickle
import functions as fun
import dishes


def main():
    clr = "x"
    while clr == "x":
        clr = "o"
        print()
        print("======================== WELCOME ========================")
        print()
        print("1.Admin")
        print("2.User")
        print("3.Exit")
        x = int(input("Enter An Option From Above: "))
        print("_________________________________________________________")
        print()
        if x == 1:
            print()
            print("=================== Admin Login Page ====================")
            print()
            p = fun.getpwd()
            if p == "sas":
                print("_________________________________________________________")
                print()
                print("                     **HELLO ADMIN**")
                while clr == "o":
                    print("_________________________________________________________")
                    print()
                    print("1.Add New Recipe")
                    print("2.Delete A Recipe")
                    print("3.View Ingredient Suggestions")
                    print("4.View All Dishes")
                    print("5.Log Out")
                    z = int(input("Enter An Option From Above:"))
                    print("_________________________________________________________")
                    print()
                    if z == 1:
                        dishes.dish_add()
                    elif z == 2:
                        dishes.dish_del()
                    elif z == 3:
                        dishes.ing_sugg()
                    elif z == 4:
                        dishes.adisplay_dishes()
                    elif z == 5:
                        print("                   **LOGGED OUT**")
                        print("_________________________________________________________")
                        clr = "x"
            else:
                print("you need the admin key for access")
        elif x == 2:
            print("1.Sign In")
            print("2.Sign Up")
            z = int(input("Enter An Option From Above: "))
            print()
            if z == 1:
                fun.signin()
            elif z == 2:
                print()
                print("==================== Create Account =====================")
                while True:
                    if fun.signup():
                        break
                print()
            while clr == "o":
                print("1.Check Favorites")
                print("2.Search Recipes")
                print("3.Sign Out")
                y = int(input("Enter An Option From Above:"))
                print("_________________________________________________________")
                print()
                if y == 1:
                    p = fun.display_fav()
                    clr = "o"
                    if p == "red":
                        clr = "x"
                elif y == 2:
                    clr = "o"
                    print("1.Search By Ingredients")
                    print("2.View All Recipes")
                    g = eval(input("Enter Your Option:"))
                    print("_________________________________________________________")
                    print()
                    if g == 1:
                        p = fun.dish_search()
                        if p == "red":
                            clr = "x"
                    elif g == 2:
                        p = fun.display_dish()
                        if p == "red":
                            clr = "x"
                elif y == 3:
                    print("                   **LOGGED OUT**")
                    print("________________________________________________________")
                    print()
                    clr = "x"
        elif x == 3:
            print("====================== EXITED =======================")
            break


main()
