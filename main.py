# Susan Harrison - 000854062
# C950 OA
from os import system, name
from datetime import timedelta
from package_delivery_system import PackageDelivery


# writing in a clear function capability to clean up some clutter while in the program
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


# running the package delivery piece that will provide information for the next set of blocks
(total_distance, packages_hash, packages) = PackageDelivery.run()

# clearing the screen to get rid of the initial run main.py command
clear()

# flavor text for program opening, as well as options
print('Welcome to the Package Delivery System Console')
print('Packages have been delivered!  All packages were delivered in {} miles'.format(total_distance))

while True:
    print()
    command = input("""\
    WGUPS Menu:
    1.  Look up an individual package ID
    2.  View delivery status of all packages for a specific time
    3.  Display the total distance of all trucks traveled
    4.  Clear screen
    5.  Exit program
    Please enter a number to continue: 
    """)

    if command == '1':
        package_id = input('Please enter a package ID: ')

        # lookup the package ID from the hash table -> O(n) complexity
        package = packages_hash.find(int(package_id))

        time_string = input('Please enter a timestamp in HH:MM:SS format: ')
        (hour, minute, sec) = time_string.split(':')
        timestamp = timedelta(hours=int(hour), minutes=int(minute), seconds=int(sec))

        print(package.report(timestamp))

    elif command == '2':
        time_string = input('Please enter a timestamp in HH:MM:SS format: ')
        (hour, minute, sec) = time_string.split(':')
        timestamp = timedelta(hours=int(hour), minutes=int(minute), seconds=int(sec))

        # looping through all packages to display their status
        for package in packages:
            print(package.inline_report(timestamp))

    # printing the total distance of the trucks traveled
    elif command == '3':
        print('The total distance the trucks have traveled is: {} miles'.format(total_distance))

    elif command == '4':
        clear()
        print('Screen cleared!')
    elif command == '5':
        print('Exiting program, have a nice day!')
        exit()
    else:
        print('Invalid command.  Please check your input and try again')
