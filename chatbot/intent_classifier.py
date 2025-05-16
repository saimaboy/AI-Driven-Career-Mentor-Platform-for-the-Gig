import spacy
from spacy.matcher import Matcher, PhraseMatcher

class IntentClassifier:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")
        self.matcher = Matcher(self.nlp.vocab)
        self.phrase_matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        self._init_patterns()

    def _init_patterns(self):
        # --- token-level patterns ---
        self.matcher.add("greeting", [[{"LOWER": {"IN": ["hello", "hi", "hey"]}}]])
        self.matcher.add("thanks",   [[{"LOWER": {"IN": ["thanks", "thank"]}}]])
        self.matcher.add("finding_clients", [
            [{"LOWER": "find"}, {"LOWER": {"IN": ["client", "work", "gig"]}}],
            [{"LOWER": {"IN": ["clients", "gigs"]}}, {"LOWER": "find"}]
        ])
        self.matcher.add("pricing", [[{"LOWER": {"IN": ["price", "pricing", "charge", "rate"]}}]])
        self.matcher.add("skill_improvement", [[{"LOWER": {"IN": ["skill", "improve", "learn"]}}]])
        self.matcher.add("profile_tips", [[{"LOWER": "profile"}, {"LOWER": {"IN": ["tip","improve","optimize"]}}]])
        self.matcher.add("analyze_skill_profile", [[{"LOWER": "analyze"}, {"LOWER": {"IN": ["skill","profile"]}}]])
        self.matcher.add("client_communication", [[{"LOWER": {"IN": ["communication","communicate","talk"]}}]])
        self.matcher.add("time_management", [[{"LOWER": {"IN": ["time","manage","management"]}}]])
        self.matcher.add("payment", [[{"LOWER": {"IN": ["payment","invoice","billing"]}}]])
        self.matcher.add("contract", [[{"LOWER": "contract"}]])
        self.matcher.add("feedback", [[{"LOWER": {"IN": ["feedback","review"]}}]])
        self.matcher.add("gig_creation", [[{"LOWER": "gig"}, {"LOWER": {"IN": ["tips","listing","create","effective"]}}]])
        self.matcher.add("success_strategies", [[{"LOWER": {"IN": ["strategy","strategies","success"]}}]])

        # --- phrase-level patterns (more natural) ---
        phrases = {
            "finding_clients": ["how do i find my first client", "where to find freelance work"],
            "pricing":          ["how should i price my services", "what should i charge"],
            "skill_improvement":["what skills should i improve", "which skills to develop"],
            "profile_tips":     ["tips to improve my profile", "how to optimize my profile"],
            "analyze_skill_profile": ["analyze my skill profile", "profile analysis"],
            "gig_creation":     ["tips for effective gig listings", "how to create a gig listing"],
            "success_strategies":["what are the best freelancing strategies", "freelancing strategies"]
        }
        for label, texts in phrases.items():
            docs = [self.nlp(text) for text in texts]
            self.phrase_matcher.add(label, None, *docs)

    def classify(self, text: str) -> str:
        doc = self.nlp(text)
        # 1) PhraseMatcher
        pm = self.phrase_matcher(doc)
        if pm:
            match_id, start, end = pm[0]
            return self.nlp.vocab.strings[match_id]
        # 2) Matcher
        m = self.matcher(doc)
        if m:
            match_id, start, end = m[0]
            return self.nlp.vocab.strings[match_id]
        return None
