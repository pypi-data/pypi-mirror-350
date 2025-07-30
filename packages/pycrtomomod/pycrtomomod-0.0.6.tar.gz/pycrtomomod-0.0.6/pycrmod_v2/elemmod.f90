!> \file elemmod.f90
!> \brief variable delarations for the FE modelling part
!> \details Replacement of former 'elem.fin' and basically contains the FE-element related variables and two methods for allocation and deallocation of global memory.
!>
!> Latest changes:
!> - translated to F90 module
!> - added nachbar (neighbor)
!> - added esp (central point)
!> - added some variables associated with
!! grid statistics
!> - add doxy style for comments
!> - add describtion and translation
!>
!> @author Andreas Kemna, Roland Martin
!> @date 11/24/1993, last change 09/2013
MODULE elemmod
    IMPLICIT none

    !> Anzahl der Knoten (bzw. Knotenvariablen)
    INTEGER(KIND = 4),PUBLIC :: sanz

    !> Anzahl der Elementtypen
    INTEGER(KIND = 4),PUBLIC :: typanz

    !> Bandbreite der Gesamtsteifigkeitsmatrix 'a'
    INTEGER(KIND = 4),PUBLIC ::  mb

    !>Elementtypen
    !! (Randelemente (ntyp > 10) am Schluss !)
    INTEGER(KIND = 4),PUBLIC,DIMENSION(:),ALLOCATABLE   :: typ

    !> Anzahl der Elemente eines bestimmten Typs
    INTEGER(KIND = 4),PUBLIC,DIMENSION(:),ALLOCATABLE   :: nelanz

    !> Anzahl der Knoten (bzw. Knotenvariablen) in einem Elementtyp
    INTEGER(KIND = 4),PUBLIC,DIMENSION(:),ALLOCATABLE   :: selanz

    !> Zeiger auf Koordinaten der Knoten
    !! (Inverser Permutationsvektor der Umnumerierung)
    INTEGER(KIND = 4),PUBLIC,DIMENSION(:),ALLOCATABLE   :: snr

    !> x-Koordinaten der Knoten
    REAL(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE     :: sx

    !> y-Koordinaten der Knoten
    REAL(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE     :: sy

    !> Elementschwerpunktkoordinaten (ESP) der Flaechenelemente
    !! x-direction
    REAL(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE     :: espx

    !> Elementschwerpunktkoordinaten (ESP) der Flaechenelemente
    !! y-direction
    REAL(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE     :: espy

    !> Zeiger auf die Nachbarn der nichtentarteten Elemente
    INTEGER, DIMENSION(:,:), ALLOCATABLE, PUBLIC        :: nachbar

    !> Knotennummern der Elemente (Reihenfolge !)
    INTEGER(KIND = 4),PUBLIC,DIMENSION(:,:),ALLOCATABLE :: nrel

    !> Anzahl der Elemente (ohne Randelemente)
    INTEGER(KIND = 4),PUBLIC                            :: elanz

    !> Anzahl der Randelemente
    INTEGER(KIND = 4),PUBLIC                            :: relanz

    !> Zeiger auf Werte der Randelemente
    INTEGER(KIND = 4),PUBLIC,DIMENSION(:),ALLOCATABLE   :: rnr

    !> Groeste Anzahl der Knoten der Flaechenelemente
    INTEGER(KIND = 4),PUBLIC                            :: max_nr_element_nodes

    !> Gitter Statistiken:

    !!Minaler Abstand zwischen (Flaechen) Elementschwerpunkten
    REAL(KIND(0D0)),PUBLIC                              :: esp_min

    !> Gitter Statistiken:
    !!Maximaler Abstand zwischen (Flaechen) Elementschwerpunkten
    REAL(KIND(0D0)),PUBLIC                              :: esp_max

    !> Gitter statistiken:
    !> Mittelwert/Median und Standardabweichung der ESP
    REAL(KIND(0D0)),PUBLIC                              :: esp_mit

    !> Gitter statistiken:
    !> Median und Standardabweichung der ESP
    REAL(KIND(0D0)),PUBLIC                              :: esp_med

    !> Gitter statistiken:
    !> Standardabweichung der ESP
    REAL(KIND(0D0)),PUBLIC                              :: esp_std

    !>Minaler Gitterabstand (Betrag)
    REAL(KIND(0D0)),PUBLIC                              :: grid_min

    !>Maximaler Gitterabstand (Betrag)
    REAL(KIND(0D0)),PUBLIC                              :: grid_max

    !>Minimaler Gitterabstand in x-Richtung
    REAL(KIND(0D0)),PUBLIC                              :: grid_minx

    !>Minimaler Gitterabstand in y-Richtung
    REAL(KIND(0D0)),PUBLIC                              :: grid_miny

    !>Maximaler Gitterabstand in x-Richtung
    REAL(KIND(0D0)),PUBLIC                              :: grid_maxx

    !>Maximaler Gitterabstand in y-Richtung
    REAL(KIND(0D0)),PUBLIC                              :: grid_maxy

    !>switch/number fictitious sink node (only for 2D)
    LOGICAL,PUBLIC                                      :: lsink

    !>number of grid node for sink
    INTEGER(KIND = 4),PUBLIC                            :: nsink

    !>switch boundary values
    LOGICAL,PUBLIC                                      :: lrandb2

    !>mittlere y-Koordinate aller Randelemente vom Typ 12 ("no flow")
    REAL(KIND(0D0)),PUBLIC                              :: sytop

    !>x-Koordinaten der Eckknotenpunkte
    REAL(KIND(0D0)),DIMENSION(:),ALLOCATABLE,PUBLIC   :: xk

    !>y-Koordinaten der Eckknotenpunkte
    REAL(KIND(0D0)),DIMENSION(:),ALLOCATABLE,PUBLIC   :: yk

    !>Elementarmatrizen
    REAL(KIND(0D0)),DIMENSION(:,:),ALLOCATABLE,PUBLIC :: elmam

    !>Elementarmatrizen
    REAL(KIND(0D0)),DIMENSION(:,:),ALLOCATABLE,PUBLIC :: elmas

    !>Elementvektor
    REAL(KIND(0D0)),DIMENSION(:),ALLOCATABLE,PUBLIC   :: elve

    ! decoupling.dat exists?
    LOGICAL ::    decexi

    ! cell numbers defining decoupling interfaces
    INTEGER(KIND = 4), DIMENSION(:, :), ALLOCATABLE,PUBLIC :: edecoup

    ! decoupling values
    REAL(KIND(0D0)), DIMENSION(:),ALLOCATABLE,PUBLIC :: edecstr

    ! number of interfaces to decouple (i.e., number of lines in decouplings.dat)
    INTEGER (KIND = 4) ::  decanz

    ! number of electrode capacitances
    INTEGER (KIND = 4) :: nr_elec_capacitances;

    ! electrode_capacitances.dat exists?
    LOGICAL :: elec_caps_file_exists;

    ! electrode capacitances
    REAL(KIND(0D0)), DIMENSION(:),ALLOCATABLE,PUBLIC :: electrode_capacitances;

END MODULE elemmod
