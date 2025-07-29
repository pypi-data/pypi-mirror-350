import pandas as pd
from state_of_the_art.recommenders.email_content import EmailContentGenerator, EmailData
from state_of_the_art.recommenders.interest_recommender import InterestRecommender
from state_of_the_art.register_papers.arxiv_miner import ArxivMiner
from state_of_the_art.paper.email_paper import EmailService
from datetime import datetime
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')  # adjust path
import django
django.setup()
from sota_landingpage.models import User

class MainRecommenderPipeline:
    def mine_papers_and_generate_report(self):
        print("Mining papers...")
        for i in ArxivMiner().mine_all_keywords():
            print(i)
        print("Building report...")
        self.build_reports_and_send_emails()
    
    def get_all_users(self):
        users = User.objects.all()
        return users

    def build_reports_and_send_emails(self):
        users = self.get_all_users()
        for user in users:
            print(f"Building report for {user.email}")
            html = self.build_html_report(user)
            current_date = datetime.now().strftime('%B %d, %Y')
            print("Sending email...")
            EmailService().send(
                content=html,
                subject=f"SOTA-Arxiv interests papers report from {current_date}",
                recepient=user.email
            )

    def get_all_interests_report(self, interests: list[str], return_list: bool = False) -> pd.DataFrame:
        recommendations = []
        self.interest_recommender = InterestRecommender()
        for interest in interests:
            papers_recommended = self.interest_recommender.recommend(topic_name=interest, n_papers=3, return_papers=True)
            recommendations.append({ 'interest': interest, 'papers': papers_recommended})
        
        if return_list:
            return recommendations

        df = pd.DataFrame(recommendations)   
        return df

    def get_user_interests(self, user: User) -> list[str]:
        from sota_landingpage.models import Interest
        result = Interest.objects.filter(user=user).values_list('interest_name', flat=True)
        str_list = [str(obj) for obj in result]
        return str_list

    def build_html_report(self, user: User) -> str:
        interests = self.get_user_interests(user)
        recommendations = self.get_all_interests_report(interests, return_list=True)
        empty_interests = [rec['interest'] for rec in recommendations if not rec['papers']]
        recommendations_with_papers = [rec for rec in recommendations if rec['papers']]
        
        total_interests = len(interests)
        days_to_lookback = self.interest_recommender.days_to_lookback
        papers_found_in_last_n_days = self.interest_recommender.number_of_papers
        # set data as a dataclass
        email_data = EmailData(
            user_email=user.email,
            recommendations_with_papers=recommendations_with_papers,
            empty_interests=empty_interests,
            total_interests=total_interests,
            days_to_lookback=days_to_lookback,
            papers_found_in_last_n_days=papers_found_in_last_n_days)

        html = EmailContentGenerator().generate_html(email_data)
        return html
        

def main():
    import fire
    fire.Fire(MainRecommenderPipeline)
if __name__ == "__main__":
    main()
