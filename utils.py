from NLP.question_generation.pipelines import pipeline


def getqag(clean_text):
    QAG_NLP  = pipeline("question-generation", model="valhalla/t5-small-qg-prepend", qg_format="prepend")
    qas = QAG_NLP(clean_text)
    return qas
