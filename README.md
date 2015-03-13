# various

## dops

better `docker ps`

![how dops looks](http://i.imgur.com/QkJ6Px9.png)
coreos.com

## etcdtree

compact listing of whole tree of etcd 
```
» etcdtree                                                                  1 ↵
coreos.com
 ├── tomk => 55
 ├── updateengine
     └── rebootlock
         └── semaphore => {"semaphore":1,"max":1,"holders":null}
 └── xomk => 88
```
