# From developer to developer
> Some chaotic notes on transitioning to the new paradigms used in this project

## Why webpack and not browserify?

Browserify system is to chaotic. There's no central place that gives the developer an overview of all the typical needs.
"Go find it yourself" atititude for everything is neither polite nor energy-saving.

Most of functionality is also "build-it yourself". Basics like inlining images as `data:base64` in css
and extracting all styling into single file are like this.

Additional research that could be done:
 - https://gist.github.com/substack/68f8d502be42d5cd4942
 - https://webpack.github.io/docs/webpack-for-browserify-users.html
 - https://github.com/kriasoft/react-starter-kit/issues/3
 - https://github.com/substack/browserify-handbook#introduction
 - https://github.com/tcoopman/react-es6-browserify/blob/master/gulpfile.js
 - https://www.google.bg/search?q=browserify+es6+react+gulp&oq=browserify+es6+react+gulp&aqs=chrome..69i57j69i60.13997j0j1&sourceid=chrome&es_sm=93&ie=UTF-8
 - http://cheton.github.io/browserify-css/


## Why react
After looking over dozens of alternatives and reading through examples, articles and videos.

Pros:

 1. Number one reason: tooling. All kinds of tools evolve for React, including a georgous integration with webpack.
 1. Uses class-based component approach. Easy to extend, possible to use ES6 features like decorators
 1. Easy and performant way to pass element down to another and specify its purpuse. Done via passing element in property:
  ```
<Heading icon={<Icon/>}>....
```
 1.


## Java server-side rendering:
http://winterbe.com/posts/2015/02/16/isomorphic-react-webapps-on-the-jvm/

## Python server-side rendering:
https://github.com/logandhead/ReactiPy
https://github.com/reactjs/react-python
https://github.com/markfinger/python-react

## Close alternatives to React worth checking out:
https://github.com/riot/riot
https://github.com/vuejs/vue

## Good Examples during development
Using sass as styling: https://github.com/react-toolbox/react-toolbox
If needed: wrapping jquery plugin (selectize): https://github.com/ggarek/react-selectize/blob/master/src/react-selectize.js

### CSS MODULES - important for styling react components
http://survivejs.com/webpack_react/styling_react/

postcss-loader cannot be used with CSS Modules out of the box due to the way css-loader processes file
imports. To make them work property, either add the css-loader’s importLoaders option:
{
    test:   /\.css$/,
    loader: "style-loader!css-loader?modules&importLoaders=1!postcss-loader"
}
{
    test: /(\.scss|\.css)$/,
    loader: ExtractTextPlugin.extract('style', 'css?sourceMap&modules&importLoaders=1&localIdentName=[name]__[local]___[hash:base64:5]!postcss!sass?sourceMap')
}

## External templates
- https://github.com/wix/react-templates
- https://github.com/reactjs/react-magic/blob/master/README-htmltojsx.md
- https://github.com/mikenikles/html-to-react

## Useful UI
- Select dropdown: https://github.com/JedWatson/react-select / http://jedwatson.github.io/react-select/
- Tabs: https://github.com/rackt/react-tabs/blob/master/lib/components/TabPanel.js

### Animation
 - old i think: https://github.com/chenglou/react-tween-state
 - old i think: https://www.youtube.com/watch?v=9cY8-xCfU9E
 - https://github.com/hzdg/gsap-react-plugin
 - https://facebook.github.io/react-native/docs/animations.html#animated
 - http://greensock.com/gsap + http://greensock.com/tweenlite

## React + canvas = 60fps
- http://engineering.flipboard.com/2015/02/mobile-web/

## React notes
Ugly looping in template:
<Comments>
  {[this.props.comments].map((data) =>
    <Comment key={data.} />
  )}
</Comments>


Template MUST have tags with upper case for custom (non html-native) elements.
 
```
<div>
    <Comments>
      {[this.props.comments].map((data) =>
        <Comment key={data.} />
      )}
    </Comments>
</div>
```


Template html can best be decouped like this:

import Comment from './comment'
import Survey from './survey'

```
export default () =>
    <div>
        <Comments>
          {[this.props.comments].map((data) =>
            <Comment key={data.} />
          )}
        </Comments>
    </div>
```

Angular, Ember and some of the rest have this weird concept of resources 
which is like duplicating business database logic on frontend.

UI must only be UI.

Angular has the weird $digest, $apply and other meaningless by themselves concepts.
React setState is much better (or even single-state with redux).

Angular directives weird:

```
scope: {
    one: '@',
    two: '=',
    three: '&'
}
```

Also naming like: `link, transclude`.

Templates in React are freaking mess. Only react-templates eases the process a bit, still some angular-like prefixing of
attributes (rt-if.. wtf).

EDIT: This is also good: https://github.com/AlexGilleran/jsx-control-statements

Server-side rendering is freaking mess. Some sort of checks for DOM should be performed in the code (canIuseDom)



`Skate.js` errors with the Signali project:

The problem with `<content>` -> you don't know what's in there until it renders.
You can do data manipulation via properties in the `<content>` because it's 
unknown and it doesn't know of its parent.
`"ready"` callback is triggered before children are resolved/

Too much data loaded on initial load.
It must be loadad async instead.

Access `setAttribute` to manipulate DOM (is it bad? - it's bad to know the template, only know data and events)
Using attributes for behavioir - due to the `<content>` tags

Slow due to the `<content>` tags.

`<content>` Must be removed but having it allows server-side rendering of content withouth gimmicks like node servers.


Current situation of `Signali` is a good transitional state until a better solution is found.
Loaders, css animations and other good UX stuff are still written in SASS and similar.
SASS still cant be fully parsed with postcss. Porting is undesired work.


## Making iteratables emit events on loop and end
https://github.com/ReactiveX/RxPY
https://github.com/Reactive-Extensions/RxJS

Thoughts: But what is the purpuse? This should be async, so it should live in an async world, so HTTP requests wont do.
May be something like firing web socket events? That's not really a thing, web sockets send signals, which is the same.

So may be use in in the frontend, with JS? To monitor server, catch new entries (via polling) and distribute them via
events? Weird.

# Router
Not using react-router because it actually hides components instead of 
modifying the data in them.  Routing that simply swaps the whole page is stupid,
it disables all options for animating transition of single components in the page.
Instead on page change -> change data and trigger rerender. 
Let elements handle tha change, not the router 

The whole purpose is to pass data not to hide elements based on URL.
So a very simple custom url change handling is in order:

1. `<Link>` element to notify of url change
1. Mechanism (like redux) to capture the notification and notify everyone subsribed
1. Data (state) is changed based on the url
1. App is rerendered with new data

Implementation is almost done but still some bits remain in progress.



If URL changes (PAGE_NAVIGATION_END) -> state changes -> renrender each Link
on render check if current location path equals link path. if the same -> merger query params and update href

Problem: changing current path path to as/asdasd/add-new


# Other notes

You can't style (*put css selector*) any tag starting with capital letter.
Instead you must set "className" property to styles.something

Tag names must  never be used for selectors. NEVER. 
Only classes and attributes.

The direcctory called `elements` in Signali project is now split to
projecct-specific (src) and other reusable elements (obshtestvo-ui).


React's 

`Component context` is something that is passed down to all descedants
BUT only accessible if the descendents explicitly asks for it


Opening modal -> remembers current url
Closing modal -> restore remembered url