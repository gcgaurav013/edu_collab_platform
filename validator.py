from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class KnowledgeValidator:
    @staticmethod
    def calculate_confidence(source_text, generated_output):
        """
        Research Logic: Hybrid Validation
        1. Semantic Similarity (Vector-based)
        2. Keyword Alignment
        """
        if not generated_output or "Error" in generated_output:
            return 0, "Validation Failed: No Input"
        
        # TF-IDF Cosine Similarity
        documents = [source_text, generated_output]
        vectorizer = TfidfVectorizer().fit_transform(documents)
        similarity = cosine_similarity(vectorizer[0:1], vectorizer[1:2])[0][0]
        
        confidence_score = round(similarity * 100, 2)
        
        # Research flagging
        status = "Validated against source" if confidence_score > 60 else "Potential Hallucination Detected"
        return confidence_score, status

    @staticmethod
    def ai_fact_check(orchestrator, source_text, generated_output):
        """Uses a secondary AI pass to fact-check the first AI's output."""
        check_prompt = f"""
        Compare the 'Generated Output' against the 'Original Source'.
        Identify any facts in the output that ARE NOT in the source.
        Output a simple 'PASS' or 'FAIL' followed by reasoning.
        
        Source: {source_text[:2000]}
        Output: {generated_output}
        """
        return orchestrator.generate(check_prompt)