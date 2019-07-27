#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Title:          datahandler.py
    Description:    Collection of fuctions which can be used to analyse
                    whatsapp group chats exported as txt-file.
    Author:         Pascal Schlaak
    Date:           2019-06-30
    Python:         3.6.7
"""

from matplotlib import pyplot as plt


# Path to group chat txt-file. Export instruction see: https://faq.whatsapp.com/de/wp/22548236?lang=en
path_to_chat_file = "....txt"


def read_data(path_to_chat_file):

    """
    Read in group chat .txt-file and return
    
    :param  str path_to_chat_file:  Path to group chat .txt-file
    :return str raw_chat_data:      Whole group chat as string
    """
    
    raw_chat_data = ""

    with open(path_to_chat_file) as text_file_data:
        # Add rows together due to new-line in messages
        for row in text_file_data:
            raw_chat_data += row.lower()
        
    return raw_chat_data


def format_data(raw_chat_data, *argv):
    
    """
    Reformatting data and split its content into timestamp, sender, message abd add them to a dictionary
    
    :param  str     raw_chat_data:  Reformatted content of group chat .txt-file
    :param  str     *argv:          All senders by name of a message to be analysed
    :return dict    chat_messages:  Dictionary including index message, date, sender, message
    """

    message_number = 1
    name_set = set()
    chat_messages = {}

    # Add all senders by name to name array
    for arg in argv:
        name_set.add(arg.lower())

    # Split chat_data back into messages
    splitted_chat_data = raw_chat_data.split("[")
    
    # Iterate through messages
    for element in splitted_chat_data:
        # Reset variables after every message
        datetime, sender, message = "", "", ""
        # Strip unnecessary characters
        element = element.strip("\r\n")
        # Split message into date and content
        item = element.split("]")
        # Get date
        datetime = item[0]
        # Check if message was writted by name of a sender which should be analysed
        for name in name_set:
            # Get sender and content (equals last element in item array)
            content = item[-1]
            if name in content:
                content = content.split(name)
                sender = name
                content = content[-1]
                message = content[2:]
                break
        
        chat_messages[message_number] = {"datetime": datetime, "sender":sender, "message":message}
        message_number += 1
    
    print("\nNumber of messages:\t%d\n" % message_number)
        
    return chat_messages, name_set


def count_messages_and_words_by_name(chat_messages, name_set, save_plot=0):

    """
    Count number of messages and words by name of sender
    to see their activity.
    
    :param  dict    chat_messages:  Dictionary with messages and their content
    :param  set     name_set:       Set of all senders by name to be analysed
    :param  int     save_plot:      Show plot = 0, save plot as png = 1; Default 0
    """

    counter_messages_dict, counter_words_dict = {}, {}

    # Init counter variables for each sender
    for name in name_set:
        counter_messages_dict[name] = 0
        counter_words_dict[name] = 0

    # Count messages and words by sender
    for message in chat_messages.values():
        for name in name_set:
            if name == message["sender"]:
                counter_messages_dict[name] += 1
                content = message["message"].split(" ")
                counter_words_dict[name] += len(content)
                break
    
    # Print number messages and words by sender
    for name in counter_messages_dict.keys():
        print("Number messages %s:\t%d\tnumber words:\t%d" % (name, counter_messages_dict[name], counter_words_dict[name]))
    

    # Plot number of messages by sender
    plt.bar(counter_messages_dict.keys(), counter_words_dict.values(), label="Messages")
    plt.bar(counter_messages_dict.keys(), counter_messages_dict.values(), label="Words")
    plt.legend()
    plt.title("Number messages per sender")
    plt.xlabel("Sender [name]")
    plt.ylabel("Messages [number]")
    
    # Check if plot should be showed or saved
    if save_plot == 0:
        plt.show()
    elif save_plot == 1:
        plt.savefig("number_messages_by_name.png", dpi=300)
        plt.close()
    else:
        print("\nError: Wrong save_plot value! Should be 0 or 1 see help() of function!")


def main():
    rcd = read_data(path_to_chat_file)
    cm, ns = format_data(rcd, "<name>")
    count_messages_and_words_by_name(cm, ns, 0)


if __name__ == "__main__":
    main()
