Solving the Data Extraction Problem
===

Yes, the clickbait title was unashamedely intentional. No, I'm not formally
solving anything (my apologies to all the formal-proof-loving people
I've mislead into my post). Yes, there's an algorithm:

    Given a tree, return a list of all subtrees - sorted by the number of 
	children relative to the root node in the subtree.

##*The Problem*

According to [wikipedia](http://en.wikipedia.org/wiki/Data_extraction): 

> **Data extraction** is the act or process of retrieving data out of 
(usually unstructured or poorly structured) data sources ... Typical 
unstructured data sources include web pages ...

The problem I'm attempting to tackle is that of extracting data from 
websites. 

##*What sort of "data" are we extracting?*

The correct answer, I'd argue, is: *the sort of data that's produced by 
the source of that data*. But let's get specific. 

Websites are structured by HTML (sure, the styling is also partially 
responsible for the *visual* structure, but as you'll see later on, 
we don't *have* to take style sheets into account).

*What data can we get from __webpages__?*

Instead of writing down some cryptic but arguably true answer, I'll give
a bit of background as to why the heck I'm even tackling this problem
(don't worry, feel free to skip the next few paragraphs - I define
"data" as *article text and tabular data*).

About 4 months ago, I debuted [eatiht](https://github.com/rodricios/eatiht) 
(a text extracting library; the predecessor to this algorithm) on [reddit](http://www.reddit.com/r/compsci/comments/2ppyot/just_made_what_i_consider_my_first_algorithm_it/).
I can only say positiive things about doing so. It's landed me an opportunity
to coauthor a paper with [Tim Weninger](http://www3.nd.edu/~tweninge/). 

It was Tim who introduced me to the *structured [tabular] data extraction* problem. 
He illustrated the scenario of trying to extract ``<table>``'s and table-like 
structures from a website. 

For example, let's take [reddit](http://www.reddit.com):

![reddit tables](http://i.imgur.com/OsA7Iiyh.png)

What's highlighted in red is what I'm referring to as *structured* or *tabular data*. 

Since we're dealing with HTML, let's have a look at the underlying markup: 

###Subreddits

![subreddits](http://i.imgur.com/d3cFlB8l.png)

###Top posts

![top posts](http://i.imgur.com/78rNdf4l.png)

