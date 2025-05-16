# freelance_mongo/chatbot/bot.py

import database as db
from chatbot.intent_classifier import IntentClassifier
from chatbot.semantic_fallback import SemanticFallback
from chatbot.response_generator import ResponseGenerator

class FreelanceSupportBot:
    def __init__(self, user_id):
        # load user info
        self.user_id      = user_id
        user             = db.get_user_by_id(user_id) or {}
        username         = user.get("username")
        user_skills      = db.get_user_skills(user_id)

        # intent modules
        self.intent_clf   = IntentClassifier()
        self.semantic_clf = SemanticFallback()
        self.resp_gen     = ResponseGenerator(
            user_id=user_id,
            user_name=username,
            user_skills=user_skills
        )

        # map intent labels to ResponseGenerator methods
        self.intent_map = {
            "greeting":               self.resp_gen.get_greeting,
            "thanks":                 self.resp_gen.get_thanks,
            "finding_clients":        self.resp_gen.get_finding_clients,
            "pricing":                self.resp_gen.get_pricing,
            "skill_improvement":      self.resp_gen.get_skill_improvement,
            "profile_tips":           self.resp_gen.get_profile_tips,
            "analyze_skill_profile":  self.resp_gen.analyze_skill_profile,
            "client_communication":   self.resp_gen.get_client_communication,
            "time_management":        self.resp_gen.get_time_management,
            "payment":                self.resp_gen.get_payment,
            "contract":               self.resp_gen.get_contract,
            "feedback":               self.resp_gen.get_feedback,
            "gig_creation":           self.resp_gen.get_gig_creation_tips,
            "success_strategies":     self.resp_gen.get_success_strategies,
        }

    def get_response(self, text: str) -> str:
        # 1) rule-based matcher
        intent = self.intent_clf.classify(text)
        if intent and intent in self.intent_map:
            return self.intent_map[intent]()

        # 2) semantic fallback
        intent = self.semantic_clf.classify(text)
        if intent and intent in self.intent_map:
            return self.intent_map[intent]()

        # 3) final default
        return self.resp_gen.get_default()


if __name__ == "__main__":
    bot = FreelanceSupportBot(user_id=1)
    print("🤖", bot.get_response("hello"))
    while True:
        msg = input("👤 ")
        if msg.lower() in ("quit", "exit"):
            break
        print("🤖", bot.get_response(msg))
