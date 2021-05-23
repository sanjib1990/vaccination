from random import choice

user_agent_strings = {
    "Samsung Galaxy S9": ("Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW)"
                          "AppleWebKit/537.36 (KHTML, like Gecko)"
                          "Chrome/62.0.3202.84 Mobile Safari/537.36"),
    "firefox": ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0)"
                "Gecko/20190101 Firefox/77.0"),
    "chrome": ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
               "Chrome/90.0.4430.212 Safari/537.36"),
    "safari": ("Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-US)"
               "AppleWebKit/530.9 (KHTML, like Gecko) Chrome/ Safari/530.9")
}


def random_user_agent() -> str:
    return choice(tuple(user_agent_strings.values()))
