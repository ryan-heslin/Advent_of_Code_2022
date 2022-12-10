#lang racket
(require racket/set)

;; Actually ASCII a minus 1, since a is worth 1, not 0
(define ASCII_a 96)
(define ASCII_A 64)

(define (split-half str)
  (let* ([length (string-length str)]
         [middle (/ length  2)])
    (cons (substring str 0 middle) (substring str middle length))

    )
  )

(define (string-contains str char)
  (letrec (
           [length (string-length str)]
           [helper (lambda (i)
                     (if (= i length)
                         #f
                         (let ([this (string-ref str i)])
                           (if (char=? this char)
                               #t
                               (helper (+ i 1))
                               ))
                         ))]
           )
    (helper 0)
    ))

;; Get distinct characters shared by pair of strings
(define (common-chars a b)
  (letrec ([ length (string-length a)]
           [ seen (mutable-set #f) ]
           [helper (lambda (i found)
                     (if (= i length) ;;string exhausted
                         found
                         (let*
                             ([char (string-ref a i)]
                              [char_seen  (set-member? seen char )]
                              [char_present (and (not char_seen) (string-contains b char))]
                              [next (if char_present (append found (list char)) found)]) ;;Add char to list if already found
                           (if char_seen
                               (helper (+ i 1) next)
                               (begin
                                 (set-add! seen char )
                                 (helper (+ i 1) next)
                                 )))))])

    (helper 0 (list ))
    ))

(define (priority char)
  (let ([bytecode (char->integer char)])
    (if (< bytecode ASCII_a)
        (- (+ 26 bytecode) ASCII_A) ;;capital letter
        (- bytecode ASCII_a)
        ))
  )


;; From https://stackoverflow.com/questions/15543935/list-to-string-conversion-in-racket
(define (list->string chars)
  (string-join (map string chars) ""))

;; Split string in half
;; Find one letter shared in each half
;; Add letter to sum
(define (total strs score)
  (if (null? strs)
      score ;;List exhausted
      (let* ([pair (split-half (car strs))]
             [ char (car (common-chars (car pair) (cdr pair))) ]
             [ this-priority (priority char)])
        (total (cdr strs) (+ score this-priority))
        )
      )
  )

(define (badges strs score)
  (if (null? strs)
      score
      (let* ([group (list (car strs) (car (cdr strs)) (caddr strs))] ;;First three
             [second (car (cdr group))]
             [first-shared (common-chars (car group) second )]
             [second-shared (common-chars second (car (cdr (cdr group))))]
             [common (car (common-chars (list->string first-shared) (list->string second-shared)))]) ;; One common char
        (badges (cdddr strs) (+ score (priority common)))

        )))

(define raw-input (file->lines "inputs/day3.txt"))
(define part-1 (total raw-input 0))
(define part-2 (badges raw-input 0))
(print part-2)
