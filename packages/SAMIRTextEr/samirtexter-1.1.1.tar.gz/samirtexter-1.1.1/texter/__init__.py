"""
Ein Modul zur Verbesserung von Rechtschriebfehlern in Deutsch.
"""
    
def kontrolliere_Nomen(Nomen, return_bei_ja="Ja, das ist ein Nomen.", return_bei_nein="Nein, das ist kein Nomen."):
    """eine Funktion die Nomen korrigiert.
    param: Nomen = Das Nomen dass korrigiert soll.
    param: return_bei_ja = falls es das Nomen gibt, wird return_bei_ja returniert.
    param: return_bei_nein = das gleiche wie bei return_bei_ja, einfach wenn das Nomen falsch ist.
    """
    with open("Haeufige_Nomen.txt", "r", encoding="utf-8") as file:
        nomen_liste = file.read().splitlines() 
    Nomen_korigiert = Nomen.capitalize()
    if Nomen in nomen_liste or Nomen_korrigiert in nomen_liste:
        return return_bei_ja
    else:
        return return_bei_nein

        
def kontrolliere_Wort(Wort, return_bei_ja="Ja, das Wort gibt es.", return_bei_nein="Nein, das Wort gibt es nicht."):
    """eine Funktion die Wörter korrigiert.
    param:  = Das Wort dass korrigiert soll.
    param: return_bei_ja = falls es das Wort gibt, wird return_bei_ja returniert.
    param: return_bei_nein = das gleiche wie bei return_bei_ja, einfach wenn das Wort falsch ist.
    """
    with open("woerter.txt", "r", encoding="utf-8") as file:
        woerter_liste = file.read()
        woerter_liste = woerter_liste.split(",")
       
    Wort_korigiert = Wort.capitalize()
    if Wort in woerter_liste or Wort_korrigiert in woerter_liste:
        return return_bei_ja
    else:
        return return_bei_nein

ausnahmen = [
    "alt", "neu", "krank", "dunkel", "hell", "schwach", "stark", "kurz", 
    "lang", "warm", "kalt", "schnell", "langsam", "klug", "weich", "hart", 
    "schön", "hoch", "tief", "breit", "eng", "sauer", "süß", "sauber", 
    "teuer", "billig", "freundlich", "fleißig", "faul", "gesund", "falsch", 
    "rund", "scharf", "klang", "frisch", "sicher", "klar", "müde", "glücklich", 
    "langweilig", "lebendig", "schlank", "träumend", "nah", "menschlich", 
    "günstig", "streng", "weich", "groß", "klein", "traurig", "lebendig", 
    "dumm", "weise", "wütend", "schüchtern", "stumm", "flach", "steif", 
    "schüchtern", "vornehm", "heiter", "verlegen", "entspannt", "unglücklich", 
    "gut", "böse", "süß", "selbstbewusst", "verliebt", "bescheiden", "emotional", 
    "sicher", "zufrieden", "anspruchsvoll", "selbstsicher", "harmlos", "natürlich", 
    "einfach", "klar", "dick", "abenteuerlustig", "cool", "menschlich", "gutmütig", 
    "musikalisch", "freundlich", "verspielt", "spannend", "ruhig", "sportlich", 
    "intelligent", "froh", "kreativ", "jovial", "hellwach", "verrückt", "zäh", 
    "klug", "lieb", "lebendig", "hübsch", "blond", "brav", "unterhaltsam", 
    "übertrieben", "unterstützend", "fröhlich", "lästig", "genial", "reizend", 
    "wunderbar", "imposant", "engagiert", "unterhaltsam", "mutig", "charmant", 
    "ausdauernd", "lebenslustig", "tüchtig", "verbindlich", "aufgeschlossen", 
    "toll", "fröhlich", "entspannt", "entschlossen", "dankbar", "gutmütig"
]

def return_Steigerung(Adjektiv, return_):
    if return_ == "Komparativ":
        if Adjektiv in ausnahmen:
            return Adjektiv + "er"
        elif "a" in Adjektiv:
                return Adjektiv.replace("a", "ä") + "er"
        elif "o" in Adjektiv:
            return Adjektiv.replace("o", "ö") + "er"
        elif "u" in Adjektiv:
            return Adjektiv.replace("u", "ü") + "er"
        else:
            return Adjektiv + "er"
    else:
        if Adjektiv in ausnahmen:
            return "am " + Adjektiv + "sten"
        if "a" in Adjektiv:
            return "am " + Adjektiv.replace("a", "ä") + "sten"
        elif "o" in Adjektiv:
                return "am " + Adjektiv.replace("o", "ö") + "sten"
        elif "u" in Adjektiv:
            return "am " + Adjektiv.replace("u", "ü") + "sten"
        else:
            return "am " + Adjektiv + "sten"