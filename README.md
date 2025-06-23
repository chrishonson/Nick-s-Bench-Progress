Passing the AWS Certified Developer Exam: A Modern Study Strategy
Hi Team,

I recently passed the AWS Certified Developer - Associate (DVA-C02) exam. Finding myself with some downtime on the bench, I decided to focus on professional development and tackle this certification. Juggling this with family life required a focused and efficient approach, so I leaned heavily on a few AI tools to act as a dynamic study partner.

The strategy I landed on was a game-changer for me, and I wanted to share it for anyone else pursuing this or other certifications.

My AI-Powered Study Framework
My approach evolved as I discovered what worked best. I treated AI not just as a search engine, but as an on-demand tutor, a flashcard creator, and an interactive quiz master that I trained on my specific course materials.

Step 1: An Evolving Study Plan
I started by asking ChatGPT to make a study plan. The result was laughably ambitious because, as a generalist tool, it didn't appreciate that my extensive client-side experience meant I had foundational gaps in backend networking concepts like subnets and DNS. While I didn't realize just how ambitious the plan was all at once, my understanding evolved more in the later half of the effort, and I updated my plan regularly(“Plans are worthless, but planning is everything” - Dwight D. Eisenhower). I used Cursor (with Gemini 2.5 Pro) to create a dedicated study repo, which became my central hub for tracking progress and organizing my notes. The key first step was providing the AI with my study materials, which included the course slides from Stéphane Maarek's "Ultimate AWS Certified Developer Associate 2025 DVA-C02" on Udemy and the official AWS exam guide. This transformed it from a general tool into a subject matter expert with the exact same context I had.

Step 2: Active Recall and Deep-Dive Clarification
Instead of just passively reading, I used the AI to actively engage with the material. A notable advantage here was using ChatGPT's voice mode. There's something about verbally asking questions and listening to a subject matter expert that really pulls you into the material. I highly recommend using this if you feel you are in a study slump.

Action: After reviewing a topic, I'd ask specific, open-ended questions like, "Explain the difference between Cognito User Pools and Identity Pools," or "Why exactly can't you use a CNAME at the zone apex?"

Result: This forced me to articulate what I didn't understand and get immediate, detailed answers. We dove deep into the nuances of an IAM Policy vs. a Resource-Based Policy and why a GSI's throttling behavior can impact a base table—complex topics that are hard to grasp from static material alone.

Step 3: Memorization with AI-Generated Flashcards
This was a major game-changer for me. Rote memorization is tough (especially for me), but critical for the exam.

Action: I used Cursor (with Gemini 1.5 Pro) continuously throughout my studies to create digital flashcards for Anki, a popular spaced-repetition flashcard app.

Result: This was incredibly effective for memorizing key concepts, the differences between services (like Aurora vs. DynamoDB), service options, default values, limits, and other specific values that frequently appear on the exam.

Step 4: Interactive Quizzing and Targeted Feedback
For practice quizzes, I found that different models performed differently. I ultimately settled on using Gemini 1.5 Pro directly, as I felt its quiz generation was better than chatGPT.

Action: I would complete a quiz and feed my answers back into the chat.

Result: The AI provided a detailed breakdown of my strengths and areas for improvement with clear rationale. This created a dynamic, personalized study plan focused on my weak spots.

Step 5: Practical Application and Code Generation
To bridge theory and practice, I used the AI to help with hands-on tasks.

Action: I asked it to "Automate the creation of an ECS cluster... using a CloudFormation template." We then refined this template iteratively, discussing specific details like the need for an IamInstanceProfile.

Result: This solidified my understanding of Infrastructure as Code (IaC) and the practical details of service configuration, which is essential for this developer-focused exam.

Key Takeaways for Your Own Study
Recognize AI's Limitations: An AI won't know your personal knowledge gaps initially. Use its first plan as a starting point, but be ready to adapt as you identify your weaknesses.

Use the Right Tool for the Job: I found a mix of tools worked best: Cursor for repo management and flashcard creation, ChatGPT for engaging voice conversations, and Gemini 1.5 Pro for high-quality Q&A and quizzes.

Embrace Spaced Repetition: Creating Anki flashcards with AI is incredibly efficient and was a game-changer for memorization.

Leverage the Feedback Loop: Don't just take quizzes. Analyze the results with the AI to find and fix your knowledge gaps.

This approach made studying feel more like an interactive, one-on-one tutoring session and allowed me to make the most of my time.

Hope this helps you in your own certification journey. Good luck!

Best,

Chris Honson