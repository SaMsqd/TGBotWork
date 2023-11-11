import flag
import gettext
import pycountry


rus = gettext.translation("iso3166", pycountry.LOCALES_DIR, languages=["ru"])
rus.install()


def get_country(code):
    try:
        ru = pycountry.countries.get(alpha_2=flag.dflagize(code)[1:3])
        return ru.name
    except AttributeError as AE:
        print(code)
        with open("none_flags.txt", mode="w") as f:
            f.write(code)
        return "None flag"


if __name__ == "__main__":
    print(get_country(flag.dflagize("🇧🇷")))
