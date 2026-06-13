"""
============================================================
Rule-Based AI Chatbot
DecodeLabs AI Internship Project - Project 1
Author   : Ayandip Sen
Version  : 1.0
Python   : 3.8+
============================================================

Architecture Overview:
    This chatbot uses a two-layer dictionary system:
        Layer 1 - Intent Map  : raw user phrase  → canonical intent key
        Layer 2 - Response DB : canonical key    → bot response string

    All logic is O(1) dictionary lookups — no if-elif chains.
"""

import sys
import datetime
from colorama import Fore, Style, init

# ── Initialise Colorama (autoreset prevents colour bleed between prints) ──────
init(autoreset=True)


# ══════════════════════════════════════════════════════════════════════════════
#  KNOWLEDGE BASE
# ══════════════════════════════════════════════════════════════════════════════

# ---------------------------------------------------------------------------
# RESPONSE DATABASE  →  canonical intent key : response string
# ---------------------------------------------------------------------------
RESPONSE_DB: dict[str, str] = {
    # Greetings
    "greeting": (
        "Hello! 👋  I'm RuleBot, your AI assistant from DecodeLabs. "
        "Type 'help' to see what I can do!"
    ),
    "morning": (
        "Good Morning! ☀️  Hope you have a fantastic and productive day ahead! "
        "How can I assist you today?"
    ),
    "afternoon": (
        "Good Afternoon! 🌤️  Hope your day is going well! "
        "What can I help you with?"
    ),
    "evening": (
        "Good Evening! 🌙  Hope you had a great day! "
        "What would you like to discuss?"
    ),
    # Identity
    "bot_identity": (
        "I am RuleBot — a Rule-Based AI Chatbot built for the DecodeLabs "
        "AI Internship Programme. I work on deterministic dictionary lookups "
        "rather than machine learning."
    ),
    "bot_name": (
        "My name is RuleBot! I was crafted as Project 1 of the DecodeLabs "
        "AI Internship. Nice to meet you! 😊"
    ),
    # Status
    "bot_status": (
        "I'm running perfectly, thank you for asking! ⚡  "
        "All systems nominal — ready to assist!"
    ),
    # Help
    "help": (
        "📋  Here's what I understand:\n"
        "  • Greetings     → hello / hi / hey / good morning / afternoon / evening\n"
        "  • About me      → who are you / what is your name\n"
        "  • My status     → how are you\n"
        "  • Topics        → python / ai / chatbot / internship / project / decode labs\n"
        "  • Gratitude     → thanks / thank you\n"
        "  • Exit          → bye / exit / quit / goodbye\n"
        "  • Fun           → joke / fact / motivation\n"
        "  • Date & Time   → what time is it / what is today"
    ),
    # Gratitude
    "gratitude": (
        "You're very welcome! 😊  It's my pleasure to help. "
        "Feel free to ask anything!"
    ),
    # Exit
    "farewell": (
        "Goodbye! 👋  Thanks for chatting with RuleBot. "
        "Keep learning and building amazing things! See you soon! 🚀"
    ),
    # Topic — Python
    "python": (
        "🐍  Python is a high-level, interpreted programming language renowned for "
        "its clean syntax and readability. Created by Guido van Rossum in 1991, it "
        "powers web development (Django/Flask), data science (NumPy/Pandas), "
        "machine learning (TensorFlow/PyTorch), and automation. It's the #1 "
        "language for AI/ML development!"
    ),
    # Topic — AI
    "ai": (
        "🤖  Artificial Intelligence (AI) is the simulation of human intelligence "
        "in machines. It encompasses Machine Learning, Deep Learning, NLP, Computer "
        "Vision, and Robotics. AI is transforming every industry — from healthcare "
        "to finance to self-driving cars. We're living in the AI revolution!"
    ),
    # Topic — Chatbot
    "chatbot": (
        "💬  A chatbot is a software application designed to simulate human "
        "conversation. Types include:\n"
        "  1. Rule-Based  → deterministic, dictionary/pattern driven (like me!)\n"
        "  2. ML-Based    → trained on data, uses intent classifiers\n"
        "  3. LLM-Based   → powered by GPT/Claude/Gemini etc.\n"
        "I am a Rule-Based chatbot — fast, predictable, and transparent!"
    ),
    # Topic — Internship
    "internship": (
        "🎓  The DecodeLabs AI Internship is a structured programme that takes you "
        "from Python fundamentals all the way to building production AI systems. "
        "Projects progress through: Rule-Based AI → NLP → ML → Deep Learning → LLMs. "
        "It's an excellent launchpad for an AI engineering career!"
    ),
    # Topic — Project
    "project": (
        "📁  This is Project 1 of the DecodeLabs AI Internship:\n"
        "  Title   : Rule-Based AI Chatbot\n"
        "  Goal    : Demonstrate deterministic AI via dictionary lookups\n"
        "  Tech    : Python 3, Colorama, datetime\n"
        "  Concepts: Control flow, hash maps, intent mapping, session analytics\n"
        "  Status  : ✅  Running successfully!"
    ),
    # Topic — DecodeLabs
    "decodelabs": (
        "🏢  DecodeLabs is an AI education and training organisation that equips "
        "engineers with practical, industry-ready AI skills. Through hands-on "
        "projects and mentorship, interns build real AI systems — from rule-based "
        "chatbots to LLM-powered assistants. Decode the future with AI! 🚀"
    ),
    # Fun — Joke
    "joke": (
        "😄  Why do programmers prefer dark mode?\n"
        "     Because light attracts bugs! 🐛\n\n"
        "     (Bonus: Why did Python win the race? "
        "Because it didn't need to compile!) 🐍"
    ),
    # Fun — Fact
    "fact": (
        "🧠  AI Fun Fact: The term 'Artificial Intelligence' was coined by "
        "John McCarthy in 1956 at the Dartmouth Conference — the same year "
        "the first AI programme, the Logic Theorist, was created by "
        "Allen Newell and Herbert Simon. AI is nearly 70 years old!"
    ),
    # Fun — Motivation
    "motivation": (
        "💪  Remember:\n"
        "  'The expert in anything was once a beginner.'\n\n"
        "  Every line of code you write, every bug you fix, and every concept "
        "you learn brings you one step closer to becoming an AI engineer. "
        "Keep going — you're doing great! 🌟"
    ),
    # Date / Time
    "current_time": "__DYNAMIC_TIME__",   # placeholder — filled at runtime
    "current_date": "__DYNAMIC_DATE__",   # placeholder — filled at runtime
    # Fallback (used programmatically; not in INTENT_MAP)
    "fallback": (
        "🤔  I'm not sure I understand that. Try typing 'help' to see "
        "what topics I can discuss! I'm always learning. 😊"
    ),
}


# ---------------------------------------------------------------------------
# INTENT MAP  →  user phrase (lowercase, stripped) : canonical key
# ---------------------------------------------------------------------------
INTENT_MAP: dict[str, str] = {
    # ── Greetings ──────────────────────────────────────────────────────────
    "hello"               : "greeting",
    "hi"                  : "greeting",
    "hey"                 : "greeting",
    "hiya"                : "greeting",
    "howdy"               : "greeting",
    "good morning"        : "morning",
    "gm"                  : "morning",
    "good afternoon"      : "afternoon",
    "good evening"        : "evening",
    "good night"          : "evening",
    # ── Identity ───────────────────────────────────────────────────────────
    "who are you"         : "bot_identity",
    "who r u"             : "bot_identity",
    "tell me about yourself": "bot_identity",
    "what are you"        : "bot_identity",
    "what is your name"   : "bot_name",
    "whats your name"     : "bot_name",
    "what's your name"    : "bot_name",
    "your name"           : "bot_name",
    # ── Status ─────────────────────────────────────────────────────────────
    "how are you"         : "bot_status",
    "how r u"             : "bot_status",
    "are you ok"          : "bot_status",
    "how do you do"       : "bot_status",
    # ── Help ───────────────────────────────────────────────────────────────
    "help"                : "help",
    "commands"            : "help",
    "what can you do"     : "help",
    "options"             : "help",
    "menu"                : "help",
    # ── Gratitude ──────────────────────────────────────────────────────────
    "thanks"              : "gratitude",
    "thank you"           : "gratitude",
    "thankyou"            : "gratitude",
    "thx"                 : "gratitude",
    "ty"                  : "gratitude",
    "cheers"              : "gratitude",
    # ── Exit ───────────────────────────────────────────────────────────────
    "bye"                 : "farewell",
    "goodbye"             : "farewell",
    "exit"                : "farewell",
    "quit"                : "farewell",
    "see you"             : "farewell",
    "see ya"              : "farewell",
    "cya"                 : "farewell",
    # ── Topics ─────────────────────────────────────────────────────────────
    "python"              : "python",
    "python language"     : "python",
    "what is python"      : "python",
    "tell me about python": "python",
    "ai"                  : "ai",
    "artificial intelligence": "ai",
    "what is ai"          : "ai",
    "tell me about ai"    : "ai",
    "chatbot"             : "chatbot",
    "what is a chatbot"   : "chatbot",
    "how do chatbots work": "chatbot",
    "internship"          : "internship",
    "decodelabs internship": "internship",
    "tell me about internship": "internship",
    "project"             : "project",
    "this project"        : "project",
    "about project"       : "project",
    "decode labs"         : "decodelabs",
    "decodelabs"          : "decodelabs",
    "what is decode labs" : "decodelabs",
    "about decodelabs"    : "decodelabs",
    # ── Fun ────────────────────────────────────────────────────────────────
    "joke"                : "joke",
    "tell me a joke"      : "joke",
    "funny"               : "joke",
    "make me laugh"       : "joke",
    "fact"                : "fact",
    "ai fact"             : "fact",
    "tell me a fact"      : "fact",
    "fun fact"            : "fact",
    "motivation"          : "motivation",
    "motivate me"         : "motivation",
    "inspire me"          : "motivation",
    "quote"               : "motivation",
    # ── Date / Time ────────────────────────────────────────────────────────
    "what time is it"     : "current_time",
    "current time"        : "current_time",
    "time"                : "current_time",
    "what time"           : "current_time",
    "what is today"       : "current_date",
    "today"               : "current_date",
    "date"                : "current_date",
    "what is the date"    : "current_date",
    "todays date"         : "current_date",
    "today's date"        : "current_date",
}

# ── Phrases that should trigger a clean exit ──────────────────────────────────
EXIT_INTENTS: frozenset[str] = frozenset({"farewell"})


# ══════════════════════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def display_banner() -> None:
    """
    Print the application startup banner to the terminal.

    Uses Colorama's Fore.YELLOW to highlight the banner and
    Fore.CYAN for the subtitle line so the welcome screen feels
    polished and is immediately distinguishable from conversation text.
    """
    banner = f"""
{Fore.YELLOW}{'=' * 52}
{'  RULE-BASED AI CHATBOT':^52}
{'  DecodeLabs AI Internship Project':^52}
{'  Version 1.0  |  Project 1':^52}
{'=' * 52}{Style.RESET_ALL}
{Fore.CYAN}  Type 'help' for commands  |  'exit' to quit{Style.RESET_ALL}
{Fore.YELLOW}{'=' * 52}{Style.RESET_ALL}
"""
    print(banner)


def get_time_greeting() -> str:
    """
    Return a time-appropriate greeting string based on the current hour.

    Time bands:
        00:00 – 11:59  →  Good Morning
        12:00 – 16:59  →  Good Afternoon
        17:00 – 23:59  →  Good Evening

    Returns:
        str: A greeting string with the appropriate salutation.
    """
    current_hour: int = datetime.datetime.now().hour

    if 0 <= current_hour < 12:
        salutation = "Good Morning ☀️"
    elif 12 <= current_hour < 17:
        salutation = "Good Afternoon 🌤️"
    else:
        salutation = "Good Evening 🌙"

    return (
        f"{salutation}! Welcome to RuleBot — your AI assistant from DecodeLabs.\n"
        f"  I'm here to help. Type 'help' to explore what I can do!"
    )


def sanitize_input(raw_input: str) -> str:
    """
    Clean and normalise raw user input for reliable dictionary lookup.

    Operations performed (in order):
        1. strip()      — remove leading / trailing whitespace
        2. lower()      — convert to lowercase for case-insensitive matching
        3. Replace smart/curly apostrophes with straight apostrophes so that
           phrases like "what's your name" match regardless of keyboard layout.

    Args:
        raw_input (str): The unprocessed string read from stdin.

    Returns:
        str: A clean, lowercase, stripped version of the input.
    """
    cleaned: str = raw_input.strip().lower()
    # Normalise curly apostrophes (e.g. from mobile keyboards)
    cleaned = cleaned.replace("\u2019", "'").replace("\u2018", "'")
    return cleaned


def get_response(user_input: str) -> tuple[str, bool]:
    """
    Resolve a user input string to the appropriate bot response.

    Algorithm:
        1. Look up user_input in INTENT_MAP  →  O(1) hash lookup
        2. If found, resolve the canonical key against RESPONSE_DB  →  O(1)
        3. Handle dynamic placeholders for time/date at runtime.
        4. If not found, return the fallback response.

    Args:
        user_input (str): Sanitised user input string.

    Returns:
        tuple[str, bool]:
            - str  : The response text to display.
            - bool : True if this response should end the session (exit intent).
    """
    # ── Step 1: intent resolution ─────────────────────────────────────────
    intent_key: str = INTENT_MAP.get(user_input, "fallback")

    # ── Step 2: response retrieval ────────────────────────────────────────
    response: str = RESPONSE_DB.get(intent_key, RESPONSE_DB["fallback"])

    # ── Step 3: runtime dynamic values ───────────────────────────────────
    if intent_key == "current_time":
        now = datetime.datetime.now()
        response = (
            f"🕐  Current time: {now.strftime('%I:%M %p')}  "
            f"({now.strftime('%H:%M')} in 24-hour format)"
        )
    elif intent_key == "current_date":
        now = datetime.datetime.now()
        response = (
            f"📅  Today is {now.strftime('%A, %d %B %Y')}  "
            f"(Day {now.timetuple().tm_yday} of {now.year})"
        )

    # ── Step 4: exit flag ─────────────────────────────────────────────────
    should_exit: bool = intent_key in EXIT_INTENTS

    return response, should_exit


def show_statistics(
    start_time: datetime.datetime,
    message_count: int,
    response_count: int,
) -> None:
    """
    Display session analytics when the chatbot exits.

    Metrics shown:
        - Session start timestamp
        - Session end timestamp
        - Total session duration (minutes and seconds)
        - Total user messages received
        - Total bot responses generated

    Args:
        start_time     (datetime.datetime): Timestamp when the session began.
        message_count  (int)              : Total user messages sent this session.
        response_count (int)              : Total bot responses generated.
    """
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    total_seconds = int(duration.total_seconds())
    minutes, seconds = divmod(total_seconds, 60)

    print(f"\n{Fore.YELLOW}{'=' * 52}")
    print(f"{'  SESSION ANALYTICS':^52}")
    print(f"{'=' * 52}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  🕐  Session Start    : {start_time.strftime('%Y-%m-%d  %I:%M:%S %p')}")
    print(f"  🕑  Session End      : {end_time.strftime('%Y-%m-%d  %I:%M:%S %p')}")
    print(f"  ⏱️   Duration         : {minutes} min {seconds} sec")
    print(f"  💬  Messages Sent    : {message_count}")
    print(f"  🤖  Responses Given  : {response_count}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'=' * 52}{Style.RESET_ALL}\n")


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    """
    Main chatbot loop — entry point of the application.

    Execution flow:
        1.  Display the welcome banner.
        2.  Print a time-appropriate greeting.
        3.  Record the session start timestamp.
        4.  Enter the continuous conversation loop:
              a. Prompt the user for input (Cyan).
              b. Sanitise the input.
              c. Skip empty input gracefully.
              d. Increment the message counter.
              e. Call get_response() for an O(1) lookup.
              f. Increment the response counter.
              g. Print the bot response (Green).
              h. If exit intent detected → break loop.
        5.  Display session analytics.
        6.  Exit cleanly.

    Error handling:
        - KeyboardInterrupt (Ctrl+C) is caught so the programme always
          displays statistics and exits gracefully instead of crashing.
        - A bare except catches any unforeseen runtime errors and prints
          a user-friendly message in Red before exiting.
    """
    # ── Setup ─────────────────────────────────────────────────────────────
    display_banner()
    time_greeting: str = get_time_greeting()
    print(f"{Fore.GREEN}  RuleBot  ›  {time_greeting}{Style.RESET_ALL}\n")

    session_start: datetime.datetime = datetime.datetime.now()
    message_count:  int = 0
    response_count: int = 0

    # ── Conversation loop ─────────────────────────────────────────────────
    try:
        while True:
            # ── Prompt ────────────────────────────────────────────────────
            try:
                raw: str = input(f"{Fore.CYAN}  You      ›  {Style.RESET_ALL}")
            except EOFError:
                # Handle piped input ending (non-interactive environments)
                break

            # ── Sanitise ──────────────────────────────────────────────────
            user_input: str = sanitize_input(raw)

            # ── Skip blanks ───────────────────────────────────────────────
            if not user_input:
                print(
                    f"{Fore.YELLOW}  RuleBot  ›  "
                    f"Please type something — I'm all ears! 👂{Style.RESET_ALL}\n"
                )
                continue

            # ── Count ─────────────────────────────────────────────────────
            message_count += 1

            # ── Lookup + respond ──────────────────────────────────────────
            response, should_exit = get_response(user_input)
            response_count += 1

            print(f"{Fore.GREEN}  RuleBot  ›  {response}{Style.RESET_ALL}\n")

            # ── Exit ──────────────────────────────────────────────────────
            if should_exit:
                break

    except KeyboardInterrupt:
        print(
            f"\n{Fore.RED}  [Interrupted]  "
            f"Session ended by keyboard interrupt.{Style.RESET_ALL}"
        )
    except Exception as error:  # noqa: BLE001
        print(
            f"\n{Fore.RED}  [Error]  An unexpected error occurred: {error}{Style.RESET_ALL}"
        )
        sys.exit(1)
    finally:
        # ── Always show analytics, regardless of how we exited ────────────
        show_statistics(session_start, message_count, response_count)


# ── Module guard ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
