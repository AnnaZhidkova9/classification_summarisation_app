# classification_summarisation_app
The functionality of the system.
The system for classifying and summarizing Arctic news is written in the Python programming language. The main task is to collect the text of news on Arctic topics from websites and output the summary for each news item. The final result is also influenced by the choice of the desired number of sentences in the summary.
The functionality of the system is arranged as follows: when the user launches the application, he sees the main screen with an available list of functions. The structure of the application's functionality: the user can choose the site where the news search will take place, select the topic, enter the desired number of sentences in the summary. In addition, the functionality of searching for news by substring is available.

The application interface.
Figure 1 shows the application interface, which is the main window that serves as the basis for the entire user interface.
 ![interface](https://github.com/AnnaZhidkova9/classification_summarisation_app/assets/86468434/8527217d-51e6-41bb-a84a-1b73a152b298)
 Figure 1 – Application interface
At the top of the interface there are interactive elements available to the user for interaction. One of these elements is a substring input field designed to search for news by name. This field provides a convenient way for the user to enter keywords or phrases that can be used to filter news. The next element is the button that is clicked to perform the search. It is used to activate the search process, initiating the processing of the substring entered by the user and displaying the search results. An example of how the search bar works is shown in Figure 2.
 ![search](https://github.com/AnnaZhidkova9/classification_summarisation_app/assets/86468434/f9910530-6e98-4957-bb59-d3d532d1785f)
 Figure 2 – An example of how the search bar works
Next, there are two drop-down lists: one with the URLs of the sites and the other with the topics (Figure 3). These lists allow the user to easily select the news source and the topic on which he wants to search for information. There is also a button next to the drop-down list of topics to cancel the application of the selected topic, which gives the user the opportunity to quickly reset the selection and return to the general list of news. 
 ![sites_themes](https://github.com/AnnaZhidkova9/classification_summarisation_app/assets/86468434/5c40056e-84a5-48df-84e2-ae1766a52bca)
 Figure 3 – Selection of the site and the subject
Next to it is a field with a selection of the desired number of sentences in the summary in the range from 1 to 5. By default, the number 3 is specified in this field, which means that when the application is launched, a three-sentence summary is displayed in the column of the summary table. The next element of the interface is a button for applying the selected number of sentences, which activates the process of summarizing the news text.
Most of the interface is occupied by a table that displays the names of all the news, the dates of their publication, the topic and the summary. All data except the summary is taken from the database and filtered by date. When you click on a row in the table, a link to the corresponding news item is clicked. The table is a data visualization tool, allowing the user to easily view and analyze information.
