# bettersheet5e
The form is live on [https://bettersheet.onrender.com/](https://bettersheet.onrender.com/). It might take a minute to load up.
# Introduction
This is a minimalistic, easy to use, modular and beginner friendly online character sheet creator for Dungeons and Dragons 5th edition.
With this form you are able to generate semi-dynamic character sheets with an intuitive design, clickable elements, with as much or as little explanation as your table requires it. _It is possible to **make a good looking, full character sheet under a minute.**_ I created this for my beginner DnD party because I wanted them to be able to:

- Have a clean and simple overview of their character sheets;
- Not worry about keeping a crumpled up piece of paper;
- Read about, and understand their abilities and items without having to hunt for information online or in the books.

For more advanced parties this is also useful, as the more integrated and official digital character sheets are often bloated with unnecessary information that gets into the way of play. 

**You are in control over the names and descriptions of your items and abilities. This tool is highly recommended for:**
- Non-English tables;
- Homebrew content;
- Adding custom lore to items, spells, weapons.

# How it works
After you fill out the form, a HTML template is generated and it downloads. **The HTML file can be opened locally in your browsers, or it could be uploaded online for free** (see recommended use).
It is recommended that you fill out everything in the form to have the full experience, but the flexibility of the generator allows you to input just the bare minimum if you are in a hurry. As a DM, I sometimes create a barebones sheet for NPC-s, to help me remember them later and to have its stats ready in one place if I need it in an instant.
**It is also possible to load a previously generated character sheet back into the form.** This is important for level ups, losing or receiving items, correcting mistakes without having to restart the creation process.
## Recommended creation flow
When I create full player character sheets using this tool, I usually note the necessary calculations (like character HP, AC, ...) on a piece of paper and start inputing everything. For weapons, features, items, spells, I use the descriptions from online databases like DnD Beyond or wikiDot as reference to personalise descriptions to the player's character or the person's preferences. To style the text it is possible to use [HTML text formatting](https://www.w3schools.com/html/html_formatting.asp). 

## Recommended use
As I mentioned before it is perfectly reasonable for everyone to have their character sheets on their own computer that can be opened locally in their browser. However, I like for my party to have a central hub for all of their character sheets that everyone can access online on their computer, tablet or phone at all times. _(Note: Do this only if there are no secret character features are planned that would be spoiled if the party could see each others' sheets. Check with the others first.)_
### Option 1: Staying local
This is the easier, more traditional route. After downloading the HTML file you are able to open it within any browser of your choice. 
### Option 2: Going Online
There is more initial setup needed for this option, but it should not take over 15 minutes even if you have never done anything like this before. **I will take you through a click by click guide for complett beginners.**

1. Create a new folder on your computer. For better organisation all of your downloaded files should go here for now.
2. Withing the files you will find an `index-template.html` template. Download it into your folder and **_change the name from `index-template.html` to `index.html`!_**
3. Using the creator form make your character sheets that you will want to upload. Place them in the same folder as `index.html`.

_Now we will need to point `index.html` to the character sheets._

4. There is an inbuilt tutorial within `index.html`, follow that in accordance with the provided example image. You only need to change the contents withing the <body> section, you can ignore everything else. _If you don't know how to edit HTML files, [follow this guide](https://www.w3schools.com/html/html_editors.asp)._


<img width="750" height="229" alt="14388" src="https://github.com/user-attachments/assets/a519c819-8a3c-4e75-bb4f-dbe8fe14a6eb" />


_For the next steps, you will need a GitHub account._

5. On the [github.com](https://github.com/) Dashboard page you need to create a new repository. Give it a name, set it to private and add a README.


<img width="750" height="729" alt="image" src="https://github.com/user-attachments/assets/f79a8a46-b8e6-479a-94fd-5461892b25f3" />


6. Click here and upload the files from your local folder including `index.html`...


<img width="750" height="370" alt="image" src="https://github.com/user-attachments/assets/57cce722-9a32-4e0e-a1d5-7274cde6284a" />


7. ...and commit the changes. _(Make sure again that the filename of_ `index-tempplate.html` _was changed properly to_ `index.html`_.)_


<img width="750" height="346" alt="image" src="https://github.com/user-attachments/assets/d352fa84-cd47-4e70-82f3-efa8a4635a19" />


_Now that your files live online, you can decide to keep them on your computer or delete them. For the next steps, you will need a Netlify account. You can even sign up with your new GitHub account._

8. After logging in, create your first 'Team' for free and click 'Add New Project'. Since we created the GitHub repository with your files, you should select 'Import from an existing project'.


<img width="750" height="127" alt="29480" src="https://github.com/user-attachments/assets/bb90ec8b-5d65-49e4-8eb1-8c4d2037976f" />


9. Select GitHub.


<img width="750" height="312" alt="24866" src="https://github.com/user-attachments/assets/3b5cb969-f462-41b7-93c7-6fb7ae6efaf3" />


10. Your repository should show up on the list. Click it. If not, maybe check the connected accounts, or click 'Configure the Netlify app on GitHub' and follow Netlify's guide.


<img width="750" height="394" alt="81149" src="https://github.com/user-attachments/assets/9f33873a-0cab-4f56-88ec-7dda68f6ad2c" />


11. Give the project a name (this will be the URL, so choose carefully), and click deploy. After a few minutes of waiting, you now have your own character sheet hosting website up and running 24/7 for free. Enjoy!



# Technical explanation, roadmap and finishing comments
In reality I made this because I was about to start learning web development with Flask in uni and I wanted to try it in advance. I was curious :) Then more and more features ballooned the project and I ended up spending almost a month working on it (instead of the one afternoon I originally thought). It was a fun learning experience though! For me, this is a really useful tool that I actually use and think is better than any alternative out there.
For my personal needs, this is a complete product, however you cannot make a Druid conveniently, using the Class Resources editor for Wild Shape. This is because I do not understand how it works and I didn't want to just hack it in with an LLM. 
If anyone ever reads this: Hi, if you want me to add Druids send me a message and I'll find the time :)
