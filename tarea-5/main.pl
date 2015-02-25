% prolog

% hechos: asocia un arma a los valores de bonificacion
% de defensa, velocidad y fuerza respectivamente a un personaje
arma(espada_y_escudo, 20, 20, 20).
arma(baston, 0, 30, 30).
arma(espada_larga, 0, 0, 60).
arma(arco_y_flecha, 0, 60, 0).

% hechos: asocia una armadura a los valores de bonificacion
% de defensa, velocidad y fuerza respectivamente a un personaje
armadura(armadura_ligera, 20, 40, 0).
armadura(armadura_completa, 60, 0, 0).
armadura(armadura_normal, 40, 20, 0).

% hecho: ingreso de un personaje
personaje(player1, 1, 10, 0, espada_y_escudo, armadura_ligera).
personaje(player2, 0, 10, 0, espada_y_escudo, armadura_ligera).

% devuelve la suma de la velocidad, defensa y fuerza que entrega
% la armadura, la arma y el valor del personaje inicialmente asignado
% las sumas son entregadas en D, V, F respectivamente.
% N es el nombre del personaje
evalpoder(N, D, V, F) :-
    personaje(N, D3, V3, F3, W, A),
    arma(W, D1, V1, F1),
    armadura(A, D2, V2, F2),
    D is D1+D2+D3,
    V is V1+V2+V3,
    F is F1+F2+F3,
    D3+F3+V3 =< 100,
    D1+V1+F1 =< 60,
    D2+V2+F2 =< 60, !.


% entrega el ganador de la pelea entre dos personajes con nombres X e Y.
% el nombre del ganador es entregado en Z. A su vez si existe un empate,
% Z tendra el valor empate.
% Si alguno de los jugadores tiene valores invalidos
% (D, V y F suman mas de 100), entregara un mensaje de alerta en Z.
pelea(X, _, Z) :-
    personaje(X, D1, V1, F1, _, _),
    Z = x_invalid, D1+V1+F1 > 100, !.

pelea(_, Y, Z) :-
    personaje(Y, D1, V1, F1, _, _),
    Z = y_invalid, D1+V1+F1 > 100, !.

pelea(X, Y, Z) :-
    evalpoder(X, D1, V1, F1),
    evalpoder(Y, D2, V2, F2),
    NG1 is (D2*100)/(V1*F1),
    NG2 is (D1*100)/(V2*F2),
    Z = X, NG1<NG2, !.

pelea(X, Y, Z) :-
    evalpoder(X, D1, V1, F1),
    evalpoder(Y, D2, V2, F2),
    NG1 is (D2*100)/(V1*F1),
    NG2 is (D1*100)/(V2*F2),
    Z = Y, NG1>NG2, !.

pelea(X, Y, Z) :-
    evalpoder(X, D1, V1, F1),
    evalpoder(Y, D2, V2, F2),
    NG1 is (D2*100)/(V1*F1),
    NG2 is (D1*100)/(V2*F2),
    Z = empate, NG1 is NG2, !.

