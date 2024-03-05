import sys 

sys.path.insert(0, '/Users/mac/Documents/GitHub/SoftEngProject/tradetalker')

from python_component.nltk_component.preprocessing import GetPOSClass, PreprocessText
pos = GetPOSClass()
p = PreprocessText(pos)

#mock article data
class Article:
    def __init__(self, id: int, header: str, content: str, labelled_sentiment: str):
        self.id = id 
        self.header = header 
        self.content = content 
        self.processed_content = p.preprocess_text(content)
        self.sentiment = labelled_sentiment


content1 = """Google has invested $1bn (£790m) to build its first UK data centre.
The tech giant said construction had started at a 33-acre site in Waltham Cross, Hertfordshire, and hoped it would be completed by 2025.
Google stressed it was too early to say how many jobs would be created but it would need engineers, project managers, data centre technicians, electricians, catering and security personnel.
The prime minister said it showed the UK had "huge potential for growth".
The project marked the latest investment by a major US tech firm in Britain, after Microsoft announced it would invest £2.5bn to expand data centres for artificial intelligence (AI) across the UK. Prime Minister Rishi Sunak hailed the investment as proof the UK has "huge potential" as a technology hub
The new Hertfordshire facility would add to Google's 27 data centres worldwide, with sites across 11 countries and 13 in the US.
It said the site would help power popular digital services, such as Google Cloud, Gmail, Docs, Sheets, search and maps.
It would also "play a critical role in supporting the company's AI innovations and will provide the UK with much-needed compute capacity".
Google said the facility would be constructed in line with net-zero aims and it planned for significant heat generated by the data centre to be used to heat homes and businesses in the local area.
'Growing demand'
Google already has more than 7,000 staff in the UK and sites in King's Cross, Central Saint Giles and Victoria in London and Manchester.
Its DeepMind AI research and development lab is also based in London.
Ruth Porat, president, chief investment officer and chief financial officer of Google, said: "This new data centre will help meet growing demand for our AI and cloud services".
She said it would "bring crucial compute capacity to businesses across the UK while creating construction and technical jobs for the local community."
A sign near the Google's headquarters in Mountain View, California
Google said it was too early to say how many jobs the site
Prime Minister Rishi Sunak said: "Foreign investment creates jobs and grows all regions of our economy, and investments like this will help to drive growth in the decade ahead."
Chancellor Jeremy Hunt, who was at the World Economic Forum in Davos, Switzerland, added: "From business conducted online to advancements in healthcare, every growing economy relies on data centres.
"Our country is no different and this major $1bn investment from Google is a huge vote of confidence in Britain as the largest tech economy in Europe."
"""
article1 = Article(11, "Google has invested $1bn (£790m) to build its first UK data centre", content1, 'positive')


content2 = """
Microsoft looks beyond Xbox hardware for gaming growth: Microsoft is accelerating a push away from its own Xbox hardware, hoping to boost growth by selling more games on rival consoles as the industry reckons with a protracted slowdown.
The technology group plans to make a handful of games that were previously offered only on its Xbox available on Sony’s PlayStation and Nintendo’s Switch, in a departure from its previous strategy of keeping games developed in-house as exclusives for its own platforms.
Four months after closing its $75bn Activision Blizzard deal, Microsoft also said the first title from the portfolio of the Call of Duty creator would start appearing on its Game Pass subscription service next month.
Phil Spencer, chief executive of Microsoft Gaming, insisted the moves were “not a change to our fundamental exclusives strategy” but reflected a desire to expand the audience for certain games that have hit a ceiling on its own platforms.
In an interview with the Financial Times, Spencer said there was “some diminishing return” from focusing only on selling more games to its existing audience of Xbox owners.
“When I look forward, for our business, finding more players in more places, many of them on the devices that they already own, is a good thing for our own growth as well,” he said.
Content delivers higher margins than hardware for Microsoft, Spencer said, adding: “Extending the software and services and games to more endpoints improves the overall profitability of the [Xbox] division.”
The latest Xbox console generation, first released in 2020, has struggled to keep up with the PlayStation 5 and Switch. Some analysts estimate PS5 outsold Xbox by almost three to one last year, but both have been comprehensively outsold by the older Switch over its lifetime.
“We have more Xbox players off of Xbox consoles than on Xbox consoles today,” Spencer said, referring to those who play its games on PCs or other devices via cloud streaming. “Those lines will continue to diverge. That’s a good thing for the health of the business because the hardware we sell is not a profit driver for us in our organisation.”
Sony announced in December that PS5 hit a milestone of 50mn sales, but the Japanese group nevertheless this week downgraded 2024 forecasts for its gaming unit, as a new wave of lay-offs hit games developers across the industry in the first weeks of the year.
Enders Analysis estimates global gaming revenue rose by less than 1 per cent last year to $184bn, a slower rate than inflation. Enders’ researchers said in a recent report that 2024 was set to be a “bumpy and uncomfortable year across the industry” as “revenue growth is likely to be flat for the next 12-24 months”.
Microsoft is among those cutting jobs, saying last month it would lay off around 1,900 staff, or about 8 per cent of its gaming workforce, including some at Activision Blizzard.
Microsoft has for several years pushed its subscription service, Game Pass, which is available on Xbox and PC but not on PlayStation. About 34mn people subscribe to Game Pass, which costs $17 a month for full access to the latest games on consoles and PC, or less for access to a limited catalogue and multiplayer features.
"""

article2 = Article(22, "Microsoft looks beyond Xbox hardware for gaming growth", content2, 'positive')


content3 = """
Behind Apple’s Doomed Car Project: False Starts and Wrong Turns
Internal disagreements over the direction of the Apple car led the effort to sputter for years before it was canceled this week. For the last decade, many Apple employees working on the company’s secretive car project, internally code-named Titan, had a less flattering name for it: the Titanic disaster. They knew the project was likely to fail.
Throughout its existence, the car effort was scrapped and rebooted several times, shedding hundreds of workers along the way. As a result of dueling views among leaders about what an Apple car should be, it began as an electric vehicle that would compete against Tesla and morphed into a self-driving car to rival Google’s Waymo.
By the time of its death — Tuesday, when executives announced internally that the project was being killed and that many members of the team were being reassigned to work on artificial intelligence — Apple had burned more than $10 billion on the project and the car had reverted to its beginnings as an electric vehicle with driving-assistance features rivaling Tesla’s, according to a half dozen people who worked on the project over the past decade.
The car project’s demise was a testament to the way Apple has struggled to develop new products in the years since Steve Jobs’s death in 2011. The effort had four different leaders and conducted multiple rounds of layoffs. But it festered and ultimately fizzled in large part because developing the software and algorithms for a car with autonomous driving features proved too difficult.
"""

article3 = Article(33,"Behind Apple’s Doomed Car Project: False Starts and Wrong Turns", content3,'negative' )

content4 = """
Alphabet’s Google was hit with a €2.1bn ($2.3bn) lawsuit by 32 media groups including Axel Springer and Schibsted on Wednesday, alleging that they had suffered losses due to the company’s practices in digital advertising.
Google’s Gemini AI illustrations of a 1943 German soldier.
Google chief admits ‘biased’ AI tool’s photo diversity offended users
Read moreThe move by the groups – which include publishers in Austria, Belgium, Bulgaria, the Czech Republic, Denmark, Finland, Hungary, Luxembourg, the Netherlands, Norway, Poland, Spain and Sweden – comes as antitrust regulators also crack down on Google’s ad-tech business.
“The media companies involved have incurred losses due to a less competitive market, which is a direct result of Google’s misconduct,” a statement issued by their lawyers, Geradin Partners and Stek, said.
“Without Google’s abuse of its dominant position, the media companies would have received significantly higher revenues from advertising and paid lower fees for ad tech services. Crucially, these funds could have been reinvested into strengthening the European media landscape,” the lawyers said.
"""

article4 = Article(44,"Google sued for $2.3bn by European media groups over digital ad losses", content4, 'negative')


articles = [article1, article2, article3, article4]

