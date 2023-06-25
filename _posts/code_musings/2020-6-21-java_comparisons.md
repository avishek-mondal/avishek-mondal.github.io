---
layout: post
title: Java Comparisons
permalink: code_musings/comparisons
---
Another clarification of a fairly basic Java  

{% highlight java %}
public class Point {
        private int x;
        private int y;

        Point(int x, int y) {
            this.x = x;
            this.y = y;
        }

        public int getX() {
            return this.x;
        }

        public int getY() {
            return this.y;
        }

        @Override
        public boolean equals(Object o) {
            if (getClass() != o.getClass())
                return false;
            Point other = (Point) o;
            return this.x == other.getX() && this.y == other.getY();
        }

        @Override
        public int hashCode() {
            // just use some inbuilt hashcode generator 
            return Objects.hash(this.x, this.y);
        }
    }
{% endhighlight %}

We can obviously debate the wisdom of using Objects.hash (maybe some bad things might happen in edge cases) as opposed to coming up with our own hashing function (definitely some bad things will happen in edge cases) - but why would we? We're all friends here, and this is just an example.  

## Comparable interface 

If for some reason, you want to use TreeSets/TreeMaps, you have to then implement your user defined class as a Comparable interface. But this is tricky! We are talking about 2D points here - how do you "compare" them? This is up to you to decide. Say for whatever application, we want to sort by x-coordinate, and then by y coordinate. With the same point class, it could be something like - 

{% highlight java %}
public class Point implements Comparable<Point> {
        private int x;
        private int y;

        Point(int x, int y) {
            this.x = x;
            this.y = y;
        }

        public int getX() {
            return this.x;
        }

        public int getY() {
            return this.y;
        }

        public int compareTo(Point o) {
            if (this.x == o.getX()) return Integer.compare(this.y, o.getY());
            else return Integer.compare(this.x, o.getX());


        }
}
{% endhighlight %}

So yea that is it. 

## Final note

Ok, so the the 2D point thing was really contrived. If you really had to do it in an interview situation, you should put in ArrayLists into your HashMaps/HashSets, everything is already pre-built for you! 

Reminder of how this works - 
{% highlight java %}
HashSet<ArrayList<Integer>> m = new HashSet<>();

ArrayList<Integer> p1 = new ArrayList<>();
p1.add(0);
p1.add(1);
m.add(p1);

ArrayList<Integer> p2 = new ArrayList<>();
p2.add(1);
p2.add(2);
// prints false
System.out.println(m.contains(p2));


ArrayList<Integer> p3 = new ArrayList<>();
p3.add(0);
p3.add(1);
// prints true
System.out.println(m.contains(p3));
{% endhighlight %}