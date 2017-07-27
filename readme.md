#Sportsbot!
##Summary
Sportsbot is a tool I use to keep track of the sports I watch and graph them. The initial motivation was to start familiarizing myself with plotly and pandas, using a data set I actually cared about. Rather than find an existing set, I thought it would be fun to make my own! I watch a lot of sports, so I figured that would be a good place to start. :)

##Flow
- I watch a sporting event.
- I have an IFTTT recipe that knows the teams I follow, and will tweet at me, asking if I watched. I can respond yes, and it will be added to a table in a MySQL db on a digitalocean droplet I own, using PeeWee. I can also add a sport manually.
- I have a series of scripts that run on cronjobs to extract data from that table and push it to plotly.
- Those plotly charts are embedded in an html dash, that is visible on my website. You can see it here: http://www.twharr.com/sports/
