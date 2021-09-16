from bs4 import BeautifulSoup
from NLP.question_generation.pipelines import pipeline

def textpreperation_qag(text, source_type):
    if source_type == "literature":
        text_soup = BeautifulSoup(text, "html.parser")
        text_soup = text_soup.get_text()
        print(f"TRYING TEXT LENGTH OF: {len(text_soup)}")

    return text_soup

@app.task(bind=True)
def getqag(clean_text):
    QAG_NLP  = pipeline("question-generation", model="valhalla/t5-small-qg-prepend", qg_format="prepend")
    qas = QAG_NLP(clean_text)
    return qas
