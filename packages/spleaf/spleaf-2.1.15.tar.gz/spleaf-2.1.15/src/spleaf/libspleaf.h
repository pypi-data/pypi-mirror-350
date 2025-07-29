// Copyright 2019-2024 Jean-Baptiste Delisle
// Licensed under the EUPL-1.2 or later

#include <stdlib.h>
#include <string.h>
#define MIN(a, b) (((a) < (b)) ? (a) : (b))
#define MAX(a, b) (((a) > (b)) ? (a) : (b))

void spleaf_cholesky(
  // Shape
  long n, long r, long *offsetrow, long *b,
  // Input
  double *A, double *U, double *V, double *phi, double *F,
  // Output
  double *D, double *W, double *G,
  // Temporary
  double *S, double *Z);

void spleaf_dotL(
  // Shape
  long n, long r, long *offsetrow, long *b,
  // Input
  double *U, double *W, double *phi, double *G, double *x,
  // Output
  double *y,
  // Temporary
  double *f);

void spleaf_solveL(
  // Shape
  long n, long r, long *offsetrow, long *b,
  // Input
  double *U, double *W, double *phi, double *G, double *y,
  // Output
  double *x,
  // Temporary
  double *f);

void spleaf_dotLT(
  // Shape
  long n, long r, long *offsetrow, long *b,
  // Input
  double *U, double *W, double *phi, double *G, double *x,
  // Output
  double *y,
  // Temporary
  double *g);

void spleaf_solveLT(
  // Shape
  long n, long r, long *offsetrow, long *b,
  // Input
  double *U, double *W, double *phi, double *G, double *y,
  // Output
  double *x,
  // Temporary
  double *g);

void spleaf_cholesky_back(
  // Shape
  long n, long r, long *offsetrow, long *b,
  // Input
  double *D, double *U, double *W, double *phi, double *G, double *grad_D,
  double *grad_Ucho, double *grad_W, double *grad_phicho, double *grad_G,
  // Output
  double *grad_A, double *grad_U, double *grad_V, double *grad_phi,
  double *grad_F,
  // Temporary
  double *S, double *Z);

void spleaf_dotL_back(
  // Shape
  long n, long r, long *offsetrow, long *b,
  // Input
  double *U, double *W, double *phi, double *G, double *x, double *grad_y,
  // Output
  double *grad_U, double *grad_W, double *grad_phi, double *grad_G,
  double *grad_x,
  // Temporary
  double *f);

void spleaf_solveL_back(
  // Shape
  long n, long r, long *offsetrow, long *b,
  // Input
  double *U, double *W, double *phi, double *G, double *x, double *grad_x,
  // Output
  double *grad_U, double *grad_W, double *grad_phi, double *grad_G,
  double *grad_y,
  // Temporary
  double *f);

void spleaf_dotLT_back(
  // Shape
  long n, long r, long *offsetrow, long *b,
  // Input
  double *U, double *W, double *phi, double *G, double *x, double *grad_y,
  // Output
  double *grad_U, double *grad_W, double *grad_phi, double *grad_G,
  double *grad_x,
  // Temporary
  double *g);

void spleaf_solveLT_back(
  // Shape
  long n, long r, long *offsetrow, long *b,
  // Input
  double *U, double *W, double *phi, double *G, double *x, double *grad_x,
  // Output
  double *grad_U, double *grad_W, double *grad_phi, double *grad_G,
  double *grad_y,
  // Temporary
  double *g);

void spleaf_expandsep(
  // Shape
  long n, long r, long rsi, long *sepindex,
  // Input
  double *U, double *V, double *phi,
  // Output
  double *K);

void spleaf_expandsepmixt(
  // Shape
  long n1, long n2, long r, long rsi, long *sepindex,
  // Input
  double *U1, double *V1, double *phi1, double *U2, double *V2, long *ref2left,
  double *phi2left, double *phi2right,
  // Output
  double *Km);

void spleaf_expandantisep(
  // Shape
  long n, long r, long rsi, long *sepindex,
  // Input
  double *U, double *V, double *phi,
  // Output
  double *K);

void spleaf_dotsep(
  // Shape
  long n, long r, long rsi, long *sepindex,
  // Input
  double *U, double *V, double *phi, double *x,
  // Output
  double *y);

void spleaf_dotsepmixt(
  // Shape
  long n1, long n2, long r, long rsi, long *sepindex,
  // Input
  double *U1, double *V1, double *phi1, double *U2, double *V2, long *ref2left,
  double *phi2left, double *phi2right, double *x,
  // Output
  double *y);

void spleaf_dotantisep(
  // Shape
  long n, long r, long rsi, long *sepindex,
  // Input
  double *U, double *V, double *phi, double *x,
  // Output
  double *y);
