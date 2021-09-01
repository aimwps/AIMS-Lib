from bs4 import BeautifulSoup
def textpreperation_qag(text, source_type):
    if source_type == "literature":
        text_soup = BeautifulSoup(text, "html.parser")
        text_soup = text_soup.get_text()
        print(f"TRYING TEXT LENGTH OF: {len(text_soup)}")

    return text_soup
