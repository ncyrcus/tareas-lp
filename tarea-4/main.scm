#lang scheme

;******** Funcion: tolist **************
;Descripcion: Funcion que asegura que el valor de entrada sea una lista
; o sino procede a convertirlo en esto
;Parametros:
;vals lista o elemento
;Retorno: returna siempre una lista con cero o mas elementos
;*****************************************************/
(define tolist
  (lambda (vals)
    (if (list? vals) vals (list vals))
  )
)


;******** Funcion: circ **************
;Descripcion: Funcion encargada de pasar el primer elemento de una lista al final
; emulando un stack-pop y queue-enqueue
;Parametros:
;vals lista
;Retorno: lista con primer elemento al final
;*****************************************************/
(define circ
  (lambda (vals)
    (append (cdr vals) (tolist (car vals)))
  )
)

;******** Funcion: leer **************
;Descripcion: Funcion encargada de leer los archivos
;Parametros:
;archivo string
;Retorno: retorna listas o estructuras de scheme encontradas en el archivo
;*****************************************************/
(define leer 
  (lambda (archivo) 
    (let ((p (open-input-file archivo)))
      (let f ((x (read p)))
        (if (eof-object? x)
          (begin
            (close-input-port p)
            '()
           )
    	   (cons x (f (read p)))
        )
      )
    )
  )
)


;******** Ligado: crosswords **************
;Descripcion: ligado al cuerpo que llama a leer el archivo crossword
;Parametros:
; --
;Retorno: retorna lo que retorna leer crosswords cuando se llame a crosswords
;*****************************************************/
(define crosswords (leer "crossword_1.txt"))


;******** Funcion: addelem **************
;Descripcion: Funcion que inserta un elmento al inicio de todas las sub listas
; o elementos (coniverte a lista) que se encuentren en una lista
;Parametros:
;elem cualquier elemento
;lista lista
;Retorno: retorna todos los sub elementos de la lista (en profundidad) con el primer elmeento siento elem
;*****************************************************/
(define addelem
  (lambda (elem lista)
    (if (empty? lista)
       '()
       (cons (cons elem (tolist (car lista))) (addelem elem (cdr lista)))
     )
   )
)

;******** Funcion: waddelem **************
;Descripcion: Funcion wrapper de addelem, evita que si la lista esta vacia
; retorne la lista vacia, al contrario, retorna el elemento
;Parametros:
;elem cualquier elemento
;lista lista
;Retorno: retorna lo mismo que addelem evitando el "bug"
;*****************************************************/
(define waddelem
  (lambda (elem lista)
    (if (empty? lista)
        (list elem)
        (cons (cons elem (tolist (car lista))) (addelem elem (cdr lista)))
     )
   )
)

;******** Funcion: crosswordlength **************
;Descripcion: Funcion que devuelve el largo de una linea del crucigrama
;Parametros:
;word lista
;Retorno: retorna un entero siendo este el largo del crossword
;*****************************************************/
(define crosswordlength
  (lambda (word)
    (if (empty? word)
      0
      (cond
        [(eq? (car word) 'r) (+ 1 (crosswordlength (cdr word)))]
        [(eq? (car word) 'b) (+ 1 (crosswordlength (cdr word)))]
        [(eq? (car word) '*) (+ 1 (crosswordlength (cdr word)))]
        [else (crosswordlength (cdr word))]
      )
    )
  )
)

;******** Funcion: superhelpercheck **************
;Descripcion: Funcion que ayuda a comprobar si existe un match en una palabra
; y el crucigrama, comprueba las horizontales
;Parametros:
;word string
;crossword lista
;Retorno: retorna true o false dependiendo si existe un match
;*****************************************************/
(define superhelpercheck
  (lambda (word crossword)
    (if (eq? (string-length word) (crosswordlength crossword))
        #t
        #f
    )
  )  
)

;******** Funcion: helpcheck **************
;Descripcion: Funcion que comprueba que todas las palabras calcen en el crucigrama
;Parametros:
;words lista de palabras en orden especifico
;crosswords lista de listas de lineas del crucigrama
;Retorno: retorna true si hay un match, false si falla en algun intento
;*****************************************************/
(define helpcheck
  (lambda (words crosswords)
       (if (empty? words)
          #t
          (if (empty? crosswords)
              #t
              (if (superhelpercheck (car words) (car crosswords))
                  (helpcheck (cdr words) (cdr crosswords))
                  #f
              )
           )
       )
    )
)

;******** Funcion: crosswords **************
;Descripcion: Funcion encargada de comprobar que alguna de las palabras
; algun set ordenado obtenga un match, funcion de mas alto nivel que anteriores
; comprueba match horizontales
;Parametros:
;words set de palabras ordenadas
;Retorno: retorna true si existe un match, false si no
;*****************************************************/
(define checkmatch
  (lambda (words)
    (if (helpcheck words crosswords)
      #t
      #f
    )
  )
)

;******** Funcion: bkt **************
;Descripcion: Funcion que genera un set de palabras ordenadas
;para ello utilizando un arbol de backtracking
;chunk permite controlar el loop y gestionar el orden de los nodos
;Parametros:
;vals lista
;chunk lista
;Retorno: retorna un set de palabras ordenadas generadas a partir de vals
;*****************************************************/
(define bkt
  (lambda (vals chunk)
    (if (empty? chunk)
    '()
    (append (waddelem (car chunk) (bkt (cdr vals) (cdr vals))) (bkt (circ vals) (cdr chunk)))
    )
  )
)

;(define optbkt
;  (lambda (vals chunk)
;    (if (empty? chunk)
;    '()
;    (if (checkmatch (waddelem (car chunk) (bkt (cdr vals) (cdr vals))))
;      (waddelem (car chunk) (bkt (cdr vals) (cdr vals)))
;      (optbkt (circ vals) (cdr chunk)))
;    )
;  )
;)

;******** Funcion: wbkt **************
;Descripcion: Funcion wrapper de bkt
;Parametros:
;vals lista
;Retorno: genera una inicializacion de pseudo-recursion de cola para bkt y devuelve por lo tanto lo mismo que bkt
;*****************************************************/
(define wbkt
  (lambda (vals)
    (bkt vals vals)
  )
)

;******** Funcion: wchckmtch **************
;Descripcion: funcion wrapper de checkmatch
;Parametros:
;list lista
;Retorno: muestra en pantalla si existe un match en el crossword de lo contrario retorna false
;*****************************************************/
(define wchckmtch
  (lambda (list)
    (if (empty? list)
        #f
        (if (checkmatch (car list))
            (display (car list))
            (wchckmtch (cdr list))
        )
    )
  )        
)                 

;******** Ligado: palabras **************
;Descripcion: ligado palabras con cuerpo leer archivo de palabras
;Parametros:
; --
;Retorno: retorna la lectura del archivo de palabras cuando se llame a palabras
;*****************************************************/
(define palabras (leer "words_1.txt"))
(wchckmtch (wbkt (car palabras)))