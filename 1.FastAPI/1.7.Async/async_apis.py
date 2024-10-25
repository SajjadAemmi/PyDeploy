import time
import requests


def rhyme_finder(word):
    url = f"https://rhyming.ir/api/rhyme-finder?api=73616a6a616461656d6d6940676d61696c2e636f6d&w={word}&sb=1&mfe=2&eq=1"
    response = requests.request("GET", url)
    return response.json()


def get_states():
    url = "https://iran-locations-api.vercel.app/api/v1/fa/states"
    response = requests.request("GET", url)
    return response.json()


def get_cities(state_id):
    url = f"https://iran-locations-api.vercel.app/api/v1/fa/cities?state_id={state_id}"
    response = requests.request("GET", url)
    return response.json()


def get_coordinates():
    states = get_states()
    for state in states:
        if state["name"] == "خراسان رضوی":
            response = get_cities(state["id"])
            cities = response["cities"]
            for city in cities:
                if city["name"] == "طرقبه":
                    latitude = city["latitude"]
                    longitude = city["longitude"]
                    break
            else:
                print("شهری به نام طرقبه پیدا نشد")
                latitude = None
                longitude = None
            break
    else:
        print("استانی با نام خراسان رضوی پیدا نشد")
        latitude = None
        longitude = None

    return latitude, longitude


def main():
    rhymes = rhyme_finder("جان")
    latitude, longitude = get_coordinates()
    print(rhymes)
    print(latitude, longitude)


if __name__ == "__main__":
    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    print(f"Executed in {elapsed:0.2f} seconds.")
