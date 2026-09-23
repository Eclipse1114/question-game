import os
import random
import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIG & QUESTION DATA
# ---------------------------------------------------------
st.set_page_config(page_title="Question Game", page_icon="❓", layout="centered")

st.markdown("""
    <style>
        stApp {
            background-color: purple;
            color: cyan;
        }
    </style>
""", unsafe_allow_html=True)

fun_questions = [
    "If you won the lottery, what's the first thing you'd buy?",
    "What's your favorite hobby?",
    "If you could travel to any universe, in either a game, movie, or book, which would you choose?",
    "What's the weirdest food combination you actually enjoy?",
    "If you could have any animal as a fully domesticated pet, what would it be?",
    "What's a movie you can watch over and over again without getting tired of it?",
    "If you could instantly become an expert in any useless superpower, what would it be?",
    "What's the funniest or most embarrassing thing that happened to you in school?",
    "If you were a ghost, who is the first person you would go haunt?",
    "What's your absolute favorite season of the year and why?",
    "If you could only eat one meal for the rest of your life, what would you choose?",
    "What's the worst movie you've ever seen from start to finish?"
]

deep_questions = [
    "If you could instantly master any skill for your career, what would it be?",
    "If you could rewrite one law to whatever you wanted, what would the new law be?",
    "Are you currently in your dream job, or do you want to do something else?",
    "What is a piece of advice someone gave you that completely changed how you look at things?",
    "What do you think is the biggest challenge people face in your line of work?",
    "If you could go back five years, what is the one thing you would tell your past self?",
    "What is a major goal you want to achieve outside of your professional life in the next few years?",
    "Do you prefer having a strict daily routine, or do you work better when things are unpredictable?",
    "What is a belief or opinion you used to hold strongly but have completely changed your mind on?",
    "What motivates you to get up and keep going when you are having a rough week?",
    "If money was not a factor at all, how would you spend your day-to-day life?",
    "What is something you are still trying to figure out about yourself?"
]

relationship_questions = [
    "Describe your dream partner.",
    "What would the perfect date look like to you?",
    "If you could do anything with your partner for the next 48 hours, what would it be?",
    "What was your very first impression of me when we first met?",
    "What is your favorite memory that we have shared together so far?",
    "What is a small, everyday gesture that always makes you feel loved or appreciated?",
    "If we could pack up and move to any city in the world tomorrow, where would you want us to go?",
    "What is a new hobby or activity you've never tried but want us to do together?",
    "What song always makes you think of our relationship when you hear it?",
    "What is something I do that always manages to make you laugh, even when you're stressed?",
    "If we were contestants on a game show together, what would be our biggest strength as a team?",
    "What does a perfectly relaxing, low-key weekend look like for the two of us?"
]

categories = {
    "1": fun_questions,
    "2": deep_questions,
    "3": relationship_questions
}

category_names = {
    "1": "Fun",
    "2": "Deep / Career",
    "3": "Relationship"
}

SAVE_FILE = "Save.txt"

# ---------------------------------------------------------
# SAVE / LOAD FUNCTIONS
# ---------------------------------------------------------
def save_game():
    """Writes current game data to Save.txt"""
    with open(SAVE_FILE, "w") as file:
        file.write(f"{st.session_state.questions_asked}\n")
        file.write(f"{st.session_state.p1}\n")
        file.write(f"{st.session_state.p2}\n")
        file.write(f"{st.session_state.category}\n")
        file.write(f"{st.session_state.current_index}\n")

def load_game():
    """Reads Save.txt if present and returns the data"""
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as file:
                lines = [line.strip() for line in file.readlines()]
                if len(lines) >= 5:
                    return {
                        "questions_asked": int(lines[0]),
                        "p1": lines[1],
                        "p2": lines[2],
                        "category": lines[3],
                        "current_index": int(lines[4])
                    }
        except Exception:
            pass
    return None

# ---------------------------------------------------------
# INITIAL STATE & AUTO-LOAD
# ---------------------------------------------------------
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    
    saved_data = load_game()
    if saved_data:
        st.session_state.game_started = True
        st.session_state.questions_asked = saved_data["questions_asked"]
        st.session_state.p1 = saved_data["p1"]
        st.session_state.p2 = saved_data["p2"]
        st.session_state.category = saved_data["category"]
        st.session_state.current_index = saved_data["current_index"]
        
        q_list = categories.get(st.session_state.category, fun_questions)
        st.session_state.current_question = random.choice(q_list)
    else:
        st.session_state.game_started = False
        st.session_state.questions_asked = 0
        st.session_state.p1 = "Player 1"
        st.session_state.p2 = "Player 2"
        st.session_state.category = "1"
        st.session_state.current_index = 0
        st.session_state.current_question = ""

# ---------------------------------------------------------
# APP UI
# ---------------------------------------------------------
st.title("❓ Question Game")

# SCREEN 1: NEW GAME SETUP (If no save found or starting fresh)
if not st.session_state.game_started:
    st.subheader("Start New Game")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.p1 = st.text_input("Player 1 Name:", value=st.session_state.p1)
    with col2:
        st.session_state.p2 = st.text_input("Player 2 Name:", value=st.session_state.p2)

    cat_choice = st.selectbox(
        "Choose Category:",
        options=["1", "2", "3"],
        format_func=lambda x: f"{x} - {category_names[x]}"
    )
    st.session_state.category = cat_choice

    if st.button("🚀 Start Game", type="primary"):
        st.session_state.game_started = True
        st.session_state.questions_asked = 0
        st.session_state.current_index = 0
        
        q_list = categories.get(st.session_state.category, fun_questions)
        st.session_state.current_question = random.choice(q_list)
        
        # Save on start
        save_game()
        st.rerun()

# SCREEN 2: MAIN GAMEPLAY
else:
    players = [st.session_state.p1, st.session_state.p2]
    current_player = players[st.session_state.current_index]

    # Header Stats
    st.caption(f"📊 Questions asked so far: **{st.session_state.questions_asked}** | 💾 *Auto-saved to Save.txt*")
    
    # Mid-game category picker
    selected_cat = st.selectbox(
        "Current Category:",
        options=["1", "2", "3"],
        index=["1", "2", "3"].index(st.session_state.category),
        format_func=lambda x: f"{x} - {category_names[x]}"
    )
    
    # If category changed, update and save immediately
    if selected_cat != st.session_state.category:
        st.session_state.category = selected_cat
        save_game()

    # Question Display Card
    st.markdown("---")
    st.subheader(f"🗣️ {current_player}'s Turn:")
    st.info(f"**\"{st.session_state.current_question}\"**")
    st.markdown("---")

    # Game Controls
    col_next, col_reset = st.columns([2, 1])

    with col_next:
        if st.button("➡️ Next Question", type="primary"):
            # Advance question counter & switch players
            st.session_state.questions_asked += 1
            st.session_state.current_index = 1 - st.session_state.current_index
            
            # Get next random question
            q_list = categories.get(st.session_state.category, fun_questions)
            st.session_state.current_question = random.choice(q_list)
            
            # Save progress
            save_game()
            st.rerun()

    with col_reset:
        if st.button("🗑️ Reset / Delete Save"):
            if os.path.exists(SAVE_FILE):
                os.remove(SAVE_FILE)
            st.session_state.game_started = False
            st.rerun()
