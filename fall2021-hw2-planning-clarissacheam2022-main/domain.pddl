(define (domain sokorobotto)
	(:requirements :typing)
	(:types shipment order location robot pallette saleitem - object
	        robot pallette - movable)
  	(:predicates
    (ships ?x - shipment ?y - order)
    (orders ?x - order ?y - saleitem )
    (unstarted ?x - shipment)
    (packing-location ?x - location)
    (available ?x - location)
    (contains ?x - pallette ?y - saleitem)
    (free ?x - robot)
    (connected ?x - location ?y - location)
    (at ?x - movable ?y - location)
    (no-robot ?x - location)
    (no-pallette ?x - location)
    (carrying ?x - robot ?y - pallette)
    (intransit ?x - pallette)
    (ispackatloc ?x - shipment ?y - location)
    (shipstarted ?x - shipment)
    (includes ?x - shipment ?y - saleitem)
    )
    
    (:action move2location
     :parameters (
      ?robot - robot ?loc1 - location ?loc2 - location
      )
     :precondition (and
        (free ?robot)
        (no-robot ?loc2)
        (at ?robot ?loc1)
        (connected ?loc1 ?loc2)
        )
     :effect (and
        (at ?robot ?loc2)
        (not (no-robot ?loc2))
        (no-robot ?loc1)
        (not (at ?robot ?loc1))
        )
    )
    
    (:action movepal
     :parameters (
     ?robot - robot ?loc1 - location ?loc2 - location ?pal - pallette
     )
     :precondition (and
     (carrying ?robot ?pal)
     (at ?robot ?loc1)
     (no-pallette ?loc2)
     (at ?pal ?loc1)
     (connected ?loc1 ?loc2)
     (no-robot ?loc2)
     )
     :effect (and
        (no-robot ?loc1)
        (not (no-robot ?loc2))
        (at ?pal ?loc2)
        (at ?robot ?loc2)
        (not (at ?pal ?loc1))
        (not (at ?robot ?loc1))
        (no-pallette ?loc1)
        (not (no-pallette ?loc2))
        )
    )
    
    (:action palpickup
     :parameters (
     ?robot - robot ?pal - pallette ?loc - location
     )
     :precondition (and
     (free ?robot)
     (at ?pal ?loc)
     (at ?robot ?loc)
     )
     :effect (and
        (not(free ?robot))
        (carrying ?robot ?pal)
        (intransit ?pal)
        )
     )
    
    (:action paldropoff
     :parameters (
     ?robot - robot ?pal - pallette ?loc - location
     )
     :precondition (and
     (carrying ?robot ?pal)
     (intransit ?pal)
     (at ?robot ?loc)
     )
     :effect (and
        (not (carrying ?robot ?pal))
        (not (intransit ?pal))
        (free ?robot)
        )
    )
    
    (:action packing
     :parameters (
     ?loc - location ?pal - pallette ?item - saleitem ?ship - shipment ?order - order
      )
     :precondition (and
      (ispackatloc ?ship ?loc)
      (contains ?pal ?item)
      (orders ?order ?item)
      (at ?pal ?loc)
      (shipstarted ?ship)
      (ships ?ship ?order)
      (packing-location ?loc)
      )
     :effect (and
        (not (unstarted ?ship))
        (includes ?ship ?item)
        (not (contains ?pal ?item))
        )
    )
    
    (:action startpack
     :parameters (
     ?loc - location ?ship - shipment
      )
     :precondition (and
      (packing-location ?loc)
      (available ?loc)
      )
     :effect (and
        (not (available ?loc))
        (shipstarted ?ship)
        (ispackatloc ?ship ?loc)
        )
    )
    
    (:action stoppack
     :parameters (
     ?ship - shipment ?loc - location ?order - order
     )
     :precondition (and
      (ispackatloc ?ship ?loc)
      (packing-location ?loc)
      )
     :effect (and
        (available ?loc)
        (not (ispackatloc ?ship ?loc))
        )
    )
)
