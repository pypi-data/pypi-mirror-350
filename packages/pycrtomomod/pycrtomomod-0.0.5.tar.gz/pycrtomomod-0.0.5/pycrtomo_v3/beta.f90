!> \file beta.f90
!> \brief Mixed boundary element contributions
!>
!> \details Compute mixed boundary element contributions \f$ \beta \f$ to be used inside \n
!> \f[ \partial_x \left( \sigma \partial_x \tilde\phi \right) + 
!> \partial_z \left( \sigma \partial_z \tilde\phi \right) 
!> \sigma k^2 \tilde \phi + I \delta (x-x_s)\delta(z-zs) = 0 \f]
!> \f[ \sigma \partial_n \tilde \phi + \beta \tilde \phi =0 \f]
!> Kemna (2000): ERT surveys are generally conducted from both the earth`s surface and boreholes, defining a vertical 2D plane. The
!corresponding model geometry is characterized by homogeneous Neumann boundary conditions, i.e. \f$ \beta =0 \f$, at the surface (no
!current flow in the normal direction) and mixed boundary conditions, i.e. \f$ \beta \neq 0 \f$, at those boundaries confining the
!considered region within the half-space. In the following, these two types are referred to as <I>surface</I> and <I>half-space</I>
!boundaries, respectively.
!> 
!> Due to their much easier implementation, most early resistivity modeling algorithms impose homogeneous Dirichlet conditions in
!the half-space boundaries, i.e. \f$ \tilde \phi = 0 \f$ (corresponding to \f$ \beta =\inf \f$). This consequently requires the
!usage of large modeling grids, extending far to sides and depth from the actual region of interest, in order to keep related
!modeling errors at an acceptable level. However, here an approach first suggested by Dey and Morrison (1979) is used instead, where
!an adequate, finite value for  on the half-space boundaries is determined via the asymptotic behavior of the potential for a
!homogeneous half-space. Such a mixed (or asymptotic) boundary condition enables the usage of comparatively small grids and, thus,
!reduces the overall computational requirements for the modeling.
!> 
!> For a point source in a homogeneous half-space with complex conductivity \f$\sigma_0\f$, the analytic solution of the 2D Helmholtz equation (see above) in the source-free region is
!> \f[ \tilde \phi _p = \frac{I}{2\pi \sigma_0} \left( K_0 (kr_-) + K_0 (kr_+) \right) \f]
!> where \f$ K_0 \f$ denotes the modified Bessel function of order zero. The radial distances \f$ r_- \f$ and \f$r_+ \f$ from any point to the source and its image (in the case\f$ z_s \neq 0 \f$), respectively, are given by
!> \f[ r_- = \sqrt{(x-x_s)^2 + (z-z_s)^2}, r_+ = \sqrt{(x-x_s)^2 + (z+z_s)^2} \f]
!> Assuming now, in a first approximation, also for the inhomogeneous case \f$ \sigma(x,z) \f$ an asymptotic behavior of the transformed potential on the half-space boundaries according to
!> \f[ \| \tilde \phi \| \propto \left( K_0 (kr_-) + K_0 (kr_+) \right) \f],
!> an expression for the boundary parameter \f$ \beta \f$ can be easily derived using the derivative property of the modified Bessel function. It results
!> \f[ \beta = \sigma k g \f]
!> with the real factor
!> \f[ g = \frac{K_1 (kr_-) \partial_n r_- + K_1 (kr_+) \partial_n r_+ }{K_0 (kr_-) + K_0 (kr_+)} \f]
!> Here, \f$ K_1 \f$ is the modified Bessel function of first order.
!>
!> @author Andreas Kemna
!> @date 12/20/1993, last change 11/20/2009

REAL (KIND(0D0)) function beta(nelec,k)

    USE electrmod
    USE elemmod
    USE wavenmod
    USE errmod

    IMPLICIT none

    !> current electrode
    INTEGER (KIND = 4)  ::     nelec
    !> current wavenumber
    INTEGER (KIND = 4)  ::     k

    !!> internal parameters

    !!> radial distance source / mirror source
    REAL (KIND(0D0))    ::     r1m, r1p
    !!> Bessel function of 0th order
    REAL (KIND(0D0))    ::     bessk0
    !!> Bessel function of 1st order
    REAL (KIND(0D0))    ::     bessk1

    !!> helper variables
    REAL (KIND(0D0))    ::     cthetm,cthetp
    REAL (KIND(0D0))    ::     xs,ys,xr,yr,x3,y3m,y3p,&
        x4,y4,r2,bk0m,bk0p,bk1m,bk1p

    ! print *, 'xk', xk
    ! print *, 'yk', yk
    !!!$.....................................................................
    beta = 0D0
    !!!$ Koordinaten der Stromelektrode bestimmen
    xs = sx(snr(enr(nelec)))
    ys = sy(snr(enr(nelec)))
    ! print *, 'Stromelektrode'
    ! print *, xs
    ! print *, ys

    !!!$ Koordinaten des aktuellen Randelements bestimmen
    xr = (xk(1)+xk(2)) / 2d0
    yr = (yk(1)+yk(2)) / 2d0
    ! print *, 'xr', xr
    ! print *, 'yr', yr

    !!!$ Abstand Randelement - Quelle/Spiegelquelle bestimmen
    x3  = xr - xs
    y3m = (yr - sytop) - (ys - sytop)
    y3p = (yr - sytop) + (ys - sytop)

    r1m = dsqrt(x3*x3 + y3m*y3m)
    r1p = dsqrt(x3*x3 + y3p*y3p)

    !!!$     Hilfsvektor bestimmen
    x4 = yk(1) - yk(2)
    y4 = xk(2) - xk(1)

    r2 = dsqrt(x4*x4 + y4*y4)

    !!!$     Ggf. Fehlermeldung
    if (r1m.lt.1d-12.or.r1p.lt.1d-12.or.r2.lt.1d-12) then
        fetxt = ' '
        errnr = 35
        goto 1000
    end if

    !!!$ Kosinus von Theta bestimmen
    cthetm = (x3*x4 + y3m*y4) / r1m / r2
    cthetp = (x3*x4 + y3p*y4) / r1p / r2

    !!!$     'beta' bestimmen
    bk0m = bessk0(r1m*kwn(k))
    bk0p = bessk0(r1p*kwn(k))

    bk1m = bessk1(r1m*kwn(k))
    bk1p = bessk1(r1p*kwn(k))

    if (bk0m+bk0p.eq.0d0) then
        beta = (cthetm+cthetp) / 2d0
    else
        beta = (cthetm*bk1m+cthetp*bk1p) / (bk0m+bk0p)
    end if

    beta = kwn(k) * beta

    ! print *, "beta", beta
    ! stop

    errnr = 0
    return

!!!$:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

!!!$     Fehlermeldungen

1000 return

end function beta
