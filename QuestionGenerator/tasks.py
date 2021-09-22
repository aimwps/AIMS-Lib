from bs4 import BeautifulSoup
from NLP.question_generation.pipelines import pipeline
from celery import shared_task
from .models import GeneratedQuestionBank
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

def textpreperation_qag(text, source_type):
    payloads = []
    if source_type == "literature":
        text_soup = BeautifulSoup(text, "html.parser")
        text_soup = text_soup.get_text()
        while len(text_soup) >= 512:
            temp = text_soup[512:]
            for i, c in enumerate(temp):
                if c == ".":
                    payload = text_soup[:512+i+1]
                    payloads.append(payload.strip())
                    text_soup = text_soup[512+i+1:].strip()
                    break
        payloads.append(text_soup)
    return payloads

@shared_task
def getqag(clean_text, source_type, source_id, user_id):
    print(f"SOURCETYPE: {source_type} | SOURCE_ID: {source_id} | USER_ID: {user_id}")
    QAG_NLP  = pipeline("question-generation", model="valhalla/t5-small-qg-prepend", qg_format="prepend")
    qas = QAG_NLP(clean_text)
    user = get_object_or_404(User, id=user_id)
    for q,a in qas.items():
        q_clean = "".join(q.strip())
        a_clean = "".join(a.replace("<pad>", "").strip())
        new_gq = GeneratedQuestionBank(
            generated_by = user,
            source_type = source_type,
            source_id = int(source_id),
            question = q_clean,
            answer = a_clean,
            user_proof = "unknown")
        new_gq.save()

    return "SUCCESS"


@shared_task(name="sum_two_numbers")
def add(x, y):
    return x + y
