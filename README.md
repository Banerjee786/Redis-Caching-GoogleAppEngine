Redis-Caching-GoogleAppEngine

This is to display the faster access of data items using Redis [Alternative to Memcache (could have also used Memcache)]. Configured 
a Redis Server to start the service before using Redis.

Commands to install and start redis-server are as follows :
sudo apt-get install redis-server
sudo service redis-server start

On clicking the button 'Redis', it navigates to the response.html page and displays the Average Response Time for a standard query looped
a number of times using Redis, while clicking on 'NonRedis' button gives us the Avg. Response Time of the same query iterated same no. of
times without Redis.

It's observed that Redis is 10 times faster than standard query [usually iterated many times(here I've iterated 100 times)].

Therefore, Redis is helpful when we same some static (rarely changing) data which needs to be fetched all the time, a faster way of 
accessing data items.

