% kb.pl

% Facts
parent(john, mary).
parent(john, bob).
parent(ann,  mary).
parent(ann,  bob).

parent(mary, susan).
parent(bob,  tom).
parent(bob,  mark).

male(john).
female(ann).
male(bob).
female(mary).
female(susan).
male(tom).
male(mark).

% Rules
% Inverse parent→child
child(X, Y) :- parent(Y, X).

% Siblings
sibling(X, Y) :-
    parent(P, X),
    parent(P, Y),
    X \= Y.

% Grandparent
grandparent(X, Y) :-
    parent(X, Z),
    parent(Z, Y).

% Cousins
cousin(X, Y) :-
    parent(P1, X),
    parent(P2, Y),
    sibling(P1, P2),
    X \= Y.

% Aunt/Uncle
aunt_uncle(X, Y) :-
    sibling(X, P),
    parent(P, Y).

% Niece/Nephew
niece_nephew(X, Y) :-
    aunt_uncle(Y, X).

