import json
from difflib import get_close_matches


def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data


def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)
        
        
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["perguntas"]:
        if q["pergunta"] == question:
            return q["resposta"]
        
        
def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')
    
    while True:
        user_input: str = input('Voce: ')
        
        if user_input.lower() == 'sair':
            break
        
        best_match: str | None = find_best_match(user_input, [q["pergunta"]for q in knowledge_base["perguntas"]])
        
        if best_match:
             answer: str = get_answer_for_question(best_match, knowledge_base)
             print(f'Bot: {answer}')
        else:
            print('Bot: Eu não sei a resposta. Você pode me ensinar?')
            new_answer: str = input('Digite a resposta ou digite "pular" para pular: ')
            
            if new_answer.lower() != 'pular':
                knowledge_base["perguntas"].append({"pergunta": user_input,"resposta":new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('Bot: Obrigado! Eu aprendi uma nova resposta!')
                
                
if __name__ == '__main__':
    chat_bot()