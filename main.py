import nltk
import ssl
from textblob import TextBlob
from newspaper import Article
import tkinter as tk
from tkinter import messagebox


def summarize():
    url_text = url.get('1.0', "end").strip()  # Corrected variable name to 'url' instead of 'utext'
    if not url_text:
        messagebox.showerror("Error", "Please enter a URL")
        return

    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    # Download NLTK data if not already downloaded
    nltk.download('punkt', quiet=True)

    try:
        article = Article(url_text)
        article.download()
        article.parse()
        article.nlp()

        title.config(state='normal')
        author.config(state='normal')
        publication.config(state='normal')
        summary.config(state='normal')
        sentiment.config(state='normal')

        title.delete('1.0', 'end')
        title.insert('1.0', article.title)
        title.config(foreground='black')  # Set text color to black

        author.delete('1.0', 'end')
        author.insert('1.0', ', '.join(article.authors))
        author.config(foreground='black')  # Set text color to black

        publication.delete('1.0', 'end')
        publication.insert('1.0', str(article.publish_date))
        publication.config(foreground='black')  # Set text color to black

        summary.delete('1.0', 'end')
        summary.insert('1.0', article.summary)
        summary.config(foreground='black')  # Set text color to black

        analysis = TextBlob(article.text)
        sentiment.delete('1.0', 'end')
        sentiment.insert('1.0',
                         f'Polarity: {analysis.sentiment.polarity}, Sentiment: {"positive" if analysis.sentiment.polarity > 0 else "negative" if analysis.sentiment.polarity < 0 else "neutral"}')
        sentiment.config(foreground='black')  # Set text color to black

        title.config(state='disabled')
        author.config(state='disabled')
        publication.config(state='disabled')
        summary.config(state='disabled')
        sentiment.config(state='disabled')

    except Exception as e:
        messagebox.showerror("Error", f"Failed to summarize article: {str(e)}")


# Create the main window
root = tk.Tk()
root.title("News Summary")
root.geometry('1200x600')

# URL input
ulabel = tk.Label(root, text="URL")
ulabel.pack()

url = tk.Text(root, height=1, width=140)
url.pack()

# Summarize button
btn = tk.Button(root, text="Summarize", command=summarize)
btn.pack()

# Title
tlabel = tk.Label(root, text="Title")
tlabel.pack()

title = tk.Text(root, height=1, width=140)
title.config(state='disabled', bg='#dddddd', foreground='black')  # Set text color to black
title.pack()

# Author
alabel = tk.Label(root, text="Author")
alabel.pack()

author = tk.Text(root, height=1, width=140)
author.config(state='disabled', bg='#dddddd', foreground='black')  # Set text color to black
author.pack()

# Publication Date
plabel = tk.Label(root, text="Publication Date")
plabel.pack()

publication = tk.Text(root, height=1, width=140)
publication.config(state='disabled', bg='#dddddd', foreground='black')  # Set text color to black
publication.pack()

# Summary
slabel = tk.Label(root, text="Summary")
slabel.pack()

summary = tk.Text(root, height=20, width=140)
summary.config(state='disabled', bg='#dddddd', foreground='black')  # Set text color to black
summary.pack()

# Sentiment Analysis
selabel = tk.Label(root, text="Sentiment Analysis")
selabel.pack()

sentiment = tk.Text(root, height=1, width=140)
sentiment.config(state='disabled', bg='#dddddd', foreground='black')  # Set text color to black
sentiment.pack()

# Start the tkinter main loop
root.mainloop()
