
from database import initialize_database
from vulnerable_app import vulnerable_application


def main():

    initialize_database()

    vulnerable_application()


if __name__ == "__main__":
    main()
