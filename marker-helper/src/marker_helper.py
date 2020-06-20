import json
import os
import pyperclip

from typing import Dict, List


def write_file(filename: str, response: str):
    with open(filename, "a") as f:
        f.write(response + "\n")


def add_comment(principle: str) -> str:
    response: str = input("Add a comment: ")
    if yes_or_no("Would you like to save?"):
        write_file(principle, response)

    return "\t\u2022 " + response


def display_comments(comments: List[str]) -> dict:
    """
    Displays the options available and returns them as a map.
    :param comments: Available comments.
    :return:
    """
    comment_map: dict = {}
    for index, line in enumerate(comments):
        comment_map[str(index+1)] = line
        print("[{}] {}".format(index+1, line).strip("\n"))
    return comment_map


def read_feedback_file(feedback_file: str) -> List[str]:
    if not os.path.exists(feedback_file):
        return []
    with open(feedback_file) as f:
        return f.readlines()


def give_feedback(task_file: str) -> str:
    """
    Gives feedback for a student
    Lets you use saved comments or create and save your own
    :param task_file: File for common comments for this task. 
    :return: Feedback string
    """
    comments: List[str] = read_feedback_file(task_file)
    comment_list: List[str] = []

    while True:
        joiner: str = "\n"
        if len(comment_list) != 0:
            print(joiner.join(comment_list))
        comment_map: dict = display_comments(comments)
        print("[b] Delete a comment")
        print("[n] Add a new comment")
        print("[e] Exit")
        text: str = input("Enter input: ")
        if text != "b" and text != "n" and text != "e" and text not in comment_map:
            print("\x1b[1;31;40m" + "Please input a valid option" + "\x1b[0m")
            continue
        elif text == "b":
            comment_list.pop()
        elif text == "n":
            comment_list.append(add_comment(task_file).strip("\n"))
        elif text == "e":
            break
        else:
            comment_list.append("\t\u2022 " + comment_map[text].strip("\n"))
        print()

    response = "\n".join(comment_list)
    return response + "\n"


def get_feedback_file(part: str, task: str):
    return f"{part.lower()}_{task.lower()}.txt"


def yes_or_no(question: str) -> bool:
    """
    Asks the user a yes or no question. Repeats the question if input invalid.
    :return:
    """
    while True:
        text: str = input(question + " [y/n] ").lower()
        if text == 'y' or text == 'yes':
            return True
        elif text == 'n' or text == 'no':
            return False
        else:
            print("\x1b[1;31;40m" + "Please enter yes or no." + "\x1b[0m")


def give_mark(task_name: str, max_mark: int) -> str:
    """
    Retrieves the mark for a particular task.
    :param task_name: Name of task to get mark for.
    :param max_mark: Maximum mark for the task.
    :return: String containing the mark of the task.
    """
    while True:
        mark_input: str = input(f"What was the mark for {task_name}? ")
        try:
            mark: float = float(mark_input)
        except ValueError:
            print("\x1b[1;31;40m" + "Please input a valid number." + "\x1b[0m")
            continue
        if mark < 0:
            print("\x1b[1;31;40m" + "Please input a valid number above 0." + "\x1b[0m")
        elif 0 < max_mark < mark:
            print("\x1b[1;31;40m" + f"Please input a valid number less than or equal to tasks[task][\"max_mark\"]."
                  + "\x1b[0m")
        else:
            return f"{task_name} - {mark}"


def mark_tasks(parts: List[Dict[str, any]]) -> str:
    """
    Marks each task for each part in the assignment.
    :param parts: Parts to be marked.
    :return: A feedback string.
    """
    feedback: str = ""
    for part in parts:
        feedback += part["name"] + ":\n"
        print(part["name"] + ":")
        for task in part["tasks"].keys():
            feedback += give_mark(task, part["tasks"][task]["max_mark"]) + "\n"
            if yes_or_no("Would you like to give feedback?"):
                feedback += give_feedback(get_feedback_file(part["name"], task))
        feedback += "\n\n"

    return feedback


def read_json(filename: str) -> List[Dict[str, any]]:
    with open(filename) as json_file:
        return json.load(json_file)


if __name__ == "__main__":
    parts: List[Dict[str, any]] = read_json("parts.json")
    feedback: str = mark_tasks(parts)
    print("\n\n" + feedback, end="")
    pyperclip.copy(feedback)
    print("Output copied to clipboard!")
