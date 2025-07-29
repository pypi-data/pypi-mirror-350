!> \file rwaven.f90
!> \brief determine wave numbers
!> \details Kemna (2000) Appendix C: The procedure used to evaluate the inverse Fourier integral \f[ \phi_i = \frac{1}{\pi} \int_0^\infty \tilde \phi_i(k)dk. \f] is based on the approach of LaBreque et al. (1996a). Since the asymptotic behavior of the transformed potential \f$\tilde \phi (k)\f$ for small and large arguments is different, the integral is split into two parts to which, respectively, adequate numerical integration techniques are then applied, i.e.,
!> \f[\int_0^\infty \tilde \phi_i(k)dk = \int_0^{k_0} \tilde \phi_i(k)dk + \int_{k_0}^\infty \tilde \phi_i(k)dk, \f]
!> with some characteristic wavenumber \f$ k_0 \f$.
!> According to the analytic solution of the 2D Helmholtz equation,
!> \f[ \tilde \phi_p = \frac{I}{2 \pi \sigma_0} \left( K-= (kr_-) + K_0 (kr_+) \right) ,\f] 
!> the (primary) transformed potential is proportional to the modified Bessel function \f$ K_0(u) \f$, with \f$ u= kr\f$. Here, \f$ r\f$ denotes the representative radial distance from the (image) source. The corresponding asymptotic behavior is given by (Abramowitz and Stegun, 1984)
!> \f[\begin{array}{cc} u \rightarrow 0 : & K_0(u) \propto -\ln u, \\ u \rightarrow \infty : & K_0 \propto e^{-u} / \sqrt{u}  \end{array}\f]
!> To overcome the singularity in the integrand at zero, the change of variable \f$ k' = (k/k_0)^{1/2}\f$ is made in the first integral of the right-hand side of the first equation. The resulting nonsingular integral, with integrand \f$ g(k') = 2 k_0 k' \tilde \phi (k) \f$, is evaluated by conventional \f$N_g-\f$point Gaussian quadrature (Press et al., 1992), yielding appropriate abscissa \f$k'_n\f$ with corresponding weights \f$ w'_n \f$. Summing up both steps, it is
!> \f[ \int_0^{k_0} \tilde \phi_i(k)dk = \int_0^1 g(k')dk' = \sum_{n=1}^{N_G} w'_n g(k'_n) = \pi \sum_{n=1}^{N_G} w_n \tilde \phi (k_n)\f]
!> where \f$ k_n = k_0 k^{'2}_0 \f$ and \f$ w_n = 2 k_0 k'_n w'_n / \pi \f$.
!> From the relations in the 3rd equation, it is seen that the behavior of \f$ \tilde\phi(k) \f$ for large arguments is characterized by an exponential decrease. Therefore, the upper integration in the 2nd equation is performed using a \f$N_L-\f$point Laguerre-type formula (Press et al., 1992). Analogous to the 4th equation, one finds
!> \f[ \int_{k_0}^\infty \tilde \phi(k) dk = \int_0^\infty e^{-k'} g(k') dk' = \sum_{n=1}^{N_L} w'_n g(k'_n) = \pi \sum_{n=1}^{N_L} w_n \tilde \phi (k_n) \f]
!> with the rescaled abscissa and weights, respectively, \f$ k_n = k_0 (k'_n +1) \f$ and \f$ w_n = k_0 e^{k'_n} w'_n /\pi \f$. Note that in the last equation, after substitution of \f$ k' = k/k_0 -1 \f$, the new function \f$ g(k') = k_0 e^{k'} \tilde \phi (k) \f$ is temporarily defined.
!> The integration bound \f$ k_0 \f$ has to be specified in relation to the spatial scale of the considered problem. A characteristic quantity in this regard is given by the minimum distance between corresponding transmitting and receiving electrodes within the underlying set of measurement configurations, denoted by \f$ r_{min} \f$. The number of employed abscissa in the integration formulas determines the valid range of the integration in terms of the distance from the source. From a numerical analysis for a homogeneous half-space, it was found that the variable choice
!> \f[ N_G = \int \left( 6 \log (r_{max}/r_{min}) \right) \f]
!> together with \f$ N_L = 4 \f$ and \f$ k_0 = 1/(2r_{min}) \f$, guarantees an error of less than 0.5 % in the inverse Fourier integration for distances ranging from \f$ r_{min}\f$ to \f$r_{max}\f$ (see Figure C.1). Herein,  denotes the maximum distance between source and receiver electrodes as being of interest within the survey.
!> @author Andreas Kemna 
!> @date 10/11/1993

subroutine rwaven()
    ! Unterprogramm zur Berechnung der Wellenzahlwerte.

    USE datmod
    USE electrmod
    USE elemmod
    USE wavenmod
    USE errmod

    IMPLICIT none


    ! PROGRAMMINTERNE PARAMETER:

    ! Indexvariablen
    INTEGER (KIND=4) ::  i,j

    ! Elektrodennummern
    INTEGER (KIND=4) ::     elec(4)

    ! Hilfsvariablen
    INTEGER (KIND=4) ::     ganz,lanz
    REAL (KIND(0D0)) ::    kwn0,dum,xke(4),yke(4),x21,y21

    !.....................................................................

    ! 'amin', 'amax' bestimmen
    amin = 1d9
    amax = 0d0

    do i=1,nanz

        ! Stromelektroden bestimmen
        elec(1) = mod(strnr(i),10000)
        elec(2) = (strnr(i)-elec(1))/10000

        ! Messelektroden bestimmen
        elec(3) = mod(vnr(i),10000)
        elec(4) = (vnr(i)-elec(3))/10000

        ! Abstaende bestimmen
        do j=1,4
            if (elec(j).gt.0) xke(j) = sx(snr(enr(elec(j))))
            if (elec(j).gt.0) yke(j) = sy(snr(enr(elec(j))))
        end do

        if (elec(3).gt.0) then
            do j=1,2
                if (elec(j).gt.0) then
                    x21  = xke(3)-xke(j)
                    y21  = yke(3)-yke(j)
                    dum  = dsqrt(x21*x21+y21*y21)
                    amin = dmin1(dum,amin)
                    amax = dmax1(dum,amax)
                end if
            end do
        end if

        if (elec(4).gt.0) then
            do j=1,2
                if (elec(j).gt.0) then
                    x21  = xke(4)-xke(j)
                    y21  = yke(4)-yke(j)
                    dum  = dsqrt(x21*x21+y21*y21)
                    amin = dmin1(dum,amin)
                    amax = dmax1(dum,amax)
                end if
            end do
        end if
    end do

    ! Ggf. Fehlermeldung
    if (amin.lt.1d-12.or.amax.lt.1d-12) then
        WRITE (fetxt,*)'check for duplicate electrodes'
        errnr = 73
        goto 1000
    end if

    ! Wellenzahlen bestimmen
    ! AK Diss p. 163
    lanz   = 4
    ! ak  ganz   = int(real(6d0*dlog10(amax)))
    ! Number of abcissas for Gauss-Legende-Integration (AK Diss p. 163)
    ganz   = int(real(6d0*dlog10(amax/amin)))
    ! Need at least 2 abcissas
    ganz   = max0(ganz,2)
    ganz   = min0(ganz,30 - lanz)
    ! Overall k number
    kwnanz = ganz+lanz
    ! k_0, AK Diss p. 163
    kwn0   = 1d0/(2d0*amin)

    ALLOCATE (kwn(kwnanz),kwnwi(kwnanz),stat=errnr)
    IF (errnr /= 0) THEN
        fetxt = 'Error memory allocation kwn'
        errnr = 94
        RETURN
    END IF

    ! REMEMBER: We only compute the k values and the weighting factors
    ! here. No actual integration is done here as we still need to caluclate 
    ! the potentials for the k-values.

    ! Gauss-Integeration
    ! Variable substitution in order to overcome the singularity at zero
    ! k' = (k / k_0)^{1/2}
    ! Integration range changes from (0, k_0) to (0, 1)
    call gauleg(0d0,1d0,kwn(1),kwnwi(1),ganz)

    ! See Ak-Diss(2000), p. 161
    ! weighting factor also needs substitution: w_n = 2 k_0 k'_n w'_n / pi
    ! The pi vanishes when evaluating the whole integral -> no need to use it
    ! anywhere.
    ! k_n = k_0 k'_n^2
    do i=1,ganz
        kwnwi(i) = 2d0*kwn0*kwnwi(i)*kwn(i)
        kwn(i)   = kwn0*kwn(i)*kwn(i)
    end do

    ! Laguerre-Integration
    ! Compute abcissas and weights for the numerical integration
    ! of the upper integral (see AK Diss, p. 161ff.)
    ! the alpha = 0d0 value removes the exp function in the
    ! Gauss-Laguere formula (Numerical recipies, p. 144, 1992)
    call gaulag(kwn(ganz+1),kwnwi(ganz+1),lanz,0d0)

    do i=ganz+1,ganz+lanz
        kwnwi(i) = kwn0*kwnwi(i)*dexp(kwn(i))
        kwn(i)   = kwn0*(kwn(i)+1d0)
    end do

    ! debug output: wavenumbers
    ! print *, ""
    ! print *, "amin/amax", amin, amax
    ! print*, "Number of wavenumbers", kwnanz
    ! print *, "wavenumber    weight"
    ! do i=1,kwnanz
    !     PRINT*, kwn(i), kwnwi(i)
    ! end do

    errnr = 0
    return

!:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

!     Fehlermeldungen

1000 return

end subroutine rwaven
