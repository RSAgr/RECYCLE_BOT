# Your Own MBBS Bot 🩺

This Streamlit application allows users to solve their medical queries by processing health-related articles from specified URLs or websites. The application uses OpenAI's language model to answer health-related questions based on the provided data.
You can either choose the bot to answer your queries using the data based on webpage(s) you provide or using its own default data.
If the user chooses to provide its own data, it could be provided as individual webpages (max 3) or providing a entire website (through which we will scrap data for the max pages you specify)

# Important:

Do Install the required packages using 'pip install -r requirements.txt'
Also install Pathway using 'pip install -U pathway'

# Project Structure:

main.py: The main application script
requirements.txt: Requirements for the project
.env: Environment file to store sensitive information like API keys

# Please Note:
The application uses FAISS (Facebook AI Similarity Search) to store and retrieve embeddings efficiently.
Ensure you have a valid OpenAI API key to use the language model.

# You can view a video demo on the working of the app:
https://www.youtube.com/watch?v=Jci8gWEP_9A&ab_channel=BansalTalks

# License:
This project is licensed under the MIT License. See the [LICENSE.txt](LICENSE.txt) file for more details.

Contributions are welcome! Please open a pull request or issue on GitHub if you have any suggestions or improvements.