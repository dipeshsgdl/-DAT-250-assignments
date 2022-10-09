# Mandatory 1

First things first, the project was fetched/cloned from the github. Upon doing that, it was made sure that required libraries were installed and it was checked that it worked just fine (flash run - worked). Next step was to do what 'normal' person would want to do and that is to create new account and try to log in. After log in, it was checked for what kind of 'features' this project had - from the users perspective. Finally after doing all that, it was 'tested' for common vulnerabilities and there was an attempt (hopefully successful) to patch all found vulnerabilities.

## SQL-Injection
User input was neither converted to injection 'safe', nor was it implemented in a 'safe' way. In order to select or insert information the way it was implemented was that the query command was formatted with the given string which was written by user. So basically that string was inserted right into the query command.
Example:
> db.execute("SELECT * FROM Users WHERE username='{}'".format(test))

It's one of the 'unsafe' ways to insert string, since one can just escape apostrophe. One of the ways to reduce injection would be to use some kind of library or something like that which could convert special symbols to something else like ascii. Also instead of using format or similar, it is better to just use arguments.
Example:
>db.execute("SELECT * FROM Users WHERE username=?", [username])

It is a safer way to insert information that was written by the user that we can't trust and as said, might reduce a chance of SQL-Injection.
The bad thing about SQL-Injection is that 'hacker' might gain access admin access if the website was implement terribly, or 'hacker' might collect crucial and/or secret information that might lead in user endangerment or financial loss.

## Imports/packages
There might been packages/imports that had vulnerabilities, which is why is it good to check if that exact library that is being used has or had vulnerabilities. If it didn't had it at that exact moment, it is still good to check occasionally for the vulnerabilities so long, one still uses third party library/package. One can use snyk or similar to check if that current library version has any whatsoever vulnerabilities in it.

## Debug Mode
In the ".flaskenv" file, flask environment wasn't set to "FLASK_ENV=product". That means that debug mode was on, and with the brute force, 'hacker' could access the terminal.
>localhost:5000/console

In order to prevent that, flask environment was changed to product.

## Insecure design
It is possible for the 'hacker' to brute force usernames and passwords. Each time username or password was incorrect, 'hacker' didn't had any whatsoever timeout which means that 'hacker' could run a brute force script or program as fast (not really - depends how fast server can respond and etc) as wanted. Another thing was that it said which one was incorrect, whether username was incorrect or password. Another problem was that passwords weren't encrypted. That means that if the database were to be leaked, 'hackers' could see the passwords in plain sight.

Solutions that were used to prevent these kinds of problems were:
* request limit was introduced (how many request can person make before timeout)
* phrasing was changed to say username, password or both were wrong
* Bcrypt was introduced in order to encrypt users passwords.
