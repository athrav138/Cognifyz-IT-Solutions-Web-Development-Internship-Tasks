while True:
    print("\n--- Select One ---")
    print("1. Right Angle Triangle")
    print("2. Pyramid")
    print("3. Inverted Right Angle Triangle")
    print("4. Square")
    print("5. Reverse Pyramid")
    print("6. Exit")

    choice = int(input("Enter a choice (1-6): "))

    if choice == 6:
        print("Exiting Program...")
        break

    n = int(input("Enter a number: "))

    if choice == 1:
        print("\nRight Angle Triangle:")
        for i in range(1, n + 1):
            for j in range(1, i + 1):
                print(j, end=" ")
            print()

    elif choice == 2:
        print("\nPyramid:")
        for i in range(1, n + 1):
            print(" " * (n - i), end="")
            for j in range(1, i + 1):
                print(j, end=" ")
            print()

    elif choice == 3:
        print("\nInverted Right Angle Triangle:")
        for i in range(n, 0, -1):
            for j in range(1, i + 1):
                print(j, end=" ")
            print()

    elif choice == 4:
        print("\nSquare:")
        for i in range(n):
            for j in range(1, n + 1):
                print(j, end=" ")
            print()

    elif choice == 5:
        print("\nReverse Pyramid:")
        for i in range(n, 0, -1):
            print(" " * (n - i), end="")
            for j in range(1, i + 1):
                print(j, end=" ")
            print()

    else:
        print("Invalid Choice! Please select between 1 and 6.")