from requests import get

def main():
    print(get("https://shouldideploy.today/api").json().get("message"))

if __name__ == "__main__":
    main()
