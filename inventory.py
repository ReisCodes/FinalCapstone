# Import tabulate module
from tabulate import tabulate


# ========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return int(self.cost)

    def get_quantity(self):
        return int(self.quantity)

    def __str__(self):
        return f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}"


# =============Shoe list===========

# The list will be used to store a list of objects of shoes.
shoe_list = []


# ==========Functions outside the class==============
def read_shoes_data():
    """
    This function will open the file inventory.txt
    and read the data from this file, then create a shoes object with this data
    and append this object into the shoes list. One line in this file represents
    data to create one object of shoes.
    """

    file = None
    while True:
        try:
            with open("inventory.txt", "r") as file:
                all_shoes = file.readlines()
                for i in range(1, len(all_shoes)):
                    shoe_info = all_shoes[i].strip().split(",")  # This separates the information of each line
                    while len(shoe_info) == 5:  # This checks the number of info is correct
                        try:
                            shoe_into_class = Shoe(shoe_info[0], shoe_info[1], shoe_info[2], shoe_info[3], shoe_info[4])
                            # creating a shoe class instance and appending it to the list
                            shoe_list.append(shoe_into_class)
                            break
                        except ValueError:   # If the length is not 5 the program will print an error message
                            print("This file line must be corrupt.")
                break
        except FileNotFoundError as error:   # If the file that we are trying to read doesn't exist will print error
            print("\nThe file you are trying to open does not exist.")
            print(error)
        finally:     # If the file isn't empty this will close the file
            if file is not None:
                file.close()


def capture_shoes():
    """
       This function will allow a user to capture data
       about a shoe and use this data to create a shoe object
       and append this object inside the shoe list.
    """
    # Collect info from user to implement into a new Shoe instance
    new_shoe_country = input("\nWhere are the shoes made? ")
    new_shoe_code = input("What is the shoe code? ")
    new_shoe_product = input("What is the shoe called? ")
    new_shoe_cost = int(input("How much does the shoe cost? "))
    new_shoe_quantity = int(input("How many pairs do you have? "))
    # Create the new instance
    new_shoe = Shoe(new_shoe_country, new_shoe_code, new_shoe_product, new_shoe_cost, new_shoe_quantity)
    shoe_list.append(new_shoe)  # append this instance to the list
    with open("inventory.txt", "a") as update_file:      # adding this new shoe to the inventory.txt file
        update_file.write(f"\n{new_shoe.__str__()}")
    update_file.close()
    print(f"\nThe {new_shoe_product} has been added to the inventory.")


def view_all():
    """
    This function will iterate over the shoes list and
    print the details of the shoes
    """
    table = []    # create an empty table to append list of lists to use tabulate module
    for i in range(len(shoe_list)):   # Iterate through each element in list of shoes
        table_element = [shoe_list[i].country, shoe_list[i].code, shoe_list[i].product, shoe_list[i].cost,
                         shoe_list[i].quantity]    # Make a list of the different info for each shoe
        table.append(table_element)       # append the list to have list of lists
    headers = ["Country", "Code", "Product", "Cost", "Quantity"]   # Create headers for the table
    print(tabulate(table, headers, tablefmt="psql"))     # Create the table in an easy-to-read manner


def re_stock():
    """
    This function will find the shoe object with the lowest quantity,
    which is the shoes that need to be re-stocked. Ask the user if they
    want to add this quantity of shoes and then update it.
    """
    quantity_list = []     # create an empty list to store the quantity of each shoe
    for i in range(0, len(shoe_list)):   # Iterate through the list of shoes and use .get_quantity and append to list
        shoe_quantity = shoe_list[i].get_quantity()
        quantity_list.append(shoe_quantity)
    lowest_quantity_shoe_index = quantity_list.index(min(quantity_list))   # Find the index in the list of the lowest
    print(f"The shoe with the lowest quantity is the {shoe_list[lowest_quantity_shoe_index].product} with only"
          f" {shoe_list[lowest_quantity_shoe_index].get_quantity()} pairs in stock.")
    # This gives the user the option to either add stock or not
    while True:
        re_stock_option = input("\nWould you like to stock more of this shoe? (yes or no) \n: ").lower()
        if re_stock_option == "yes":
            while True:
                # If they choose to add stock this will add the added pairs to the old number and print to user
                try:
                    re_stock_quantity = int(input("\nHow many pairs would you like to add to the stock? "))
                    shoe_list[lowest_quantity_shoe_index].quantity = \
                        shoe_list[lowest_quantity_shoe_index].get_quantity() + re_stock_quantity
                    print(f"\nYou now have {shoe_list[lowest_quantity_shoe_index].get_quantity()} pairs of the "
                          f"{shoe_list[lowest_quantity_shoe_index].product} in stock.")
                    # This re-writes the file to append the new quantity of the updated shoe and restores the rest
                    with open("inventory.txt", "w") as update_file:
                        update_file.write("Country,Code,Product,Cost,Quantity")

                    with open("inventory.txt", "a+") as update_file:
                        for shoe in shoe_list:
                            update_file.write(f"\n{shoe.__str__()}")
                    update_file.close()
                    break
                except ValueError:   # If the user does not enter a valid number receive an error
                    print("\nOops! That was not a valid number, try again!")
            break
        elif re_stock_option == "no":    # loop breaks if they choose not to add stock
            break
        else:   # loops again if they don't put a valid option
            print("Sorry, this is not a valid option. Try again.\n"


def search_shoe():
    """
     This function will search for a shoe from the list
     using the shoe code and return this object so that it will be printed.
    """
    while True:
        shoe_code_to_search = input("\nWhat shoe would you like to search for, enter code here: ")
        shoe_list_codes = []  # Create an empty list to store shoe codes
        for shoes in shoe_list:   # iterate through list of shoes to add all the codes to the empty list
            shoe_list_codes.append(shoes.code)
        if shoe_code_to_search not in shoe_list_codes:  # if the code they search for is not in list get error (re-loop)
            print("This code does not exist.\n")
            continue
        else:
            for shoe in shoe_list:   # if code is in list will iterate through shoe list to find a match
                if shoe_code_to_search == shoe.code:
                    print(f"\n{shoe}")   # once it finds the match will print the shoe info to the screen
        break


def value_per_item():
    """
    This function will calculate the total value for each item.
    value = cost * quantity.
    Then prints this information on the console for all the shoes.
    """
    value_list = []   # Create an empty list to store the values of the shoes
    for shoe in shoe_list:   # Iterates through list of shoes creates a value for each shoe
        value = int(shoe.quantity) * int(shoe.cost)
        value_and_name = [shoe.product, value]   # create a list of the product name and its value just calculated
        value_list.append(value_and_name)    # This list is appended to the empty list to create a list of lists

    headers = ["Product", "Value(ZAR)"]     # use tabulate to print out the info for each shoe in an easy-to-read manner
    print(tabulate(value_list, headers, tablefmt="psql"))


def highest_qty():
    """
    This function determines the product with the highest quantity and
    prints a prompt suggesting to put this shoe as being for sale.
    """
    quantity_list = []   # create an empty list to store shoe quantity's
    for i in range(0, len(shoe_list)):   # iterate through the list of shoes gather the quantity and append list
        shoe_quantity = shoe_list[i].get_quantity()
        quantity_list.append(shoe_quantity)
    highest_quantity_shoe_index = quantity_list.index(max(quantity_list))  # locate index of the highest quantity
    # Display relevant message to user to put this shoe on a sale.
    print(f"\nThe shoe with the highest quantity is the {shoe_list[highest_quantity_shoe_index].product}, you have"
          f" {shoe_list[highest_quantity_shoe_index].get_quantity()} pairs in stock. You should put this shoe on sale.")


# ==========Main Menu=============
def main():
    """
    This main function iterates through a menu giving the user different options
    to perform some of the above functions.
    """
    read_shoes_data()    # call on the read_shoes_function to create a list of shoes
    while True:
        user_choice = input('''\nPlease Select one of the following options:  
                      c  - Capture Shoes
                      va - View all Shoes
                      re - Restock Shoes
                      s  - Search Shoe
                      v  - View Shoe Values
                      hq - Highest Quantity Shoe
                      e  - Exit
                      : ''').lower()

        # Dependent of the users choice the function will call on the relevant function to perform the task
        if user_choice == "c":
            capture_shoes()

        elif user_choice == "va":
            view_all()

        elif user_choice == "re":
            re_stock()

        elif user_choice == "s":
            search_shoe()

        elif user_choice == "v":
            value_per_item()

        elif user_choice == "hq":
            highest_qty()

        # If the user chooses option 'e' it will exit the program and print a goodbye message.
        elif user_choice == "e":
            print("See you later.")
            exit()

        # If the user does not enter a valid option the program will display an error message and loop back to the menu
        else:
            print("\nPlease enter a valid option.\n")


main()
