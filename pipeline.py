from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain


def run_research_pipeline(topic: str):
    state = {}

    # search agent working
    print("\n" + " =" * 50)
    print("[bold green] step 1: Search Agent is gathering information... [/bold green]")
    print("\n" + " =" * 50)
    yield {"step": "search_start", "state": state}

    search_agent = build_search_agent()
    search_result = search_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"find recent, relaible and detaild information about: {topic}",
                )
            ]
        }
    )

    state["search_results"] = search_result["messages"][-1].content
    print("\n search result: ", state["search_results"])
    yield {"step": "search_end", "state": state}

    # reader agent working
    print("\n" + " =" * 50)
    print(
        "[bold green] step 2: Reader Agent is extracting content from URLs... [/bold green]"
    )
    print("\n" + " =" * 50)
    yield {"step": "reader_start", "state": state}

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{state['search_results'][:800]}",
                )
            ]
        }
    )

    state["scraped_content"] = reader_result["messages"][-1].content
    print("\n scraped content: ", state["scraped_content"])
    yield {"step": "reader_end", "state": state}

    # writer chain working
    print("\n" + " =" * 50)
    print(
        "[bold green] step 3: Writer Chain is generating the final report ... [/bold green]"
    )
    print("\n" + " =" * 50)
    yield {"step": "writer_start", "state": state}

    research_combined = (
        f"SEARCH RESULTS: \n {state['search_results']}  \n\n"
        f"DETAILED SCRAPED CONTENT: \n {state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke(
        {"topic": topic, "research": research_combined}
    )

    print("/n Report: ", state["report"])
    yield {"step": "writer_end", "state": state}

    print("\n" + " =" * 50)
    print("[bold green] step 4: Critic Agent is reviewing the report ... [/bold green]")
    print("\n" + " =" * 50)
    yield {"step": "critic_start", "state": state}

    state["critic_review"] = critic_chain.invoke({"report": state["report"]})
    print("\n Critic review: ", state["critic_review"])
    yield {"step": "critic_end", "state": state}


if __name__ == "__main__":
    topic = input("\n Enter a research topic: ")
    for progress in run_research_pipeline(topic):
        pass
