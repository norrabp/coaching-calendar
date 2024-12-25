from client import FlaskAPIClient


def main():
    client = FlaskAPIClient()
    client.login("root@root.com", "rootroot")
    client.register("Nick Saban", "nicksaban@gmail.com", "bad_pass", "1234567890", "COACH")
    client.register("Jim Harbaugh", "jimharbaugh@gmail.com", "bad_pass", "1234567890", "COACH")
    client.register("Pete Carroll", "petecarroll@gmail.com", "bad_pass", "1234567890", "COACH")
    client.register("JJ McCarthy", "jjmccarthy@gmail.com", "bad_pass", "1234567890", "STUDENT")
    client.register("Blake Corum", "blakecorum@gmail.com", "bad_pass", "1234567890", "STUDENT")
    client.register("Mike Sainristil", "mikesainristil@gmail.com", "bad_pass", "1234567890", "STUDENT")
    client.register("Tua Tagovailoa", "tua@gmail.com", "bad_pass", "1234567890", "STUDENT")
    client.register("Derrick Henry", "dhenry@gmail.com", "bad_pass", "1234567890", "STUDENT")
    client.register("Reggie Bush", "reggiebush@gmail.com", "bad_pass", "1234567890", "STUDENT")
    client.register("Matt Leinart", "mattleinart@gmail.com", "bad_pass", "1234567890", "STUDENT")


if __name__ == "__main__":
    main()
