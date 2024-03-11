"""Recommends companies to follow based on the user's followed companies and keywords
from articles.
"""

import random
import re

import pandas as pd

MIN_REC = 10


class RecommendationSystem:
    """Recommends companies to follow based on the user's followed companies and
    keywords.
    """

    # data is a dict, first two keys' value are a list of dicts (records), last key is
    # a list of strings, each string being 20 words separated by commas
    # keys: following, non_following, keywords
    def __init__(self, data: dict) -> None:
        """Initializes the RecommendationSystem class with the provided parameters."""
        self.industry_groups = {
            "Finance and Banking": [
                "Insurance - Property & Casualty",
                "Insurance - Diversified",
                "Insurance - Specialty",
                "Banks - Diversified",
                "Banks - Regional",
                "Financial Data & Stock Exchanges",
                "Asset Management",
            ],
            "Technology and Telecommunications": [
                "Telecom Services",
                "Internet Content & Information",
                "Software - Application",
            ],
            "Retail and Consumer Goods": [
                "Discount Stores",
                "Packaged Foods",
                "Food Distribution",
                "Luxury Goods",
                "Beverages - Non-Alcoholic",
                "Beverages - Wineries & Distilleries",
                "Specialty Retail",
                "Apparel Retail",
                "Home Improvement Retail",
                "Grocery Stores",
                "Household & Personal Products",
                "Department Stores",
            ],
            "Manufacturing and Industrial": [
                "Other Industrial Metals & Mining",
                "Copper",
                "Rental & Leasing Services",
                "Aerospace & Defense",
                "Residential Construction",
                "Oil & Gas Integrated",
                "Oil & Gas Refining & Marketing",
                "Industrial Distribution",
                "Specialty Chemicals",
                "Specialty Industrial Machinery",
                "Packaging & Containers",
                "Paper & Paper Products",
                "Furnishings, Fixtures & Appliances",
            ],
            "Healthcare and Pharmaceuticals": [
                "Drug Manufacturers - General",
                "Drug Manufacturers - Specialty & Generic",
                "Medical Instruments & Supplies",
                "Medical Devices",
            ],
            "Real Estate": [
                "REIT - Diversified",
                "REIT - Industrial",
            ],
            "Utilities": [
                "Utilities - Independent Power Producers",
                "Utilities - Regulated Electric",
                "Utilities - Regulated Water",
                "Utilities - Diversified",
            ],
            "Entertainment and Hospitality": [
                "Restaurants",
                "Lodging",
                "Airlines",
                "Gambling",
            ],
            "Other": [
                "Gold",
                "Tobacco",
                "Consulting Services",
                "Conglomerates",
                "Specialty Business Services",
                "Advertising Agencies",
                "Publishing",
                "Other Precious Metals & Mining",
            ],
        }
        self.rec: set = set({})
        self.followed = pd.DataFrame.from_dict(data["following"])
        self.not_followed = pd.DataFrame.from_dict(data["non_following"])

        # flattens
        self.article_words = (
            [] if len(data["keywords"]) == 0 else ",".join(data["keywords"]).split(",")
        )

    def recommend(self) -> set:
        """Returns the recommended companies."""
        if self.not_followed.empty:
            return set({})
        self.article_recs()
        if not self.followed.empty:
            self.industry_recs()
        self.leftover_recs()
        return self.rec

    def get_companies(self, num: int, grp: str) -> list:
        """Gets n companies from a specified industry group."""
        # Get all companies of the selected industry and shuffles
        industry_filtered = self.not_followed[
            self.not_followed["Industry"].isin(self.industry_groups[grp])
        ]["CompanyID"].to_list()
        random.shuffle(industry_filtered)

        # Adds up to n companies
        if num > len(industry_filtered):
            num = len(industry_filtered)
        return [industry_filtered[i] for i in range(num)]

    def article_recs(self) -> None:
        """Adds companies appearing in key words to recommendations."""
        # Certain words appear in company names but do not imply any specific company,
        # so should be blacklisted
        blacklist = {
            "group",
            "plc",
            "ord",
            "mining",
            "systems",
            "banking",
            "value",
            "retail",
            "european",
            "engineering",
            "industries",
            "investment",
            "trust",
            "american",
            "international",
        }

        # Put all words in lowercase and remove blacklisted and repeated words
        words = {word.lower() for word in self.article_words}
        words = words.difference(blacklist)

        # Check if each word is a company, check if it is an already followed company
        # so it doesn't waste time querying the db
        for wrd in words:
            out = self.is_company(wrd)
            if out[0]:
                self.rec.add(out[1].iloc[0])

    def industry_recs(self) -> None:
        """Adds companies from the same industry as followed to recommendations."""
        # Get followed companies, their industry and dividend yield
        total_count = len(self.followed)
        # Get proportion of followed covered by each industry
        industries = (self.followed["Industry"].value_counts() / total_count).to_dict()
        # Calculate proportions of followed covered by each industry group
        group_sums = {}
        for key, values in self.industry_groups.items():
            total = 0
            for value in values:
                if value in industries:
                    total += industries[value]
            group_sums[key] = total

        # Add companies sharing industry with followed to rec
        for key in group_sums:
            n = int(group_sums[key] * 10)
            if n >= 1:
                companies = self.get_companies(n, key)
                for comp in companies:
                    self.rec.add(comp)

    def leftover_recs(self) -> None:
        """Adds random companies to recommendations."""
        # If not many companies are recommended, adds some at random
        if len(self.rec) < MIN_REC:
            leftovers = self.not_followed["CompanyID"].to_list()
            random.shuffle(leftovers)
            while len(self.rec) < MIN_REC:
                if len(leftovers) == 0:
                    break
                x = leftovers[0]
                leftovers = leftovers[1::]
                self.rec.add(x)

    # Check key word is in a not_followed CompanyName
    def is_company(self, wrd: str) -> tuple:
        """Checks if a word is a company. If it is, returns the company id."""
        pattern = r"\b" + re.escape(wrd) + r"\b"
        x = self.not_followed.loc[
            self.not_followed.apply(
                (lambda row: row.astype(str).str.contains(pattern, case=False).any()),
                axis=1,
            )
        ]
        return ((not x.empty), x["CompanyID"])  # is_company, companyId
