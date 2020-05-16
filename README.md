# Uses tex/mathjax as image in editor/reviewer
## Rationale
Most of the time, I don't care about the LaTeX/MathJax code, appart
when I want to edit it. I prefer to see the result. So this add-on
does just that. Editor and browser show the result of the
compilation. And you see the original code only when you click on the
field you want to edit.

![Example](ex.png)

## Warning
### Incompatible add-ons
A previous version of the add-on was incompatible with multiple other
add-ons. It is now corrected.

## Technical

The note editor is actually an html page. Each time a field is edited,
javascripts sends the new value to python, which eventually save the
value in the database. For this reason, I need to ensure that images
are replaced by original TeX as soon as the user click in the
field. This leaves less freedom that what I would have wanted to
do. Most of the features in TODO seems too risky to implement right
now.

## Internal
It changes the javascript methods:
* onFocus
* setFields

## TODO
### Save TeX in tag
Save original tex in html image tag. So that if the bug I consider
above occurs, tex can be taken back. 

### Replace by TeX code when clicking on image
Currently, as soon as field is selected, LaTeX code come back. It may
be better to do this change when we click on image. I'll see when I
use the add-on whether I find it worth to take the time to implement
this feature.

### When opening editor, do not select first field.
This way, we can see the imagen of the first field tex.


## Links, licence and credits

Key         |Value
------------|-------------------------------------------------------------------
Copyright   | Arthur Milchior <arthur@milchior.fr>
Based on    | Anki code by Damien Elmes <anki@ichi2.net>
License     | GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
Source in   | https://github.com/Arthur-Milchior/anki-tex-as-image
Addon number| [882784122](https://ankiweb.net/shared/info/882784122)
