import streamlit as st
import streamlit.components.v1 as components
import time
st.title("👑 RAJA MANTRI CHOR SIPAHI")
st.subheader("🏰 ROYAL COURT",text_alignment="center")
st.divider()
warriors=4
st.write(f"👥 Let's form a team of {warriors} players:")
first_player=st.text_input("Enter name of 1st player:",width=400)
second_player=st.text_input("Enter name of 2nd player:",width=400)
third_player=st.text_input("Enter name of 3rd player:",width=400)
fourth_player=st.text_input("Enter name of 4th player:",width=400)
players=[first_player,second_player,third_player,fourth_player]
if(st.button("Create Your Team",type="primary")):
    if all(players):
        st.session_state.scores={player:0 for player in players}
        st.success("Your team has been created..!")
    else:
        st.error("Enter names of all players..!")
st.divider()

# game logic
if "player_turn" not in st.session_state: # variable to track which player turn
    st.session_state.player_turn=1
if "game_start" not in st.session_state: # variable to track when game starts
    st.session_state.game_start=False
if "selected_chit" not in st.session_state: # variable to track chit selected
    st.session_state.selected_chit=False
if "player_chits" not in st.session_state: # variable to track each players chits
    st.session_state.player_chits={}
if "game_phase" not in st.session_state: # used to determine when to use tts
    st.session_state.game_phase="selection"
if "round_count" not in st.session_state: # for tracking the rounds
    st.session_state.round_count=0
if "tts_played" not in st.session_state:
    st.session_state.tts_played=False
st.subheader("ENTER TOTAL NUMBER OF GAME TURNS...")
game_turn=st.number_input("Your Game Turns Decide How Long Game Continues:",width=400)
if(st.button("START THE GAME",type="primary",)):
   st.session_state.game_start=True
if(st.session_state.game_start and st.session_state.round_count<game_turn):
        st.write("CHOOSE ONE OF THE CHIT:")
        col1,col2,col3,col4=st.columns(4)
        with col1:
            raja_btn=st.button("❓\nSECRET CHIT",key="raja",use_container_width=True,disabled="raja" in st.session_state.player_chits.values())
        with col2:
            mantri_btn=st.button("❓\nSECRET CHIT",key="mantri",use_container_width=True,disabled="mantri" in st.session_state.player_chits.values())
        with col3:
            chor_btn=st.button("❓\nSECRET CHIT",key="chor",use_container_width=True,disabled="chor" in st.session_state.player_chits.values())
        with col4:
            sipahi_btn=st.button("❓\nSECRET CHIT",key="sipahi",use_container_width=True,disabled="sipahi" in st.session_state.player_chits.values())
        chit_clicked=False
        if(st.session_state.player_turn<=warriors):
            st.write(f"🎮 Turn of player : {st.session_state.player_turn}")
            st.write(f"👤 Player Name : {players[st.session_state.player_turn-1]}")
            if raja_btn:
                st.session_state.player_chits[players[st.session_state.player_turn-1]]=st.session_state.selected_chit="raja"
                chit_clicked=True
            if mantri_btn:
                st.session_state.player_chits[players[st.session_state.player_turn-1]]=st.session_state.selected_chit="mantri"
                chit_clicked=True
            if chor_btn:
                st.session_state.player_chits[players[st.session_state.player_turn-1]]=st.session_state.selected_chit="chor"
                chit_clicked=True
            if sipahi_btn:
                st.session_state.player_chits[players[st.session_state.player_turn-1]]=st.session_state.selected_chit="sipahi"
                chit_clicked=True
            if(chit_clicked):
                st.session_state.player_turn+=1
        if(len(st.session_state.player_chits)==warriors):
            raja_player=next(player for player,role in st.session_state.player_chits.items() if role=="raja")
            mantri_player=next(player for player,role in st.session_state.player_chits.items() if role=="mantri")
            chor_player=next(player for player,role in st.session_state.player_chits.items() if role=="chor")
            sipahi_player=next(player for player,role in st.session_state.player_chits.items() if role=="sipahi")
            st.session_state.game_phase="dialogue"
        if(st.session_state.game_phase=="dialogue"):
            if not st.session_state.tts_played:
                raja_dialogue1="Mantri Mantri"
                mantri_dialogue="Ji huzoor..."
                raja_dialogue2="Chor ka pata lagao..."
                # generating speech using browswer tts

                components.html(
                f"""
                <script>
                    const speech1 = new SpeechSynthesisUtterance("{raja_dialogue1}");
                    const speech2 = new SpeechSynthesisUtterance("{mantri_dialogue}");
                    const speech3 = new SpeechSynthesisUtterance("{raja_dialogue2}");

                    speech1.lang = "hi-IN";
                    speech2.lang = "hi-IN";
                    speech3.lang = "hi-IN";

                    speech1.onend = () => window.speechSynthesis.speak(speech2);
                    speech2.onend = () => window.speechSynthesis.speak(speech3);

                    window.speechSynthesis.speak(speech1);
                </script>
                """,
                height=0
                )
            time.sleep(2)
            # mantri turns for guess between chor and sipahi
            candidate_1=next(player for player,role in st.session_state.player_chits.items() if role=="chor")
            candidate_2=next(player for player,role in st.session_state.player_chits.items() if role=="sipahi")
            st.subheader(f"{mantri_player} पता लगाओ, चोर कौन है और सिपाही कौन!")
            mantri_choice=st.radio(
                "Who do you think is Chor?",
                [candidate_1,candidate_2]
            )
            st.session_state.tts_played = True
            if(st.button("I found my Choice",type="primary")):
                if(st.session_state.player_chits[mantri_choice]=="chor"):
                    st.session_state.scores[raja_player]+=1000
                    st.session_state.scores[mantri_player]+=800
                    st.session_state.scores[chor_player]+=0
                    st.session_state.scores[sipahi_player]+=500
                else:
                    st.session_state.scores[raja_player]+=1000
                    st.session_state.scores[mantri_player]+=0
                    st.session_state.scores[chor_player]+=800
                    st.session_state.scores[sipahi_player]+=500
                st.write(f"Turn {st.session_state.round_count+1} ends up...!")
                st.session_state.round_count+=1
                # prepare for next round
                st.session_state.player_chits={}
                st.session_state.player_turn=1
                st.session_state.game_phase="selection"
                st.session_state.tts_played = False
        # scoring of game
if(st.button("REVEAL THE WINNER",type="primary",disabled=st.session_state.round_count<game_turn)):
    all_scores=list(st.session_state.scores.values())
    max_score=max(all_scores)
    winner=next(highest_player for highest_player,score in st.session_state.scores.items()
                if score==max_score)
    st.success(f"🏆 Congratulations! {winner}. You  are  Winner!!")
    st.subheader("****SCOREBOARD****")
    for key,value in st.session_state.scores.items():
        st.write(f"{key} : {value}")