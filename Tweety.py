
import pandas as pd
import  tweepy
import string
import numpy as np
import matplotlib.pyplot as plt
import nltk
from bs4 import BeautifulSoup
import sys
import re
import streamlit as st
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#name of app
st.set_page_config(page_title='Tweety',
		       page_icon=':hatched_chick:')

#background image for the app

page_bg_img = '''
<style>
body {
background-image: url("https://www.setaswall.com/wp-content/uploads/2018/04/Gifts-Snowflakes-Ribbon-Bowknot-1440x2880.jpg");
background-size: cover;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

def percentage(part ,whole):
    return 100 * float(part)/float(whole)


sid = SentimentIntensityAnalyzer()

#function that would clean the data
@st.cache
def review_to_words( raw_review ):
    # Function to convert a raw review to a string of words
    # The input is a single string (a raw movie review), and 
    # the output is a single string (a preprocessed movie review)
    
    # 1. Remove HTML
    review_text = BeautifulSoup(raw_review,features="html.parser").get_text() 
    
    # 2. Remove non-letters        
    letters_only = re.sub("[^a-zA-Z]", " ", review_text) 
    
    #puncuation
    text  = "".join([char for char in  letters_only if char not in string.punctuation])
    
    
    # 3. Convert to lower case, split into individual words
    words = text.lower().split()                             
    
    # 4. In Python, searching a set is much faster than searching
    #   a list, so convert the stop words to a set
    stops = set(stopwords.words("english"))                  
    
    # 5. Remove stop words
    meaningful_words = [w for w in words if not w in stops]   
    
    # 6. Join the words back into one string separated by space, 
    # and return the result.
    return( " ".join(meaningful_words ))   


#left top details of app
st.sidebar.markdown('**ABOUT PROJECT :-**')
buffer1 = st.sidebar.checkbox('Made with\n')
if buffer1 ==1:
    st.sidebar.markdown('**Python** 3.6 version')
    st.sidebar.markdown('**Tweepy** Twitter API to fetch the data')
    st.sidebar.markdown('**Streamlit** this Magic ingredient here handles the Web part')
    st.sidebar.markdown('**AWS** Deployment on the Cloud')
    st.sidebar.markdown('**NLTK** Package that has some cool pre-trained model that allows us to Classify the input Text')


buffer2 = st.sidebar.checkbox('Source Code ')
if buffer2 == 1:
    st.sidebar.markdown('https://github.com/Shivampurbia')
                          


#title of our app
st.title('Tweety :hatched_chick:')
st.subheader('An interactive Web app to perform Sentiment Analysis on Tweets of any Hot topic, Product or Trend.')



#secret keys we need to access the API  
consumer_key = 'xWaBy4T6PoPMPwGcToE8UQHgM'
consumerkey_secret = 'ZEjIDz3MmCBw46dzsQyqMOAZiWNjvOWoKr08kjxtrr92i1s0fa'
access_token = '3226759777-W3ZjS4btcsY0Md0AzntXGwXzBT31o8l5wKvlDDG'
accesstoken_secret = 'IufUiSiN3u00wLYWkyXNDMxSLjbUDIyWX8LYNCsv5SEKG'
st.write(' ')
st.write(' ')

st.write('FOR DEMO')
user_input = st.text_input("Write any sentence to check its polarity (a metric to determine whether a piece of text is +ve or -ve)","EXAMPLE : this is my pet project and i love it.")

#cleansing and NLP  part
demo = review_to_words(user_input)
t = sid.polarity_scores(demo)
if st.button("Run Demo"):
    st.write("Neutral ,Positive and Negative value of text is :")
    st.write(t['neu']   ,t['pos'],t['neg'])
    if t['neu']>t['pos'] and t['neu'] > t['neg'] and t['neu']>0.85:
        st.markdown('Text is classified as **Neutral**. :confused::neutral_face:')
    elif t['pos'] > t['neg']:
        st.markdown('Text is classified as **Positive**. :smiley:')
        st.balloons()
    elif t['neg'] > t['pos']:
        st.markdown('Text is classified as **Negative**. :disappointed: ')
    else:
        st.markdown('Text is classified as **Neutral**. :confused::neutral_face:')

    st.write(' ')
    st.write(' ')
    



st.write(' ')
st.write(' ')
st.write(' ')
st.write(' ')
st.markdown('Enter the **#Hashtag** you want search and perform Analytics.')
hashtag  = st.text_input('Examples : trump, Blacklivesmatter, tesla etc')
if hashtag != '':
    st.write('Calling Tweeter API to fetch the DATA of #'+hashtag)

st.write(' ')
st.write(' ')

auth = tweepy.OAuthHandler(consumer_key , consumerkey_secret )
auth.set_access_token(access_token, accesstoken_secret)
api = tweepy.API(auth)

searchWord = hashtag

x = st.slider('Select the Number of Tweets',
    0, 1000)
noOfsearchWord = x

tweets = tweepy.Cursor(api.search , q = searchWord ).items(noOfsearchWord) 
    
if x is not 0:
    positive = 0
    negative = 0
    neutral = 0
    with st.spinner('Loading tweets....'):
        for tweet in tweets:
            if tweet.lang == "en":
                st.write(tweet.text)
                print('\n')
                tweet.text = review_to_words(tweet.text)
                temp = sid.polarity_scores(tweet.text)

                if temp['neu']>0.90 and temp['neu']>temp['pos'] and  temp['neu']>temp['neg']:
                    neutral += 1
                elif temp['pos'] > temp['neg']:
                    positive += 1
                else:
                    negative += 1
    st.success('Done!')
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write(' ')
    positive = percentage(positive , noOfsearchWord)
    neutral  = percentage(neutral ,  noOfsearchWord)
    negative = percentage(negative ,noOfsearchWord)  
	
    positive = format(positive , '.2f')
    neutral = format(neutral,'.2f')
    negative = format(negative , '.2f')
	
    #passing the pirchart in streamlit function as st.pyplot()
    labels = ['Positive ['+str(positive)+'%]' , 'Neutral ['+str(neutral)+'%]' , 'Negative['+str(negative)+'%]']
    sizes = [positive,neutral,negative]
    colors = ['yellowgreen','gold','red']
    patches, texts = plt.pie(sizes , colors =colors , startangle = 90)
    plt.legend(patches,labels, loc = "best")
    plt.title("This is how People are reacting on " + searchWord +" by analyzing " +str(noOfsearchWord)+" tweets" )
    plt.axis('equal')
    plt.tight_layout()
    st.pyplot(plt.show())

st.write(' ')
st.write(' ')
st.write(' ')
st.write(' ')
st.write(' ')
st.write(' ')
st.write(' ')
st.write(' ')
st.write(' ')
st.write(' ')
st.write(' ')
st.write(' ')
st.markdown('Made with :heart: by [Shivam](https://www.linkedin.com/in/shivam-purbia-b35a65166/?originalSubdomain=in)')
      
         

    
