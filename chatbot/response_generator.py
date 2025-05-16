import random
import database as db


class ResponseGenerator:
    def __init__(self, user_id=None, user_name=None, user_skills=None):
        self.user_id = user_id
        self.user_name = user_name
        self.user_skills = user_skills

    def get_greeting(self):
        """Return a greeting response"""
        greetings = [
            f"Hello{' ' + self.user_name if self.user_name else ''}! How can I help you with your freelancing journey today?",
            f"Hi there{' ' + self.user_name if self.user_name else ''}! I'm your freelancing assistant. What would you like to know?",
            f"Hey{' ' + self.user_name if self.user_name else ''}! Ready to boost your freelancing career? Ask me anything!"
        ]
        return random.choice(greetings)

    def get_thanks(self):
        """Return a response to thanks"""
        responses = [
            "You're welcome! Let me know if you need any other help with your freelancing.",
            "Glad I could help! Don't hesitate to ask more questions.",
            "Anytime! Success in your freelancing journey!"
        ]
        return random.choice(responses)

    def get_finding_clients(self):
        """Return advice on finding clients"""
        response = "Here are some tips for finding clients and gigs:\n\n"

        tips = [
            "Complete your profile with all relevant skills and experience",
            "Create impressive portfolio samples that showcase your capabilities",
            "Set competitive rates initially to build a good reputation",
            "Write personalized proposals for each job",
            "Network with other freelancers in your field",
            "Ask satisfied clients for referrals",
            "Consider specializing in a niche to stand out",
            "Be proactive in looking for gigs - don't just wait for clients to find you",
            "Follow up with potential clients professionally"
        ]

        # Add 5 random tips
        sampled_tips = random.sample(tips, 5)
        for i, tip in enumerate(sampled_tips, 1):
            response += f"{i}. {tip}\n"

        # Personalized advice if skills are available
        if self.user_skills:
            skill_names = [skill['name'] for skill in self.user_skills]
            if len(skill_names) > 0:
                random_skill = random.choice(skill_names)
                response += f"\nWith your skill in {random_skill}, you might want to search for gigs that specifically require this expertise."

        return response

    def get_pricing(self):
        """Return advice on pricing"""
        response = "Setting the right price is crucial for freelance success. Here's my advice:\n\n"

        pricing_tips = [
            "Research market rates for your skills and experience level",
            "Consider the complexity and urgency of each project",
            "Factor in your overhead costs and desired profit margin",
            "Value your time including research, communication, and revisions",
            "Consider offering package deals for related services",
            "Gradually increase your rates as you gain more experience and positive reviews",
            "Be clear about what's included in your price and what costs extra",
            "Consider different pricing models: hourly, project-based, or retainer",
            "Don't undervalue yourself - quality clients are willing to pay for quality work"
        ]

        # Add 5 random tips
        sampled_tips = random.sample(pricing_tips, 5)
        for i, tip in enumerate(sampled_tips, 1):
            response += f"{i}. {tip}\n"

        # Personalized advice if skills are available
        if self.user_skills:
            advanced_skills = [skill for skill in self.user_skills if
                               skill.get('proficiency_level') in ['Advanced', 'Expert']]
            if advanced_skills:
                random_adv_skill = random.choice(advanced_skills)
                response += f"\nSince you're {'an expert' if random_adv_skill.get('proficiency_level') == 'Expert' else 'advanced'} in {random_adv_skill['name']}, you might consider charging premium rates for projects requiring this specialized skill."

        return response

    def get_skill_improvement(self):
        """Return advice on skill improvement"""
        response = "Continuous learning is essential for freelancers. Here are ways to improve your skills:\n\n"

        learning_tips = [
            "Take online courses in your field (check our Courses page for recommendations)",
            "Join professional communities and forums to learn from peers",
            "Work on personal projects to practice new techniques",
            "Read industry blogs, books, and publications",
            "Attend webinars and virtual conferences",
            "Follow experts in your field on social media",
            "Seek feedback on your work from experienced professionals",
            "Collaborate with other freelancers on projects",
            "Set aside dedicated time each week for learning"
        ]

        # Add 5 random tips
        sampled_tips = random.sample(learning_tips, 5)
        for i, tip in enumerate(sampled_tips, 1):
            response += f"{i}. {tip}\n"

        # Personalized course recommendation if skills are available
        if self.user_id:
            from recommenders import recommend_courses
            courses = recommend_courses(self.user_id, 1)
            if courses:
                course = courses[0]
                response += f"\nBased on your profile, you might benefit from taking '{course['title']}' on {course['provider']}."

        return response

    def get_profile_tips(self):
        """Return advice on improving freelancer profile"""
        response = "A strong profile attracts more clients. Here's how to improve yours:\n\n"

        profile_tips = [
            "Use a professional profile picture",
            "Write a compelling bio that highlights your unique value proposition",
            "Showcase your best and most relevant work in your portfolio",
            "Include specific metrics and results from past projects",
            "Highlight your educational background and certifications",
            "List all your relevant skills with accurate proficiency levels",
            "Add testimonials from satisfied clients",
            "Keep your profile updated with your latest accomplishments",
            "Use keywords relevant to your industry to improve searchability"
        ]

        # Add 5 random tips
        sampled_tips = random.sample(profile_tips, 5)
        for i, tip in enumerate(sampled_tips, 1):
            response += f"{i}. {tip}\n"

        return response

    def get_client_communication(self):
        """Return advice on client communication"""
        response = "Good communication is key to successful freelancing. Here are some tips:\n\n"

        communication_tips = [
            "Respond promptly to client messages, even if just to acknowledge receipt",
            "Set clear expectations about communication channels and response times",
            "Use professional language and check for errors before sending",
            "Ask clarifying questions to fully understand the client's needs",
            "Provide regular updates on project progress",
            "Document important decisions and agreements in writing",
            "Be honest about challenges and propose solutions",
            "Listen actively to client feedback and concerns",
            "Express gratitude for the opportunity to work together"
        ]

        # Add 5 random tips
        sampled_tips = random.sample(communication_tips, 5)
        for i, tip in enumerate(sampled_tips, 1):
            response += f"{i}. {tip}\n"

        return response

    def get_time_management(self):
        """Return advice on time management"""
        response = "Effective time management is crucial for freelancers. Here's how to improve:\n\n"

        time_tips = [
            "Use time tracking tools to understand how you spend your working hours",
            "Break projects into smaller, manageable tasks with deadlines",
            "Set realistic timelines and build in buffer time for unexpected issues",
            "Use the Pomodoro Technique (25 minutes of focus, then a short break)",
            "Batch similar tasks together to minimize context switching",
            "Schedule dedicated time for client communication",
            "Learn to say no to projects that don't align with your goals or availability",
            "Create and follow a consistent daily routine",
            "Use project management tools to stay organized"
        ]

        # Add 5 random tips
        sampled_tips = random.sample(time_tips, 5)
        for i, tip in enumerate(sampled_tips, 1):
            response += f"{i}. {tip}\n"

        return response

    def get_payment(self):
        """Return advice on payments and invoicing"""
        response = "Managing payments properly is essential for freelancers. Here's my advice:\n\n"

        payment_tips = [
            "Always use professional invoices with all the necessary details",
            "Set clear payment terms and deadlines upfront",
            "Consider requiring a deposit before starting work",
            "Keep track of all your invoices and payments for tax purposes",
            "Use secure payment platforms that protect both you and the client",
            "Follow up politely but firmly on overdue payments",
            "Consider offering multiple payment methods for client convenience",
            "Include your payment terms in your contract",
            "Keep receipts for all business expenses for tax deductions"
        ]

        # Add 5 random tips
        sampled_tips = random.sample(payment_tips, 5)
        for i, tip in enumerate(sampled_tips, 1):
            response += f"{i}. {tip}\n"

        return response

    def get_contract(self):
        """Return advice on contracts"""
        response = "Good contracts protect both you and your clients. Here's what to consider:\n\n"

        contract_tips = [
            "Always use written contracts, even for small projects",
            "Clearly define the scope of work and deliverables",
            "Include payment terms, amounts, and deadlines",
            "Specify the project timeline and milestones",
            "Address ownership and copyright of the work",
            "Include a process for handling revisions and changes to the scope",
            "Consider adding a kill fee for canceled projects",
            "Specify confidentiality terms if necessary",
            "Consider having a lawyer review your contract template"
        ]

        # Add 5 random tips
        sampled_tips = random.sample(contract_tips, 5)
        for i, tip in enumerate(sampled_tips, 1):
            response += f"{i}. {tip}\n"

        response += "\nNote: I'm not a legal professional. Consider consulting with a lawyer for contract advice specific to your situation."

        return response

    def get_feedback(self):
        """Return advice on handling feedback"""
        response = "Feedback is valuable for your growth as a freelancer. Here's how to handle it effectively:\n\n"

        feedback_tips = [
            "Ask for specific feedback on your completed projects",
            "Be open to constructive criticism without taking it personally",
            "Thank clients for their feedback, even if it's negative",
            "Use feedback to identify patterns and areas for improvement",
            "Implement relevant suggestions in future projects",
            "Ask clarifying questions if feedback is vague",
            "Create a system for collecting and organizing feedback",
            "Share positive feedback (with permission) as testimonials",
            "Follow up with clients after implementing their suggestions"
        ]

        # Add 5 random tips
        sampled_tips = random.sample(feedback_tips, 5)
        for i, tip in enumerate(sampled_tips, 1):
            response += f"{i}. {tip}\n"

        return response

    def get_gig_creation_tips(self):
        """Return tips for creating effective gigs"""
        tips = [
            "Use a clear, specific title that includes your main skill and deliverable",
            "Break down your services into different packages or tiers",
            "Include realistic delivery timeframes for each package",
            "Be specific about what's included and what costs extra",
            "Add eye-catching visuals that showcase your work",
            "Highlight your unique selling point - what makes your service special",
            "List the exact deliverables the client will receive",
            "Address common client concerns or questions in your description",
            "Include relevant keywords to help clients find your gig",
            "Set appropriate expectations about revisions and communication"
        ]

        response = "Here are some tips for creating effective gigs that attract clients:\n\n"

        # Add 5 random tips
        sampled_tips = random.sample(tips, 5)
        for i, tip in enumerate(sampled_tips, 1):
            response += f"{i}. {tip}\n"

        return response

    def analyze_skill_profile(self):
        """Analyze the user's skill profile and provide insights"""
        if not self.user_id or not self.user_skills:
            return "I can analyze your skill profile once you've added skills to your profile. Go to the Profile page to add your skills."

        response = "Based on your skill profile, here's my analysis:\n\n"

        # Count skills by category
        categories = {}
        for skill in self.user_skills:
            category = skill['category']
            if category in categories:
                categories[category] += 1
            else:
                categories[category] = 1

        # Identify strongest and weakest categories
        if categories:
            strongest_category = max(categories.items(), key=lambda x: x[1])[0]
            response += f"Your strongest category appears to be {strongest_category} with {categories[strongest_category]} skills.\n\n"

            # Check for advanced/expert skills
            advanced_skills = [skill for skill in self.user_skills if
                               skill.get('proficiency_level') in ['Advanced', 'Expert']]
            if advanced_skills:
                response += "Your top skills are:\n"
                for skill in advanced_skills[:3]:
                    response += f"- {skill['name']} ({skill.get('proficiency_level')})\n"

            # Suggest skill gaps
            conn = db.get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                           SELECT s.id, s.name, s.category, COUNT(gs.skill_id) as frequency
                           FROM skills s
                                    JOIN gig_skills gs ON s.id = gs.skill_id
                           WHERE s.category = ?
                           GROUP BY s.id
                           ORDER BY frequency DESC LIMIT 5
                           """, (strongest_category,))

            popular_skills = cursor.fetchall()
            conn.close()

            user_skill_ids = [skill['id'] for skill in self.user_skills]
            missing_popular_skills = [skill for skill in popular_skills if skill[0] not in user_skill_ids]

            if missing_popular_skills:
                response += "\nTo strengthen your profile, consider adding these in-demand skills:\n"
                for skill in missing_popular_skills[:2]:
                    response += f"- {skill[1]} (Popular in {skill[2]})\n"

        return response

    def get_success_strategies(self):
        """Return strategies for freelancing success"""
        strategies = [
            "Specialize in a niche rather than being a generalist to command higher rates",
            "Build a personal brand that showcases your unique value proposition",
            "Create systems and templates to streamline repetitive tasks",
            "Develop excellent communication skills to build client trust",
            "Always deliver more value than the client expects",
            "Network consistently, not just when you need work",
            "Learn to spot and avoid problem clients early",
            "Continuously update your skills to stay competitive",
            "Seek long-term relationships rather than one-off projects",
            "Set aside time for marketing even when you're busy with client work"
        ]

        response = "Here are some proven strategies for freelancing success:\n\n"

        # Add 5 random strategies
        sampled_strategies = random.sample(strategies, 5)
        for i, strategy in enumerate(sampled_strategies, 1):
            response += f"{i}. {strategy}\n"

        return response

    def get_default(self):
        """Return a default response when no specific pattern is matched"""
        default_responses = [
            "I'm here to help with your freelancing questions. You can ask me about finding clients, pricing, improving skills, managing your profile, communicating with clients, managing time, handling payments, contracts, or getting feedback.",

            "I'm not sure I understand your question. I can assist with various freelancing topics like finding work, setting prices, skill development, profile optimization, client communication, time management, payments, contracts, and handling feedback. What would you like to know?",

            "As your freelancing assistant, I can provide advice on many aspects of freelance work. Could you please clarify what specific information you're looking for? I can help with client acquisition, pricing strategies, skill development, and more."
        ]
        return random.choice(default_responses)
