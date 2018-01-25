# LetterCount

LetterCount allows users to query for the number of times the letter 'p' (or 'P') appeared in their favorite subreddit
in the past 1000 posts. Currently only post titles are checked for the letter. Post content and comments are ignored. 
With the application running, you can request a word count for your favorite subreddit by making a request to 
`http://127.0.0.1:8000/reddit/<name of subreddit>`, i.e. to count occurrences of 'p' in /r/aww you could navigate to 
`http://127.0.0.1:8000/reddit/aww` in your browser.


## Running the application
1) Clone repository: `git clone git@github.com:lfowlie/letterCount.git`
2) It is probably a good idea to use virtualenv to keep dependencies clean, so install virtualenv: 
`pip install virtualenv`
3) If you're using virtualenv, create an environment: `virtualenv <path to environment>` Note that this project
uses `python 2.7.10`, you can specify a specific instance of python for virtualenv to use with the `--python` flag
4) Activate the virtual environment you just created: `source <path to environment from step 3>/bin/activate`
5) Within the top level `lettercount` folder, install dependencies: `pip install -r requirements.txt`
6) Run it: `python manage.py runserver`
7) Request a count for your favorite subreddit in browser or via curl: `curl http://127.0.0.1:8000/reddit/aww/`


## Future Improvements

- The Reddit API limits history to the past 1000 posts. An improvement over the current approach would be to run a 
 recurring job that pulls down the post history of every subreddit (there are a little over 1 million)every 10 minutes
 or some other reasonable amount of time. The 'p' count would be updated in the database and retrieved at request time
 to be displayed to the user. This would also require storing some kind of "most recent post retrieved" in the database
 for each subreddit so we know where to start counting from the next time we pull down post history.
 
- Integrate with other APIs. For example we could allow users to count the number of occurences of 'p' in the 'Pizza'
 wikipedia article by integrating with their API and allowing users to navigate to `/wikipedia/pizza`
 
- Depending on how this data is to be consumed, one improvement could be to create a frontend or change responses to be
 JSON format.
 
- Extend to allow obtaining a count for any letter or even word. This should just be a matter of adding a query
 parameter to the request to allow the user to request a specific letter or word, and then searching all post titles for
 that letter or word instead.

- Extend to allow checking for occurrences of the letter in the post contents and/or comments.

- Add logging and metrics