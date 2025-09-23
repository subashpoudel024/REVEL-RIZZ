def prompt(user_query: str = None) -> str:
    base_prompt = '''
    Analyze the person in this image and evaluate their overall appearance, style, and presentation. 
    Provide constructive suggestions to enhance their looks, grooming, and fashion. 
    Focus on actionable, practical, and personalized recommendations. 
    Do not add unrelated details or opinions. 
    Return concise, clear advice only shortly in 40 words only.
    '''
    
    if user_query:
        return base_prompt + f'\nAlso, take into account the user’s request: "{user_query}".'
    else:
        return base_prompt

