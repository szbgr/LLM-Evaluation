import streamlit as st
import json
import visualization


EXAMPLE_JSON_PATH = "example_GPT-4_responses.json"


def load_example_json():
    with open(EXAMPLE_JSON_PATH, 'r') as example_file:
        return json.load(example_file)


def main():
    st.title('LLM Answers Evaluation')

    # Display two images side by side below the title
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/ChatGPT_logo.svg/800px-ChatGPT_logo.svg.png", width=300)
    with col2:
        st.image("https://eu-images.contentstack.com/v3/assets/blt6b0f74e5591baa03/blt98d8a946b63c9b5f/64b7170ab314c94aa481d8c3/Untitled_design_(1).jpg", width=540)

    # Step 1: Choose your JSON source
    st.markdown("### Step 1: Choose your JSON source")
    st.caption(
        "You can either upload a JSON file or use a preexisting example with five basic knowledge logic questions evaluated by ChatGPT 4. You can only evaluate one file at a time.")
    source_option = st.radio("Choose a JSON source", ('Upload File', 'Use Example'))

    data = []
    user_feedback = {}

    if source_option == 'Upload File':
        uploaded_file = st.file_uploader("", type='json')
        if uploaded_file is not None:
            data = json.load(uploaded_file)
    else:
        data = load_example_json()
        st.info("Using the preexisting example with five basic knowledge logic questions.")

    if data:
        user_feedback = {str(i): {'rating': None, 'comment': ''} for i in range(len(data))}

        st.markdown("### Step 2: Evaluate the responses")
        for i, item in enumerate(data):
            with st.container():
                st.markdown(f"#### Question {item['question_id']}:")
                st.write(item['prompt'])
                st.markdown("**Answer:**")
                st.write(item['output'])

                st.markdown("**Rating:**")
                rating = st.slider("", 1, 5, key=f"{i}_rating")
                st.markdown(
                    f"<h3 style='color: {visualization.get_color(rating)};'>{rating}: {visualization.get_description(rating)}</h3>",
                    unsafe_allow_html=True)

                user_feedback[str(i)]['rating'] = rating

                st.markdown("**Comment:**")
                comment = st.text_area("", key=f"{i}_comment")
                user_feedback[str(i)]['comment'] = comment

        st.markdown("### Step 3: Create your ratings JSON")
        st.markdown("Create the JSON file extended with your ratings and feedback.")

        if st.button('Prepare Download'):
            st.caption("Click the button below to download the JSON file.")
            for i, item in enumerate(data):
                item.update(user_feedback[str(i)])
            updated_json = json.dumps(data, indent=2)
            st.download_button(label="Download JSON with Feedback", data=updated_json,
                               file_name="updated_feedback.json", mime="application/json")

        st.markdown("### Step 4: Visualize your ratings")
        st.markdown("""
            The below plot shows the distribution of ratings. The chart visually represents the evaluation of the data in a unique style, 
            similar to a Likert chart displaying the spread of the scores across categories. The chart's divergence at the midpoint highlights 
            the contrast between ratings that indicate a lack of understanding (1 and 2) and those that reflect partial to complete correctness (3 to 5).
        """)
        if st.button('Create Visualization'):
            ratings_list = [feedback['rating'] for feedback in user_feedback.values() if feedback['rating'] is not None]
            if ratings_list:
                df = visualization.ratings_to_df(ratings_list, "Ratings")
                fig = visualization.plot_data(df)

                average_rating = sum(ratings_list) / len(ratings_list)
                st.markdown(f"#### Average rating: {average_rating:.2f}")

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No ratings to visualize. Please evaluate the responses first.")


if __name__ == "__main__":
    main()
