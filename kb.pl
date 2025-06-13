#% === Facts ===
#parent(john, mary).
#parent(john, bob).
#parent(ann, mary).
#parent(ann, bob).
#
#parent(mary, susan).
#parent(bob, tom).
#parent(bob, mark).
#
#male(john).
#female(ann).
#male(bob).
#female(mary).
#female(susan).
#male(tom).
#male(mark).
#
#% === Rules ===
#% 1. child is inverse of parent
#child(X, Y) :- parent(Y, X).
#
#% 2. siblings share a parent and are distinct
#sibling(X, Y) :-
#    parent(P, X),
#    parent(P, Y),
#    X \= Y.
#
#% 3. grandparent relation
#grandparent(X, Y) :-
#    parent(X, Z),
#    parent(Z, Y).
#
#% 4. cousin: children of siblings
#cousin(X, Y) :-
#    parent(P1, X),
#    parent(P2, Y),
#    sibling(P1, P2),
#    X \= Y.
#
#% 5. aunt/uncle relation
#aunt_uncle(X, Y) :-
#    sibling(X, P),
#    parent(P, Y).
#
#% 6. niece/nephew inverse
#niece_nephew(X, Y) :-
#    aunt_uncle(Y, X).
#

% kb.pl
parent(alice, bob).
parent(bob, charlie).
parent(charlie, diana).
parent(diana, edward).
parent(edward, fiona).
parent(fiona, george).
parent(helen, ian).
parent(ian, jane).
parent(jane, kevin).
parent(kevin, lisa).

% Rules
ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).
sibling(X, Y)  :- parent(Z, X), parent(Z, Y), X \= Y.
grandparent(X, Y) :- parent(X, Z), parent(Z, Y).
descendant(X, Y)  :- ancestor(Y, X).

