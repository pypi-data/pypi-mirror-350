SUBROUTINE besp_elem
!!!$     
!!!$     Unterprogramm zum Bestimmen der kleinsten moeglichen 
!!!$     Skalenlaenge zur stochastischen Regularisierung
!!!$     
!!!$     Copyright by Andreas Kemna
!!!$     
!!!$     Erste Version von Roland Martin                          29-Jul-2009
!!!$     
!!!$     Letzte Aenderung                                         07-Aug-2009
!!!$     
!!!$.....................................................................
  
  USE alloci
  USE elemmod        ! fuer nachbar, nrel etc. 
  
  IMPLICIT none
  
!!!$     PROGRAMMINTERNE PARAMETER:-------------------------------------------
!!!$     Indexvariablen
  INTEGER :: i,j,ifp
!!!$     Abstaende d. Schwerpunktskoordinaten der Flaechenelemente
  REAL(KIND(0D0)) :: ax,ay,ar
!!!$     ESP Abstaende
  REAL(KIND(0D0)),DIMENSION(:),ALLOCATABLE :: abst
!!!$-----------------------------------------------------------------------

  IF (.NOT.ALLOCATED(abst)) ALLOCATE (abst(elanz))
  
  grid_min = 10.**5.; grid_max = 0.
  grid_minx = 10.**5.; grid_maxx = 0.
  grid_miny = 10.**5.; grid_maxy = 0.

  DO i=1,elanz ! only if there is a good ordering.. TODO..

     DO j=1,max_nr_element_nodes

        IF (nachbar(i,j)==0) CYCLE

        abst(i) = SQRT((espx(i) - espx(nachbar(i,j)))**2D0 + &
             (espy(i) - espy(nachbar(i,j)))**2D0)

     END DO                 ! inner loop ik=1,max_nr_element_nodes

     DO j=1,elanz

        IF (i==j) CYCLE

        ax = ABS(espx(i) - espx(j))
        ay = ABS(espy(i) - espy(j))

        ar = SQRT(ax**2D0 + ay**2D0)

        grid_min = MIN(grid_min,ar)
        grid_max = MAX(grid_max,ar)
        grid_minx = MAX(MIN(grid_minx,ax),grid_min)
        grid_maxx = MAX(grid_maxx,ax)
        grid_miny = MAX(MIN(grid_miny,ay),grid_min)
        grid_maxy = MAX(grid_maxy,ay)

     END DO

  END DO                    ! outer loop i=1,elanz

!!!$     maximaler wert aus der Menge der Nachbarmittelpunkte
  esp_max = MAXVAL(abst) 
  esp_min = MINVAL(abst)

  esp_mit = SUM(abst)/elanz

  esp_std = 0.
  DO i=1,elanz
     esp_std = esp_std + SQRT((abst(i) - esp_mit)**2D0)
  END DO
  esp_std = esp_std / MAX(1, elanz - 1)

  CALL MDIAN1(abst,elanz,esp_med)

  CALL get_unit(ifp)
  OPEN (ifp,FILE='inv.gstat',STATUS='replace')
  WRITE (ifp,'(a/)')'Grid statistics:'
  WRITE (ifp,'(20X,A,I10)')'Gridcells:'//ACHAR(9),elanz
  WRITE (ifp,'(20X,A,2F10.4)')'ESP Min/Max:'//ACHAR(9),&
       esp_min,esp_max
  WRITE (ifp,'(20X,A,2F10.4)')'GRID Min/Max:'//ACHAR(9),&
       grid_min,grid_max
  WRITE (ifp,'(20X,A,2F10.4)')'GRID-x Min/Max:'//ACHAR(9),&
       grid_minx,grid_maxx
  WRITE (ifp,'(20X,A,2F10.4)')'GRID-y Min/Max:'//ACHAR(9),&
       grid_miny,grid_maxy
  WRITE (ifp,'(20X,A,3F10.4)')'Mean/Median/Var:'//ACHAR(9),&
       esp_mit,esp_med,esp_std
  CLOSE (ifp)

  IF (ALLOCATED(abst)) DEALLOCATE (abst)

END SUBROUTINE besp_elem
      
