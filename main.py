"""
============================================================
                Marvellous SmartHire AI Agent
============================================================
Author       : Piyush Manohar Khairnar
Date         : 10/05/2026

Description  :
This project is a text-based AI Mock Interview Agent.

This project demonstrates the practical implementation of:

1. AI Agent
2. LLM Integration
3. Prompt Engineering
4. Answer Evaluation
5. Interview Automation
6. Report Generation
7. Memory through interview history
============================================================
"""

from questions import questions
from interview_agent import MockInterviewAgent
from report_generator import save_report

def print_header():
    """
    Function Name : print_header
    """

    print("=" * 70)
    print("              Marvellous Infosystems")
    print("              AI Mock Interview Agent")
    print("              Text Based Version")
    print("              Author : Piyush Manohar Khairnar")
    print("              Date   : 10/05/2026")
    print("              आम्ही Technical संस्कार करतो !!!")
    print("=" * 70)


def show_menu():
    """
    Function Name : show_menu
    Description   : Displays interview mode options to the user.
    """

    print("\nSelect Interview Mode:")
    print("1. Start Full Interview")
    print("2. Start Topic-wise Interview")
    print("3. Exit")


def get_available_topics():
    """
    Function Name : get_available_topics
    Description   : Extracts unique topics from the question bank.
    Return Value  : List of available topics.
    """

    topics = []

    # Traverse all questions and collect unique topics
    for item in questions:
        if item["topic"] not in topics:
            topics.append(item["topic"])

    return topics


def start_interview(agent, selected_questions):
    """
    Function Name : start_interview
    Description   : Conducts the interview by asking selected questions.
    Parameters    :
        agent              : Object of MockInterviewAgent class
        selected_questions : List of questions selected for interview
    """

    # Ask questions one by one
    for index, item in enumerate(selected_questions, start=1):
        topic = item["topic"]
        question = item["question"]

        print("\n" + "=" * 70)
        print(f"Question {index}")
        print("Topic    :", topic)
        print("Question :", question)
        print("=" * 70)

        # Accept student's answer through text input
        answer = input("\nEnter your answer:\n")

        # Handle empty answer case
        if answer.strip() == "":
            answer = "Student did not provide any answer."

        print("\nEvaluating your answer using LLM...")
        print("Please wait while AI Interview Agent is analyzing your response.")

        # Send question and answer to AI Agent for evaluation
        evaluation = agent.evaluate_answer(topic, question, answer)

        print("\nEvaluation Result:")
        print("-" * 70)
        print(evaluation)
        print("-" * 70)

        # Ask user whether to continue interview or stop
        choice = input("\nDo you want to continue? yes/no: ")

        if choice.lower() != "yes":
            break


def main():
    """
    Function Name : main
    Description   : Entry point of the AI Mock Interview Agent project.
    """

    print_header()

    print("\nWelcome to Marvellous SmartHire AI Mock Interview Agent.")
    print("This system conducts technical interviews using text input and LLM evaluation.")
    print("This project is designed for practical understanding of AI Agents.\n")

    # Accept student name
    student_name = input("Enter student name: ")

    # If student name is empty, use default name
    if student_name.strip() == "":
        student_name = "Student"

    # Create object of MockInterviewAgent
    agent = MockInterviewAgent(student_name)

    print(f"\nWelcome {student_name} to Marvellous Infosystems AI Mock Interview.")
    print("The interview will evaluate your technical answers using LLM.")

    while True:
        show_menu()

        choice = input("\nEnter your choice: ")

        # Full interview mode
        if choice == "1":
            start_interview(agent, questions)

            # Generate final report after interview completion
            report = agent.generate_final_report()
            print(report)

            # Save final report into reports folder
            filename = save_report(student_name, report)

            print("\nInterview completed successfully.")
            print("Final report generated successfully.")
            print("Report saved at:", filename)

            break

        # Topic-wise interview mode
        elif choice == "2":
            topics = get_available_topics()

            print("\nAvailable Topics:")

            # Display available topics
            for index, topic in enumerate(topics, start=1):
                print(f"{index}. {topic}")

            try:
                topic_choice = int(input("\nSelect topic number: "))

                # Validate topic choice
                if topic_choice < 1 or topic_choice > len(topics):
                    print("\nInvalid topic number. Please try again.")
                    continue

                selected_topic = topics[topic_choice - 1]

                selected_questions = []

                # Select questions matching selected topic
                for item in questions:
                    if item["topic"] == selected_topic:
                        selected_questions.append(item)

                print(f"\nYou selected topic: {selected_topic}")

                start_interview(agent, selected_questions)

                # Generate final report
                report = agent.generate_final_report()
                print(report)

                # Save final report
                filename = save_report(student_name, report)

                print("\nInterview completed successfully.")
                print("Final report generated successfully.")
                print("Report saved at:", filename)

                break

            except ValueError:
                print("\nInvalid input. Please enter a valid number.")

        # Exit option
        elif choice == "3":
            print("\nThank you for using Marvellous Infosystems AI Mock Interview Agent.")
            print("Keep learning, keep practicing.")
            print("आम्ही Technical संस्कार करतो !!!")
            break

        # Invalid menu option
        else:
            print("\nInvalid choice. Please try again.")


# Program execution starts from here
if __name__ == "__main__":
    main()