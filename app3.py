import streamlit as st
import time
from PIL import Image

# Helper functions
def score_form_boards(score_input):
    if score_input >= 300:
        return 0
    elif score_input >= 274:
        return 1
    elif score_input >= 217:
        return 2
    elif score_input >= 175:
        return 3
    elif score_input >= 150:
        return 4
    elif score_input >= 137:
        return 5
    elif score_input >= 123:
        return 6
    elif score_input >= 112:
        return 7
    elif score_input >= 102:
        return 8
    elif score_input >= 92:
        return 9
    else:
        return 10

def form_board_grade(score):
    if score == 10:
        return 'A'
    elif score == 9:
        return 'A'
    elif score == 8:
        return 'B+'
    elif score == 7:
        return 'B+'
    elif score == 6:
        return 'B'
    elif score == 5:
        return 'B'
    elif score == 4:
        return 'B'
    elif score == 3:
        return 'B-'
    elif score == 2:
        return 'B-'
    elif score == 1:
        return 'C'
    else:
        return 'C'

def score_pin_board(holes_filled):
    if holes_filled <= 15:
        return 0  # Grade C
    elif 16 <= holes_filled <= 18:
        return 1  # Grade C
    elif 19 <= holes_filled <= 21:
        return 2  # Grade B-
    elif 22 <= holes_filled <= 24:
        return 3  # Grade B-
    elif 25 <= holes_filled <= 28:
        return 4  # Grade B
    elif 29 <= holes_filled <= 31:
        return 5  # Grade B
    elif 32 <= holes_filled <= 34:
        return 6  # Grade B
    elif 35 <= holes_filled <= 40:
        return 7  # Grade B+
    elif 41 <= holes_filled <= 50:
        return 8  # Grade B+
    elif 51 <= holes_filled <= 60:
        return 9  # Grade A
    else:
        return 10  # Grade A

def pin_board_grade(score):
    if score == 0 or score == 1:
        return 'C'
    elif score == 2 or score == 3:
        return 'B-'
    elif score >= 4 and score <= 6:
        return 'B'
    elif score == 7 or score == 8:
        return 'B+'
    elif score >= 9:
        return 'A'

def perception_test_evaluation(correct_answers):
    if correct_answers == 0:
        return 0, 'C'
    elif 1 <= correct_answers <= 3:
        return 1, 'C'
    elif 4 <= correct_answers <= 6:
        return 2, 'B-'
    elif 7 <= correct_answers <= 9:
        return 3, 'B-'
    elif 10 <= correct_answers <= 12:
        return 4, 'B'
    elif 13 <= correct_answers <= 15:
        return 5, 'B'
    elif 16 <= correct_answers <= 18:
        return 6, 'B'
    elif 19 <= correct_answers <= 21:
        return 7, 'B+'
    elif 22 <= correct_answers <= 24:
        return 8, 'B+'
    elif 25 <= correct_answers <= 26:
        return 9, 'A'
    elif 27 <= correct_answers <= 28:
        return 10, 'A'
    else:
        return 'Invalid score', 'Invalid grade'

def determine_operation(pb_score, fb_score, p_score):
    total_score = pb_score + fb_score + p_score
    
    operations_data = {
        'Spinning': {
            "Blow room & Carding": {"recommended": [7, 5, 7], "minimum": [6, 4, 6]},
            "Draw Frame & Speed Frame": {"recommended": [6, 4, 3], "minimum": [5, 3, 2]},
            "Ring Frame": {"recommended": [7, 7, 5], "minimum": [5, 5, 4]},
            "Auto Coner & Open End": {"recommended": [7, 5, 7], "minimum": [6, 4, 6]},
            "TFO": {"recommended": [6, 4, 3], "minimum": [5, 3, 2]},
            "Helper/Cleaner": {"recommended": [5, 4, 3], "minimum": [4, 3, 3]},
        },
        'Weaving Preparatory': {
            "Warper": {"recommended": [7, 5, 7], "minimum": [6, 4, 6]},
            "Sizing": {"recommended": [7, 7, 7], "minimum": [5, 6, 5]},
            "Winding": {"recommended": [6, 4, 3], "minimum": [5, 3, 2]},
            "Beam Loader": {"recommended": [5, 4, 3], "minimum": [4, 3, 3]},
            "Creel Boy": {"recommended": [5, 4, 3], "minimum": [4, 3, 3]},
            "Helper & Cleaner": {"recommended": [5, 4, 3], "minimum": [4, 3, 3]},
        },
        'Weaving': {
            "Weaver": {"recommended": [7, 7, 5], "minimum": [5, 5, 4]},
            "Knotter": {"recommended": [7, 7, 7], "minimum": [5, 5, 5]},
            "Drawer": {"recommended": [7, 7, 8], "minimum": [5, 5, 6]},
            "Doffer": {"recommended": [6, 4, 3], "minimum": [5, 3, 2]},
            "Weft Boy": {"recommended": [5, 4, 3], "minimum": [4, 3, 3]},
            "Quality Checker": {"recommended": [7, 7, 7], "minimum": [5, 5, 5]},
            "Beam Loader": {"recommended": [5, 4, 3], "minimum": [4, 3, 3]},
            "Helper & Cleaner": {"recommended": [5, 4, 3], "minimum": [4, 3, 3]},
        },
        'Processing': {
            "Fabric & Yarn Dyeing": {"recommended": [7, 7, 7], "minimum": [5, 5, 5]},
            "Drier": {"recommended": [6, 4, 3], "minimum": [5, 3, 2]},
            "Stenter & Shearing": {"recommended": [7, 7, 5], "minimum": [5, 5, 4]},
            "Helper & Cleaner": {"recommended": [5, 4, 3], "minimum": [4, 3, 3]},
        },
        'Finish Folding': {
            "Length Cutting OP.": {"recommended": [7, 7, 7], "minimum": [5, 5, 5]},
            "Length Hemming OP.": {"recommended": [7, 7, 7], "minimum": [5, 5, 5]},
            "Cross Cutting": {"recommended": [7, 7, 5], "minimum": [5, 5, 4]},
            "Cross Cutting Checker": {"recommended": [5, 4, 3], "minimum": [4, 3, 3]},
            "Stitcher": {"recommended": [7, 7, 5], "minimum": [5, 5, 4]},
            "Checker": {"recommended": [7, 7, 5], "minimum": [5, 5, 5]},
            "Packer & Helper": {"recommended": [5, 4, 3], "minimum": [4, 3, 3]},
            "Mendor": {"recommended": [7, 7, 7], "minimum": [5, 5, 5]},
        },
        'Grey Folding': {
            "Grey Checker": {"recommended": [5, 7, 7], "minimum": [5, 5, 5]},
            "Material Handler": {"recommended": [5, 4, 3], "minimum": [4, 3, 3]},
            "Helper": {"recommended": [5, 4, 3], "minimum": [4, 3, 3]},
        },
        'Engineering': {
            "Mechanic & Fitter": {"recommended": [7, 7, 7], "minimum": [5, 5, 5]},
            "Electrician": {"recommended": [8, 7, 7], "minimum": [6, 7, 4]},
            "General Trade": {"recommended": [7, 6, 4], "minimum": [6, 5, 4]},
        },
    }
    
    recommended_operations = []
    minimum_operations = []
    
    for operation_type, operations in operations_data.items():
        for operation, scores in operations.items():
            rec_scores = scores["recommended"]
            min_scores = scores["minimum"]
            
            if pb_score >= rec_scores[0] and fb_score >= rec_scores[1] and p_score >= rec_scores[2]:
                recommended_operations.append((operation_type, operation))
            
            if pb_score >= min_scores[0] and fb_score >= min_scores[1] and p_score >= min_scores[2]:
                minimum_operations.append((operation_type, operation))
    
    return {
        "recommended": recommended_operations,
        "minimum": minimum_operations,
    }

# Main function for the Streamlit app
def main():
    st.sidebar.title("Tests")
    app_mode = st.sidebar.selectbox("Choose the test", ["Perception Test", "Form Board Test", "Pin Board Test", "Score Evaluation", "Operations Recommendation"])

    if app_mode == "Perception Test":
        st.title('Perception Test')
        correct_answers = ['X', 'P', 'l', '9', 't', '1', 'b', 'z', 'e', '3', 'h', 'u', '5', 'c', '6', 'j', '2', 'k', '8', 'f', 'o', 'm', '4', 's', 'd', 'r', 'g', 'n']

        instruction_image_path = '1.jpg'
        example_image_path = '2.jpg'
        example_image_path1 = '3.jpg'
        perception_test_sheet_path = '4.jpg'

        st.image(Image.open(instruction_image_path), caption='Instructions', use_column_width=True)
        st.image(Image.open(example_image_path), caption='Example Answers', use_column_width=True)
        st.image(Image.open(example_image_path1), caption='Example Answers', use_column_width=True)

        st.header('Enter Your Answers')
        user_answers = []
        perception_test_sheet_image = Image.open(perception_test_sheet_path)

        for i in range(3, 31):
            if (i - 1) % 5 == 0:
                st.image(perception_test_sheet_image, caption='Perception Test Sheet', use_column_width=True)
            answer = st.text_input(f"Enter your answer for square {i}", key=f"square_{i}")
            user_answers.append(answer)

        if st.button('Submit Answers'):
            score = sum(1 for user_ans, correct_ans in zip(user_answers, correct_answers) if user_ans.strip().lower() == correct_ans.lower())
            st.write(f'Thank you for your responses! Your score is {score} out of {len(correct_answers)}.')
            for i, (user_ans, correct_ans) in enumerate(zip(user_answers, correct_answers), start=1):
                if user_ans.strip().lower() == correct_ans.lower():
                    st.success(f'Question {i}: Correct - {user_ans}')
                else:
                    st.error(f'Question {i}: Incorrect - Your answer: {user_ans}, Correct answer: {correct_ans}')

    elif app_mode == "Form Board Test":
        st.title("Form Board Test")
        st.subheader("Test your spatial relations and general intelligence")

        # Timer for Form Board A
        if 'start_time_a' not in st.session_state:
            st.session_state.start_time_a = 0
        if 'end_time_a' not in st.session_state:
            st.session_state.end_time_a = 0
        if 'running_a' not in st.session_state:
            st.session_state.running_a = False

        # Timer for Form Board B
        if 'start_time_b' not in st.session_state:
            st.session_state.start_time_b = 0
        if 'end_time_b' not in st.session_state:
            st.session_state.end_time_b = 0
        if 'running_b' not in st.session_state:
            st.session_state.running_b = False

        def start_test_a():
            st.session_state.start_time_a = time.time()
            st.session_state.running_a = True

        def stop_test_a():
            st.session_state.running_a = False
            st.session_state.end_time_a = time.time()

        def start_test_b():
            st.session_state.start_time_b = time.time()
            st.session_state.running_b = True

        def stop_test_b():
            st.session_state.running_b = False
            st.session_state.end_time_b = time.time()

        st.subheader("Form Board A")
        st.button("Start Test A", on_click=start_test_a)
        st.button("Stop Test A", on_click=stop_test_a)

        if st.session_state.running_a:
            elapsed_time_a = time.time() - st.session_state.start_time_a
            st.write(f"Timer A: {elapsed_time_a:.2f} seconds")

        if not st.session_state.running_a and st.session_state.start_time_a != 0:
            elapsed_time_a = st.session_state.end_time_a - st.session_state.start_time_a
            st.write(f"Test A Duration: {elapsed_time_a:.2f} seconds")

        st.subheader("Form Board B")
        st.button("Start Test B", on_click=start_test_b)
        st.button("Stop Test B", on_click=stop_test_b)

        if st.session_state.running_b:
            elapsed_time_b = time.time() - st.session_state.start_time_b
            st.write(f"Timer B: {elapsed_time_b:.2f} seconds")

        if not st.session_state.running_b and st.session_state.start_time_b != 0:
            elapsed_time_b = st.session_state.end_time_b - st.session_state.start_time_b
            st.write(f"Test B Duration: {elapsed_time_b:.2f} seconds")

        if st.session_state.end_time_a != 0 and st.session_state.end_time_b != 0:
            total_time = (st.session_state.end_time_a - st.session_state.start_time_a) + (st.session_state.end_time_b - st.session_state.start_time_b)
            st.write(f"Total Time for Form Boards A and B: {total_time:.2f} seconds")

            score_input = total_time * (100 / 60)
            score = score_form_boards(score_input)
            grade = form_board_grade(score)
            st.write(f"Score: {score}, Grade: {grade}")

            if st.button("Generate Report"):
                candidate_id = st.text_input("Enter Candidate ID:")
                report = f"Candidate ID: {candidate_id}\nTest A Duration: {elapsed_time_a:.2f} seconds\nTest B Duration: {elapsed_time_b:.2f} seconds\nTotal Time: {total_time:.2f} seconds\nScore: {score}\nGrade: {grade}\n"
                st.write("Report:")
                st.write(report)
                with open(f"report_{candidate_id}.txt", "w") as file:
                    file.write(report)
                st.write(f"Report saved as report_{candidate_id}.txt")

    elif app_mode == "Pin Board Test":
        st.title("Pin Board Test")
        st.subheader("Test your fine motor skills with the pin board")

        if 'start_time_right' not in st.session_state:
            st.session_state.start_time_right = 0
        if 'end_time_right' not in st.session_state:
            st.session_state.end_time_right = 0
        if 'running_right' not in st.session_state:
            st.session_state.running_right = False

        if 'start_time_left' not in st.session_state:
            st.session_state.start_time_left = 0
        if 'end_time_left' not in st.session_state:
            st.session_state.end_time_left = 0
        if 'running_left' not in st.session_state:
            st.session_state.running_left = False

        def start_test_right():
            st.session_state.start_time_right = time.time()
            st.session_state.running_right = True

        def stop_test_right():
            st.session_state.running_right = False
            st.session_state.end_time_right = time.time()

        def start_test_left():
            st.session_state.start_time_left = time.time()
            st.session_state.running_left = True

        def stop_test_left():
            st.session_state.running_left = False
            st.session_state.end_time_left = time.time()

        st.subheader("Right Hand Test")
        st.button("Start Test (Right Hand)", on_click=start_test_right)
        st.button("Stop Test (Right Hand)", on_click=stop_test_right)

        if st.session_state.running_right:
            elapsed_time_right = time.time() - st.session_state.start_time_right
            st.write(f"Right Hand Timer: {elapsed_time_right:.2f} seconds")

        if not st.session_state.running_right and st.session_state.start_time_right != 0:
            elapsed_time_right = st.session_state.end_time_right - st.session_state.start_time_right
            st.write(f"Right Hand Test Duration: {elapsed_time_right:.2f} seconds")

        st.subheader("Left Hand Test")
        st.button("Start Test (Left Hand)", on_click=start_test_left)
        st.button("Stop Test (Left Hand)", on_click=stop_test_left)

        if st.session_state.running_left:
            elapsed_time_left = time.time() - st.session_state.start_time_left
            st.write(f"Left Hand Timer: {elapsed_time_left:.2f} seconds")

        if not st.session_state.running_left and st.session_state.start_time_left != 0:
            elapsed_time_left = st.session_state.end_time_left - st.session_state.start_time_left
            st.write(f"Left Hand Test Duration: {elapsed_time_left:.2f} seconds")

        filled_holes_right = st.number_input("Enter the number of holes filled (Right Hand):", min_value=0, max_value=150, step=1)
        filled_holes_left = st.number_input("Enter the number of holes filled (Left Hand):", min_value=0, max_value=150, step=1)

        total_filled_holes = filled_holes_right + filled_holes_left
        st.write(f"Total number of holes filled: {total_filled_holes}")

        score = score_pin_board(total_filled_holes)
        grade = pin_board_grade(score)
        st.write(f"Score: {score}, Grade: {grade}")

        if st.button("Generate Report"):
            candidate_id = st.text_input("Enter Candidate ID:")
            report = f"Candidate ID: {candidate_id}\nRight Hand Test Duration: {elapsed_time_right:.2f} seconds\nLeft Hand Test Duration: {elapsed_time_left:.2f} seconds\nTotal Number of Filled Holes: {total_filled_holes}\nScore: {score}\nGrade: {grade}\n"
            st.write("Report:")
            st.write(report)
            with open(f"report_{candidate_id}.txt", "w") as file:
                file.write(report)
            st.write(f"Report saved as report_{candidate_id}.txt")

    elif app_mode == "Score Evaluation":
        st.title("Score Evaluation")
        st.subheader("Evaluate Perception Test Score")

        correct_answers = st.number_input("Enter the number of correct answers out of 28 in 3 minutes:", min_value=0, max_value=28, step=1)
        if st.button("Evaluate Score"):
            score, grade = perception_test_evaluation(correct_answers)
            st.write(f"You got {correct_answers} correct answers, which corresponds to a score of {score} and a grade of '{grade}'.")

    elif app_mode == "Operations Recommendation":
        st.title("Operations Recommendation")
        st.subheader("Determine the appropriate operation for a candidate based on their scores")

        pb_score = st.number_input("Enter the Pin Board (PB) score:", min_value=0, max_value=10, step=1)
        fb_score = st.number_input("Enter the Form Boards (FB) score:", min_value=0, max_value=10, step=1)
        p_score = st.number_input("Enter the Perception (P) score:", min_value=0, max_value=10, step=1)

        if st.button("Determine Operations"):
            operations = determine_operation(pb_score, fb_score, p_score)
            st.write("Based on your scores:")
            st.write(f"Total Score: {pb_score + fb_score + p_score}")
            st.write("Recommended Operations:")
            for op_type, op_name in operations["recommended"]:
                st.write(f"- {op_type}: {op_name}")
            st.write("Minimum Operations:")
            for op_type, op_name in operations["minimum"]:
                st.write(f"- {op_type}: {op_name}")

if __name__ == "__main__":
    main()
