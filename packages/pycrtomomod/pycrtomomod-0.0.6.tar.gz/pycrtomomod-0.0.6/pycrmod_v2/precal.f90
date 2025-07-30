!> \file precal.f90
!> \brief pre-compute element contributions
!>
!> \details This module computes the element contributions of all element types in a <I> bare </I> structure. When used to compile the FE stiffness matrix, the corresponding conductivities and wavenumbers are applied. When referring to Schwarz (1991) or Kemna (1995, 2000), these bare contributions are named form functions. More information on form functions of specific element types can be found in:
!> - elem3.f90:  triangular area element 
!> - elem8.f90:  quadrilateral (rectangle) area element
!> - elem11.f90: mixed boundary element 
!> - elem12 doesn't exist because von Neumann boundary conditions don't contribute anything
!>
!> @author Andreas Kemna
!> @date 12/21/1995, last change 11/22/1998

subroutine precal()

    !!!$     Unterprogramm zur Berechnung der Element- und Randelementbeitraege
    !!!$     sowie der Konfigurationsfaktoren zur Berechnung der gemischten
    !!!$     Randbedingung.

    !!!$     Andreas Kemna                                            21-Dec-1995
    !!!$     Letzte Aenderung   22-Sep-1998

    !!!$.....................................................................

    USE femmod
    USE electrmod
    USE elemmod
    USE wavenmod
    USE errmod
    USE konvmod, ONLY : lsytop
    IMPLICIT none


    !!!$.....................................................................

    !!!$     PROGRAMMINTERNE PARAMETER:

    !!!$     Hilfsfunction
    REAL (KIND(0D0))  ::   beta

    !!!$     Aktuelle Elementnummer
    INTEGER (KIND=4)  ::    iel

    !!!$     Aktuelle Randelementnummer
    INTEGER (KIND=4)  ::     rel

    !!!$     Aktueller Elementtyp
    INTEGER (KIND=4)  ::     ntyp

    !!!$     Anzahl der Knoten im aktuellen Elementtyp
    INTEGER (KIND=4)  ::      nkel

    !!!$     Indexvariablen
    INTEGER (KIND=4)  ::  i,j,imn,m,n,l,k

    !!!$.....................................................................

    lbeta  = .false.
    lrandb = .false.
    iel    = 0

    ALLOCATE (xk(max_nr_element_nodes),yk(max_nr_element_nodes),elmas(max_nr_element_nodes,max_nr_element_nodes),&
        elmam(max_nr_element_nodes,max_nr_element_nodes),elve(max_nr_element_nodes),stat=errnr)
    IF (errnr /= 0) then
        fetxt = 'allocation problem elbg elmam'
        errnr = 97 
        GOTO 1000
    END IF
    ALLOCATE (elbg(elanz,(max_nr_element_nodes*(max_nr_element_nodes+1))/2,kwnanz),stat=errnr)
    IF (errnr /= 0) then
        fetxt = 'allocation problem elbg elbg'
        errnr = 97 
        GOTO 1000
    END IF
    ALLOCATE (relbg(relanz,(max_nr_element_nodes*(max_nr_element_nodes+1))/2),stat=errnr)
    ALLOCATE (kg(relanz,eanz,kwnanz),stat=errnr)
    IF (errnr /= 0) then
        fetxt = 'allocation problem elbg relbg or kg'
        errnr = 97 
        GOTO 1000
    END IF

    IF (lsytop) THEN
        CALL bsytop
    ELSE
        sytop = 0d0
    END IF

    ! loop over all element types
    do i=1,typanz
        ntyp = typ(i)
        nkel = selanz(i)

        ! loop over all elements of this type
        do j=1,nelanz(i)
            iel = iel + 1
            ! loop over each node of this element
            do m=1,nkel
                xk(m) = sx(snr(nrel(iel,m)))
                yk(m) = sy(snr(nrel(iel,m)))
            end do
            WRITE (fetxt,'(a,I7,2F10.2)')'Elementnr',iel
            !!!$     Randelement, linearer Ansatz
            ! Mixed boundaries
            if (ntyp.eq.11) then
                !!!$ Ggf. Fehlermeldung
                    if (lrandb) then
                        fetxt = ' '
                        errnr = 101
                        goto 1000
                    end if

                lbeta = .true.
                call elem1

                !!!$     Randelementbeitraege berechnen
                imn = 0
                rel = iel - elanz

                !!!$     Ggf. Fehlermeldung
                if (rel.le.0) then
                    fetxt = ' '
                    errnr = 36
                    goto 1000
                end if

                ! loop over each node in this element
                do m=1,nkel
                    do n=1,m
                        imn = imn + 1
                        relbg(rel,imn) = elmam(m,n)
                    end do
                end do

                !!!$     Konfigurationsfaktoren zur Berechnung der gemischten Randbedingung
                !!!$     berechnen
                ! loop over electrodes
                do l=1,eanz
                    ! loop over all wavenumbers
                    do k=1,kwnanz
                        kg(rel,l,k) = beta(l,k)
                        if (errnr.ne.0) goto 1000
                    end do
                end do

            else if (ntyp.eq.12) then
                ! Neumann no-flow boundary
                CYCLE

            else if (ntyp.eq.13) then
                ! Ggf. Fehlermeldung
                if (lbeta) then
                    fetxt = ' '
                    errnr = 101
                    goto 1000
                end if

                lrandb = .true.
                CYCLE

                !!!$     Zusammengesetztes Viereckelement
                !!!$     (vier Teildreiecke mit linearem Ansatz)
            else if (ntyp.eq.8) then

                do k=1,kwnanz
                    call elem8(elmas,elve,kwn(k),max_nr_element_nodes)
                    if (errnr.ne.0) goto 1000

                    !!!$     Elementbeitraege berechnen
                    imn = 0

                    do m=1,nkel
                        do n=1,m
                            imn = imn + 1
                            elbg(iel,imn,k) = elmas(m,n)
                        end do
                    end do
                end do
            else
                !!!$ Dreieckelement, linearer Ansatz
                if (ntyp.eq.3) then
                    call elem3
                    if (errnr.ne.0) goto 1000
                    !!!$     Parallelogrammelement, bilinearer Ansatz
                else if (ntyp.eq.5) then

                    call elem5
                    if (errnr.ne.0) goto 1000
                    !!!$  Fehlermeldung
                else
                    fetxt = ' '
                    errnr = 18
                    goto 1000
                end if

                !!!$ Elementbeitraege berechnen
                do k=1,kwnanz
                    imn = 0

                    do m=1,nkel
                        do n=1,m
                            imn = imn + 1
                            elbg(iel,imn,k) = elmas(m,n) + elmam(m,n)*kwn(k)*kwn(k)
                        end do
                    end do
                end do
            end if
        end do
    end do

    IF (ALLOCATED (xk)) DEALLOCATE (xk,yk,elmas,elmam,elve)

    errnr = 0

    return

!!!$:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

!!!$     Fehlermeldungen

1000 return

end subroutine precal
