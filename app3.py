import streamlit as st
from PIL import Image

def main():
    st.title('Perception Test')

    # Pre-defined correct answers list
    correct_answers = ['X', 'P', 'l', '9', 't', '1', 'b', 'z', 'e', '3', 'h', 'u', '5', 'c', '6', 'j', '2', 'k', '8', 'f', 'o', 'm', '4', 's', 'd', 'r', 'g', 'n']

    # Load images (adjust paths as necessary)
    instruction_image_path = '1.jpg'  # Update path
    example_image_path = '2.jpg'  # Update path
    example_image_path1 = '3.jpg'
    perception_test_sheet_path = '4.jpg'

    # Display Instruction and Example Image
    st.image(Image.open(instruction_image_path), caption='Instructions', use_column_width=True)
    st.image(Image.open(example_image_path), caption='Example Answers', use_column_width=True)
    st.image(Image.open(example_image_path1), caption='Example Answers', use_column_width=True)

    # Inputs for answers
    st.header('Enter Your Answers')
    user_answers = []
    perception_test_sheet_image = Image.open(perception_test_sheet_path)  # Load the image once

    for i in range(3, 31):  # Adjust based on the number of questions
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

if __name__ == "__main__":
    main()
