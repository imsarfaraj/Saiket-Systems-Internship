import requests

class CurrencyConverter:

    def __init__(self):
        self.amt = None
        self.baseCurrency = None
        self.targetCurrency = None
        self.rates = None

    def getUserInput(self):
        # amount
        while True:
            try:
                self.amt = float(input("Enter amount: "))
                if self.amt <= 0:
                    print("Amount must be positive")
                    continue
                break
            except ValueError:
                print("Invalid amount, Please enter valid Amount")

        # base currency
        while True:
            self.baseCurrency = input("Enter base currency (3 letters): ").upper()
            if len(self.baseCurrency) == 3 and self.baseCurrency.isalpha():
                break

            print("Please enter 3-letter currency code (e.g. USD, EUR, INR)")

        # target currency
        while True:
            self.targetCurrency = input("Enter currency name which you want to convert: ").upper()
            if len(self.targetCurrency) == 3 and self.targetCurrency.isalpha():
                break

            print("Please enter 3-letter currency code (e.g. USD)")



    def callingAPI(self):
        try:

            self.url = f"https://api.exchangerate-api.com/v4/latest/{self.baseCurrency}"
            self.response = requests.get(self.url, timeout=5)
            self.response.raise_for_status()
            self.data = self.response.json()

            if "rates" not in self.data:
                print("Invalid base currency!")
                self.rates = None
                return False

            self.rates = self.data["rates"]
            return True


        except requests.exceptions.RequestException:
            print('API connection failed, Check Connection')
            return False

        except Exception as e:
            print(f"Some error occurred: {e}")
            return False

    def convertCurrency(self):
        try:
            success = self.callingAPI()

            if not success or self.rates is None:
                print("Can not convert without valid rates.")
                return

            if self.targetCurrency in self.rates:
                rate = self.rates[self.targetCurrency]
                finalamt = self.amt * rate
                print(f"final amount is: {finalamt:.2f}")

            else:
                print("Invalid target currency!")

        except KeyError:
            print("Currency is not found")

        except ValueError:
            print("Invalid amount Entered")

        except Exception as e:
            print(f"Some error occurred: {e}")


def main():

    c = CurrencyConverter()
    c.getUserInput()
    c.convertCurrency()

if __name__ == "__main__":
    main()

