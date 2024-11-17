from main.models import Site, Link, ImagineOrder, Image, Permissions, Package
from django.core.management.base import BaseCommand, CommandError
import requests
from urllib.parse import urlparse
from django.core.files.base import ContentFile
from shopbot.settings import ROOT
from openai import OpenAI
from django.contrib.auth.models import User
from openai import OpenAI
import pandas as pd
import tiktoken
from openai import OpenAI
import numpy as np
import os
os.environ['OPENAI_API_KEY'] = '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'

gpt_client = OpenAI(api_key= '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')

client = OpenAI(api_key= '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')

def remove_newlines(serie):
    
    return serie

max_tokens = 500
tokenizer = tiktoken.get_encoding("cl100k_base")
# Function to split the text into chunks of a maximum number of tokens
def split_into_many(text, max_tokens = max_tokens):

    # Split the text into sentences
    sentences = text.split('. ')

    # Get the number of tokens for each sentence
    n_tokens = [len(tokenizer.encode(" " + sentence)) for sentence in sentences]

    chunks = []
    tokens_so_far = 0
    chunk = []

    # Loop through the sentences and tokens joined together in a tuple
    for sentence, token in zip(sentences, n_tokens):

        # If the number of tokens so far plus the number of tokens in the current sentence is greater
        # than the max number of tokens, then add the chunk to the list of chunks and reset
        # the chunk and tokens so far
        if tokens_so_far + token > max_tokens:
            chunks.append(". ".join(chunk) + ".")
            chunk = []
            tokens_so_far = 0

        # If the number of tokens in the current sentence is greater than the max number of
        # tokens, go to the next sentence
        if token > max_tokens:
            continue

        # Otherwise, add the sentence to the chunk and add the number of tokens to the total
        chunk.append(sentence)
        tokens_so_far += token + 1

    return chunks


class Command(BaseCommand):

    def handle(self, *args, **options):
        

        # Create a list to store the text files
        texts=[]

        # Get all the text files in the text directory
        for file in os.listdir("/midjourney-back/media/brocker"):

            # Open the file and read the text
            with open("/midjourney-back/media/brocker/" + file, "r", encoding="UTF-8") as f:
                text = f.read()

                # Omit the first 11 lines and the last 4 lines, then replace -, _, and #update with spaces.
                texts.append((file[11:-4].replace('-',' ').replace('_', ' ').replace('#update',''), text))

        # Create a dataframe from the list of texts
        df = pd.DataFrame(texts, columns = ['fname', 'text'])

        # Set the text column to be the raw text with the newlines removed
        df['text'] = df.fname + ". " + remove_newlines(df.text)
        df.to_csv('/midjourney-back/media/brockerdone/scraped.csv')
        df.head()

        shortened = []




        df.to_csv('/midjourney-back/media/brockerdone/embeddings.csv')
        df.head()

        df = pd.read_csv('/midjourney-back/media/brockerdone/scraped.csv', index_col=0)
        df.columns = ['title', 'text']

        # Tokenize the text and save the number of tokens to a new column
        df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))

        # Visualize the distribution of the number of tokens per row using a histogram
        df.n_tokens.hist()

        shortened = []

        # Loop through the dataframe
        for row in df.iterrows():

            # If the text is None, go to the next row
            if row[1]['text'] is None:
                continue

            # If the number of tokens is greater than the max number of tokens, split the text into chunks
            if row[1]['n_tokens'] > max_tokens:
                shortened += split_into_many(row[1]['text'])

            # Otherwise, add the text to the list of shortened texts
            else:
                shortened.append( row[1]['text'] )

        df = pd.DataFrame(shortened, columns = ['text'])
        df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))
        df.n_tokens.hist()

        

        df['embeddings'] = df.text.apply(lambda x: client.embeddings.create(input=x, model='text-embedding-ada-002').data[0].embedding)

        df.to_csv('/midjourney-back/media/brockerdone/embeddings.csv')
        df.head()