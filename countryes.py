import flag
import gettext
import pycountry


rus = gettext.translation("iso3166", pycountry.LOCALES_DIR, languages=["ru"])
rus.install()


def get_country(code):
    ru = pycountry.countries.get(alpha_2=flag.dflagize(code)[1:3])
    return ru.name


if __name__ == "__main__":
    print(get_country(flag.dflagize("🇧🇷")))
