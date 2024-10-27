import gradio as gr
import fetch_threads as api
import summarize_threads as summarize
import rag_prep as rag
import re

CSS ="""
#component-0 > div:nth-child(11) { height: 600px !important; }
"""

def display_text_list():
    text_list = summarize.summarize_tweets()
    formatted_data=""
    for i, item in enumerate(text_list):
        title = f"<h3>{i+1}. {item['title']}</h3>"
        new_sum = re.sub(r'\n', ' ', item['summary'])
        summary = f"<p>{new_sum}</p>"
        formatted_data+=title
        formatted_data+=summary
    
    # print(formatted_data)
    return [formatted_data, gr.TextArea(visible=False), gr.Markdown(visible=True), gr.Markdown(visible=False)]


with gr.Blocks(css=CSS, theme=gr.themes.Soft()) as demo:

    # Intro
    gr.Markdown("<h1><center>Reddit Agent</center></h1>")
    gr.Markdown("<h4><center>Ask anything you want to search reddit for and chat with Reddit Threads to get personalized answers</center></h4>")
    
    # Fetch Reddit Threads
    with gr.Row():
        with gr.Column():
            query = gr.Textbox(label="Fetch Reddit Threads", placeholder="Please enter your query to search... ")
            n = gr.Slider(1,20,value=1,step=1,label="Select no of Reddit Threads you want to fetch", interactive=True)
            
            with gr.Row():
                fetch_tweet_btn = gr.Button(value="Fetch Tweets")
                summarize_tweet_btn = gr.Button(value="Summarize Tweets")
        with gr.Column():
            tweet_details = gr.TextArea(label="Results", max_lines=8)

    fetch_tweet_btn.click(api.get_reddit, inputs=[query,n], outputs=[tweet_details])

    # Summarization Section
    gr.Markdown("<br />")
    Note = gr.Markdown("<h4>Note: Summarizing tweets takes time please wait...</h4>")
    head = gr.Markdown("<h1>Reddit Threads Summarized</h1>", visible=False)
    result = gr.Markdown()
    loader = gr.TextArea(label="Summary Results", visible=True)
    summarize_tweet_btn.click(display_text_list, inputs=[], outputs=[result,loader,head,Note])

    # Chat with Reddit Threads
    gr.Markdown("<br />")
    gr.ChatInterface(fn=rag.ask_questions, type="messages", examples=["hello", "hola", "merhaba"], title="Chat with Redit Threads")

demo.launch()