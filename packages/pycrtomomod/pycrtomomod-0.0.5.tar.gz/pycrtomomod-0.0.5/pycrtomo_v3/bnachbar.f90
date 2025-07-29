!> \file bnachbar.f90
!> \brief find neighbouring forward modelling cells 
!> \details Find neighbouring model cells to carry out the triangular regularization in the inversion update process. The algorithms attempts to find equal edges of triangular and quadrilateral elements and marks them as neighbors 

!> @author Roland Martin
!> @date 07/29/2009, last change 08/26/2009
SUBROUTINE bnachbar
!!!$     
!!!$     Unterprogramm zum Bestimmen der Elementnachbarn
!!!$     zur Realisierung der Triangulationsregularisierung
!!!$     sowie der kleinsten moeglichen Skalenlaenge der
!!!$     stochastischen Regularisierung
!!!$     
!!!$     Copyright by Andreas Kemna 2009
!!!$     
!!!$     Erste Version von Roland Martin                          29-Jul-2009
!!!$     
!!!$     Letzte Aenderung                                         07-Aug-2009
!!!$     
!!!$.....................................................................

  USE alloci
  USE modelmod       ! fuer manz
  USE elemmod        ! fuer nachbar, nrel etc. 
  USE errmod       ! errnr und fetxt
  USE konvmod , ONLY : lverb

  IMPLICIT none


!!!$     PROGRAMMINTERNE PARAMETER:----------------------------------------
!!!$     Indexvariablen
  INTEGER :: i,j,ik,jk,count
!!!$     Knotennummer der Kanten zaehler von element i und j
  INTEGER :: ik1,ik2,jk1,jk2
!!!$-----------------------------------------------------------------------

  IF (.NOT.ALLOCATED (nachbar)) &
       ALLOCATE (nachbar(manz,max_nr_element_nodes+1),STAT=errnr)
  IF (errnr/=0) THEN
     WRITE (*,'(/a/)')'Allocation problem nachbar in bnachbar'
     errnr = 97
     RETURN
  END IF

  nachbar = 0
  count = 0
  !$OMP PARALLEL DEFAULT (none) &
  !$OMP PRIVATE (i,ik,ik1,ik2,j,jk,jk1,jk2) &
  !$OMP SHARED (nachbar,max_nr_element_nodes,count,elanz,nrel,lverb)
  !$OMP DO
  DO i=1,elanz

     !$OMP ATOMIC
     count = count + 1

     IF (lverb) WRITE (*,'(a,t70,F6.2,a)',ADVANCE='no')ACHAR(13)// &
          'bnachbar/ ',REAL (count * (100./elanz)),'%'

     DO ik=1,max_nr_element_nodes

        ik1 = nrel(i,ik)
        ik2 = nrel(i,MOD(ik,max_nr_element_nodes)+1)

        DO j=1,elanz

           IF (j==i) CYCLE

           DO jk=1,max_nr_element_nodes

              jk1 = nrel(j,jk)
              jk2 = nrel(j,MOD(jk,max_nr_element_nodes)+1)

              IF ( (ik1==jk1.AND.ik2==jk2) .OR. &
                   (ik1==jk2.AND.ik2==jk1) ) THEN

                 nachbar(i,ik) = j ! Element teilt kante
                 nachbar(i,max_nr_element_nodes+1) = nachbar(i,max_nr_element_nodes+1)+1 ! Anzahl der Nachbarn

              END IF

           END DO
!!$           IF (nachbar(i,max_nr_element_nodes + 1) < max_nr_element_nodes) THEN
!!$              PRINT*,'found border element',ik1,ik2
!!$           END IF
        END DO              ! inner loop j=1,elanz

     END DO

  END DO                    ! outer loop i=1,elanz
  !$OMP END PARALLEL

END SUBROUTINE bnachbar
