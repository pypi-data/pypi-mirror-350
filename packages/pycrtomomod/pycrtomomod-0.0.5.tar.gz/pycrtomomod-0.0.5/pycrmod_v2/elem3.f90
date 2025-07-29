!> \file elem3.f90
!> \brief form functions of triangular area elements
!> \details Kemna (1995): A two-dimensional base element \f$ G^{(j)}\f$ can be formed out of a unity triangle. The function \f$ \tilde \phi (x,z) \f$ can be described via a linear approach
!> \f[ \tilde \phi (x,z) \approx c_1^{(j)} + c_2^{(j)} x + c_3^{(j)} z \f]
!> with \f$ (x,z) \in G^{(j)}  \ \ \ (j=1,...,n_e) \f$. It is uniquely determined by the potential values at the three nodes, \f$ \tilde \phi _{i_1 (j)} , \tilde \phi _{i_2 (j)} , \tilde \phi _{i_3 (j)} \f$ (see figure below).
!> \image html elem3_sketch.png "Triangle with linear approach"
!> The approach yields (Schwarz 1991)
!> \f[ \int \int_{G^{(j)}} {\left[ \left( \frac{\partial \tilde \phi}{\partial x} \right)^2 +\left( \frac{\partial \tilde \phi}{\partial z } \right)^2 \right] } dx dz = \tilde {\phi}^{(j)^T} S_1^{'(j)} \tilde \phi^{(j)} \f]
!> \f[ \int \int_{G^{(j)}} \tilde \phi ^2 dx dz = \tilde {\phi}^{(j)^T} S_2^{'(j)} \tilde \phi^{(j)} \f]
!> with \f$ \tilde \phi^{(j)} = \left( \tilde \phi_{i_1 (j)}, \tilde \phi_{i_2 (j)},\tilde \phi_{i_3 (j)} \right)\f$ being the vector of the values of the triangle nodes. The element matrices are 
!> \f[ S_1^{'(j)} = u_1 * U_1 + u_2 * U_2 + u_3 * U_3, \f]
!> \f[ S_2^{'(j)} = u_4 * U_4\f]
!> with 
!> \f[ u_1 = \left[ (x_3 - x_1)^2 + (z_3 - z_1)^2 \right] / u_4, \f]
!> \f[ u_2 = -\left[ (x_3 - x_1)(x_2-x_1) + (z_3-z_1)(z_2 - z_1) \right] / u_4, \f]
!> \f[ u_2 = \left[ (x_2 - x_1)^2+(z_2-z_1)^2 \right] / u_4, \f]
!> \f[ u_2 = (x_2 - x_1)(z_3-z_1) - (x_3-x_1)(z_2 - z_1)  \f]
!> and
!> \f[ U_1 = \frac{1}{2} \left( \begin{array}{ccc} 1 & -1 & 0 \\ -1 & 1 & 0 \\ 0 & 0 & 0  \end{array} \right), \ \ \ U_2 = \frac{1}{2} \left( \begin{array}{ccc} 2 & -1 & -1 \\ -1 & 0 & 1 \\ -1 & 1 & 0  \end{array} \right) \f]
!> \f[ U_3 = \frac{1}{2} \left( \begin{array}{ccc} 1 & 0 & -1 \\ 0 & 0 & 0 \\ -1 & 0 & 1  \end{array} \right), \ \ \ U_4 = \frac{1}{24} \left( \begin{array}{ccc} 2 & 1 & -1 \\ 1 & 2 & 1 \\ 1 & 1 & 2  \end{array} \right) \f]
!> Note that the above core element matrices \f$ U_1,...,U_4 \f$ are independent of the element's geometry. Therefore they can be applied universally.
!> The 3x3 matrices \f$ S_1^{'(j)} \f$ and \f$ S_2^{'(j)} \f$ can be transformed into the global \f$ n_k \times n_k \f$ stiffness matrices \f$ S_1 \f$ and \f$ S_2 \f$: a specific element \f$ (s_3^{(j)})_{mn} \ \ \ (m,n \in \{ 1,...,n_k \}) \f$ is set to
!> \f[ (s_3^{(j)})_{mn} = \left\{ \begin{array}{cc} (s_3^{'(j)})_{\kappa \lambda} & if\ \kappa,\lambda \in \{ 1,2 \}\  with \ m=i_k(j) \ and \ n=i_\lambda (j)   \\  0 & else \end{array} \right. \f]
!> with \f$ (s_3^{'(j)})_{\kappa \lambda} \f$ being an part of \f$  \f$
!> @author Andreas Kemna
!> @date 10/11/1993, last change 11/05/1997
subroutine elem3()

!!!$     Unterprogramm liefert die Elementmatrizen 'elmas(3,3)' und 'elmam(3,3)'
!!!$     sowie den Elementvektor 'elve(3)' fuer ein Dreieckelement mit linearem
!!!$     Ansatz ( Elementtyp Nr.3 ).

!!!$     Andreas Kemna                                            11-Oct-1993
!!!$     Letzte Aenderung   05-Nov-1997

!!!$.....................................................................

  USE elemmod,only:xk,yk,elmam,elmas,elve
  USE errmod

  IMPLICIT none


!!!$.....................................................................

!!!$     PROGRAMMINTERNE PARAMETER:

!!!$     Grundelementmatrizen
  INTEGER (KIND = 4)  ::     s1(3,3),s2(3,3),s3(3,3),s4(3,3)

!!!$     Grundelementvektor
  INTEGER (KIND = 4)  ::     sb(3)

!!!$     Hilfsvariablen
  REAL (KIND(0D0))    ::     x21,x31,y21,y31,det,a,b,c

!!!$     Indexvariablen
  INTEGER (KIND = 4)  ::     i,j

!!!$.....................................................................

  data s1/1,-1,0,-1,1,0,0,0,0/
  data s2/2,-1,-1,-1,0,1,-1,1,0/
  data s3/1,0,-1,0,0,0,-1,0,1/
  data s4/2,1,1,1,2,1,1,1,2/
  data sb/1,1,1/

  x21 = xk(2) - xk(1)
  x31 = xk(3) - xk(1)
  y21 = yk(2) - yk(1)
  y31 = yk(3) - yk(1)
  det = x21*y31 - x31*y21

!!!$     Ggf. Fehlermeldung
  if (det.le.0d0) then
     fetxt = TRIM(fetxt)//' hat evtl falsche Kontennummerierung'
     print*,'det,x21,y31,x31,y21',det,x21,y31,x31,y21
     errnr = 26
     return
  end if

  a =   (x31*x31 + y31*y31) / det
  b = - (x31*x21 + y31*y21) / det
  c =   (x21*x21 + y21*y21) / det

  do i=1,3
     elve(i) = det * dble(sb(i)) / 6d0

     do j=1,3
        elmas(i,j) = (a*dble(s1(i,j)) + &
             b*dble(s2(i,j)) + c*dble(s3(i,j))) / 2d0
        elmam(i,j) = det * dble(s4(i,j)) / 2.4d1
     end do
  end do

  errnr = 0

  return
end subroutine elem3
