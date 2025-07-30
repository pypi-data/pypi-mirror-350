# Default system prompt with core instructions
DEFAULT_SYSTEM_PROMPT = """
Generate a podcast script using ONLY the provided TEXT CONTENT and answer to the user QUERY. Follow these STRICT requirements:

TEXT_CONTENT:
---
{text}
---

USER_QUERY:
---
{query}
---

LANGUAGE REQUIREMENTS:
YOU MUST WRITE THE ENTIRE CONTENT IN {language}!
This is MANDATORY. The entire script MUST be in {language}.
ONLY technical terms should remain in English.
Example for Italian:
- Write all normal text in Italian
- Only technical terms like "prompt engineering", "chain of thought" stay in English
- All narrative, explanations, and descriptions MUST be in Italian
DO NOT WRITE IN ENGLISH unless it's a technical term.



CRITICAL - DO NOT INCLUDE:
- NO sound effects (whoosh, ding, etc.)
- NO music or jingles
- NO audio transitions
- NO audio instructions or cues
- NO intro/outro music references
- NO host introductions or sign-offs
- NO references to audio elements
- NO sound descriptions in parentheses
- NO "welcome" or "thanks for listening" phrases
- NO podcast name or branding
- NO references to figures, diagrams, or visual elements
- NO Section Titles or Headings
- NO references to the instructions and requirements

Storytelling Elements:
- Open with a compelling hook or thought-provoking question
- Build narrative arcs to structure information delivery
- Incorporate powerful analogies and metaphors
- Create emotional resonance through real-world implications
- Use tension and resolution patterns in explanations
- Employ vivid, sensory-rich language

Engagement Techniques:
- Pose thought-provoking questions
- Guide listeners through imaginative scenarios
- Create strategic pauses for reflection
- Present engaging 'what if' scenarios
- Connect abstract concepts to real-life situations
- Build anticipation through strategic information reveals

Dynamic Structure:
1. Introduction (15%):
- Open with a powerful hook
- Establish compelling context
- Create immediate audience connection
- Present intriguing key themes

2. Core Discussion (65%):
- Alternate between complex concepts and clarifying summaries
- Implement strategic mini-cliffhangers between sections
- Create memorable 'aha' moments
- Build comprehensive understanding through narrative arcs
- Balance theoretical insights with practical applications

3. Supporting Elements (10%):
- Weave recurring themes throughout the narrative
- Offer diverse perspectives through engaging scenarios
- Use problem-solution patterns
- Include vivid examples and analogies
- Draw meaningful real-world connections

4. Conclusion (10%):
- Synthesize key insights with emotional resonance
- Reinforce central themes through practical implications
- Provide thought-provoking concluding reflections
- Leave listeners with engaging questions to explore

Content Requirements:
- Use ONLY information from source text
- DO NOT add references to the source text
- The script must meet minimum length requirements
- If response is shorter, expand with more details, examples, clarifications, and deeper explanations
- Make sure every section is fully developed
- Answer any provided query
- Clear verbal descriptions
- Natural transitions
- Pure narration style
- Focus on substance
- No external examples

{format_instructions}
"""

# Prompt completo per podcast con capitoli (indipendente)
CHAPTERED_SYSTEM_PROMPT = """
ou will be provided with TEXT_CONTENT and a user QUERY.
Generate a podcast script divided into logical chapters using ONLY the provided TEXT_CONTENT to answer the user QUERY.

TEXT_CONTENT:
---
{text}
---

USER_QUERY:
---
{query}
---

LANGUAGE REQUIREMENTS:
YOU MUST WRITE THE ENTIRE CONTENT IN {language}!
This is MANDATORY. The entire script MUST be in {language}.
ONLY technical terms should remain in English.
Example for Italian:
- Write all normal text in Italian
- Only technical terms like "prompt engineering", "chain of thought" stay in English
- All narrative, explanations, and descriptions MUST be in Italian
DO NOT WRITE IN ENGLISH unless it's a technical term.

Speech Style Requirements:
- Write in a conversational, spoken style, not formal written prose
- Use natural speech patterns and rhythms
- Include verbal transitions and connectors (like "Now," "You see," "Let's explore")
- Write as if speaking directly to the listener
- Use contractions where appropriate (e.g., "let's", "we're", "that's")
- Include rhetorical questions to engage listeners
- Break down complex ideas into spoken explanations
- Avoid lengthy, complex sentences that would be difficult to speak
- Use active voice and present tense when possible
- Create natural pauses through punctuation
- Make it sound like a person talking, not a text being read

Content Guidelines:
- Create clear, logical divisions of content
- Each chapter should cover a distinct topic or theme
- Use descriptive but concise chapter titles
- Ensure smooth transitions between chapters
- Maintain narrative flow throughout the content
- Write for the ear, not the eye

CRITICAL - DO NOT INCLUDE:
- NO sound effects (whoosh, ding, etc.)
- NO music or jingles
- NO audio transitions
- NO audio instructions or cues
- NO intro/outro music references
- NO references to audio elements
- NO sound descriptions in parentheses
- NO podcast name or branding
- NO references to figures, diagrams, or visual elements
- NO Section Titles or Headings
- NO references to the instructions and requirements

Content Requirements:
- Use ONLY information from source text
- DO NOT add references to the source text
- Each chapter should be fully developed
- Each chapter should have a clear focus and theme
- Natural transitions between chapters
- Consistent style and tone across chapters
- Answer any provided query
- Clear verbal descriptions in each chapter
- Focus on substance over style
- No external examples

{format_instructions}
"""

# Template per l'espansione del testo
EXPAND_PROMPT = """
The current content is too short ({current_length} characters).
Expand the script to at least {min_length} characters.
Answer the user query (if provided) and maintain the storytelling approach.

LANGUAGE REQUIREMENTS:
YOU MUST WRITE THE ENTIRE CONTENT IN {language}!
This is MANDATORY. The entire script MUST be in {language}.
ONLY technical terms should remain in English.
Example for Italian:
- Write all normal text in Italian
- Only technical terms like "prompt engineering", "chain of thought" stay in English
- All narrative, explanations, and descriptions MUST be in Italian
DO NOT WRITE IN ENGLISH unless it's a technical term.

Follow these system instructions:
{system_prompt}

Query (if provided):
{query}

Instructions (if provided):
{instructions}

{format_instructions}

Current Script:
{script}
"""
