from openai import OpenAI
import requests
import os
from dotenv import load_dotenv

load_dotenv()




def create_summaries(ticker):

    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    data = get_earnings_call_transcript(ticker)

    text = data['content'][:40000]

    performance_prompt_path = './prompts/performance_prompt.txt'
    outlook_prompt_path = './prompts/outlook_prompt.txt'
    risk_prompt_path = './prompts/risk_prompt.txt'

    performance_summary = summarize_text(text, performance_prompt_path, client)
    print('Performance summary complete')
    
    outlook_summary = summarize_text(text, outlook_prompt_path, client)
    print('Outlook summary complete')
    
    risk_summary = summarize_text(text, risk_prompt_path, client)
    print('Risk summary complete')

    output_data = {'symbol': data['symbol'], 'quarter': data['quarter'], 'year': data['year'], 
                   'performance': performance_summary, 'outlook': outlook_summary, 'risk': risk_summary}
    

    return output_data



def summarize_text(text, prompt_file_path, client):

    prompt = open(prompt_file_path, 'r').read() % (text)
    
    response = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {
          "role": "system",
          "content": "You are a helpful assistant and expert financial and investment analyst."
        },
        {
          "role": "user",
          "content": prompt
        }
      ],
      temperature=1,
      max_tokens=3006,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    
    return response.choices[0].message.content




def get_earnings_call_transcript(ticker):
    fmp_api_key = os.getenv('FMP_API_KEY')

    url = f'https://fmpcloud.io/api/v3/earning_call_transcript/{ticker}?apikey={fmp_api_key}'
    response = requests.get(url)
    data = response.json()[0]

    return data