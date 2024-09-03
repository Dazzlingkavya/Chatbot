import re
import random
import tkinter as tk

# Predefined long responses
R_EATING = "I don't eat, but I do enjoy hearing about different foods and recipes! What's your favorite thing to eat?"
R_ADVICE = "Don't stress too much about getting everything perfect—just take it one step at a time. You've got the skills and drive, so trust yourself and keep going. We're all figuring it out as we go!"

def unknown():
    responses = ["Could you please re-phrase that?",
                 "...",
                 "Sounds about right.",
                 "What does that mean?"]
    return random.choice(responses)

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognised_words))

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

def check_all_messages(message):
    highest_prob_list = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        probability = message_probability(message, list_of_words, single_response, required_words)
        highest_prob_list[bot_response] = probability

    # Mathematical operation check
    def calculate_expression(expression):
        try:
            result = eval(expression)
            return f"The answer is {result}"
        except:
            return "Sorry, I can't calculate that."

    # Responses mapped to specific triggers
    response('Hello!', ['hello', 'hi', 'hey', 'sup', 'heyo','hlo'], single_response=True)
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('yeah! its been a long time',['long','time','no','see'],required_words=['long'])
    response('Its my pleasure',['Thank','You','for','being','with','me'],required_words=['Thank'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response('Thank you!', ['i', 'love', 'code', 'palace'], required_words=['code', 'palace'])
    response(R_ADVICE, ['give', 'advice'], required_words=['advice'])
    response(R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])

    # Check for mathematical expressions
    math_expression = re.search(r'\d+(\s*[-+*/]\s*\d+)+', " ".join(message))
    if math_expression:
        return calculate_expression(math_expression.group())

    # Ensure there's a fallback if highest_prob_list is empty
    best_match = max(highest_prob_list, key=highest_prob_list.get)

    return unknown() if highest_prob_list[best_match] == 0 else best_match

def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response

# GUI setup with tkinter
def send_message():
    user_input = user_entry.get()
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, "You: " + user_input + "\n")
    chat_log.insert(tk.END, "Chatmate: " + get_response(user_input) + "\n\n")
    chat_log.config(state=tk.DISABLED)
    user_entry.delete(0, tk.END)
    chat_log.yview(tk.END)

# Main application window
app = tk.Tk()
app.title("Chatbot")

# Chat log (text area)
chat_log = tk.Text(app, bg="lightgray", height=20, width=50, state=tk.DISABLED)
chat_log.pack(padx=10, pady=10)

# User input (entry box)
user_entry = tk.Entry(app, bg="white", width=40)
user_entry.pack(padx=10, pady=10, side=tk.LEFT)

# Send button
send_button = tk.Button(app, text="Send", command=send_message)
send_button.pack(padx=10, pady=10, side=tk.RIGHT)

# Start the GUI event loop
app.mainloop()
