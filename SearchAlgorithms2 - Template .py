import heapq
import streamlit as st
import time

class Node:
    def __init__(self, value):
        self.value = value
        self.state = value
        self.parentstate = None
        self.action = None
        self.edgeCost = 0
        self.gOfN = 0  
        self.hOfN = 0  
        self.heuristicFn = None

def get_successors(state):
    successors = []
    idx = state.index(0)
    row, col = divmod(idx, 3)
    
    moves = {
        'Down': (row - 1, col),   
        'Up': (row + 1, col),     
        'Right': (row, col - 1), 
        'Left': (row, col + 1)   
    }
    
    for action, (r, c) in moves.items():
        if 0 <= r < 3 and 0 <= c < 3:
            new_idx = r * 3 + c
            new_state = list(state)
            new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
            successors.append((action, new_state))
            
    return successors

def h1_misplaced(state, goal):
    return sum(1 for s, g in zip(state, goal) if s != g and s != 0)

def h2_manhattan(state, goal):
    total = 0
    for i, tile in enumerate(state):
        if tile == 0:
            continue
        goal_i = goal.index(tile)
        total += abs(i // 3 - goal_i // 3) + abs(i % 3 - goal_i % 3)
    return total

def h3_linear_conflict(state, goal):
    conflict_count = 0
    total = h2_manhattan(state, goal)
    
    # Rows
    for row in range(3):
        row_tiles = [state[row*3 + col] for col in range(3) if state[row*3 + col] != 0]
        for i in range(len(row_tiles)):
            for j in range(i+1, len(row_tiles)):
                t1, t2 = row_tiles[i], row_tiles[j]
                if goal.index(t1)//3 == row and goal.index(t2)//3 == row:
                    if goal.index(t1) > goal.index(t2):
                        conflict_count += 1
    # Cols
    for col in range(3):
        col_tiles = [state[row*3 + col] for row in range(3) if state[row*3 + col] != 0]
        for i in range(len(col_tiles)):
            for j in range(i+1, len(col_tiles)):
                t1, t2 = col_tiles[i], col_tiles[j]
                if goal.index(t1)%3 == col and goal.index(t2)%3 == col:
                    if goal.index(t1) > goal.index(t2):
                        conflict_count += 1
                        
    return total + 2 * conflict_count

class SearchAlgorithms:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.Path = []
        self.fullPath = []
        self.totalCost = -1

    def search(self, mode, heuristic_func=h2_manhattan):
        start_node = Node(self.start)
        start_node.gOfN = 0
        start_node.hOfN = heuristic_func(self.start, self.end)
        
        counter = 0
        
        if mode == 'BFS' or mode == 'DFS':
            frontier = [start_node]
        else:
            if mode == 'UCS':
                f = start_node.gOfN
            elif mode == 'Astar':
                f = start_node.gOfN + start_node.hOfN
            elif mode == 'Greedy':
                f = start_node.hOfN
            frontier = [(f, counter, start_node)]
            
        explored = set()
        
        while frontier:
            if mode == 'BFS':
                current = frontier.pop(0)
            elif mode == 'DFS':
                current = frontier.pop()
            else:
                _, _, current = heapq.heappop(frontier)
            
            if current.state == self.end:
                path_actions = []
                path_states = []
                cost = current.gOfN
                
                curr = current
                while curr:
                    if curr.action:
                        path_actions.append(curr.action)
                    path_states.append(curr.state)
                    curr = curr.parentstate
                    
                path_actions.reverse()
                path_states.reverse()
                
                self.Path = path_actions
                self.fullPath = path_states
                self.totalCost = cost
                return self.Path, self.fullPath, self.totalCost
                
            state_tuple = tuple(current.state)
            if state_tuple in explored:
                continue
            explored.add(state_tuple)
            
            for action, next_state in get_successors(current.state):
                if tuple(next_state) in explored:
                    continue
                    
                next_node = Node(next_state)
                next_node.parentstate = current
                next_node.action = action
                next_node.edgeCost = 1
                next_node.gOfN = current.gOfN + 1
                next_node.hOfN = heuristic_func(next_state, self.end)
                
                if mode in ['BFS', 'DFS']:
                    frontier.append(next_node)
                else:
                    if mode == 'UCS':
                        f = next_node.gOfN
                    elif mode == 'Astar':
                        f = next_node.gOfN + next_node.hOfN
                    elif mode == 'Greedy':
                        f = next_node.hOfN
                    counter += 1
                    heapq.heappush(frontier, (f, counter, next_node))
                
        return [], [], -1

    def UCS(self):
        return self.search('UCS')

    def Astar(self, heuristic_func=h2_manhattan):
        return self.search('Astar', heuristic_func)

    def Greedy(self, heuristic_func=h2_manhattan):
        return self.search('Greedy', heuristic_func)
        
    def BFS(self):
        return self.search('BFS')
        
    def DFS(self):
        return self.search('DFS')

def main():
    s3 = SearchAlgorithms([1, 2, 3, 4, 0, 6, 7, 5, 8], [1,2,3,4,5,6,7,8,0])
    path, fullPath, cost = s3.UCS()
    print('UCS Path: ' + str(path), end='\nFull Path is: ')
    print(fullPath)
    print(" + total Cost = " + str(cost))

    s4 = SearchAlgorithms([1, 2, 3, 4, 0, 6, 7, 5, 8], [1,2,3,4,5,6,7,8,0])
    path, fullPath, cost = s4.Astar()
    print('AstarHeuristic Path: ' + str(path), end='\nFull Path is: ')
    print(fullPath)
    print(" + total Cost = " + str(cost))

    s4 = SearchAlgorithms([1, 2, 3, 4, 0, 6, 7, 5, 8], [1,2,3,4,5,6,7,8,0])
    path, fullPath, cost = s4.Greedy()
    print('GreedyHeuristic Path: ' + str(path), end='\nFull Path is: ')
    print(fullPath)
    print(" + total Cost = " + str(cost))

main()

# ──────────────────────────────────────────────────────────────
# Streamlit GUI
# ──────────────────────────────────────────────────────────────

def render_grid_html(state, goal=None, size=52):
    """Render a 3x3 puzzle grid as styled HTML."""
    html = f'<table style="border-collapse:collapse;margin:0 auto;">'
    for i in range(3):
        html += '<tr>'
        for j in range(3):
            tile = state[i * 3 + j]
            if tile == 0:
                bg = "#1a1a2e"
                color = "transparent"
                border_color = "#2d2d4a"
                txt = ""
            else:
                is_correct = goal and tile == goal[i * 3 + j]
                if is_correct:
                    bg = "linear-gradient(135deg, #00b894, #00cec9)"
                    border_color = "#00b894"
                else:
                    bg = "linear-gradient(135deg, #6c5ce7, #a29bfe)"
                    border_color = "#6c5ce7"
                color = "#fff"
                txt = str(tile)
            html += (
                f'<td style="width:{size}px;height:{size}px;text-align:center;'
                f'vertical-align:middle;font-size:{size//2}px;font-weight:700;'
                f'font-family:Inter,sans-serif;color:{color};'
                f'background:{bg};border:2px solid {border_color};'
                f'border-radius:10px;padding:0;">{txt}</td>'
            )
        html += '</tr>'
    html += '</table>'
    return html

st.set_page_config(page_title="8‑Puzzle Solver", page_icon="🧩", layout="wide")

# ── Custom CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

/* Global */
.stApp {
    font-family: 'Inter', sans-serif;
}

/* Header */
.main-header {
    text-align: center;
    padding: 1.5rem 0 0.5rem 0;
}
.main-header h1 {
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6c5ce7, #a29bfe, #00cec9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}
.main-header p {
    color: #888;
    font-size: 1rem;
    margin-top: 0;
}

/* Cards */
.card {
    background: rgba(30, 30, 50, 0.6);
    border: 1px solid rgba(108, 92, 231, 0.25);
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
    backdrop-filter: blur(12px);
    margin-bottom: 1rem;
}
.card h3 {
    font-size: 1rem;
    font-weight: 700;
    color: #a29bfe;
    margin: 0 0 0.8rem 0;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* Algorithm info cards */
.algo-card {
    background: rgba(30, 30, 50, 0.55);
    border: 1px solid rgba(108, 92, 231, 0.2);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    transition: transform 0.2s, border-color 0.2s;
}
.algo-card:hover {
    transform: translateY(-2px);
    border-color: rgba(108, 92, 231, 0.5);
}
.algo-card.active {
    border: 2px solid #6c5ce7;
    background: rgba(108, 92, 231, 0.12);
}
.algo-card .algo-name {
    font-size: 1.1rem;
    font-weight: 700;
    color: #e0e0e0;
}
.algo-card .algo-formula {
    font-family: 'Courier New', monospace;
    font-size: 0.85rem;
    color: #a29bfe;
    margin: 0.4rem 0;
    padding: 0.3rem 0.6rem;
    background: rgba(0,0,0,0.3);
    border-radius: 6px;
    display: inline-block;
}
.algo-card .algo-tag {
    display: inline-block;
    padding: 0.15rem 0.5rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}
.tag-optimal { background: rgba(0, 184, 148, 0.2); color: #00b894; }
.tag-suboptimal { background: rgba(253, 121, 168, 0.2); color: #fd79a8; }

.algo-detail {
    font-size: 0.78rem;
    color: #999;
    line-height: 1.6;
    text-align: left;
    margin-top: 0.5rem;
}
.algo-detail span { color: #e0e0e0; font-weight: 600; float: right; }

/* Heuristic bars */
.h-bar-container {
    margin: 0.4rem 0;
}
.h-bar-label {
    font-size: 0.82rem;
    color: #ccc;
    margin-bottom: 3px;
    display: flex;
    justify-content: space-between;
}
.h-bar-label .h-val {
    font-weight: 700;
    color: #fff;
    background: rgba(108,92,231,0.3);
    padding: 0 8px;
    border-radius: 10px;
    font-size: 0.78rem;
}
.h-bar-track {
    background: rgba(255,255,255,0.06);
    border-radius: 6px;
    height: 8px;
    overflow: hidden;
}
.h-bar-fill {
    height: 100%;
    border-radius: 6px;
    transition: width 0.4s ease;
}
.h-bar-fill.h1 { background: linear-gradient(90deg, #e17055, #fdcb6e); }
.h-bar-fill.h2 { background: linear-gradient(90deg, #0984e3, #74b9ff); }
.h-bar-fill.h3 { background: linear-gradient(90deg, #00b894, #55efc4); }

.dominance-tag {
    text-align: center;
    font-size: 0.78rem;
    margin-top: 0.6rem;
    padding: 0.35rem 0.7rem;
    border-radius: 8px;
}
.dominance-pass {
    background: rgba(0,184,148,0.15);
    color: #00b894;
    border: 1px solid rgba(0,184,148,0.3);
}
.dominance-fail {
    background: rgba(253,121,168,0.15);
    color: #fd79a8;
    border: 1px solid rgba(253,121,168,0.3);
}

/* Step cards */
.step-card {
    background: rgba(30,30,50,0.5);
    border: 1px solid rgba(108,92,231,0.15);
    border-radius: 14px;
    padding: 0.7rem;
    text-align: center;
    margin-bottom: 0.5rem;
}
.step-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #a29bfe;
    margin-bottom: 0.4rem;
}
.step-action {
    font-size: 0.68rem;
    color: #74b9ff;
    background: rgba(9,132,227,0.15);
    display: inline-block;
    padding: 0.1rem 0.5rem;
    border-radius: 10px;
    margin-bottom: 0.4rem;
}
.arrow-col {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    color: #6c5ce7;
    padding-top: 2rem;
}

/* Result metrics */
.metric-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
}
.metric-box {
    flex: 1;
    background: rgba(30,30,50,0.5);
    border: 1px solid rgba(108,92,231,0.2);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.metric-box .metric-value {
    font-size: 1.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6c5ce7, #00cec9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.metric-box .metric-label {
    font-size: 0.78rem;
    color: #888;
    margin-top: 0.2rem;
}

/* Hide default streamlit elements */
div[data-testid="stTextInput"] label { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Header ──
st.markdown("""
<div class="main-header">
    <h1>🧩 8‑Puzzle Solver</h1>
    <p>AI Search Algorithms — A*, UCS, Greedy, BFS & DFS</p>
</div>
""", unsafe_allow_html=True)

# ── Algorithm selection cards ──
algo_data = {
    "A* Search": {"key": "Astar", "formula": "f(n) = g(n) + h(n)", "tag": "Optimal", "tag_class": "tag-optimal",
                  "complete": "Yes", "optimal": "If h admissible", "nodes": "Fewest", "memory": "Moderate"},
    "UCS": {"key": "UCS", "formula": "f(n) = g(n)", "tag": "Optimal", "tag_class": "tag-optimal",
            "complete": "Yes", "optimal": "Always", "nodes": "Most", "memory": "High"},
    "Greedy BFS": {"key": "Greedy", "formula": "f(n) = h(n)", "tag": "Suboptimal", "tag_class": "tag-suboptimal",
                   "complete": "Not always", "optimal": "No", "nodes": "Fewest*", "memory": "Low"},
    "BFS": {"key": "BFS", "formula": "FIFO Queue", "tag": "Optimal", "tag_class": "tag-optimal",
            "complete": "Yes", "optimal": "Yes (unit cost)", "nodes": "Many", "memory": "High"},
    "DFS": {"key": "DFS", "formula": "LIFO Stack", "tag": "Suboptimal", "tag_class": "tag-suboptimal",
            "complete": "Not always", "optimal": "No", "nodes": "Varies", "memory": "Low"},
}

algo_cols = st.columns(5)
selected_algo = st.session_state.get("selected_algo", "Astar")

for col_idx, (name, data) in enumerate(algo_data.items()):
    with algo_cols[col_idx]:
        active_class = "active" if data["key"] == selected_algo else ""
        st.markdown(f"""
        <div class="algo-card {active_class}">
            <span class="algo-tag {data['tag_class']}">{data['tag']}</span><br>
            <span class="algo-name">{name}</span><br>
            <span class="algo-formula">{data['formula']}</span>
            <div class="algo-detail">
                Complete <span>{data['complete']}</span><br>
                Optimal <span>{data['optimal']}</span><br>
                Nodes expanded <span>{data['nodes']}</span><br>
                Memory <span>{data['memory']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Select", key=f"btn_{data['key']}", use_container_width=True):
            st.session_state["selected_algo"] = data["key"]
            st.rerun()

selected_algo = st.session_state.get("selected_algo", "Astar")

st.markdown("---")

# ── Input Section ──
left_col, mid_col, right_col = st.columns([1, 1, 1])

default_start = [1, 2, 3, 4, 0, 6, 7, 5, 8]
default_goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]

with left_col:
    st.markdown('<div class="card"><h3>📋 Start State</h3>', unsafe_allow_html=True)
    start_state = []
    for i in range(3):
        row_cols = st.columns(3)
        for j in range(3):
            val = row_cols[j].text_input(
                label=f"S{i}{j}",
                value=str(default_start[i * 3 + j]),
                key=f"s_{i}_{j}",
                label_visibility="collapsed"
            )
            start_state.append(int(val) if val.strip().isdigit() else 0)
    st.markdown(render_grid_html(start_state, default_goal, size=48), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with mid_col:
    st.markdown('<div class="card"><h3>🎯 Goal State</h3>', unsafe_allow_html=True)
    goal_state = []
    for i in range(3):
        row_cols = st.columns(3)
        for j in range(3):
            val = row_cols[j].text_input(
                label=f"G{i}{j}",
                value=str(default_goal[i * 3 + j]),
                key=f"g_{i}_{j}",
                label_visibility="collapsed"
            )
            goal_state.append(int(val) if val.strip().isdigit() else 0)
    st.markdown(render_grid_html(goal_state, goal_state, size=48), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="card"><h3>📊 Live Heuristics</h3>', unsafe_allow_html=True)
    try:
        h1_val = h1_misplaced(start_state, goal_state)
        h2_val = h2_manhattan(start_state, goal_state)
        h3_val = h3_linear_conflict(start_state, goal_state)
        max_h = max(h3_val, 1)

        for label, val, cls in [("h1 — Misplaced tiles", h1_val, "h1"),
                                 ("h2 — Manhattan distance", h2_val, "h2"),
                                 ("h3 — Linear conflict", h3_val, "h3")]:
            pct = min(val / max(max_h, 1) * 100, 100)
            st.markdown(f"""
            <div class="h-bar-container">
                <div class="h-bar-label"><span>{label}</span><span class="h-val">{val}</span></div>
                <div class="h-bar-track"><div class="h-bar-fill {cls}" style="width:{pct}%"></div></div>
            </div>
            """, unsafe_allow_html=True)

        holds = h3_val >= h2_val >= h1_val >= 0
        cls = "dominance-pass" if holds else "dominance-fail"
        icon = "✓" if holds else "✗"
        st.markdown(
            f'<div class="dominance-tag {cls}">{icon} h3 ≥ h2 ≥ h1 ≥ 0 — {"Holds" if holds else "Failed"}</div>',
            unsafe_allow_html=True
        )
    except Exception:
        st.markdown('<p style="color:#888;">Enter valid states to see heuristics.</p>', unsafe_allow_html=True)

    # Heuristic selection for A*/Greedy
    if selected_algo in ["Astar", "Greedy"]:
        st.markdown('<br>', unsafe_allow_html=True)
        heuristic_name = st.radio("Heuristic function:", ["h1 — Misplaced", "h2 — Manhattan", "h3 — Linear Conflict"],
                                   index=1, key="heuristic_radio")
    st.markdown('</div>', unsafe_allow_html=True)

# ── Solve Button ──
st.markdown("<br>", unsafe_allow_html=True)

if st.button("Solve Puzzle", type="primary", use_container_width=True):
    heuristic = h2_manhattan
    if selected_algo in ["Astar", "Greedy"]:
        h_name = st.session_state.get("heuristic_radio", "h2 — Manhattan")
        if "h1" in h_name:
            heuristic = h1_misplaced
        elif "h3" in h_name:
            heuristic = h3_linear_conflict

    t0 = time.perf_counter()
    solver = SearchAlgorithms(start_state, goal_state)

    if selected_algo == "Astar":
        path, fullPath, cost = solver.Astar(heuristic)
    elif selected_algo == "UCS":
        path, fullPath, cost = solver.UCS()
    elif selected_algo == "Greedy":
        path, fullPath, cost = solver.Greedy(heuristic)
    elif selected_algo == "BFS":
        path, fullPath, cost = solver.BFS()
    elif selected_algo == "DFS":
        path, fullPath, cost = solver.DFS()

    elapsed = (time.perf_counter() - t0) * 1000  # ms

    if cost == -1:
        st.error("❌ No solution found! The puzzle may be unsolvable from this configuration.")
    else:
        # ── Result metrics ──
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-box">
                <div class="metric-value">{cost}</div>
                <div class="metric-label">Total Moves</div>
            </div>
            <div class="metric-box">
                <div class="metric-value">{len(fullPath)}</div>
                <div class="metric-label">States Visited</div>
            </div>
            <div class="metric-box">
                <div class="metric-value">{elapsed:.1f} ms</div>
                <div class="metric-label">Solve Time</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Path actions ──
        if path:
            arrows = {"Up": "⬆", "Down": "⬇", "Left": "⬅", "Right": "➡"}
            action_html = " → ".join(
                f'<span style="background:rgba(108,92,231,0.2);padding:0.2rem 0.6rem;border-radius:8px;'
                f'font-weight:600;color:#a29bfe;">{arrows.get(a, "")} {a}</span>'
                for a in path
            )
            st.markdown(
                f'<div style="text-align:center;margin:0.8rem 0;line-height:2.2;">{action_html}</div>',
                unsafe_allow_html=True
            )

        # ── Step‑by‑step grid visualization ──
        st.markdown('<div class="card"><h3>🗺️ Solution Path</h3></div>', unsafe_allow_html=True)

        # Show up to 6 per row
        steps_per_row = min(len(fullPath), 6)
        for row_start in range(0, len(fullPath), steps_per_row):
            row_end = min(row_start + steps_per_row, len(fullPath))
            cols = st.columns(row_end - row_start)
            for idx in range(row_start, row_end):
                with cols[idx - row_start]:
                    action_badge = ""
                    if idx > 0:
                        arrows = {"Up": "⬆", "Down": "⬇", "Left": "⬅", "Right": "➡"}
                        action_badge = f'<div class="step-action">{arrows.get(path[idx-1], "")} {path[idx-1]}</div>'
                    step_label = "Start" if idx == 0 else ("Goal ✓" if idx == len(fullPath) - 1 else f"Step {idx}")
                    st.markdown(f'<div class="step-card"><div class="step-label">{step_label}</div>{action_badge}</div>', unsafe_allow_html=True)
                    st.markdown(render_grid_html(fullPath[idx], goal_state, size=36), unsafe_allow_html=True)
