# A few notes
- This autograder is going to execute your code on my laptop. Security measures are a work in progress. Please don't do anything malicious.
- The autograder will only work during class.
- The autograder does not work on the stanford visitor wifi
# Making a private repo instructions. If you know have an alternate way you'd like to do this, feel free to skip:
- Go to github and make a new repo. *Make sure it's private*
- Go to your cs140e-25win directory and run `git remote add submit <your repo url>`
- Run `git push submit main`
- If you get an error in your push becuase you don't have access to your private repo, ask chatgpt "how to configure your command line to have access to your git private repos"
- Give Joe edit access to your repo in Settings > Collaborators on Github. Joe's github username is `dghosef`

# Turn in instructions
- Modify the `sunet`, `repo`, and `lab` variables in `sender.py` accordingly
- Make sure your repository is updated
- From your `cs140e-25win` directory, run `git commit -am "minor" or equivalent` and then `git push submit main`
- Run `python sender.py`. After about a minute, if you run `git pull`, you should see the output of the autograder in the `checkoffs` directory of the *autograder repo*
- Ask Joe if it's not working
# Checkoff Notes:
- *Trusting Trust*: For trusting trust, as long as Ken successfully logs in at the end of the output, you are good. Don't worry about any compiler warnings or if you fail the diff
