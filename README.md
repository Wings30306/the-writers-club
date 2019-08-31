# The Writers' Club

When I did the first project ([User Centric Frontend](https://wings30306.github.io/WingsBookClub/)), the main question I got from friends who write and read was: "Can you make it interactive so we can post our own stories and give feedback?" A few months have passed since, but it's here now: a website where you can post your own stories with no requirements: All stories are welcome here with no requirements or limitations for rating, genre, whether it's original or a fan fic, which fandom, how many chapters... and give feedback on other people's stories.

Happy reading / writing!
 
## UX

Read the full document for [thought process and database schemas](thought-process-and-database-schemas.pdf). As this project focuses on the back-end, a [template](https://startbootstrap.com/template-overviews/clean-blog/) has been used for the front-end look.


### User Stories
1.	As a reader, I would like to be able to read stories, preferably without signing in.
2.	**WIP** As a reader, I would like to see the ratings by other people to decide which story I would like to read.
4.	As a reader, I would like to be able to filter stories by fandom, genre, rating,…
5.	As a reader, I would like to give feedback for stories. I understand I’ll have to sign in to do this.
6.	**WIP** As a reader, I would also like to rate stories when I give feedback.
7.	As a writer, I would like to easily add new chapters / stories.
8.	As a writer, I would like to be able to change already-uploaded chapters too, in case I find a mistake or typo that needs to be corrected.
9.	**WIP** As a writer, I would like to be able to upload a cover image for my story. 
1.  If I don’t have a cover image, I'd like to have a choice of placeholder. 
1.	**WIP** As a writer, I would like to receive any feedback in email so I don’t always have to check the site for new posts.
1.	As a writer, I would like to be able to add a keyword (new genre, new fandom,…) if the one applicable to my story isn’t listed yet.
1.	**WIP** As a writer, I would like to know how many times my story has been read. Visualisation (statistical graphs)  would be also be  nice for this. Perhaps a dashboard for each author, to be accessed on sign-in?
1.	**WIP** As an admin, I would like to be able to suspend or block users who don’t follow the terms and conditions, for example those who post spam or don’t follow the guidelines for appropriate conduct.
1. **WIP** As an admin, I'd like to be able to delete inappropriate comments in feedback or edit the story characteristics if they were put in incorrectly.


## Features
 
### Existing Features
- User Registration: allows new users to create an account so they can log in.
- User Log-in: allows existing users to log in using their username or email and password. Passwords are hashed for security reasons. Log-in is required to read adult-rated stories, post your own stories and give feedback. 
- User Profiles: allow users to tell others about themselves, provide a list of stories posted by this user. A user must be logged in to edit their own profile. A user cannot edit someone else's profile. A user must be logged in and an adult to be able to see adult-rated stories by the user whose profile they visit.
- Search: allows a user to search for stories by rating, genre, fandom and/or author.
- All Stories: exactly what it says: provides a list of all stories available to the user (filters out adult-rated stories if user is not logged in or underage).
- Story pages: the main reason of existence for this project. These pages, generated for each chapter of each story, allow the user to actually read said story. 
- Admin Area/Meet the Team: introduces users to the admin team. If user is an admin, they will also see reports by users that may require admin action. 

### Features Left to Implement
- Allow users to upload their own cover image for a story.
- Show graphs for writers as detailed in user stories.
- Allow readers to rate other people's stories.
- Allow readers to search for stories based on other users' average rating.
- Allow admins to block/suspend users when necessary.


## Technologies Used

### Languages
- [HTML](https://html.com/#What_is_HTML) provides the main building blocks of the website in terms of structure and fixed content.
- [CSS](https://techterms.com/definition/css) adds custom styling beyond what's provided in the template.
- [Javascript](https://www.javascript.com/) is used to make the Quill editor work: 
    - customize user options for styling their story, feedback or profile text.
    - transfer the content of the Quill editor to a hidden input field in order to send it to the back-end for storing in the Database.
- [Python](https://www.python.org/) provides the connection to the backend, specifically the NoSQL (Mongo) database that's hosted by [mlab](https://mlab.com). Also, it allows the use of the [Jinja](https://palletsprojects.com/p/jinja/) templating language that's used to display the data to the user and make the website dynamic - no need for hard-coding everything!

### Frameworks
- [Bootstrap](https://getbootstrap.com/) provides the grid system that's used to make the website look good, as well as several components such as the responsive nav bar. The [template](https://startbootstrap.com/template-overviews/clean-blog/) used was also built with and provided by Bootstrap.

### Libraries

- [JQuery](https://jquery.com) was used to simplify DOM manipulation. It is also required to make Bootstrap work. 
- [Popper](https://popper.js.org/) is required to make Bootstrap work.
- [QuillJS](https://quilljs.com/) provides the text editor that allow users to style their own content (stories, feedback, profile text). If you want _italic_ or **bold** text for example, you can add this easily.


## Testing

In this section, you need to convince the assessor that you have conducted enough testing to legitimately believe that the site works well. Essentially, in this part you will want to go over all of your user stories from the UX section and ensure that they all work as intended, with the project providing an easy and straightforward way for the users to achieve their goals.

Whenever it is feasible, prefer to automate your tests, and if you've done so, provide a brief explanation of your approach, link to the test file(s) and explain how to run them.

For any scenarios that have not been automated, test the user stories manually and provide as much detail as is relevant. A particularly useful form for describing your testing process is via scenarios, such as:

1. Contact form:
    1. Go to the "Contact Us" page
    2. Try to submit the empty form and verify that an error message about the required fields appears
    3. Try to submit the form with an invalid email address and verify that a relevant error message appears
    4. Try to submit the form with all inputs valid and verify that a success message appears.

In addition, you should mention in this section how your project looks and works on different browsers and screen sizes.

You should also mention in this section any interesting bugs or problems you discovered during your testing, even if you haven't addressed them yet.

If this section grows too long, you may want to split it off into a separate file and link to it from here.

## Deployment

This section should describe the process you went through to deploy the project to a hosting platform (e.g. GitHub Pages or Heroku).

In particular, you should provide all details of the differences between the deployed version and the development version, if any, including:
- Different values for environment variables (Heroku Config Vars)?
- Different configuration files?
- Separate git branch?

In addition, if it is not obvious, you should also describe how to run your code locally.


## Credits

### Content
- All stories were provided by the respective authors/users.

### Media
- The masthead image [Person Typing On Typewriter](https://www.pexels.com/photo/person-typing-on-typewriter-958164/) was posted by [rawpixel.com](https://www.pexels.com/@rawpixel) on www.pexels.com.
- The paintings for the cover image choice were kindly provided by [CreaFien](https://robbehenderickx.wixsite.com/creafien)

### Acknowledgements

- I based the layout for the site on this [template: Start Bootstrap - Clean Blog](https://startbootstrap.com/template-overviews/clean-blog/)