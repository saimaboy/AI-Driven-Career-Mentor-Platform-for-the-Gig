import sqlite3

# — adjust this path if your DB is elsewhere —
DB_PATH = "freelance.db"

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()


    # (id, title, description, provider, url, difficulty_level, duration, price)
    new_courses = [
        # — BUSINESS —
        (28, "Business Strategy and Innovation",
         "Learn frameworks and best practices for strategic planning and innovation in modern businesses",
         "Coursera", "https://coursera.org/business-strategy", "Intermediate", "20 hours", 49.00),

        (29, "Financial Modeling & Valuation",
         "Build robust financial models and valuation techniques using Excel and real-world scenarios",
         "Udemy", "https://udemy.com/financial-modeling-valuation", "Advanced", "25 hours", 59.99),

        (30, "Lean Startup Methodology",
         "Master lean startup principles to launch, test, and scale new business ideas efficiently",
         "Udemy", "https://udemy.com/lean-startup-methodology", "Beginner", "10 hours", 19.99),

        (31, "Leadership & Management Essentials",
         "Develop key leadership skills for managing teams and projects",
         "edX", "https://edx.org/leadership-management", "Beginner", "15 hours", 0.00),

        (32, "Digital Transformation Strategies",
         "Learn how to drive and manage digital transformation across organizations",
         "LinkedIn Learning", "https://linkedin.com/learning/digital-transformation-strategies",
         "Intermediate", "12 hours", 29.99),

        # — DATA SCIENCE —
        (33, "Data Visualization with Tableau",
         "Create interactive dashboards and visualizations with Tableau",
         "Coursera", "https://coursera.org/data-visualization-tableau", "Intermediate", "20 hours", 49.00),

        (34, "Advanced SQL for Data Science",
         "Master complex SQL queries, window functions, and performance tuning for data analysis",
         "Udemy", "https://udemy.com/advanced-sql-data-science", "Advanced", "18 hours", 34.99),

        (35, "Time Series Forecasting with Python",
         "Analyze and forecast time series data using Python libraries like statsmodels and Prophet",
         "Udemy", "https://udemy.com/time-series-forecasting-python", "Intermediate", "15 hours", 29.99),

        (36, "Big Data Analytics with Spark",
         "Process and analyze large datasets using Apache Spark (Scala/Python)",
         "edX", "https://edx.org/big-data-spark", "Advanced", "30 hours", 99.00),

        (37, "Machine Learning Deployment on AWS",
         "Learn how to deploy ML models using AWS SageMaker and Lambda",
         "Udacity", "https://udacity.com/aws-machine-learning-deployment", "Advanced", "20 hours", 199.00),

        (38, "Python Performance Optimization",
         "Optimize Python code with profiling, caching, and concurrency techniques",
         "Udemy", "https://udemy.com/python-performance", "Advanced", "15 hours", 34.99),

        (39, "C# .NET Core API Development",
         "Build robust RESTful APIs with ASP.NET Core and Entity Framework",
         "Pluralsight", "https://pluralsight.com/csharp-netcore-api", "Intermediate", "12 hours", 29.99),

        (40, "Rust Fundamentals and Systems Programming",
         "Learn memory-safe systems programming in Rust from the ground up",
         "Udemy", "https://udemy.com/rust-fundamentals", "Beginner", "10 hours", 19.99),

        (41, "Next.js & React Server Components",
         "Build fast, SSR-powered React apps using Next.js and the latest server components",
         "Coursera", "https://coursera.org/nextjs-react", "Intermediate", "20 hours", 49.99),

        (42, "Advanced Angular Patterns",
         "Master state management, performance tuning, and testing in Angular",
         "Udemy", "https://udemy.com/angular-advanced", "Advanced", "18 hours", 39.99),

        (43, "WordPress Plugin Development",
         "Create custom WordPress plugins using PHP, hooks, and the REST API",
         "Skillshare", "https://skillshare.com/wp-plugin-dev", "Intermediate", "12 hours", 24.99),

        (44, "Flutter & Dart Deep Dive",
         "Build high-performance mobile apps with Flutter and Dart best practices",
         "Udemy", "https://udemy.com/flutter-dart-deep-dive", "Advanced", "25 hours", 29.99),

        (45, "Android Jetpack Compose",
         "Design Android UIs declaratively with Jetpack Compose",
         "Udacity", "https://udacity.com/android-jetpack-compose", "Intermediate", "15 hours", 199.00),

        (46, "SwiftUI for iOS Apps",
         "Build modern iOS interfaces using SwiftUI and Combine",
         "Ray Wenderlich", "https://rw.com/swiftui-ios", "Beginner", "12 hours", 0.00),

        (47, "Natural Language Processing Bootcamp",
         "Apply NLP pipelines with spaCy and NLTK to real-world text data",
         "Coursera", "https://coursera.org/nlp-bootcamp", "Advanced", "40 hours", 79.00),

        (48, "Computer Vision with OpenCV",
         "Process images and video with OpenCV and Python for real-time vision apps",
         "Udemy", "https://udemy.com/opencv-computer-vision", "Intermediate", "20 hours", 34.99),

        (49, "Reinforcement Learning A-Z",
         "Implement Q-Learning, Policy Gradients, and Deep RL algorithms in Python",
         "Udemy", "https://udemy.com/reinforcement-learning-az", "Advanced", "35 hours", 39.99),

        (50, "UX Research & Design",
         "Conduct user interviews, usability tests, and wireframe prototypes",
         "NNGroup", "https://nngroup.com/ux-research", "Beginner", "15 hours", 299.00),

        (51, "Adobe XD Masterclass",
         "Design and prototype interactive UIs with Adobe XD",
         "Skillshare", "https://skillshare.com/adobe-xd-masterclass", "Beginner", "10 hours", 15.00),

        (52, "3D Modeling with Blender",
         "Create 3D assets, textures, and animations in Blender",
         "Coursera", "https://coursera.org/blender-3d-modeling", "Intermediate", "20 hours", 49.99),

        (53, "Creative Writing: Storytelling",
         "Master narrative techniques to craft compelling short stories",
         "Udemy", "https://udemy.com/creative-writing-storytelling", "Beginner", "8 hours", 19.99),

        (54, "Technical Documentation for Developers",
         "Write clear API docs, tutorials, and user guides that devs love",
         "Pluralsight", "https://pluralsight.com/technical-documentation", "Intermediate", "12 hours", 29.99),

        (55, "SEO Writing Advanced Techniques",
         "Boost organic traffic by mastering on-page SEO and keyword strategy",
         "Coursera", "https://coursera.org/seo-writing-advanced", "Advanced", "15 hours", 39.00),

        (56, "Email Marketing Automation",
         "Set up drip campaigns, A/B testing, and segmentation in Mailchimp",
         "Udemy", "https://udemy.com/email-marketing-automation", "Intermediate", "10 hours", 24.99),

        (57, "Affiliate Marketing Mastery",
         "Scale affiliate revenue with niche research, funnels, and compliance",
         "Skillshare", "https://skillshare.com/affiliate-marketing-mastery", "Intermediate", "5 hours", 10.00),

        (58, "Google Analytics 4 Deep Dive",
         "Measure user behavior and conversions with GA4’s new data model",
         "Coursera", "https://coursera.org/ga4-deep-dive", "Advanced", "12 hours", 49.00),

        (59, "Video Motion Graphics with After Effects",
         "Animate shapes, text, and logos with Adobe After Effects",
         "LinkedIn Learning", "https://linkedin.com/learning/after-effects-motion-graphics",
         "Intermediate", "20 hours", 29.99),

        (60, "Podcast Production & Editing",
         "Record, edit, and publish professional-quality podcasts",
         "Udemy", "https://udemy.com/podcast-production-editing", "Beginner", "8 hours", 19.99),

        (61, "Negotiation Skills for Freelancers",
         "Negotiate rates, scope, and contracts confidently",
         "edX", "https://edx.org/negotiation-freelancers", "Beginner", "6 hours", 0.00),

        (62, "Sales Funnel Strategies",
         "Design high-converting funnels using email, ads, and landing pages",
         "Coursera", "https://coursera.org/sales-funnel-strategies", "Intermediate", "12 hours", 49.00),
    ]
    # then do:
    for c in new_courses:
        cursor.execute("""
                       INSERT INTO courses
                       (id, title, description, provider, url, difficulty_level, duration, price)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                       """, c)

    new_course_skills = [
        # BUSINESS COURSES
        (28, 63),  # Business Strategy → Business Analysis
        (28, 62),  # Business Strategy → Project Management

        (29, 66),  # Financial Modeling → Financial Analysis
        (29, 65),  # Financial Modeling → Accounting

        (30, 63),  # Lean Startup → Business Analysis
        (30, 62),  # Lean Startup → Project Management

        (31, 69),  # Leadership → HR Management
        (31, 62),  # Leadership → Project Management

        (32, 49),  # Digital Transformation → Digital Marketing
        (32, 63),  # Digital Transformation → Business Analysis

        # DATA SCIENCE COURSES
        (33, 31),  # Tableau → Tableau
        (33, 24),  # Tableau → Data Analysis

        (34, 29),  # Advanced SQL → Statistics
        (34, 24),  # Advanced SQL → Data Analysis

        (35, 29),  # Time Series → Statistics
        (35, 25),  # Time Series → Machine Learning

        (36, 25),  # Spark → Machine Learning
        (36, 24),  # Spark → Data Analysis

        (37, 25),  # AWS ML → Machine Learning
        (37, 26),  # AWS ML → Deep Learning

        (38, 1), (38, 24),  # Python Performance → Python, Data Analysis
        (39, 4),  # C# .NET Core → C#
        (40, 10),  # Rust Fundamentals → Rust
        (41, 12), (41, 15),  # Next.js → React, Node.js
        (42, 13),  # Advanced Angular → Angular
        (43, 18), (43, 5),  # WP Plugin → WordPress, PHP
        (44, 23),  # Flutter Deep Dive → Flutter
        (45, 21), (45, 8),  # Jetpack Compose → Android Dev, Kotlin
        (46, 20), (46, 7),  # SwiftUI → iOS Dev, Swift
        (47, 27),  # NLP Bootcamp → NLP
        (48, 28), (48, 26),  # OpenCV → Computer Vision, Deep Learning
        (49, 25), (49, 26),  # RL A-Z → ML, Deep Learning
        (50, 34), (50, 33),  # UX Research → UX, UI Design
        (51, 39), (51, 34),  # Adobe XD → Illustrator, UX Design
        (52, 35), (52, 37),  # Blender → Graphic Design, Illustration
        (53, 45),  # Storytelling → Creative Writing
        (54, 44),  # Tech Docs → Technical Writing
        (55, 46),  # SEO Writing Advanced → SEO Writing
        (56, 53), (56, 49),  # Email Automation → Email Marketing, Digital Marketing
        (57, 55),  # Affiliate Mastery → Affiliate Marketing
        (58, 56),  # GA4 → Google Analytics
        (59, 58), (59, 57),  # Motion Graphics → Animation, Video Editing
        (60, 60), (60, 59),  # Podcast Prod → Audio Editing, Voice Over
        (61, 67), (61, 68),  # Negotiation → Customer Service, Sales
        (62, 68), (62, 49),  # Sales Funnel → Sales, Digital Marketing
    ]
    # then do:
    for cs in new_course_skills:
        cursor.execute(
            "INSERT INTO course_skills (course_id, skill_id) VALUES (?,?)", cs
        )

    conn.commit()
    conn.close()
    print("✅ 25 new courses + mappings added!")


if __name__ == "__main__":
    main()
