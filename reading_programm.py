def opening():
    f = open("C:\\Users\\ernes\\Documents\\Code\\IntIdea codes\\1st-project\\Chat.txt", mode="r")
    while True:
        line = f.readline()
        if line != "":
            print(line, end="")

    f.close()

def main():
    opening()


if __name__ == '__main__':
    main()