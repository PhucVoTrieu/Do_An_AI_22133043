import streamlit as st
import tictactoe as ttt
import time
# Initialize game state

if 'board' not in st.session_state:
    st.balloons()
    st.session_state.board = ttt.initial_state()
    st.session_state.user = None
    st.session_state.user_turn = False

mm =      """
            <style>
            .stButton>button {
  display: inline-block;
  padding: 15px 25px;
  font-size: 75px;
  height: 75px;  
  width: 100px; 
  cursor: pointer;
  text-align: center;
  text-decoration: none;
  outline: none;
  color: #9932CC;
  background-color: white;
  border: none;
  border-radius: 15px;
  box-shadow: 3px 3px 3px 3px gray;
}

.stButton>button:hover {
    background-color: #9932CC
     
    }

.stButton>button:active {
  background-color: pink; 
  box-shadow: 0 5px #666;
  transform: translateY(4px);
}
            </style>
            """                 
#
def draw():
    # Define custom CSS for X and O    04AA6D
    st.markdown(mm,unsafe_allow_html=True)
    cols = st.columns(6)
    for i in range(0,3):
        for j in range(0,3):
            with cols[j]:
                if board[i][j] == ttt.EMPTY:
                  if st.button("", key=f"{i}-{j}",use_container_width=True) and st.session_state.user_turn == True:
                        user_move(i, j)
                        st.rerun()
                else:
                   
                    if board[i][j] == 'X':
                        
                        st.button("❌", key=f"{i}-{j}",use_container_width=True) 
                    elif board[i][j] == 'O':
                       st.button("⭕", key=f"{i}-{j}",use_container_width=True) 
                        
                                      
def reset_game():
    st.session_state.board = ttt.initial_state()
    st.session_state.user = None
    st.session_state.user_turn = False

def ai_move():
    if st.session_state.user != ttt.current_player(st.session_state.board) and not ttt.terminal(st.session_state.board):
        move = ttt.minimax(st.session_state.board)
        st.session_state.board = ttt.result(st.session_state.board, move)

def user_move(i, j):
    if st.session_state.user == ttt.current_player(st.session_state.board) and not ttt.terminal(st.session_state.board):
        if st.session_state.board[i][j] == ttt.EMPTY:
            st.session_state.board = ttt.result(st.session_state.board, (i, j))
            st.session_state.user_turn = False
            st.rerun()

st.title("Tic-Tac-Toe")

if st.session_state.user is None:
    st.subheader("Choose your player:")
    col = st.columns(5)                 
    with col[0]:
        b = st.button("Play as X ")
        if b:
            st.session_state.user = ttt.X
            st.session_state.user_turn=True 
            st.rerun()
    with col[1]:
        b = st.button("Play as O " )
        if b:
            st.session_state.user = ttt.O
            st.session_state.user_turn=False
            st.rerun()
else:
    
    board = st.session_state.board
    game_over = ttt.terminal(board)
    player = st.session_state.user_turn
    if game_over:
        st.balloons()
        draw()
        winner = ttt.winner(board)
        if winner is None:
            st.header("Game Over: Tie.")
        else:
            st.header(f"Game Over: {winner} wins.")
        if st.button("Play Again"):
            reset_game()
            st.rerun()
    else:
        if st.session_state.user_turn==True:
            st.header(f"Play as {st.session_state.user}")
            draw()

        else:
            st.header("Computer thinking...")
            draw()
            if st.session_state.user_turn==False:
                time.sleep(0.5)
                ai_move()
                st.session_state.user_turn = True
                st.rerun()
   
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://img.freepik.com/free-vector/background-horizon-futuristic_23-2148310639.jpg?t=st=1716049487~exp=1716053087~hmac=4a12dec6db36dc123818f23b31d906402bd1013fea816535161fcf1107cf55a3&w=996");
background-size:  cover;
background-position: center center;
background-repeat: no-repeat;
background-attachment: local;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

