!> \file kompab.f90
!> \brief compilation of the stiffness matrix S and the right-hand-side source vector b
!> \details The stiffness matrix S is compiled from the form functions (see <I>elem1, elem3, elem8</I>) and the conductivity of the individual cells according to (Kemna, 2000, pp. 52):
!> \f[ S = \sum_{j=1}^{N_e} \sigma_j \left( S_{1j}+ k^2 S_{2j} \right) + \sum_{j=1}^{N_b} \beta_j S_{3j} \f]
!> The matrix is stored in band format, the matrix elements \f$ S_{mn} \f$ are assigned to the band matrix (a vector of length ((bandwidth+1)*nr_nodes)) via
!> \f[ S_{mn} \rightarrow S_{band}(max(m,n)*bandwidth + min(m,n)) \f]

!> @author Andreas Kemna
!> @date 10/11/1993, last change 11/05/1997

subroutine kompab(nelec,ki,my_a,my_b)

    !     Unterprogramm zur Kompilation der FE-Matrix 'a' in Bandform
    !     (vorgegebene Bandbreite 'mb') und des Konstantenvektors 'b'
    !     ( A * x + b = 0 ).

    !     Andreas Kemna                                            17-Dec-1993
    !     Letzte Aenderung   15-Jul-2007

    !.....................................................................

    USE alloci
    USE femmod
    USE sigmamod
    USE electrmod
    USE elemmod
    USE wavenmod
    USE errmod

    IMPLICIT none


    !.....................................................................

    !     EIN-/AUSGABEPARAMETER:
    !> (OpenMP thread safe) stiffness matrix
    COMPLEX (KIND (0D0)),DIMENSION((mb+1)*sanz) ::     my_a
    !> (OpenMP thread safe) right-hand-side (source) vector
    COMPLEX (KIND (0D0)),DIMENSION(sanz) ::     my_b

    !> current electrode number
    INTEGER (KIND = 4) ::     nelec

    !> current wave number
    INTEGER (KIND = 4) ::     ki

    !.....................................................................

    !     PROGRAMMINTERNE PARAMETER:

    !     Aktuelle Elementnummer
    INTEGER (KIND = 4) ::     iel

    !     Aktuelle Randelementnummer
    INTEGER (KIND = 4) ::     rel

    !     Aktueller Elementtyp
    INTEGER (KIND = 4) ::     ntyp

    !     Anzahl der Knoten im aktuellen Elementtyp
    INTEGER (KIND = 4) ::     nkel

    !     Hilfsvariablen
    REAL (KIND(0D0))   ::     dum
    COMPLEX(KIND(0D0)) ::     dum2
    INTEGER (KIND = 4) ::     im,imax,imin
    INTEGER (KIND = 4) ::     nzp,nnp,idif,ikl

    !     Indexvariablen
    INTEGER (KIND = 4) ::     i,j,k,l

    !.....................................................................

    !     Gesamtsteifigkeitsmatrix und Konstantenvektor auf Null setzen
    my_a = DCMPLX(0D0)
    my_b = DCMPLX(0D0)

    iel = 0

    do i=1,typanz
        ntyp = typ(i)
        nkel = selanz(i)

        do j=1,nelanz(i)
            iel = iel + 1
            ikl = 0

            if (ntyp.gt.11) CYCLE

            do k=1,nkel
                nzp = nrel(iel,k)

                do l=1,k
                    nnp  = nrel(iel,l)
                    idif = iabs(nzp-nnp)

                    !     Ggf. Fehlermeldung
                    if (idif.gt.mb) then
                        WRITE (fetxt,*)'kompab idif',idif,' iel ',iel
                        fetxt = ' '
                        errnr = 19
                        goto 1000
                    else

                        ! Aufbau der Gesamtsteifigkeitsmatrix und ggf. des Konstantenvektors
                        ikl = ikl + 1

                        imax = max0(nzp,nnp)
                        imin = min0(nzp,nnp)
                        im   = imax*mb + imin

                        ! mixed boundary
                        if (ntyp.eq.11) then
                            rel  = iel - elanz
                            dum  = relbg(rel,ikl) * kg(rel,nelec,ki)
                            ! >> RM
                            dum2 = sigma(rnr(rel))
                        else
                            dum  = elbg(iel,ikl,ki)
                            dum2 = sigma(iel)
                        end if
                        ! GRIDBUG was causing some problems here
                        ! sigma index can be overaccessed due to some segementation
                        ! issue which will cause undefined sigma access..
                        ! FIXED this with grid consisitency check during read in

                        my_a(im) = my_a(im) + dcmplx(dum) * dum2
                        ! << RM
                        if (lsr) then
                            dum2   = dcmplx(dum) * (dum2 - sigma0)
                            my_b(nzp) = my_b(nzp) + dum2 * pota(nnp)
                            if (nnp.ne.nzp) my_b(nnp) = my_b(nnp) + dum2 * pota(nzp)
                        end if
                    end if
                end do
            end do
        END do
    end do

    ! electrode capacitances: start
    if (nr_elec_capacitances.gt.0) then
        write (*,*) ''
        write (*,*) 'Electrode capacitances'
        write (*,*) eanz
        write (*,*) nr_elec_capacitances
        write (*,*) 'sanz', sanz, mb
        write(*,*) 'Applying electrode capacitances'
        do i=1,eanz
            im = j*mb + imin
            write (*,*) 'electrode node', i, snr(enr(i))
            ! see Schwartz, eq. 3.3 (page 142)
            ! compute index of diagonal element (i, i) in my_a
            write(*, *) 'index', (mb * sanz) + i
            my_a((mb * sanz) + i)  = my_a((mb * sanz) + i) + dcmplx(0, electrode_capacitances(i))
            !
        end do
    end if
    ! electrode capacitances: end


    !     Ggf. Konstantenvektor belegen
    if (.not.lsr) my_b(enr(nelec)) = dcmplx(-1d0)

        !     akc BAW-Tank
        !     ak        my_b(211) = dcmplx(1d0)
        !     akc Model EGS2003
        !     ak        my_b(1683) = dcmplx(1d0)
        !     akc Lysimeter hor_elem\normal
        !     ak        my_b(129) = dcmplx(1d0)
        !     akc Lysimeter hor_elem\fine
        !     ak        my_b(497) = dcmplx(1d0)
        !     akc Simple Tucson Model
        !     ak        my_b(431) = dcmplx(1d0)
        !     akc TU Berlin Mesokosmos
        !     ak        my_b(201) = dcmplx(1d0)
        !     akc Andy
        !     ak        my_b(2508) = dcmplx(1d0)
        !     akc Sandra (ele?_anom)
        !     ak        my_b(497) = dcmplx(1d0)
        !     akc Adrian (Tank)
        !     ak        my_b(1660) = dcmplx(1d0)

    if (lsink) my_b(nsink) = dcmplx(1d0)

    errnr = 0
    return

!:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

!     Fehlermeldungen

1000 return

end subroutine kompab
