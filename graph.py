from typing import TypedDict, List, Annotated
import operator
from langgraph.graph import StateGraph, END, START
from agents import pro_agent, con_agent, judge_agent

class DebateState(TypedDict):
    topic: str
    current_round: str
    round_count: int
    pro_history: Annotated[List[str], operator.add] 
    con_history: Annotated[List[str], operator.add] 
    verdict: str


def pro_node(state: DebateState):
   
    last_pro = state["pro_history"][-1:] if state["pro_history"] else []
    last_con = state["con_history"][-1:] if state["con_history"] else []
    
    response = pro_agent(
        topic=state["topic"],
        current_round=state["current_round"],
        pro_history=last_pro,
        con_history=last_con
    )
   
    return {"pro_history": [response]}


def con_node(state: DebateState):
    
    last_pro = state["pro_history"][-1:] if state["pro_history"] else []
    last_con = state["con_history"][-1:] if state["con_history"] else []
    
    response = con_agent(
        topic=state["topic"],
        current_round=state["current_round"],
        pro_history=last_pro,
        con_history=last_con
    )
    
   
    next_round_count = state["round_count"] + 1
    
    
    return {
        "con_history": [response],
        "round_count": next_round_count,
        "current_round": f"Round {next_round_count}"
    }


def judge_node(state: DebateState):
    
    verdict = judge_agent(
        topic=state["topic"],
        pro_history=state["pro_history"],
        con_history=state["con_history"]
    )
    return {"verdict": verdict}




def should_continue(state: DebateState):
    """
    Determines whether to loop back for another debate round 
    or proceed to the judge node.
    """
    
    if state["round_count"] > 3:
        return "judge"
    return "pro"



def create_debate_graph():
    """
    Constructs, configures, and compiles the 3-round debate workflow.
    Returns an executable LangGraph Runnable application.
    """
    builder = StateGraph(DebateState)
    
    
    builder.add_node("pro", pro_node)
    builder.add_node("con", con_node)
    builder.add_node("judge", judge_node)
    
   
    builder.add_edge(START, "pro")
    builder.add_edge("pro", "con")
    
    builder.add_conditional_edges(
        "con",
        should_continue,
        {
            "pro": "pro",
            "judge": "judge"
        }
    )
    
    builder.add_edge("judge", END)


    return builder.compile()