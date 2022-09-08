import nltk
from nltk import word_tokenize, sent_tokenize
import pandas as pd
import tweepy
from tweepy import OAuthHandler
import random

#making the twitter keys for my bot public so the entire code has access to the tweepy api 
ck = 'bi30Ft3DTJffyn5ckyXTW8D5T'
cs = 'FdxszhgorktdETPkFFz2w70Joo57qQG2KCOpm0kZyVl1pTK85V'
auth = tweepy.OAuthHandler(ck, cs)
ak = '873765616888422400-qq9xsOmyvedgJ7Z30s2eF9TT233chG9'
asec = 'SeCZHzLgJwVofpusqsJ46wN6tC8N6xw9SVmcrjkLsSViB'
auth.set_access_token(ak, asec)
api = tweepy.API(auth)

#small function to generate the tweets about the player that the user wants
def twitterGen(name):
    tweets = tweepy.Cursor(api.search_tweets, q=name, count = 15).items(150)#scrape the most recent 150 tweets mentioning the specific player
    outfile = open('tweets.txt', 'w', encoding = "utf-8")
    for t in tweets:    #write to a tweets.txt file
        outfile.write(t.text)

#reads the tweets from the text file and has the file in sentence format
def genSentences(file, sentences):
    fileR = open(file, 'r', encoding = 'utf-8')
    words = word_tokenize(fileR.read())
    uniqueWords = []
    for w in words:
        if w not in uniqueWords:
            uniqueWords.append(w)           #get all unique words from all the tweets and put them into a dataframe
    followMatrix = pd.DataFrame(index = uniqueWords, columns=uniqueWords, data = 0)
    newSentList = []
    for s in sentences:
        newSentList.append(s.split(' '))
    for n in newSentList:                   #for each sentence in the tweets.txt file, record each word and what
        for u in uniqueWords:               #it follows into the dataframe in order to get the follow frequencies
            if(u in n):
                for i in range(0,len(n)):
                    if(n[i] == u):
                        if(i != len(n)-1):
                            if(n[i+1] in uniqueWords):
                                followMatrix.at[u, n[i+1]] = followMatrix.at[u, n[i+1]]+1
    sentence = []
    sentenceList = []
    counter1 = 0            #pass each word as the starter words for each sentence
    for u in uniqueWords:
        if(u != ' ' and len(sentenceList) <= 5):
            sentence.append(u)
            sentence = gensentences2(u, uniqueWords, followMatrix, sentence, counter1)
            sentence = []

#helper funtion to create the sentences
def gensentences2(word, uniqueWords, followMatrix,sentence,counter):
    if(counter == 15):
        if(len(sentence) == 15):    #if the sentence has 15 words in it, then have the twitter bot tweet it out
            twLine = ' '
            for s in sentence:
                twLine = twLine+s+ ' '
            api.update_status(twLine)       #updating the status of the twitter bot
        return sentence
    else:
        maxEl = ' '
        followingList = []
        for u in uniqueWords:
            if(word != ' '):
                if(followMatrix.at[word, u] >= 1):
                    #print('true')
                    for i in range(1,followMatrix.at[word,u]+1):
                        followingList.append(u)                     #create a list of all the different words that follow each word
        wappend = ' '           #for example, if a 'Harden' is followed by points three times it will show [points,points,points]
        if(len(followingList) == 1):
            index = 0
        elif(len(followingList)!= 1 and len(followingList)!= 0):
            index = random.randint(0,len(followingList)-1)      #randomly choose a word from the following list for each words, words that are following the word more frequently have a higher chance of being chosen
        if(len(followingList) > 0):
            wappend = followingList[index]
            sentence.append(wappend)                    #append the randomly chosen word to the list sentence
        counter =  counter+1
        gensentences2(wappend, uniqueWords, followMatrix, sentence, counter)        #recursively pass the current word you just appened to repeat the process until the full sentence is completed

#main program
name = input('Enter the player,coach, team, etc that you want to tweet about')
twitterGen(name)
file = 'tweets.txt'
fileR = open(file, 'r', encoding = 'utf-8')
sentences = sent_tokenize(fileR.read())
genSentences(file, sentences)
