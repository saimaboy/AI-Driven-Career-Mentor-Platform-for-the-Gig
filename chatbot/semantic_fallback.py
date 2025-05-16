import torch
from sentence_transformers import SentenceTransformer, util

class SemanticFallback:
    def __init__(self):
        # load a small but strong paraphrase model
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        # same intents as in intent_classifier
        self.intents = [
            "greeting","thanks","finding_clients","pricing","skill_improvement",
            "profile_tips","analyze_skill_profile","client_communication",
            "time_management","payment","contract","feedback",
            "gig_creation","success_strategies"
        ]
        # precompute embeddings
        self.intent_embeddings = self.model.encode(self.intents, convert_to_tensor=True)

    def classify(self, text: str) -> str:
        emb = self.model.encode(text, convert_to_tensor=True)
        cos_scores = util.cos_sim(emb, self.intent_embeddings)[0]
        best_score, best_idx = torch.max(cos_scores, dim=0)
        # threshold—tune as you like
        if best_score.item() > 0.6:
            return self.intents[best_idx.item()]
        return None
