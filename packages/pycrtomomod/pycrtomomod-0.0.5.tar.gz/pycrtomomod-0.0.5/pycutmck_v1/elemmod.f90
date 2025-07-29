MODULE elemmod
!!$c 'elem.fin'
!!$
!!$c Andreas Kemna                                            24-Nov-1993
!!$c                                       Letzte Aenderung   20-Nov-2009
!!$         
!!$c.....................................................................

!!!$Anzahl der Knoten (bzw. Knotenvariablen)
  INTEGER(KIND = 4),PUBLIC                            :: sanz
!!!$Anzahl der Elementtypen
  INTEGER(KIND = 4),PUBLIC                            :: typanz
!!!$Bandbreite der Gesamtsteifigkeitsmatrix 'a'
  INTEGER(KIND = 4),PUBLIC                            ::  mb

!!!$Elementtypen
!!!$(Randelemente (ntyp > 10) am Schluss !)
  INTEGER(KIND = 4),PUBLIC,DIMENSION(:),ALLOCATABLE   :: typ

!!!$Anzahl der Elemente eines bestimmten Typs
  INTEGER(KIND = 4),PUBLIC,DIMENSION(:),ALLOCATABLE   :: nelanz

!!!$Anzahl der Knoten (bzw. Knotenvariablen) in einem Elementtyp
  INTEGER(KIND = 4),PUBLIC,DIMENSION(:),ALLOCATABLE   :: selanz

!!!$Zeiger auf Koordinaten der Knoten
!!!$(Inverser Permutationsvektor der Umnumerierung)
  INTEGER(KIND = 4),PUBLIC,DIMENSION(:),ALLOCATABLE   :: snr

!!!$x-Koordinaten der Knoten
  REAL(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE     :: sx

!!!$y-Koordinaten der Knoten
  REAL(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE     :: sy

!!!$ Elementschwerpunktkoordinaten (ESP) der Flaechenelemente
  REAL(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE     :: spx,spy

!!!$Knotennummern der Elemente (Reihenfolge !)
  INTEGER(KIND = 4),PUBLIC,DIMENSION(:,:),ALLOCATABLE :: nrel

!!!$Anzahl der Elemente (ohne Randelemente)
  INTEGER(KIND = 4),PUBLIC                            :: elanz

!!!$Anzahl der Randelemente
  INTEGER(KIND = 4),PUBLIC                            :: relanz

!!!$Zeiger auf Werte der Randelemente
  INTEGER(KIND = 4),PUBLIC,DIMENSION(:),ALLOCATABLE   :: rnr

!!!$ Groeste Anzahl der Knoten der Flaechenelemente
  INTEGER(KIND = 4),PUBLIC                            :: smaxs

END MODULE elemmod
