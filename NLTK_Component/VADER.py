from nltk.sentiment.vader import SentimentIntensityAnalyzer
from NLTK_Component.preprocessing import PreprocessText

text_sample = "The social media platform X has lost 71% of its value since it was bought by Elon Musk, according to the mutual fund Fidelity. Fidelity, which owns a stake in X Holdings, said in a disclosure obtained by Axios that it had marked down the value of its shares by 71.5% since Musk’s purchase. Musk acquired Twitter for $44bn in October 2022 and renamed the platform X in July 2023. Fidelity’s estimate would place the value of X at about $12.5bn. The number of monthly users of X dropped by 15% in the first year since Musk’s takeover amid concerns over a rise in hate speech on the platform. Since Musk’s takeover, X has cut at least 50% of staff and reduced moderation. And in September, the European Union issued a warning to Musk after it found that X had the highest ratio of disinformation posts of all large social media platforms. Fidelity’s revised valuation of X came from a disclosure which ran to the end of November 2023, Axios reported. X did not immediately respond to a request for comment. That disclosure would cover the fallout from a number of major companies pulling advertising on X after Musk endorsed an antisemitic conspiracy theory, the New York Times reported. Musk responded to the boycott by telling companies to “go fuck yourself” during an interview at an event in New York. Musk is the world’s richest man, according to Forbes, with a net worth of $251bn. When he acquired Twitter, Musk said he was buying the company “to try to help humanity”. Since the takeover Musk has reinstated a number of people previously banned from the platform, including former president Donald Trump and the rightwing conspiracy theorist Alex Jones. Trump is facing more than 90 criminal charges stemming from subversion of the 2020 election that he lost to Joe Biden, retention of government secrets after his presidency and hush-money payments to porn actor Stormy Daniels. He is also attempting to fend off civil lawsuits over business affairs and a rape allegation deemed substantially true by a judge. Meanwhile, Jones recently proposed to pay $55m over 10 years to the Sandy Hook families who sued him for spreading lies that the 2012 schoolhouse killings in Newtown, Connecticut, were part of a hoax meant to force the US to accept gun control. Jones’s offer came after a Texas judge ruled that Jones, the host of Infowars, could not invoke bankruptcy protection to avoid paying the nearly $1.5bn he was ordered to pay to families of the victims of one of the deadliest school shootings in US history. Believers of Jones’s lies aimed abuse and threats at the families"

sample_input = {121: ["text article1", "company_name"]}



class SentimentAnalyser:

    def __init__(self):
        self.sent_int_analyzer = SentimentIntensityAnalyzer()

        
    def get_article_sentiment(self, processed_news_article: str) -> dict:
        """
        Determines the sentiment possibilities of the article.
        Implements Sentiment Analysis from the NLTK module: https://www.nltk.org/howto/sentiment.html

        Arguments:
            - article: A string of pre-processed words in the article. 
w
        Returns:
            ---
        """

        sentiment = self.sent_int_analyzer.polarity_scores(processed_news_article) #A dictionaries of review sentiments which consists of compound, negative, neutral, and positive probablities.  
        output = {}
        output['pos'] = sentiment['pos'] * 100 
        output['neg'] = sentiment['neg'] * 100 
        output['neu'] = sentiment['neu'] * 100 
        output['overall'] = sentiment['compound'] 

        print("This text has an overall compound score of " + str(output['overall']) + "\nThe probability that the text is positive is " + str(output['pos']) + "%\nThe probability that the text is negative is " + str(output['neg']) + "%\nThe probability that the text is neutral is " + str(output['neu']) + "%")
        return output

s = SentimentAnalyser()
print(s.get_article_sentiment(text_sample))

