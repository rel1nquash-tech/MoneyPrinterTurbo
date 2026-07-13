from app.trends.library import TopicAngle, TopicSeed, build_topic_library
from app.trends.registry import TrendTopic


_SEEDS = [
    TopicSeed("ChatGPT for brainstorming", "chatgpt", "ChatGPT can turn vague ideas into structured angles, outlines, and next steps.", ["chatgpt", "ideas", "productivity"]),
    TopicSeed("ChatGPT for email writing", "chatgpt", "Clear prompts help transform rough notes into concise replies, summaries, and follow-ups.", ["chatgpt", "email", "productivity"]),
    TopicSeed("ChatGPT for learning faster", "chatgpt", "AI tutors can explain concepts, quiz users, and adjust examples to their level.", ["chatgpt", "learning", "education"]),
    TopicSeed("ChatGPT for coding help", "chatgpt", "AI can explain errors, draft snippets, and suggest debugging paths when used carefully.", ["chatgpt", "coding", "developer"]),
    TopicSeed("ChatGPT memory and context", "chatgpt", "Useful answers depend on what the model is told and what context it can use.", ["chatgpt", "context", "prompt engineering"]),
    TopicSeed("AI meeting summaries", "productivity", "Meeting tools can capture decisions, owners, and follow-ups from long conversations.", ["productivity", "meetings", "ai tools"]),
    TopicSeed("AI calendar planning", "productivity", "AI scheduling can group tasks, protect focus time, and reduce planning friction.", ["productivity", "calendar", "automation"]),
    TopicSeed("AI note-taking systems", "productivity", "AI notes become more useful when they connect ideas, actions, and searchable context.", ["productivity", "notes", "workflow"]),
    TopicSeed("AI research assistants", "productivity", "Research workflows improve when AI summarizes, compares, and organizes source material.", ["productivity", "research", "ai tools"]),
    TopicSeed("AI personal knowledge bases", "productivity", "AI search over personal notes can surface old ideas exactly when they matter.", ["productivity", "knowledge management", "ai tools"]),
    TopicSeed("AI image generators", "ai-tools", "Image models convert text prompts into visuals for concepts, ads, thumbnails, and design drafts.", ["ai tools", "image generation", "creative"]),
    TopicSeed("AI video generators", "ai-tools", "Video models can speed up ideation, storyboards, b-roll concepts, and short-form clips.", ["ai tools", "video", "creative"]),
    TopicSeed("AI voice cloning", "ai-tools", "Voice tools create narration workflows but also raise consent and identity questions.", ["ai tools", "voice", "ethics"]),
    TopicSeed("AI transcription tools", "ai-tools", "Speech-to-text turns audio and video into searchable, editable material.", ["ai tools", "transcription", "productivity"]),
    TopicSeed("AI spreadsheet assistants", "ai-tools", "AI can explain formulas, clean data, and generate simple analysis workflows.", ["ai tools", "spreadsheets", "productivity"]),
    TopicSeed("AI browser agents", "automation", "Browser agents can navigate websites, gather information, and complete repetitive steps.", ["automation", "agents", "workflow"]),
    TopicSeed("AI workflow automation", "automation", "Combining triggers, actions, and AI decisions can remove repetitive manual work.", ["automation", "workflow", "productivity"]),
    TopicSeed("AI customer support bots", "automation", "Support bots can answer common questions while routing edge cases to humans.", ["automation", "support", "business"]),
    TopicSeed("AI data entry automation", "automation", "AI can extract fields from messy documents and move them into structured systems.", ["automation", "data entry", "business"]),
    TopicSeed("AI content repurposing", "automation", "One long asset can become clips, captions, summaries, and newsletters with AI help.", ["automation", "content", "marketing"]),
    TopicSeed("future AI assistants", "future-of-ai", "Assistants may become proactive collaborators that plan, remember, and execute tasks.", ["future of ai", "assistants", "agents"]),
    TopicSeed("AI in education", "future-of-ai", "AI tutors could personalize practice while teachers focus on judgment and motivation.", ["future of ai", "education", "learning"]),
    TopicSeed("AI in healthcare", "future-of-ai", "AI may help with triage, documentation, imaging support, and patient communication.", ["future of ai", "healthcare", "ethics"]),
    TopicSeed("AI in creative work", "future-of-ai", "Creative teams can use AI for drafts, variations, references, and rapid experimentation.", ["future of ai", "creative", "ai tools"]),
    TopicSeed("AI and jobs", "future-of-ai", "AI changes tasks before it changes entire jobs, making adaptation the key story.", ["future of ai", "jobs", "automation"]),
    TopicSeed("prompt structure", "prompt-engineering", "Better prompts define role, task, context, constraints, examples, and output format.", ["prompt engineering", "prompts", "chatgpt"]),
    TopicSeed("few-shot prompting", "prompt-engineering", "Examples teach the model the pattern faster than abstract instructions alone.", ["prompt engineering", "examples", "chatgpt"]),
    TopicSeed("chain-of-thought alternatives", "prompt-engineering", "Asking for concise reasoning summaries can improve usefulness without exposing hidden reasoning.", ["prompt engineering", "reasoning", "chatgpt"]),
    TopicSeed("prompt constraints", "prompt-engineering", "Constraints like length, tone, audience, and format make outputs easier to use.", ["prompt engineering", "workflow", "chatgpt"]),
    TopicSeed("prompt iteration", "prompt-engineering", "Strong AI workflows improve prompts through critique, revision, and comparison.", ["prompt engineering", "iteration", "productivity"]),
    TopicSeed("AI hallucinations", "ai-tools", "Models can sound confident while being wrong, so verification remains essential.", ["ai tools", "accuracy", "risk"]),
    TopicSeed("AI privacy basics", "ai-tools", "Users should understand what data they upload and how tools may store or process it.", ["ai tools", "privacy", "security"]),
    TopicSeed("AI model context windows", "chatgpt", "Context windows define how much information a model can consider at one time.", ["chatgpt", "context", "model basics"]),
    TopicSeed("AI agents versus chatbots", "automation", "Agents use tools and take steps, while chatbots mostly respond inside conversation.", ["automation", "agents", "ai tools"]),
    TopicSeed("AI for small businesses", "productivity", "Small teams can use AI for support, content, operations, and faster internal drafting.", ["productivity", "business", "automation"]),
    TopicSeed("AI for creators", "ai-tools", "Creators can use AI to ideate hooks, scripts, thumbnails, captions, and edits.", ["ai tools", "creators", "shorts"]),
    TopicSeed("AI ethics basics", "future-of-ai", "Bias, consent, transparency, and accountability shape whether AI is trusted.", ["future of ai", "ethics", "trust"]),
    TopicSeed("AI regulation", "future-of-ai", "Governments are trying to balance innovation, safety, competition, and consumer protection.", ["future of ai", "regulation", "policy"]),
    TopicSeed("open-source AI models", "ai-tools", "Open models give developers more control over deployment, privacy, and customization.", ["ai tools", "open source", "models"]),
    TopicSeed("multimodal AI", "future-of-ai", "Models that understand text, images, audio, and video unlock broader workflows.", ["future of ai", "multimodal", "ai tools"]),
]

_ANGLES = [
    TopicAngle("{label}: the Shorts version", "Here is the simple version people actually remember.", "Create a concise explainer about {label}: {detail}", ["explainer", "shorts"]),
    TopicAngle("The best use case for {label}", "This is where AI saves real time instead of just sounding impressive.", "Show a practical workflow involving {label}: {detail}", ["use case", "productivity"]),
    TopicAngle("The hidden risk in {label}", "AI is useful, but this mistake can ruin the output.", "Explain the main caution or limitation around {label}: {detail}", ["risk", "ai literacy"]),
    TopicAngle("How to try {label} today", "You do not need a huge setup to test this idea.", "Give a simple offline-friendly script angle for testing {label}: {detail}", ["how to", "workflow"]),
    TopicAngle("What {label} means for the future", "The real story is how the workflow changes next.", "Connect {label} to a future-of-work or future-of-AI lesson: {detail}", ["future of ai", "analysis"]),
]

_VOICES = [
    "clear AI educator",
    "practical productivity guide",
    "future-tech narrator",
    "calm automation coach",
]

_TOPICS = build_topic_library("ai", _SEEDS, _ANGLES, _VOICES)


def get_daily_topics(limit: int) -> list[TrendTopic]:
    return _TOPICS[: max(limit, 0)]
